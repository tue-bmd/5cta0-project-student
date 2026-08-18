# Rubric: Virtual Patient Assignment (5CTA0), Student Version

**GRADE = Attained points (max 100 + 5 bonus report + 5 bonus features)**

This rubric shows what is graded and what partial credit looks like. Each task's notebook prompt remains the source of truth for exact requirements and variable names.

| Part | Topic | Points |
|---|---|---|
| 1 · Data loading, exploration, R-peak detection | Setup + Ch 14 (matched filter / NP detection) | 10 |
| 2 · HRV: time domain, distribution fit, spectral analysis, time-frequency | Ch 3 + Ch 9 + Ch 11 to 13 | 35 |
| 3 · Arrhythmia detection: features, NP and Bayesian rules | Ch 14 (NP, matched filter) + Ch 10 (Bayesian) | 25 |
| 4 · Ejection fraction with MLE, Fisher, CRLB | Ch 6 to 7 (estimation theory) | 30 |
| **Bonus** · Clinical integration report | All parts | +5.0 |
| **Bonus** · Extra candidate features (Task 3.1) | Detection (Ch 14) | +2.5 each (≤ 2 extra), +5.0 max |

> **Note.** Cells marked *provided* don't earn points on their own. Credit is awarded for your additions in the `YOUR CODE HERE` blocks and markdown answer cells.

> **How to read the tables.** Each task is a list of criteria, each worth its own points. Criteria are graded independently, so you can still earn a later one after losing an earlier one. Your grader picks the tier that matches your work, and may award a value in between when your work sits between two descriptions.

> **How the criteria map to the notebook.** This rubric follows the task structure of the assignment. Tasks 1.3, 2.2, 2.3, 4.2 and 4.3 are split into lettered subtasks in the notebook, so their criteria below use those same ids (1.3a, 2.2b, 4.3d and so on). Every other task is a single notebook prompt, so its criteria are listed by name and carry no letter.

---

## Part 1 · Data Loading, Exploration and R-Peak Detection (10 pts)

### Task 1.1 · Data loading and PVC burden (2 pts)

*Are the recording duration and the PVC burden correctly computed and reported?*

#### Recording duration (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not computed, or the block doesn't run | Computed but the units are wrong | Computed and reported in the stated units |

#### PVC burden with beat counts (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not computed, or the denominator is wrong | Correct denominator, but the N and V beat counts are not shown | Correct denominator, printed next to the N and V beat counts |

### Task 1.2 · Echocardiogram visual inspection (1 pt)

*Did you identify ED and ES?*

#### ED and ES identified (0.5 pts)

| Insufficient (0 pts) | Sufficient (0.25 pts) | Excellent (0.5 pts) |
|---|---|---|
| Not identified, or both wrong | Only one of the two is correct | Both correctly identified |

#### Reasoning (0.5 pts)

| Insufficient (0 pts) | Sufficient (0.25 pts) | Excellent (0.5 pts) |
|---|---|---|
| No reasoning, or clearly wrong | Reasoning given but it does not refer to LV-cavity size | A short justification that refers to LV-cavity size |

### Task 1.3 · Matched-filter R-peak detection (7 pts)

*Is the matched filter correctly implemented, evaluated against the annotation, and critically discussed?*

#### 1.3a · Why amplitude thresholding fails (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not addressed | Names one cause but does not tie it back to the threshold | Explains that baseline drift and Gaussian noise together defeat a plain amplitude threshold |

#### 1.3b · Matched filter and refractory spacing (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| Not implemented, or the template is wrong | Filter runs but the ECG is not zero-meaned, or no refractory constraint | Cross-correlation of the zero-mean noisy ECG with the QRS template, normalised, with 250 ms minimum peak spacing |

#### 1.3c · Detection performance and limitations (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| No evaluation against the annotation | Only one of TPR and FP count, or the ±50 ms window is not used, or a limitation with no concrete improvement | TPR and FP count within ±50 ms, plus a limitation and one concrete improvement |

---

## Part 2 · HRV: Distribution Fitting and Spectral Analysis (35 pts)

### Task 2.1 · Time-domain HRV metrics (5 pts)

*Are mean RR, HR, SDNN and RMSSD correctly computed from the right interval series?*

#### Mean RR (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not computed, or from the wrong series | From `rr_N` but reported without units | Computed from `rr_N` and reported with units |

#### HR (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not computed | Computed but not in bpm | Reported in bpm |

#### SDNN (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not computed, or from `rr_all` | From `rr_N` but wrong `ddof` or wrong units | Correctly computed from `rr_N` |

