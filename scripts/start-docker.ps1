# Script : start-docker.ps1

# Vérifie si Docker Desktop est déjà en cours d'exécution
$dockerProcess = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue

if (-not $dockerProcess) {
    Write-Host "⏳ Démarrage de Docker Desktop..."
    Start-Process "C:\Program Files\Docker\Docker Desktop.exe"
    Start-Sleep -Seconds 10

    # Attendre que Docker soit vraiment prêt (optionnel, boucle d'attente)
    $maxRetries = 30
    $retry = 0
    while ((-not (docker info -ErrorAction SilentlyContinue)) -and ($retry -lt $maxRetries)) {
        Write-Host "🕒 En attente de Docker... ($retry/$maxRetries)"
        Start-Sleep -Seconds 2
        $retry++
    }

    if ($retry -ge $maxRetries) {
        Write-Host "❌ Docker ne s'est pas lancé à temps."
        exit 1
    }

    Write-Host "✅ Docker est prêt !"
} else {
    Write-Host "✅ Docker Desktop est déjà en cours d'exécution."
}

# Lance docker compose
Write-Host "🚀 Lancement de docker compose..."
docker compose up --build
