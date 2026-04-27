# Agentic / assisted EDA — open-source options for the narrative pipeline

Use this as a **selection menu** for tooling around `data/raw` → `data/processed` → charts. Nothing here is required; pick **one** profiling path and **optionally** one LLM-assisted layer.

**Course integrity:** The DSAN 5200 brief restricts **AI-authored narrative**. Using agents or LLMs for **internal EDA, cleaning, or code generation** is common but must be **disclosed** in your **AI usage log** if you rely on them.

**Fork / clone first:** Do **not** recreate upstream skill catalogs from scratch. **Fork** the GitHub repos you need, **clone your forks** into [`vendor/`](../vendor/README.md), then copy or adapt skills into `.cursor/skills/`. Optional shallow **reference** clones: [`scripts/vendor/clone_upstream_refs.sh`](../scripts/vendor/clone_upstream_refs.sh) / [`clone_upstream_refs.ps1`](../scripts/vendor/clone_upstream_refs.ps1). Python deps stay on **`pip` + `requirements-narrative.txt`** unless you contribute patches upstream.

---

## Decision for *this* project (5200 narrative + public aggregate data)

**Chosen stack**

| Layer | Choice | Why |
|-------|--------|-----|
| **Core QA / EDA reports** | **[ydata-profiling](https://github.com/ydataai/ydata-profiling)** | **Deterministic**: same CSV → same profile HTML/JSON — best fit for **appendix reproducibility**, grading, and audit. No API keys. Matches “scripted pipeline” mindset ([`scripts/narrative/`](../scripts/narrative/README.md)). |
| **Agentic orchestration** | **Fork → clone → adapt** + **`.cursor/skills/eda-narrative/SKILL.md`** | **Fork** [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) / [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) on GitHub; **clone into** [`vendor/`](../vendor/README.md); cherry-pick skills into `.cursor/skills/`. Our `eda-narrative` skill encodes **this repo’s** paths ([`VISUALIZATION_PLAN.md`](VISUALIZATION_PLAN.md), `data/`) — it **extends** upstream patterns, not a greenfield rewrite. |
| **Exploration only (optional)** | **[PandasAI](https://github.com/sinaptik-ai/pandas-ai)** or ad-hoc chat | **Do not treat as source of truth.** Useful for brainstorming questions over a loaded frame; outputs must be **re-implemented** in plain pandas in committed scripts and **logged** if material. Poor fit as pipeline backbone — **non-deterministic** unless you freeze model/version and validate every number. |

**Deferred / not recommended as primary**

- **LangChain / LangGraph-only “EDA agent”** — high integration cost for a semester narrative; only worth it if you already depend on LangGraph elsewhere.
- **Warehouse-first commercial analytics agents** (e.g. nao-style stacks) — overkill for CSV + API pulls in `5200_finalproj/data/`.

**Implementation order (wired in-repo):** (1) fetch scripts → (2) **`scripts/narrative/profile_dataset.py`** → `data/meta/profiles/` → (3) tidy scripts → `data/processed/` → Quarto → (4) Cursor skill **`.cursor/skills/eda-narrative/`**.

---

## 1. Agent “skills” catalogs (workflow playbooks for Cursor / Codex / Claude Code)

These repositories collect **SKILL.md**-style instructions (load data → validate → profile → plot), often portable across assistants.

| Resource | URL | Fit for this project |
|----------|-----|----------------------|
| **Awesome Agent Skills** (curated list) | https://github.com/VoltAgent/awesome-agent-skills | Browse for **data analysis / visualization** tags; install skills into `.cursor/skills/` or your agent’s skills path. |
| **Scientific Agent Skills** (research + analysis) | https://github.com/K-Dense-AI/scientific-agent-skills | Categories include **EDA**, stats, publication-quality figures — closest “scientific EDA agent pack” in one place. |
| **OpenAI Skills catalog** (reference format) | https://github.com/openai/skills | Useful as a **pattern** for writing your own `SKILL.md` for BLS → tidy → Quarto. |
| **datalayer/agent-skills** | https://github.com/datalayer/agent-skills | Python-centric **composable skills** for agents (if you later wire Pydantic AI / custom runners). |

**Practical approach here:** **Fork upstream on GitHub → clone your fork into [`vendor/`](../vendor/README.md)** → copy or symlink one **scientific** or **data viz** skill into `.cursor/skills/` and tailor paths to our **`data/` layout** (`sources.yaml`, `raw/` vs `processed/`). Keep **`.cursor/skills/eda-narrative/`** as the project-specific layer on top.

---

## 2. Conversational / agentic analytics libraries (tabular EDA)

| Tool | URL | Role |
|------|-----|------|
| **PandasAI** | https://github.com/sinaptik-ai/pandas-ai | Natural-language questions → pandas / SQL; good for **exploration** after you load CES/OEW CSVs locally. Requires API keys for LLM backend — treat outputs as **drafts**, verify numerically. |
| **LangChain / LangGraph** | https://github.com/langchain-ai/langchain · https://github.com/langchain-ai/langgraph | Build **custom** “EDA agent” with tools (`python_repl`, file reader, `ydata-profiling`). More setup; maximum control. |

Use these **after** deterministic downloads (see §4) so the model is not hallucinating URLs or series IDs.

---

## 3. Specialized analytics-agent frameworks (heavier)

| Tool | URL | Notes |
|------|-----|------|
| **OpenAI Agents SDK** | https://github.com/openai/openai-agents-python | Multi-agent workflows; overkill unless you already use it. |
| **nao**, **Agno Dash**, etc. | Commercial / analytics-focused blogs often cite **nao** (`getnao/nao`) — verify license and scope before adopting. |

Prefer **skills + small scripts** for a student narrative pipeline unless you need warehouse hooks.

---

## 4. Deterministic EDA / profiling (non-LLM, pipeline-friendly)

Use these for **reproducible** quality reports (good for **`meta/`** and appendix figures); pair with optional LLM **interpretation** only.

| Tool | URL | Role |
|------|-----|------|
| **ydata-profiling** | https://github.com/ydataai/ydata-profiling | One-command HTML profile; alerts on skew, missingness, correlations. |
| **Sweetviz** | https://github.com/fbdesignpro/sweetviz | Fast comparison between train/target groups (if you split cohorts). |

Recommended pattern: **`scripts/narrative/profile_tables.py`** → writes `data/meta/profile_<dataset>.html` (gitignored if large) + short JSON summary in `processed/`.

---

## 5. Suggested stack for *this* repo (minimal + auditable)

1. **Ingest:** existing `scripts/narrative/fetch_bls_series.py` + future Census/OEWS fetchers.  
2. **Profile:** **ydata-profiling** or pandas `describe` + saved JSON manifest in `data/meta/`.  
3. **Assist:** optional **Cursor skill** (custom `SKILL.md`) encoding your column dictionary and chart intents — no API cost, full control.  
4. **Explore:** optional **PandasAI** or ad-hoc notebooks **not committed** if large; export only **clean scripts** + **processed** CSVs.  
5. **Document:** anything LLM-assisted goes in the brief’s **AI usage log**.

---

## 6. What to add next in-repo (optional)

| Artifact | Purpose |
|----------|---------|
| `.cursor/skills/eda-narrative/SKILL.md` | Project-specific EDA playbook (paths, BLS series hygiene, merge checks). |
| `scripts/narrative/profile_dataset.py` | Wrap ydata-profiling → `data/meta/` |
| `requirements-narrative.txt` | Pin `pandas`, `requests`, `pyyaml`, `ydata-profiling`, etc., separate from ML stack |

---

## Revision

Revisit this list after you lock **SOC vintage** and **geography**; profiling options stay the same, but merge keys should appear in both **`sources.yaml`** and any agent skill text.
