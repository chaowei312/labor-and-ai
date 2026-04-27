# Agent hardware budget (local machine)

**Last profiled:** from this workspace host — re-run commands in §Refresh if hardware changes.

| Resource | Detected |
|----------|----------|
| **CPU** | AMD Ryzen 9 9950X3D (16 cores) |
| **System RAM** | ~94 GB |
| **GPU** | NVIDIA GeForce RTX 5090 (~32 GB VRAM) |
| **Driver** | see `nvidia-smi` |

---

## Default policy (DSAN 5200 narrative pipeline)

| Workload | Device | Rationale |
|----------|--------|-----------|
| `scripts/narrative/*` (BLS API, pandas, CSV, **ydata-profiling**, Quarto render) | **CPU / RAM** | Dominant cost is I/O and pandas; profiling lib is CPU-oriented unless you explicitly enable GPU backends. |
| Git, file ops, Quarto static site | **CPU** | No GPU benefit. |
| Large pandas joins (OEWS + exposure tables) | **CPU** — use **chunking** if RAM spikes; you have **~94 GB** headroom for realistic coursework tables. |

**Do not** spin GPU jobs by default — wastes power and adds CUDA friction for zero gain on typical tabular scripts.

---

## When to use GPU (CUDA)

Use **GPU** only when the user explicitly runs GPU-backed tooling or asks for it:

| Case | GPU? |
|------|------|
| PyTorch / JAX / CuPy numerical work | **Yes**, prefer CUDA when tensors are large and code already uses `.to("cuda")`. |
| Local LLM inference (llama.cpp, Ollama, vLLM) | **Yes** — RTX 5090 is suitable; cap **batch/context** if VRAM warnings appear (~32 GB is generous). |
| **ydata-profiling** | **Usually CPU** unless project fork enables GPU path (not default here). |
| **MinerU PDF extraction** | May use GPU if pipeline backend is configured — already worked on this machine; leave user env as-is. |

**Rule of thumb:** If `import torch` and `torch.cuda.is_available()` is True, optional GPU for **heavy** tensor work; otherwise stay on CPU.

---

## Practical budgets (soft caps for agents)

- **Parallel fetch scripts:** ≤ **4** concurrent HTTP workers unless user asks otherwise.
- **Pandas:** Avoid loading **multi‑GB** CSV into memory twice; use `dtype=` + `chunksize=` for huge OEWS dumps.
- **GPU VRAM:** For ad‑hoc CUDA, assume **≤24 GB** PyTorch reservation is safe for co‑existence with display/OS; leave headroom if training alongside desktop.
- **Long runs:** Narrative pipeline full refresh should finish in **minutes** on this hardware; if >30 min, prefer profiling **minimal** mode or smaller date windows.

---

## Refresh hardware snapshot

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
powershell -NoProfile -Command "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB; (Get-CimInstance Win32_Processor).Name"
```

Update the **Detected** table above after major upgrades.