#### RMSSD (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not computed, or from `rr_all` | From `rr_N` but wrong units | Correctly computed from `rr_N` |

#### Clinical comparison (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| No comparison given | Reference ranges mentioned but your values are not placed against them | Your values briefly compared against clinical reference ranges |

### Task 2.2 · LSE Gaussian fit via Gauss-Newton (10 pts)

*Is the Jacobian derived by hand, Gauss-Newton implemented from scratch, and the result compared against `curve_fit` and MLE?*

#### 2.2a · Jacobian by hand (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| Not derived, or quoted with no derivation | Only one of the two partials is correct | Both partials of the Gaussian derived analytically |

#### 2.2b · Gauss-Newton from scratch (4 pts)

| Insufficient (0 pts) | Sufficient (2 pts) | Excellent (4 pts) |
|---|---|---|
| Not attempted, or `curve_fit` stands in for a hand-written iteration | Hand written iteration with estimates reported, but no convergence plot | Implemented from scratch with a convergence plot and the converged estimates reported |

#### 2.2c · Compare and interpret (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| No comparison against `curve_fit` | Comparison present but the MLE-versus-LSE explanation is missing | Matches `curve_fit` to at least four decimals, plus a short explanation of why MLE and LSE differ in general |

### Task 2.3 · Spectral HRV: open-ended investigation (15 pts)

*Is stationarity tested, are non-parametric and parametric spectra estimated and reconciled, and are the consequences for the PSD framework drawn out?*

#### 2.3a · WSS validation (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| WSS not tested | Test performed but not justified, or no conclusion stated | Test performed and justified, conclusion stated |

#### 2.3b · Non-parametric estimators (5 pts)

| Insufficient (0 pts) | Sufficient (2.5 pts) | Excellent (5 pts) |
|---|---|---|
| Nothing, or one estimator with no LF/HF | Fewer than two estimators overlaid, or LF/HF not reported per estimator, or no bias-variance and leakage discussion | At least two Ch 12 estimators overlaid, LF/HF per estimator, canonical choice justified, and a quantitative bias-variance plus leakage discussion at the 0.15 Hz boundary |

#### 2.3c · AR with AIC order selection (4 pts)

| Insufficient (0 pts) | Sufficient (2 pts) | Excellent (4 pts) |
|---|---|---|
| AR not implemented, or AIC not used | AR fit with an AIC sweep, but the range is not motivated or robustness is not discussed | Fit via Yule-Walker with the AIC sweep plotted, the swept range motivated, and LF/HF robustness to the order discussed |

#### 2.3d · Reconcile the two (2 pts)

| Insufficient (0 pts) | Sufficient (1 pt) | Excellent (2 pts) |
|---|---|---|
| Comparison not performed | Side-by-side LF/HF reported but the discussion is superficial | Welch and AR overlaid with shaded LF/HF bands, absolute and relative gap reported, methodological trade-off articulated |

#### 2.3e · Reflection on stationarity (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Consequences not discussed | Conclusion connects only vaguely to the PSD framework | Conclusion states what the stationarity finding means for PSD framework validity |

### Task 2.4 · Time-frequency LF/HF trajectory (5 pts)

*Is the trajectory computed on the full 30 min record, plotted with the clinical threshold, and connected back to the stationarity finding?*

#### Trajectory construction (2 pts)

| Insufficient (0 pts) | Sufficient (1 pt) | Excellent (2 pts) |
|---|---|---|
| Trajectory not computed | Only the 15 min window used, or the window length or overlap is wrong | Full 30 minute record, 5 min window at 60 % overlap, real wall-clock time axis |

#### Plot (2 pts)

| Insufficient (0 pts) | Sufficient (1 pt) | Excellent (2 pts) |
|---|---|---|
| No plot produced | Band powers or the ratio missing, or the LF/HF = 2 threshold not marked | LF and HF band powers and the LF/HF ratio plotted with the clinical threshold marked |

#### Interpretation (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Interpretation absent | Trajectory described but not connected back to the stationarity finding | Discussion connects back to Task 2.3a and flags any late-recording episode of elevated LF/HF |

---

## Part 3 · Arrhythmia Detection: Features, NP and Bayesian Rules (25 pts)

### Task 3.1 · Multi-feature design and AUC comparison (10 pts)

*Are at least three candidate features designed, scored by analytic AUC, and the best one promoted with justification? (Designing **more than three** is a separate bonus. See below.)*

#### Feature design (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| No feature, or fewer than three candidates | Three candidates but they are near-duplicates of the same aspect, or no H₀ guard | At least three features, each capturing a distinct aspect of the PVC signature, with the H₀ guard applied |

