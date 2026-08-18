# 5CTA0 Project — Virtual Patient Workup

**Course:** Statistical Signal Processing (5CTA0) · Eindhoven University of Technology (TU/e)

**Weight:** 30 % of the final grade (≈ 42 hours of work)

---

## Contents

- [Assignment overview](#assignment-overview)
- [Project files](#project-files)
- [Getting started](#getting-started)
- [Submission](#submission)
- [Data sources](#data-sources)
- [Getting help](#getting-help)

---

## Project files

| File | What it's for |
|------|---------------|
| [`project.ipynb`](project.ipynb) | The assignment and file to submit in the end (see [Submission](#submission)) |
| [`python_tutorial.ipynb`](python_tutorial.ipynb) | Python refresher (start here if new to Python) |
| [`rubric_student.md`](rubric_student.md) | How each task is graded |
| [`check_my_notebook.py`](check_my_notebook.py) | Self-check script to run before submitting (see [Submission](#submission)) |
| [`requirements.txt`](requirements.txt) | Packages to install for this assignment (see [Getting started](#getting-started)) |

---

## Assignment overview

| Part | Topic | Key concepts | Points |
|------|-------|--------------|--------|
| 1 | Data loading & R-peak detection | Matched filter, NP detection (Ch 14) | 10 |
| 2 | HRV: time-domain, distribution fitting, spectral & time-frequency analysis | Random signals (Ch 3), LSE (Ch 9), Spectral estimation (Ch 11–13) | 35 |
| 3 | Multi-feature arrhythmia detection | Neyman-Pearson & Bayesian detection (Ch 14, Ch 10) | 25 |
| 4 | LV ejection fraction estimation | MLE, Fisher information, CRLB (Ch 6–7) | 30 |
| **Bonus** | Written clinical integration report | All parts | +5 |
| **Bonus** | Extra candidate features in arrhythmia detection (Task 3.1) | Neyman-Pearson detection (Ch 14) | +2.5 each (≤ 2 extra), +5 max |

Work entirely inside **`project.ipynb`**. Do **not** add, remove, or reorder cells — keep the answer-cell structure intact. (You only rename the file at submission time — see [Submission](#submission).)

### Notebook conventions

| Marker | Meaning |
|--------|---------|
| 📋 **Task** | Something you need to solve |
| 🧠 `Your code here` | Write your code below this line in code cells |
| 🧠 *Your solution* | Replace this prompt with your written answer in markdown cells |
| `TODO` | An unanswered placeholder — replace it with your solution, or leave it if you don't know |

### Don't know an answer? Leave it blank

Every code task ships with a small `TODO` placeholder (for example
`duration_h = pvc_burden = TODO`). **If you don't know a task, just leave it
untouched and move on** — the notebook is built to still run **top to bottom**:

- unanswered quantities print as `—`, and any figure that depends on them is
  skipped with a short note (the run does **not** crash);
- leaving a task blank only costs that task's marks — it never affects the others;
- so you can always produce a **valid, runnable submission**, even if it's partial. Always check with `uv run python check_my_notebook.py project_group<groupnumber>.ipynb` before submitting.

---

## Getting started

We use [**uv**](https://docs.astral.sh/uv/getting-started/installation/#installation-methods), a fast Python package and environment manager. It also installs Python for you, so it is the only tool you need, no separate Python or Miniconda install required.

Steps 2–4 below are all run in **one terminal**. Open it once in step 1 and reuse it for every command in steps 2–4.

### 1 · Editor & Workspace

We recommend working on this assignment in **Visual Studio Code (VS Code)**. If you have not worked with an editor before:

1. Install VS Code from [code.visualstudio.com](https://code.visualstudio.com/), and add the **Python** and **Jupyter** extensions (from the Extensions panel on the left).
2. Download [this assignment repository](https://github.com/tue-bmd/5cta0-project-student) to your computer. If you are comfortable with Git, you can instead clone it.

   ```bash
   git clone https://github.com/tue-bmd/5cta0-project-student.git
   ```

3. Open VS Code and open the assignment folder (**File → Open Folder…**) so your editor is looking at the correct files.
4. Open a terminal inside VS Code: **Terminal → New Terminal**. It opens in the assignment folder automatically — use this same terminal for every command in steps 2–4 below.

> Not using VS Code? Open your OS's own terminal instead (PowerShell on Windows, Terminal on macOS/Linux), then `cd` into the assignment folder. Every command below works identically either way.

   ```bash
   cd 5cta0-project-student
   ```

### 2 · Install uv

In the terminal from step 1, run the command for your platform. Click the arrow (▶) to expand it.

<details open>
<summary><b>Windows</b></summary>

In a **PowerShell** terminal (in VS Code or search for it in the Start menu) run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

</details>

<details>
<summary><b>macOS / Linux</b></summary>

In your **Terminal** run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

</details>

After it finishes, **close and reopen the terminal** (in VS Code: close the terminal panel, then **Terminal → New Terminal** again), then check the install worked:

```bash
uv --version
```

If `uv` isn't found, the terminal wasn't reopened after installing — repeat the close/reopen step above.

### 3 · Create a virtual environment

A virtual environment is an isolated space that keeps this project's packages separate from everything else on your computer. In the same terminal (already in the assignment folder), create one specifically for this assignment. uv will download Python 3.11 for you if you don't have it:

```bash
uv venv --python 3.11
```

This creates a `.venv` folder inside the project. You do **not** need to activate it, the `uv` commands below use it automatically.

### 4 · Install dependencies

Install all packages required for this assignment:

```bash
uv pip install -r requirements.txt
```

### 5 · Open the notebook

Pick whichever you prefer, VS Code or your browser. Click the arrow (▶) to expand the instructions for your method.

<details>
<summary><b>VS Code (recommended)</b></summary>

Open `project.ipynb` from the file explorer, then click **Select Kernel** (top-right of the notebook) and choose the `.venv` interpreter you just created (shown as Python 3.11 with path `<project-folder>/.venv/bin/python`).

</details>

<details>
<summary><b>Jupyter (in your browser)</b></summary>

Launch the classic Jupyter interface from the terminal:

```bash
uv run jupyter notebook project.ipynb
```

This opens the notebook in your web browser, already using the project environment.

</details>

### 6 · Are you new to Python? Then start with a focused tutorial

Before you start working on the tasks, read through **`python_tutorial.ipynb`**. This is a project-focused refresher exactly on the code patterns that the assignment uses.

### 7 · Work through the tasks

- Read every instruction cell carefully before writing code.
- A few cells might take some time to finish compiling, be aware of this and remain patient.
- Write your code where you see the `🧠 Your solution` marker, replacing the `TODO` placeholder.
- If you don't know a task, **leave it untouched**, the notebook still runs top to bottom.
- Do **not** modify any other code or cell structure.
- Written discussion answers go in the markdown cells labelled **"🧠 Your solution — Task X.Y"**.


### 8 · Finishing a working session & getting back to work

- Save your changes with `Ctrl+S` (`Cmd+S` on Mac), or turn on **AutoSave** via **File → Auto Save** so every change saves automatically.
- To resume later, just reopen the assignment folder (or run `uv run jupyter notebook project.ipynb` again for the browser). VS Code picks up the environment automatically, nothing to reinstall, but re-select the `.venv` kernel (see step 5 above) before running any code.

## Submission

This is a **group** assignment, so you submit **one notebook per group**. **One member submits on behalf of the whole group.** More than one member may upload the same file if you prefer, that is fine too.

Groups are formed through the **enrollment system in Canvas** — sign up for a group there, and use that group number in your filename.

Submit **only** your notebook through Ans, renamed to **`project_group<groupnumber>.ipynb`** (for example `project_group12.ipynb`), using your group number.

Before submitting:

1. Run **Kernel → Restart Kernel and Run All Cells** and verify there are no errors.
2. Save the notebook (`Ctrl+S` / `Cmd+S`).
3. Check that all output cells are visible (plots, printed values, etc.).
4. Rename the file to `project_group<groupnumber>.ipynb`.
5. Run the self-check first to catch the most common submission mistakes:

   ```bash
   uv run python check_my_notebook.py project_group<groupnumber>.ipynb
   ```

   Note that this does not grade your answers, it only checks that the notebook opens, is named correctly, ran top-to-bottom, and has no errors. Tasks you left blank are reported as a friendly ⚠️ note (not an error), so a partial notebook still passes.

6. Upload the notebook file to Ans.

> [!WARNING]
> A notebook that cannot be executed from top to bottom will receive a significant penalty.
> Leaving a task **blank** is fine and does not break the run, but a task you *attempted*
> must not raise an error. Fix or clear any cell that errors before submitting.

---

## Data sources

The notebook automatically downloads the required datasets on first run:

| Dataset | Source |
|---------|--------|
| MIT-BIH Arrhythmia DB, record 119 (ECG Holter, 360 Hz) | [PhysioNet](https://physionet.org/content/mitdb/) via `wfdb` |
| CAMUS echocardiography validation set (A2C view) | [CAMUS](https://www.creatis.insa-lyon.fr/Challenge/camus/) via `zea` |

An internet connection is required for the first run. Subsequent runs use the cached data.

---

## Getting help

- Post questions in the Canvas discussion board.
- During (booked) lab sessions a TA will be available for questions.
- Refer to the course slides and textbook for theoretical background.
