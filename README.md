# DSAN 5200 — Data-Driven Narrative (AI & Labor Markets)

This folder is the **DSAN 5200 submission** workspace. It is **independent** of `../routing-in-sparse-attention/` (DSAN 5300). Nothing in this directory is shared with 5300 — no models, no posters, no figures.

Working theme: **AI-related labor-market change** as an economic / workforce story (national → sector → local → expert), anchored at **Jan 2010** so the AlexNet (2012) + transformer/LLM era both sit inside the panel.

## Submission links

- **Live site:** https://chaowei312.github.io/labor-and-ai/
- **Public mirror (hosts the site):** https://github.com/chaowei312/labor-and-ai

GitHub Pages is restricted to public repos on the org's Free plan, so the Classroom repo is the canonical source of record and the personal mirror is the deployment target. Both repos contain identical commits.

## Required deliverables (per `project.pdf`)

- **Hosted website URL** + **GitHub Classroom repo URL** (extraction: [`agent_view/project/auto/project.md`](agent_view/project/auto/project.md)).
- Visual minimums: ≥2 static, ≥2 interactive, ≥1 linked, ≥1 infographic — unified theme.
- Narrative arc + technical appendix + AI usage log if applicable.

## Where to look

| File | Purpose |
|------|---------|
| [`narrative_site/`](narrative_site/) | Quarto site (renders to `_site/`, gitignored). The deliverable. |
| [`scripts/figs/README.md`](scripts/figs/README.md) | **Per-chart Python chunks** (one figure per file) — review iteratively before knitting into Quarto |
| [`data/README.md`](data/README.md) · [`data/sources.yaml`](data/sources.yaml) | Source catalog, merge keys, time windows |
| [`data/meta/data_diary.md`](data/meta/data_diary.md) | Pipeline status, vintages, suppression caveats |
| [`agent_view/project/auto/project.md`](agent_view/project/auto/project.md) | MinerU extract of the brief |
| [`notes/`](notes/) | Planning, design and process notes (see [`notes/README.md`](notes/README.md)) |

**For agents:** narrative findings must be **discovered from `data/processed/` and `data/meta/`** — [`notes/PROJECT_PLAN.md`](notes/PROJECT_PLAN.md) is hypothesis space, not evidence. See `.cursor/rules/dsan-5200-data-discovery.mdc`.

## Pipeline at a glance

```bash
cd 5200_finalproj
pip install -r requirements-narrative.txt
# Bash:
bash scripts/run_pipeline.sh
# PowerShell:
scripts/run_pipeline.ps1
```

Coverage: BLS CES monthly Jan 2010 → latest, OEWS national anchor years 2012/2015/2018/2021/2023, Felten et al. AIOE (SOC 2010). Snapshots land in [`data/meta/`](data/meta/).

## One-figure-per-script workflow

Per-chart drafts live in [`scripts/figs/`](scripts/figs/) and write standalone PNG/SVG into [`narrative_site/figs/`](narrative_site/figs/). Iterate on each chart by running the matching script alone, then Quarto pages embed finished figures by file path — keeps the giant `index.qmd` from becoming a moving target.

## Deploying to GitHub Pages

The narrative site is deployed by the workflow at [`.github/workflows/publish.yml`](.github/workflows/publish.yml). It runs on every push that touches the site, the figure scripts, the processed data, or the workflow itself.

The Classroom repo (`dsan-5200/project-2026-36-1`) is **private** and the org is on the GitHub Free plan, which does not allow GitHub Pages on private org repos. The same commit is therefore mirrored to a **public personal repo** (`chaowei312/labor-and-ai`), where Pages is enabled with **Source = GitHub Actions**. The live URL is **https://chaowei312.github.io/labor-and-ai/**.

To re-deploy after edits:

```bash
git push origin main      # graded Classroom copy
git push mirror main      # public copy that hosts the site
```

`mirror` is the second remote pointing at `https://github.com/chaowei312/labor-and-ai.git`. The push to `mirror` triggers `Deploy narrative site to GitHub Pages` automatically; the Pages URL appears in the workflow summary.

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
python scripts/fetch_bls_series.py
python scripts/materialize_bls_latest.py
python scripts/figs/build_linked_view_data.py
for fig in scripts/figs/fig_*_interactive.py scripts/figs/fig_10_linked_view.py; do
  python "$fig"
done
cd narrative_site && quarto render && open _site/index.html
```

`narrative_site/_site/` and `data/processed/` are gitignored. The deployment is always rebuilt from the committed sources.
