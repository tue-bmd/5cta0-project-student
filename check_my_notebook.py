#!/usr/bin/env python3
"""Self-check your project notebook *before* you submit it.

Run this on your notebook to catch the most common submission problems before
you upload to Canvas:

  • is the file a valid, openable notebook?
  • is it named  project_group<groupnumber>.ipynb ?
  • did every code cell run, top-to-bottom, from a fresh kernel?
  • does the saved notebook contain any error outputs?

It does NOT look at whether your answers are correct — it only checks that the
notebook is complete and runnable so that it can actually be graded.

Usage:
    python check_my_notebook.py project_group12.ipynb
    python check_my_notebook.py --help

This file is self-contained (standard library only) so it can be shared with
students as-is.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# project_group<groupnumber>, tolerant of Canvas' bulk-download prefixes. This is
# a GROUP assignment, one notebook per group. Anchoring on the literal
# "project...group" means a leading numeric submission id that Canvas prepends is
# never mistaken for the group number. An optional separator (project_group_12)
# is tolerated.
SUBMISSION_RE = re.compile(r"project[_\-]+group[_\-]*(?P<num>\d+)", re.I)

RENAME_ASK = (
    "Rename the file to project_group<groupnumber>.ipynb "
    "(e.g. project_group12.ipynb), using your Canvas group number."
)
RUN_ALL_ASK = (
    "Open the notebook and run Kernel → Restart Kernel and Run All Cells, then "
    "save, so every cell is executed top-to-bottom with its output."
)

# --- task-coverage detection ------------------------------------------------
# Leaving a task blank is allowed (you simply do not earn its marks) — these
# patterns let the self-check tell you *which* tasks are still unanswered so a
# blank task is reported as a friendly ⚠️ note, not a hard error.
TASK_CODE = re.compile(r"🧠\s*Your solution.*?Tasks?\s+(?P<id>[0-9]+\.[0-9]+[a-z]?)")
TASK_MD = re.compile(r"^#{3,6}\s*🧠\s*Your solution\b(?P<rest>.*)$")
# Lines that are part of the empty placeholder, not a real answer:
PLACEHOLDER_NOISE = re.compile(r"^\s*#\s*(\.\.\.\s*your code here|─+\s*🧠|🧠)")
# The auto-inserted "unanswered" placeholder line, e.g.  duration_h = TODO
# (an assignment) or  return TODO  (an emptied helper function body).
SEED_LINE = re.compile(r"^\s*(?:return\s+|[\w][\w\s,=]*=\s*)TODO\b")
WRITE_HERE = "write your explanation here"


def _code_region_answered(lines) -> bool:
    """Decide whether a code task region has a real answer.

    Tasks whose output feeds the cell's report lines ship with an auto seed of
    the form ``foo = bar = TODO``. While that untouched seed is present, the task
    is unanswered — the surviving ``print(...)`` report lines are *not* an answer.
    Once the student replaces ``TODO`` with their own code the seed disappears, so
    any remaining real (non-comment) line means the task is answered. Tasks with
    no seed (the answer area is otherwise empty) count as answered as soon as the
    student writes any code there."""
    if any(SEED_LINE.match(ln) for ln in lines):
        return False  # seed left untouched → unanswered (report lines don't count)
    for ln in lines:
        s = ln.strip()
        if s and not s.startswith("#"):
            return True
    return False


def task_coverage(nb):
    """Inspect which tasks have a real answer. Returns (answered, total, blank)
    where ``blank`` is the ordered list of unanswered task ids."""
    answered: dict[str, bool] = {}
    order: list[str] = []

    def see(tid):
        if tid not in answered:
            order.append(tid)
            answered[tid] = False

    for cell in nb["cells"]:
        src = cell.get("source", [])
        if not src:
            continue
        if cell.get("cell_type") == "code":
            # split the cell into per-task regions at each 🧠 marker line
            marks = [(i, m.group("id")) for i, ln in enumerate(src) if (m := TASK_CODE.search(ln))]
            for k, (idx, tid) in enumerate(marks):
                see(tid)
                end = marks[k + 1][0] if k + 1 < len(marks) else len(src)
                if _code_region_answered(src[idx + 1 : end]):
                    answered[tid] = True
        else:  # markdown
            m = TASK_MD.match(src[0].rstrip())
            if m:
                idm = re.search(r"[0-9]+\.[0-9]+[a-z]?", m.group("rest"))
                tid = idm.group(0) if idm else (m.group("rest").strip() or "written")
                see(tid)
                body = "".join(src[1:]).strip().lower()
                body = body.replace(">", "").strip()
                if body and WRITE_HERE not in body:
                    answered[tid] = True

    blank = [t for t in order if not answered[t]]
    return len(order) - len(blank), len(order), blank


class NotebookError(Exception):
    """A notebook we cannot parse — it has to be re-saved / re-exported."""


def load_notebook(path):
    """Parse a .ipynb into a dict, raising NotebookError with a readable message
    on anything that makes the file unusable (missing, unreadable, not JSON, or
    not a notebook)."""
    p = Path(path)
    if not p.exists():
        raise NotebookError(f"file not found: {p}")
    try:
        raw = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise NotebookError(f"could not read file ({e})")
    if not raw.strip():
        raise NotebookError("file is empty")
    try:
        nb = json.loads(raw)
    except json.JSONDecodeError as e:
        raise NotebookError(f"corrupted / not valid JSON (line {e.lineno}, col {e.colno}: {e.msg})")
    if not isinstance(nb, dict) or not isinstance(nb.get("cells"), list):
        raise NotebookError("no top-level 'cells' list — not a Jupyter notebook")
    return nb


def name_follows_convention(path) -> bool:
    """True iff the filename is project_group<groupnumber>.ipynb."""
    m = SUBMISSION_RE.search(Path(path).stem)
    return bool(m and m.group("num"))


@dataclass
class HealthReport:
    """Result of inspecting a notebook's *saved state* (no re-execution)."""

    n_code: int  # number of non-empty code cells
    unrun: int  # how many of those were never executed
    run_counts: list  # execution_count of executed cells, in document order
    monotonic: bool  # executed strictly top-to-bottom
    fresh_run_all: bool  # execution_counts are exactly 1..N (Restart & Run All)
    errored: list  # [(cell_number, ename), ...] for cells with error output


