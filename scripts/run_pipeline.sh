#!/usr/bin/env bash
# DSAN 5200 narrative — full refresh (run from 5200_finalproj/)
set -euo pipefail
cd "$(dirname "$0")/../.."

echo "== fetch BLS =="
python scripts/fetch_bls_series.py

echo "== materialize CSV + DATA_SNAPSHOT =="
python scripts/materialize_bls_latest.py

echo "== derive indexed series + DERIVED_RATES =="
python scripts/derive_ces_indices.py

echo "== AIOE exposure (Felten et al.) =="
python scripts/fetch_aioe_appendix.py
python scripts/ingest_aioe_soc.py

echo "== OEWS national panel (deep-learning era) =="
if [[ "${DSAN5200_FETCH_OEWS:-0}" == "1" ]]; then
  python scripts/fetch_oews_year.py --years 2012,2015,2018,2021,2023
else
  echo "Skip fetch: export DSAN5200_FETCH_OEWS=1 to (re)download OEWS bundles."
fi
if [[ -d data/raw/large/oews ]]; then
  python scripts/ingest_oews_panel.py
else
  echo "Skip ingest: data/raw/large/oews not present."
fi

echo "== ydata-profiling =="
python scripts/profile_dataset.py --minimal

echo "== Quarto site =="
if [[ -f narrative_site/_quarto.yml ]]; then
  (cd narrative_site && quarto render)
else
  echo "Skip: narrative_site not initialized"
fi

echo "Done."
