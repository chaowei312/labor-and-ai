# Vendor / upstream repos (fork or clone **before** customizing)

**Policy:** Do **not** rewrite community catalogs or skills from scratch. **Fork on GitHub → clone your fork** into `5200_finalproj/vendor/`, then copy, symlink, or submodule the pieces you need into `.cursor/skills/` or `scripts/`.

Cloned directories under `vendor/` are **gitignored** in this project (only this `README.md` and `.gitkeep` are tracked) so your course repo stays small.

---

## 1. Agent-skills catalogs (fork these)

| Upstream | Fork URL | Purpose |
|----------|----------|---------|
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | `https://github.com/VoltAgent/awesome-agent-skills/fork` | Curated skill index — cherry-pick EDA / viz skills |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | `https://github.com/K-Dense-AI/scientific-agent-skills/fork` | Research + EDA + figure skills |
| [openai/skills](https://github.com/openai/skills) | `https://github.com/openai/skills/fork` | Reference **SKILL.md** structure only |

After forking under **your** GitHub user (`YOUR_USER`):

```bash
cd 5200_finalproj/vendor
git clone https://github.com/YOUR_USER/awesome-agent-skills.git
git clone https://github.com/YOUR_USER/scientific-agent-skills.git
cd awesome-agent-skills && git remote add upstream https://github.com/VoltAgent/awesome-agent-skills.git
```

Pull upstream updates when needed: `git fetch upstream && git merge upstream/main`.

---

## 2. Optional reference mirrors (no fork)

If you only want a **read-only** copy to browse (not edit), use shallow clones — still **not** a substitute for a fork if you change files:

```bash
cd 5200_finalproj
bash scripts/vendor/clone_upstream_refs.sh
```

See [`scripts/vendor/README.md`](../scripts/vendor/README.md).

---

## 3. Python libraries (pip — no fork unless you contribute)

These are consumed via **`requirements-narrative.txt`** (pinned versions). Upstream source if you need to read code:

| Package | Repo |
|---------|------|
| ydata-profiling | [ydataai/ydata-profiling](https://github.com/ydataai/ydata-profiling) |
| PandasAI (optional) | [sinaptik-ai/pandas-ai](https://github.com/sinaptik-ai/pandas-ai) |

Fork only if you patch behavior; otherwise `pip install` is enough.

---

## 4. Wire skills into Cursor

From a **cloned fork** under `vendor/`:

1. Copy a chosen skill folder into `.cursor/skills/<name>/` **or** add a junction/symlink (Windows: `mklink /J`).
2. Edit **`SKILL.md`** only after you have upstream in git history — keep attribution in comments if required by license.

Our project-specific orchestration stays in **`.cursor/skills/eda-narrative/`** (this repo); it **defers** to patterns borrowed from forks rather than reinventing layout.
