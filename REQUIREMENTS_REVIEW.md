# Requirements review (DSAN 5200 submission snapshot)

This folder is a **standalone copy** of the `routing-in-sparse-attention` work for **DSAN 5200**. It is **not** auto-synced with `../routing-in-sparse-attention/` (DSAN **5300**). Affiliation strings were changed to **5200** here only.

**Website:** The extracted brief in [`agent_view/project/auto/project.md`](agent_view/project/auto/project.md) requires a **project website URL** (plus GitHub Classroom). Use [`agent_view/README.md`](agent_view/README.md) to regenerate from `project.pdf` after MinerU updates.

## About `project.pdf`

`project.pdf` was **not present** anywhere under this workspace when the review was generated, so this cannot claim line-by-line rubric compliance. Drop the official assignment PDF next to this file or paste the bullet requirements in chat for a tighter checklist.

---

## Typical final-project expectations vs this work

| Expectation | Status | Notes |
|-------------|--------|--------|
| Clear research question(s) | **Met** | Q1–Q3 stated in `reports/final_report.md` (quality, speed, linguistic interpretability). |
| Related work / positioning | **Met** | Dense vs fixed sparse vs learned sparse; citations in report and poster drafts. |
| Methods described | **Met** | MoSA, RFGSA, PRSA; `reports/cross_model_comparison.md` is the compact technical spine. |
| Controlled experiments | **Met** | Matched backbone (~44 M params), WikiText-103, 10-epoch budget, comparable eval. |
| Quantitative results | **Met** | JSON under `results/`; tables in reports (PPL, latency, routing stats, hypothesis tests). |
| Code / reproducibility narrative | **Partially met** | `code_submission/README.md` documents layout, env vars (`PRSA_REPO`, `MOSA_REPO`, checkpoints). Checkpoints **not** bundled; many scripts still assume upstream Linux paths unless env overrides are set. |
| Figures | **Partially met** | Report uses Quarto-rendered outputs; poster assets include SVGs. Root `figures/` referenced in repo `README.md` may be incomplete on disk—regenerate via scripts in `code_submission/statistics/` and `code_submission/inference/` as documented. |
| Poster / presentation artifact | **Met (sources)** | `poster/poster.qmd` (+ Typst outputs). Render locally for PDF; exported `poster.pdf` may not be in repo. |
| Long-form write-up | **Met** | `reports/final_report.md` (+ supporting `cross_model_comparison.md`, `rfgsa_ablation_study.md`). |

---

## Points for improvement (before grading or portfolio)

1. **Align with `project.pdf`** once available: page limits, required sections, citation style, or deliverable filenames.
2. **Reproducibility bundle**: add a single `environment.yml` or `requirements.txt` pinned to versions you actually used; document minimum GPU / CUDA in one place.
3. **Paths**: replace or wrap hard-coded `/home/lopedg/project/...` defaults with env-only resolution + clear `.env.example`.
4. **Artifacts**: include or link **rendered** poster PDF and key publication figures in a grader-friendly `deliverables/` folder if the syllabus asks for uploads.
5. **5200 branding**: only this `5200_finalproj/` tree was retitled to DSAN 5200 in poster/report sources; grep the rest if you merge branches.
6. **Ethics / limitations**: strengthen a short subsection on compute, data license (WikiText-103), and generalisation beyond English LM if the rubric weights reflection.

---

## Quick map of this folder

| Path | Role |
|------|------|
| `reports/` | Main narrative: `final_report.md`, comparisons, ablations |
| `code_submission/` | Models, training, inference, statistics pipeline |
| `results/` | Metrics JSON, hypothesis outputs, logs |
| `poster/` | Quarto/Typst poster sources |
| `scripts/` | Older/alternate script copies at repo root (see `code_submission/` for submission-oriented layout) |
