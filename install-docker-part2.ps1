# Script de Instalação do Docker Desktop - Parte 2
# Execute APÓS reiniciar o computador
# Requer PowerShell como Administrador

Write-Host "🐳 Instalando Docker Desktop - Parte 2..." -ForegroundColor Cyan

# Verifica privilégios de administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Execute este script como Administrador!" -ForegroundColor Red
    exit 1
}

# Verifica se WSL está funcionando
Write-Host "`n✓ Verificando WSL..." -ForegroundColor Yellow
try {
    wsl --set-default-version 2
    Write-Host "✅ WSL 2 configurado!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  WSL ainda não está pronto. Pode precisar instalar uma distribuição." -ForegroundColor Yellow
}

# Baixa Docker Desktop
Write-Host "`n📥 Baixando Docker Desktop..." -ForegroundColor Yellow
$dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
$installerPath = "$env:TEMP\DockerDesktopInstaller.exe"

try {
    Write-Host "Isso pode levar alguns minutos..." -ForegroundColor Gray
    Invoke-WebRequest -Uri $dockerUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "✅ Download concluído!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao baixar: $_" -ForegroundColor Red
    Write-Host "Tente baixar manualmente de: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Instala Docker Desktop
Write-Host "`n🚀 Instalando Docker Desktop..." -ForegroundColor Yellow
Write-Host "Aguarde, isso pode levar alguns minutos..." -ForegroundColor Gray

Start-Process -FilePath $installerPath -ArgumentList "install", "--quiet", "--accept-license" -Wait -NoNewWindow

# Limpeza
Write-Host "`n🧹 Limpando arquivos temporários..." -ForegroundColor Yellow
Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

Write-Host "`n✅ Instalação do Docker Desktop concluída!" -ForegroundColor Green
Write-Host "`n📋 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "1. Inicie o Docker Desktop (procure no Menu Iniciar)" -ForegroundColor White
Write-Host "2. Aguarde o Docker inicializar completamente" -ForegroundColor White
Write-Host "3. Aceite os termos de serviço se solicitado" -ForegroundColor White
Write-Host "4. Aguarde o ícone do Docker na bandeja ficar verde" -ForegroundColor White
Write-Host "`n5. Teste com: docker --version" -ForegroundColor Yellow
Write-Host "6. Navegue até seu projeto e execute: docker-compose up --build" -ForegroundColor Yellow

Write-Host "`nPressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
