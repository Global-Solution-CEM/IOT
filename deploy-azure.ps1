# Script de Deploy para Azure App Service
# Execute este script no PowerShell para fazer deploy da API no Azure

param(
    [string]$ResourceGroupName = "rg-aprenda-plus",
    [string]$AppServiceName = "aprenda-plus-api",
    [string]$Location = "brazilsouth",
    [string]$SubscriptionId = "",
    [string]$GeminiApiKey = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploy Aprenda Plus API - Azure" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Azure CLI está instalado
Write-Host "Verificando Azure CLI..." -ForegroundColor Yellow
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✓ Azure CLI encontrado (versão: $($azVersion.'azure-cli'))" -ForegroundColor Green
} catch {
    Write-Host "✗ Azure CLI não encontrado!" -ForegroundColor Red
    Write-Host "Instale o Azure CLI: https://aka.ms/InstallAzureCLIWindows" -ForegroundColor Yellow
    exit 1
}

# Verificar login
Write-Host "`nVerificando login no Azure..." -ForegroundColor Yellow
$account = az account show --output json 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "Fazendo login no Azure..." -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Falha no login!" -ForegroundColor Red
        exit 1
    }
}

# Selecionar subscription se fornecida
if ($SubscriptionId) {
    Write-Host "Selecionando subscription: $SubscriptionId" -ForegroundColor Yellow
    az account set --subscription $SubscriptionId
}

$currentSub = az account show --query id -o tsv
Write-Host "✓ Logado no Azure (Subscription: $currentSub)" -ForegroundColor Green

# Criar Resource Group se não existir
Write-Host "`nVerificando Resource Group..." -ForegroundColor Yellow
$rgExists = az group exists --name $ResourceGroupName --output tsv
if ($rgExists -eq "false") {
    Write-Host "Criando Resource Group: $ResourceGroupName" -ForegroundColor Yellow
    az group create --name $ResourceGroupName --location $Location
    Write-Host "✓ Resource Group criado" -ForegroundColor Green
} else {
    Write-Host "✓ Resource Group já existe" -ForegroundColor Green
}

# Criar App Service Plan (Free tier)
Write-Host "`nVerificando App Service Plan..." -ForegroundColor Yellow
$planName = "$AppServiceName-plan"
$planExists = az appservice plan list --resource-group $ResourceGroupName --query "[?name=='$planName']" -o tsv
if (-not $planExists) {
    Write-Host "Criando App Service Plan: $planName (Free tier)" -ForegroundColor Yellow
    az appservice plan create `
        --name $planName `
        --resource-group $ResourceGroupName `
        --sku FREE `
        --is-linux
    Write-Host "✓ App Service Plan criado" -ForegroundColor Green
} else {
    Write-Host "✓ App Service Plan já existe" -ForegroundColor Green
}

# Criar Web App
Write-Host "`nVerificando Web App..." -ForegroundColor Yellow
$appExists = az webapp list --resource-group $ResourceGroupName --query "[?name=='$AppServiceName']" -o tsv
if (-not $appExists) {
    Write-Host "Criando Web App: $AppServiceName" -ForegroundColor Yellow
    az webapp create `
        --resource-group $ResourceGroupName `
        --plan $planName `
        --name $AppServiceName `
        --runtime "PYTHON:3.11"
    Write-Host "✓ Web App criada" -ForegroundColor Green
} else {
    Write-Host "✓ Web App já existe" -ForegroundColor Green
}

# Configurar variáveis de ambiente
Write-Host "`nConfigurando variáveis de ambiente..." -ForegroundColor Yellow
az webapp config appsettings set `
    --resource-group $ResourceGroupName `
    --name $AppServiceName `
    --settings `
        SCM_DO_BUILD_DURING_DEPLOYMENT=true `
        ENABLE_ORYX_BUILD=true `
        PYTHON_VERSION=3.11 `
        PORT=8000 `
        WEBSITES_PORT=8000 `
        WEBSITES_ENABLE_APP_SERVICE_STORAGE=false

if ($GeminiApiKey) {
    Write-Host "Configurando GEMINI_API_KEY..." -ForegroundColor Yellow
    az webapp config appsettings set `
        --resource-group $ResourceGroupName `
        --name $AppServiceName `
        --settings GEMINI_API_KEY=$GeminiApiKey
    Write-Host "✓ GEMINI_API_KEY configurada" -ForegroundColor Green
} else {
    Write-Host "⚠ GEMINI_API_KEY não fornecida. A API funcionará em modo mock." -ForegroundColor Yellow
    Write-Host "  Para configurar depois, execute:" -ForegroundColor Yellow
    Write-Host "  az webapp config appsettings set --resource-group $ResourceGroupName --name $AppServiceName --settings GEMINI_API_KEY=sua_chave" -ForegroundColor Gray
}

# Configurar startup command
Write-Host "`nConfigurando startup command..." -ForegroundColor Yellow
az webapp config set `
    --resource-group $ResourceGroupName `
    --name $AppServiceName `
    --startup-file "startup.sh"

Write-Host "✓ Startup command configurado" -ForegroundColor Green

# Fazer deploy do código
Write-Host "`nFazendo deploy do código..." -ForegroundColor Yellow
Write-Host "Navegando para pasta backend..." -ForegroundColor Gray
Push-Location backend

# Criar arquivo .deployment se não existir
if (-not (Test-Path ".deployment")) {
    Write-Host "Criando arquivo .deployment..." -ForegroundColor Gray
    @"
[config]
SCM_DO_BUILD_DURING_DEPLOYMENT=true
"@ | Out-File -FilePath ".deployment" -Encoding utf8
}

# Deploy usando ZIP
Write-Host "Criando pacote ZIP..." -ForegroundColor Gray
$zipFile = "deploy.zip"
if (Test-Path $zipFile) {
    Remove-Item $zipFile
}

# Criar ZIP excluindo arquivos desnecessários
$filesToExclude = @("__pycache__", "*.pyc", ".env", "venv", "*.log", "logs", ".git")
$excludeArgs = $filesToExclude | ForEach-Object { "-x", "*/$_/*" }
Compress-Archive -Path * -DestinationPath $zipFile -Force

Write-Host "Fazendo upload e deploy..." -ForegroundColor Gray
az webapp deployment source config-zip `
    --resource-group $ResourceGroupName `
    --name $AppServiceName `
    --src $zipFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Deploy concluído com sucesso!" -ForegroundColor Green
} else {
    Write-Host "✗ Erro no deploy!" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Limpar arquivo ZIP
Remove-Item $zipFile -ErrorAction SilentlyContinue
Pop-Location

# Obter URL da aplicação
$appUrl = az webapp show --resource-group $ResourceGroupName --name $AppServiceName --query defaultHostName -o tsv
$fullUrl = "https://$appUrl"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Deploy Concluído!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "URL da API: $fullUrl" -ForegroundColor Green
Write-Host "Documentação: $fullUrl/docs" -ForegroundColor Cyan
Write-Host "Health Check: $fullUrl/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Comandos úteis:" -ForegroundColor Yellow
Write-Host "  Ver logs: az webapp log tail --resource-group $ResourceGroupName --name $AppServiceName" -ForegroundColor Gray
Write-Host "  Ver configurações: az webapp config appsettings list --resource-group $ResourceGroupName --name $AppServiceName" -ForegroundColor Gray
Write-Host "  Reiniciar app: az webapp restart --resource-group $ResourceGroupName --name $AppServiceName" -ForegroundColor Gray
Write-Host ""

