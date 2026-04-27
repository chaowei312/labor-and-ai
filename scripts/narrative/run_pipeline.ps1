# DSAN 5200 narrative — full refresh (from 5200_finalproj/)
$ErrorActionPreference = "Stop"
$ProjRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\")).Path
Set-Location $ProjRoot

Write-Host "== fetch BLS =="
python scripts/narrative/fetch_bls_series.py

Write-Host "== materialize CSV + DATA_SNAPSHOT =="
python scripts/narrative/materialize_bls_latest.py

Write-Host "== derive indexed series + DERIVED_RATES =="
python scripts/narrative/derive_ces_indices.py

Write-Host "== AIOE exposure (Felten et al.) =="
python scripts/narrative/fetch_aioe_appendix.py
python scripts/narrative/ingest_aioe_soc.py

Write-Host "== OEWS national panel (deep-learning era) =="
if ($env:DSAN5200_FETCH_OEWS -eq "1") {
    python scripts/narrative/fetch_oews_year.py --years 2012,2015,2018,2021,2023
} else {
    Write-Host "Skip fetch: set `$env:DSAN5200_FETCH_OEWS = '1' to (re)download OEWS bundles."
}
if (Test-Path "data/raw/large/oews") {
    python scripts/narrative/ingest_oews_panel.py
} else {
    Write-Host "Skip ingest: data/raw/large/oews not present."
}

Write-Host "== ydata-profiling =="
python scripts/narrative/profile_dataset.py --minimal

Write-Host "== Quarto site (if narrative_site exists) =="
if (Test-Path "narrative_site/_quarto.yml") {
    Set-Location narrative_site
    quarto render
    Set-Location ..
} else {
    Write-Host "Skip: narrative_site/_quarto.yml not found"
}

Write-Host "Done."
