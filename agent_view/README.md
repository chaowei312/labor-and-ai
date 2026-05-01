# DSAN 5200 — assignment brief (agent view)

The canonical **Markdown extraction** of the course `project.pdf` is:

- [`project/auto/project.md`](project/auto/project.md)

MinerU also writes JSON alongside (`project_content_list*.json`, `project_model.json`) under `project/auto/` if you need structure or debugging.

## Regenerate from PDF

After updating `project.pdf`, from the repo root:

```bash
mkdir -p agent_view
mineru -p "project.pdf" -o "agent_view" -m auto -b pipeline
```

Output layout is `agent_view/project/auto/project.md`.

## Website requirement

The brief requires submission of a **URL to your project website** (plus GitHub Classroom). Plan for public hosting (e.g. Quarto on GU Domains; see the MD file).
