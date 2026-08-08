Write-Host "Running backend tests..."
Push-Location backend
try { pytest } finally { Pop-Location }
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Running frontend tests..."
Push-Location frontend
try { npm test } finally { Pop-Location }
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
