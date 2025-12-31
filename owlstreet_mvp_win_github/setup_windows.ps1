# setup_windows.ps1
$ErrorActionPreference = "Stop"

if (!(Test-Path ".venv")) {
  python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "✅ Setup done. Next: ./update_data.ps1 then ./run_api.ps1"
