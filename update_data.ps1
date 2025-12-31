# update_data.ps1
$ErrorActionPreference = "Stop"
. .\.venv\Scripts\Activate.ps1

python scripts\update_ndx_universe.py
python scripts\update_sec_ticker_cik.py

Write-Host "✅ Data updated. You can start API: ./run_api.ps1"
