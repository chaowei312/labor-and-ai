# Clone upstream references (optional)

Use **`clone_upstream_refs`** only for **local browsing** of upstream repos. For anything you **edit**, fork on GitHub first and clone **your fork** — see [`vendor/README.md`](../../vendor/README.md).

## Bash (Git Bash / WSL / macOS)

From workspace root (`final-project/`):

```bash
bash 5200_finalproj/scripts/vendor/clone_upstream_refs.sh
```

## PowerShell

```powershell
cd 5200_finalproj\scripts\vendor
.\clone_upstream_refs.ps1
```

Shallow clones land in `5200_finalproj/vendor/` (gitignored).
