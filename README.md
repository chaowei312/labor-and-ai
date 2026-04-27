# DSAN 5200 — Data-Driven Narrative (AI & Labor Markets)

This folder is the **DSAN 5200 submission** workspace. It is **independent** of `../routing-in-sparse-attention/` (DSAN 5300). Nothing in this directory is shared with 5300 — no models, no posters, no figures.

Working theme: **AI-related labor-market change** as an economic / workforce story (national → sector → local → expert), anchored at **Jan 2010** so the AlexNet (2012) + transformer/LLM era both sit inside the panel.

## Required deliverables (per `project.pdf`)

- **Hosted website URL** + **GitHub Classroom repo URL** (extraction: [`agent_view/project/auto/project.md`](agent_view/project/auto/project.md)).
- Visual minimums: ≥2 static, ≥2 interactive, ≥1 linked, ≥1 infographic — unified theme.
- Narrative arc + technical appendix + AI usage log if applicable.

## Where to look

| File | Purpose |
|------|---------|
| [`PROJECT_PLAN.md`](PROJECT_PLAN.md) | Narrative arc, sector pillars (services × manufacturing equal weight), checklist |
| [`STORYBOARD.md`](STORYBOARD.md) | Wireframe of site sections vs data artifacts |
| [`VISUALIZATION_PLAN.md`](VISUALIZATION_PLAN.md) | Reuters/Pudding-style scroll plan + requirement mapping |
| [`scripts/narrative/figs/README.md`](scripts/narrative/figs/README.md) | **Per-chart Python chunks** (one figure per file) — review iteratively before knitting into Quarto |
| [`data/README.md`](data/README.md) · [`data/sources.yaml`](data/sources.yaml) | Source catalog, merge keys, time windows |
| [`data/meta/data_diary.md`](data/meta/data_diary.md) | Pipeline status, vintages, suppression caveats |
| [`narrative_site/`](narrative_site/) | Quarto site (renders to `_site/`, gitignored) |
| [`agent_view/project/auto/project.md`](agent_view/project/auto/project.md) | MinerU extract of the brief |
| [`AGENT_EDA_TOOLS.md`](AGENT_EDA_TOOLS.md) · [`AGENT_HARDWARE_BUDGET.md`](AGENT_HARDWARE_BUDGET.md) | Optional tooling and CPU/GPU policy |
| [`REQUIREMENTS_REVIEW.md`](REQUIREMENTS_REVIEW.md) | Checklist vs brief |

**For agents:** narrative findings must be **discovered from `data/processed/` and `data/meta/`** — `PROJECT_PLAN.md` is hypothesis space, not evidence. See `.cursor/rules/dsan-5200-data-discovery.mdc`.

## Pipeline at a glance

```bash
cd 5200_finalproj
pip install -r requirements-narrative.txt
# Bash:
bash scripts/narrative/run_pipeline.sh
# PowerShell:
scripts/narrative/run_pipeline.ps1
```

Coverage: BLS CES monthly Jan 2010 → latest, OEWS national anchor years 2012/2015/2018/2021/2023, Felten et al. AIOE (SOC 2010). Snapshots land in [`data/meta/`](data/meta/).

## One-figure-per-script workflow

Per-chart drafts live in [`scripts/narrative/figs/`](scripts/narrative/figs/) and write standalone PNG/SVG into [`narrative_site/figs/`](narrative_site/figs/). Iterate on each chart by running the matching script alone, then Quarto pages embed finished figures by file path — keeps the giant `index.qmd` from becoming a moving target.

## Deploying to GitHub Pages

The narrative site is deployed by the workflow at [`.github/workflows/publish.yml`](.github/workflows/publish.yml). It runs on every push that touches the site, the figure scripts, the processed data, or the workflow itself.

One-time setup, after pushing this folder as a GitHub repo:

1. **GitHub → Settings → Pages**: under *Source*, choose **GitHub Actions**.
2. **GitHub → Actions** tab: enable workflows on this repo (first time only).
3. Push a commit (or click *Run workflow* on `Deploy narrative site to GitHub Pages` from the Actions tab).

After the run finishes, the site URL appears in the workflow summary and on the *Pages* settings panel — typically `https://<user>.github.io/<repo>/`. That is the URL to submit alongside the GitHub Classroom repo URL.

What the workflow does, in order:

1. Check out the repo.
2. Install Quarto (pinned to 1.5.57).
3. Render the Quarto site (`narrative_site/` → `narrative_site/_site/`).
4. Upload `narrative_site/_site/` as the Pages artifact.
5. Deploy via the official `actions/deploy-pages` action.

The committed `narrative_site/figs/*.html` fragments are the source of truth for the deployed page (the Plotly output bakes the data in). The site has no executable `{python}` / `{r}` / `{ojs}` chunks, so the workflow does not need a language runtime.

To regenerate figure HTML fragments locally after a data refresh:

```bash
cd 5200_finalproj
pip install -r requirements-narrative.txt
python scripts/narrative/fetch_bls_series.py
python scripts/narrative/materialize_bls_latest.py
python scripts/narrative/figs/build_linked_view_data.py
for fig in scripts/narrative/figs/fig_*_interactive.py scripts/narrative/figs/fig_10_linked_view.py; do
  python "$fig"
done
cd narrative_site && quarto render && open _site/index.html
```

`narrative_site/_site/` and `data/processed/` are gitignored. The deployment is always rebuilt from the committed sources.
