# Launch the constraint laboratory from Windows PowerShell.
# One engine; this script only selects Python and pins numeric-library threads.
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
if (-not $env:OMP_NUM_THREADS) { $env:OMP_NUM_THREADS = "1" }
if (-not $env:OPENBLAS_NUM_THREADS) { $env:OPENBLAS_NUM_THREADS = "1" }
if (-not $env:MKL_NUM_THREADS) { $env:MKL_NUM_THREADS = "1" }
$venv = Join-Path (Get-Location) ".venv\Scripts\python.exe"
if (Test-Path $venv) {
  $python = $venv
} else {
  $python = "python"
}
& $python -m rs_constraint_lab @args
exit $LASTEXITCODE
