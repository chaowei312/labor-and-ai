# Notes

Planning, design, and process documents for the DSAN 5200 narrative submission. None of these files are deliverables in themselves — the deliverable is the rendered site under [`../narrative_site/`](../narrative_site/) and the data + figure pipeline under [`../scripts/narrative/`](../scripts/narrative/) and [`../data/`](../data/). These notes exist so the editorial reasoning and audit trail are reproducible.

| File | Purpose |
|------|---------|
| [`PROJECT_PLAN.md`](PROJECT_PLAN.md) | Editorial framing, sector pillars (services × manufacturing equal weight), risks, time window. |
| [`STORYBOARD.md`](STORYBOARD.md) | Four-act spine, per-figure plan, requirement-minimums map. |
| [`VISUALIZATION_PLAN.md`](VISUALIZATION_PLAN.md) | Design vocabulary, Reuters/Pudding-style scroll plan, locked typography/color spec. |
| [`REQUIREMENTS_REVIEW.md`](REQUIREMENTS_REVIEW.md) | Submission checklist against `agent_view/project/auto/project.md`. |
| [`AGENT_EDA_TOOLS.md`](AGENT_EDA_TOOLS.md) | Tooling decisions for the EDA layer; why `ydata-profiling` is the source of truth for numbers. |
| [`AGENT_HARDWARE_BUDGET.md`](AGENT_HARDWARE_BUDGET.md) | Local CPU/GPU policy for the agentic pipeline. |
| [`CLAUDE_DESIGN_PROMPT.md`](CLAUDE_DESIGN_PROMPT.md) | The single brief used to drive the Claude Design pass that produced the design system. Quoted in the [appendix AI usage log](../narrative_site/appendix.qmd). |

For graders: the audit trail you most likely want is `STORYBOARD.md` (story spine), `REQUIREMENTS_REVIEW.md` (rubric mapping), and `CLAUDE_DESIGN_PROMPT.md` (AI-assistance disclosure).