#### Per-class fits and AUC (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| No AUC reported | AUC reported without the per-class Gaussian fits | Every candidate has a per-class Gaussian fit and a reported analytic AUC |

#### Canonical pick (2 pts)

| Insufficient (0 pts) | Sufficient (1 pt) | Excellent (2 pts) |
|---|---|---|
| Nothing promoted into `feat_N` and `feat_V` | Promoted, but the pool and the pick are not justified | Promoted into `feat_N` and `feat_V`, with both the pool and the pick justified |

#### Separation and target (2 pts)

| Insufficient (0 pts) | Sufficient (1 pt) | Excellent (2 pts) |
|---|---|---|
| AUC target missed and no visual panel | AUC target missed, or the visual panel is missing | Best feature reaches AUC ≥ 0.90 and a visual panel confirms the cleanest class separation |

### Task 3.2 · NP detector, ROC and AUC (7 pts)

*Is the NP threshold derived analytically, the ROC plotted, and both empirical and analytic AUC reported?*

#### NP threshold (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| The $P_{FA}$ constraint is not enforced through the inverse Gaussian CDF | Inverse Gaussian CDF used, but at the wrong target or from the wrong class parameters | Derived analytically at the prompt's $P_{FA}$ from $\hat\mu_0, \hat\sigma_0$ |

#### ROC curve (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| ROC absent | Plotted but the axes are unlabelled or the sweep misses part of the feature range | Plotted over the full swept threshold range |

#### Empirical and analytic AUC (2 pts)

| Insufficient (0 pts) | Sufficient (1 pt) | Excellent (2 pts) |
|---|---|---|
| Neither reported | Only one of the two reported | Both reported |

#### Operating point and context (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Operating point not marked and no clinical framing | Operating point not marked on the ROC, or the AUC is not contextualised clinically | NP operating point marked, agreement between the two AUCs noted, AUC contextualised clinically |

### Task 3.3 · Youden's J (3 pts)

*Is the Youden-optimal threshold computed and compared against the NP point?*

#### J-optimal threshold (1.5 pts)

| Insufficient (0 pts) | Sufficient (0.75 pts) | Excellent (1.5 pts) |
|---|---|---|
| Youden's J not computed | $J^*$ and $\gamma^*$ reported but not $P_D / P_{FA}$ | $J^*$, $\gamma^*$ and $P_D / P_{FA}$ at the J-optimal threshold reported |

#### NP versus Youden (1.5 pts)

| Insufficient (0 pts) | Sufficient (0.75 pts) | Excellent (1.5 pts) |
|---|---|---|
| The two points are not compared | Numeric comparison only, with no clinical implication | Compared numerically, with the clinical implication of choosing one over the other |

### Task 3.4 · Bayesian decision-rule design (5 pts)

*Are the three decision rules implemented and compared, and are the choice of selection metric and the deployed frame justified on clinical grounds?*

#### Priors and one rule (2 pts)

| Insufficient (0 pts) | Sufficient (1 pt) | Excellent (2 pts) |
|---|---|---|
| No Bayesian rule implemented | Priors assumed rather than estimated from the data, or NP and MAP thresholds not compared | Priors estimated empirically, one Bayesian rule such as MAP implemented, NP and MAP thresholds compared |

#### Three rules (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Fewer than two rules | Only two rules, or no summary score per rule | All three rules (NP at the prompt's $P_{FA}$, MAP, asymmetric-cost Bayes) with a summary score per rule |

#### Deployment choice (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Nothing promoted into `predict_pvc(feat)` | Promoted, but the metric choice is not justified on clinical grounds | A rule selected under a clinically-justified metric and promoted into `predict_pvc(feat)` |

#### SSP insights (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| No insight offered | Only one of the two insights offered | Explains why the Bayesian rules converge here, and that the NP versus Bayesian choice is a clinical decision rather than a statistical one |

---

## Part 4 · Left Ventricular Ejection Fraction (30 pts)

### Task 4.1 · LV areas and ED/ES identification (3 pts)

*Is the per-frame LV-cavity area computed, are ED and ES identified from it, and is the per-frame table reported?*

#### LV areas (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not computed, or the wrong label counted | Right label counted but not stored in `lv_areas` in px² | `lv_areas` is the per-frame count of LV-cavity pixels |

#### ED and ES (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Neither identified, or both wrong | Only one of the two is correct | Identified as the argmax and argmin of `lv_areas` |

#### Per-frame table (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| No table printed | Table printed but the ED and ES rows are not flagged | Per-frame area table printed with the ED and ES rows flagged |

