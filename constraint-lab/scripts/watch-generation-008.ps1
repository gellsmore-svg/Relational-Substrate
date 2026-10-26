# Print Generation 008 status every five seconds.
# Not executed on the Linux host that runs this experiment. Native PowerShell validation is not claimed.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
$Python = Join-Path (Get-Location) ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { $Python = "python" }
& $Python -m rs_constraint_lab generation008 status --watch 5 @args