def analyze(nb) -> HealthReport:
    """Inspect a parsed notebook for the common runnability signals, without
    re-executing it."""
    code_cells = [
        c
        for c in nb["cells"]
        if c.get("cell_type") == "code" and "".join(c.get("source", [])).strip()
    ]
    counts = [c.get("execution_count") for c in code_cells]
    run_counts = [ec for ec in counts if ec is not None]
    errored = [
        (i, o.get("ename", "error"))
        for i, c in enumerate(code_cells, 1)
        for o in c.get("outputs", [])
        if o.get("output_type") == "error"
    ]
    return HealthReport(
        n_code=len(code_cells),
        unrun=sum(1 for ec in counts if ec is None),
        run_counts=run_counts,
        monotonic=all(a < b for a, b in zip(run_counts, run_counts[1:])),
        fresh_run_all=run_counts == list(range(1, len(run_counts) + 1)),
        errored=errored,
    )


@dataclass
class Check:
    """One submission-health check result. ``level`` is "ok" | "warn" | "bad";
    ``fix`` is the action to suggest when it is not OK."""

    level: str
    message: str
    fix: str | None = None


# Rendered the same way by both the student self-check and the TA grader.
EMOJI = {"ok": "✅", "warn": "⚠️", "bad": "❌"}


def submission_report(nb, path) -> list[Check]:
    """The single source of truth for the submission health checks (filename,
    execution, errors, task coverage). Both check_my_notebook and the grader
    render this list, so they always agree. ``bad`` means the notebook can't be
    graded as submitted; ``warn`` is advisory (rename, fresh kernel, blank tasks)
    and never blocks — leaving tasks blank is allowed."""
    rep = analyze(nb)
    checks: list[Check] = []

    if name_follows_convention(path):
        checks.append(Check("ok", "filename follows project_group<groupnumber>.ipynb"))
    else:
        checks.append(
            Check(
                "warn",
                f"filename '{Path(path).name}' is not project_group<groupnumber>.ipynb",
                RENAME_ASK,
            )
        )

    if rep.n_code == 0:
        checks.append(Check("bad", "no code cells with content were found", RUN_ALL_ASK))
    elif rep.unrun:
        checks.append(
            Check("bad", f"{rep.unrun} of {rep.n_code} code cells were never run", RUN_ALL_ASK)
        )
    elif not rep.monotonic:
        checks.append(
            Check(
                "bad",
                f"code cells were run out of order (run numbers {rep.run_counts[:8]}…)",
                RUN_ALL_ASK,
            )
        )
    elif not rep.fresh_run_all:
        checks.append(
            Check(
                "warn",
                f"cells ran in order but not from a fresh kernel "
                f"(run numbering starts at {rep.run_counts[0]}, not 1)",
                RUN_ALL_ASK,
            )
        )
    else:
        checks.append(
            Check("ok", f"all {rep.n_code} code cells ran top-to-bottom from a fresh kernel")
        )

    if rep.errored:
        names = ", ".join(dict.fromkeys(n for _, n in rep.errored))
        cells = ", ".join(str(i) for i, _ in rep.errored[:6])
        checks.append(
            Check(
                "bad",
                f"{len(rep.errored)} cell(s) ended in an error ({names}; cell {cells})",
                f"Fix the errors so the notebook runs cleanly from top to bottom "
                f"(it currently raises {names}).",
            )
        )
    elif rep.n_code:
        checks.append(Check("ok", "no error outputs are saved in the notebook"))

    answered, total, blank = task_coverage(nb)
    if total and blank:
        shown = ", ".join(blank[:10]) + ("…" if len(blank) > 10 else "")
        checks.append(
            Check("warn", f"{answered}/{total} tasks answered — {len(blank)} left blank: {shown}")
        )
    elif total:
        checks.append(Check("ok", f"all {total} tasks have an answer"))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Self-check your project notebook before submitting. Checks that the "
            "file opens, is named correctly, ran top-to-bottom, and has no errors "
            "— it does NOT check whether your answers are correct."
        ),
        epilog="example: python check_my_notebook.py project_group12.ipynb",
    )
    parser.add_argument(
        "notebook",
        type=Path,
        help="path to your notebook, e.g. project_group12.ipynb",
    )
    args = parser.parse_args()
    path = args.notebook

    print(f"Checking: {path.name}\n")

    try:
        nb = load_notebook(path)
    except NotebookError as e:
        print(f"  ❌ this file cannot be opened as a notebook: {e}\n")
        print("Please re-save / re-export the notebook (and if it stays broken, re-download")
        print("the template and copy your answers across), then run this check again.")
        return 1

    checks = submission_report(nb, path)
    for c in checks:
        print(f"  {EMOJI[c.level]} {c.message}")

    print()
    blockers = [c.fix for c in checks if c.level == "bad" and c.fix]
    if blockers:
        print("❌ Please fix the following before submitting:")
        for i, fix in enumerate(dict.fromkeys(blockers), 1):
            print(f"   {i}. {fix}")
        return 1

    advisories = [c.fix for c in checks if c.level == "warn" and c.fix]
    if advisories:
        print("✅ Your notebook is valid and can be submitted — recommended first:")
        for i, fix in enumerate(dict.fromkeys(advisories), 1):
            print(f"   {i}. {fix}")
    elif any(c.level == "warn" for c in checks):
        print("✅ Your notebook is valid and ready to submit (see the ⚠️ notes above).")
    else:
        print("✅ All checks passed — your notebook looks ready to submit!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
