# Script de Instalacao do Docker Desktop para Windows
# Requer PowerShell como Administrador

Write-Host "Instalando Docker Desktop para Windows..." -ForegroundColor Cyan

# Verifica privilegios de administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERRO: Execute este script como Administrador!" -ForegroundColor Red
    Write-Host "Clique com botao direito no PowerShell > Executar como Administrador" -ForegroundColor Yellow
    exit 1
}

# 1. Instala WSL 2
Write-Host "`nPasso 1: Instalando WSL 2..." -ForegroundColor Yellow
wsl --install
if ($LASTEXITCODE -ne 0) {
    Write-Host "AVISO: WSL pode precisar de reinicializacao" -ForegroundColor Yellow
}

# 2. Habilita recursos necessarios
Write-Host "`nPasso 2: Habilitando recursos do Windows..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart

# 3. Baixa Docker Desktop
Write-Host "`nPasso 3: Baixando Docker Desktop..." -ForegroundColor Yellow
$dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
$installerPath = "$env:TEMP\DockerDesktopInstaller.exe"

try {
    Invoke-WebRequest -Uri $dockerUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "Download concluido!" -ForegroundColor Green
} catch {
    Write-Host "ERRO ao baixar: $_" -ForegroundColor Red
    exit 1
}

# 4. Instala Docker Desktop
Write-Host "`nPasso 4: Instalando Docker Desktop..." -ForegroundColor Yellow
Start-Process -FilePath $installerPath -ArgumentList "install", "--quiet" -Wait -NoNewWindow

# Limpeza
Remove-Item $installerPath -Force

Write-Host "`nInstalacao concluida!" -ForegroundColor Green
Write-Host "`nIMPORTANTE:" -ForegroundColor Yellow
Write-Host "1. Reinicie o computador" -ForegroundColor White
Write-Host "2. Apos reiniciar, inicie o Docker Desktop" -ForegroundColor White
Write-Host "3. Aguarde o Docker inicializar (icone na bandeja)" -ForegroundColor White
Write-Host "4. Execute: docker --version" -ForegroundColor White
Write-Host "`nApos instalacao, rode o projeto com:" -ForegroundColor Cyan
Write-Host "   docker-compose up --build" -ForegroundColor White