### Task 4.2 · FAC, `lv_long_axis_length()`, Simpson's EF (5 pts)

*Are both EF methods computed, is the long-axis helper correctly implemented, and is the difference explained?*

#### 4.2a · FAC EF (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| `EF_area` left as a stub, or the formula is wrong | Right formula applied to the wrong frames | FAC single-plane EF computed correctly |

#### 4.2b · `lv_long_axis_length()` (2 pts)

| Insufficient (0 pts) | Sufficient (1 pt) | Excellent (2 pts) |
|---|---|---|
| Left as a stub, which makes Simpson's EF meaningless | Returns a distance but uses the single extreme rows instead of the 10 % centroids, or swaps apex and base | Implemented exactly as the prompt describes, returning the distance between the two centroids |

#### 4.2c · Simpson's EF (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| Not computed | Volumes computed but `EF_simpson` is wrong, or only one phase handled | Simpson single-plane EF computed correctly from `V_ed` and `V_es` |

#### 4.2d · Comparison (1 pt)

| Insufficient (0 pts) | Sufficient (0.5 pts) | Excellent (1 pt) |
|---|---|---|
| The two methods are not compared | Quantitative comparison with no geometric reasoning | Quantitative comparison tied to LV geometry through the longitudinal-shortening factor that FAC ignores |

### Task 4.3 · MLE, Fisher information and CRLB (22 pts)

*Are $\sigma$ estimated empirically, the MLE derived and shown efficient, the CRLB computed, the parameter-transformation CRLB on EF derived, and the CI-width-versus-$N$ plot produced and discussed?*

#### 4.3a · Estimate $\sigma$ (3 pts)

| Insufficient (0 pts) | Sufficient (1.5 pts) | Excellent (3 pts) |
|---|---|---|
| Not attempted, or only one cardiac phase estimated | Both phases estimated but wrong `ddof`, or the pooled `sigma_A` is missing | `sigma_A_ed`, `sigma_A_es` and the pooled `sigma_A` computed from the near-ED and near-ES frames |

#### 4.3b · MLE of the mean (5 pts)

| Insufficient (0 pts) | Sufficient (2.5 pts) | Excellent (5 pts) |
|---|---|---|
| Not attempted, or the MLE is asserted rather than derived and no MLE-based EF is reported | One of the two parts present. Either the derivation without the EF, or the EF with the MLE only asserted | Log likelihood written and differentiated to show the sample mean is the MLE, and the MLE-based EF coded at the prompt's $N$ |

#### 4.3c · Fisher information and CRLB (8 pts)

| Insufficient (0 pts) | Sufficient (4 pts) | Excellent (8 pts) |
|---|---|---|
| Nothing attempted, or the CRLB is quoted rather than derived | Two of the three parts present. Typically the Fisher information derived and the CRLB evaluated, with efficiency asserted rather than shown | Fisher information derived from the expected second derivative, CRLB evaluated for $N = 1$ and $N = 3$, and the MLE shown to achieve the bound with the $\sqrt{N}$ variance reduction reported |

#### 4.3d · EF CRLB by the delta method (6 pts)

| Insufficient (0 pts) | Sufficient (3 pts) | Excellent (6 pts) |
|---|---|---|
| Nothing attempted, or the gradient is wrong, which invalidates everything downstream | Two or three of the four parts present. Typically the gradient and the 95 % CI, but no CI-width plot or no trade-off discussion | Gradient derived, 95 % CI on EF at $N = 3$ computed, CI full width plotted against $N$ with the clinical target marked, and the variance-versus-bias trade-off of averaging more frames discussed |

---

## Bonus: Clinical Integration Report (+5 pts)

*Is the report numerically consistent with your analysis, and is each clinical claim explicitly tied back to the method that produced it?*

| Insufficient (0 pts) | Sufficient (+2.5 pts) | Excellent (+5 pts) |
|---|---|---|
| Report absent, or values inconsistent with your results | Numerically consistent, but the interpretation is generic and not linked to methods | All computed clinical values cited, and each conclusion explicitly linked to the SSP method that produced it |

---

## Bonus: Extra Candidate Features (+2.5 each, max +5)

*Did you design additional, distinct, well-analysed features beyond the three required in Task 3.1?*

| Insufficient (0 pts) | Sufficient (+2.5 pts) | Excellent (+5 pts) |
|---|---|---|
| Only the three required features, or the extras are trivial or not analysed | One extra distinct feature, properly analysed with its own per-class Gaussian fit and AUC | Two extra distinct features, each properly analysed, for five features in total |
