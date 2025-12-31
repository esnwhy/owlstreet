# run_api.ps1
$ErrorActionPreference = "Stop"
. .\.venv\Scripts\Activate.ps1

uvicorn app:app --reload --port 8000
