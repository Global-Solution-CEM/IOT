#!/bin/bash
# Script de Deploy para Azure App Service (Azure Cloud Shell)
# Execute este script no Azure Cloud Shell para fazer deploy da API

set -e  # Parar em caso de erro

# Configurações padrão
RESOURCE_GROUP_NAME="${RESOURCE_GROUP_NAME:-rg-aprenda-plus}"
APP_SERVICE_NAME="${APP_SERVICE_NAME:-aprenda-plus-api}"
LOCATION="${LOCATION:-brazilsouth}"
PLAN_NAME="${APP_SERVICE_NAME}-plan"

echo "========================================"
echo "Deploy Aprenda Plus API - Azure"
echo "========================================"
echo ""

# Verificar se Azure CLI está disponível
echo "Verificando Azure CLI..."
if ! command -v az &> /dev/null; then
    echo "✗ Azure CLI não encontrado!"
    exit 1
fi
echo "✓ Azure CLI encontrado"

# Verificar login
echo ""
echo "Verificando login no Azure..."
if ! az account show &> /dev/null; then
    echo "Fazendo login no Azure..."
    az login
fi
echo "✓ Logado no Azure"

# Criar Resource Group se não existir
echo ""
echo "Verificando Resource Group..."
if ! az group show --name "$RESOURCE_GROUP_NAME" &> /dev/null; then
    echo "Criando Resource Group: $RESOURCE_GROUP_NAME"
    az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION"
    echo "✓ Resource Group criado"
else
    echo "✓ Resource Group já existe"
fi

# Criar App Service Plan (Free tier)
echo ""
echo "Verificando App Service Plan..."
if ! az appservice plan show --name "$PLAN_NAME" --resource-group "$RESOURCE_GROUP_NAME" &> /dev/null; then
    echo "Criando App Service Plan: $PLAN_NAME (Free tier)"
    az appservice plan create \
        --name "$PLAN_NAME" \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --sku FREE \
        --is-linux
    echo "✓ App Service Plan criado"
else
    echo "✓ App Service Plan já existe"
fi

# Criar Web App
echo ""
echo "Verificando Web App..."
if ! az webapp show --name "$APP_SERVICE_NAME" --resource-group "$RESOURCE_GROUP_NAME" &> /dev/null; then
    echo "Criando Web App: $APP_SERVICE_NAME"
    az webapp create \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --plan "$PLAN_NAME" \
        --name "$APP_SERVICE_NAME" \
        --runtime "PYTHON:3.11"
    echo "✓ Web App criada"
else
    echo "✓ Web App já existe"
fi

# Configurar variáveis de ambiente
echo ""
echo "Configurando variáveis de ambiente..."
az webapp config appsettings set \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --name "$APP_SERVICE_NAME" \
    --settings \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true \
        ENABLE_ORYX_BUILD=true \
        PYTHON_VERSION=3.11 \
        PORT=8000 \
        WEBSITES_PORT=8000 \
        WEBSITES_ENABLE_APP_SERVICE_STORAGE=false \
    --output none

# Configurar GEMINI_API_KEY se fornecido
if [ -n "$GEMINI_API_KEY" ]; then
    echo "Configurando GEMINI_API_KEY..."
    az webapp config appsettings set \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --name "$APP_SERVICE_NAME" \
        --settings GEMINI_API_KEY="$GEMINI_API_KEY" \
        --output none
    echo "✓ GEMINI_API_KEY configurada"
else
    echo "⚠ GEMINI_API_KEY não fornecida. A API funcionará em modo mock."
    echo "  Para configurar depois, execute:"
    echo "  az webapp config appsettings set --resource-group $RESOURCE_GROUP_NAME --name $APP_SERVICE_NAME --settings GEMINI_API_KEY=sua_chave"
fi

# Configurar startup command
echo ""
echo "Configurando startup command..."
az webapp config set \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --name "$APP_SERVICE_NAME" \
    --startup-file "startup.sh"
echo "✓ Startup command configurado"

# Fazer deploy do código
echo ""
echo "Fazendo deploy do código..."

# Verificar se a pasta backend existe
if [ ! -d "backend" ]; then
    echo "⚠ Pasta 'backend' não encontrada no diretório atual."
    echo ""
    echo "Opções para continuar:"
    echo "1. Se você tem o código em um repositório Git, clone-o:"
    echo "   git clone <seu-repositorio>"
    echo "   cd <nome-do-repositorio>"
    echo "   ./deploy-azure.sh"
    echo ""
    echo "2. Faça upload dos arquivos usando o Cloud Shell:"
    echo "   - Clique no ícone de upload no Cloud Shell"
    echo "   - Faça upload da pasta 'backend' ou de um ZIP com o código"
    echo "   - Extraia se necessário: unzip arquivo.zip"
    echo ""
    echo "3. Use deploy direto via Git (se configurado):"
    echo "   az webapp deployment source config --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP_NAME --repo-url <url> --branch main --manual-integration"
    echo ""
    read -p "Pressione Enter para tentar continuar mesmo assim (pode falhar) ou Ctrl+C para cancelar..."
fi

# Tentar navegar para backend (pode falhar se não existir)
if [ -d "backend" ]; then
    cd backend
else
    echo "⚠ Continuando no diretório atual (assumindo que os arquivos estão aqui)..."
    # Verificar se main.py existe
    if [ ! -f "main.py" ] && [ ! -f "backend/main.py" ]; then
        echo "✗ Erro: Arquivo main.py não encontrado!"
        echo "   Certifique-se de que os arquivos do projeto estão disponíveis."
        exit 1
    fi
fi

# Criar arquivo .deployment se não existir
if [ ! -f ".deployment" ]; then
    echo "Criando arquivo .deployment..."
    cat > .deployment <<EOF
[config]
SCM_DO_BUILD_DURING_DEPLOYMENT=true
EOF
fi

# Criar pacote ZIP
echo "Criando pacote ZIP..."
ZIP_FILE="deploy.zip"
rm -f "$ZIP_FILE"

# Criar ZIP excluindo arquivos desnecessários
zip -r "$ZIP_FILE" . \
    -x "*.pyc" \
    -x "__pycache__/*" \
    -x "*.log" \
    -x "logs/*" \
    -x ".env" \
    -x "venv/*" \
    -x ".git/*" \
    -x "*.zip"

# Fazer deploy
echo "Fazendo upload e deploy..."
az webapp deployment source config-zip \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --name "$APP_SERVICE_NAME" \
    --src "$ZIP_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Deploy concluído com sucesso!"
else
    echo "✗ Erro no deploy!"
    rm -f "$ZIP_FILE"
    exit 1
fi

# Limpar arquivo ZIP
rm -f "$ZIP_FILE"
# Voltar ao diretório anterior se estivermos em backend
[ -d "backend" ] && cd .. || true

# Obter URL da aplicação
APP_URL=$(az webapp show --resource-group "$RESOURCE_GROUP_NAME" --name "$APP_SERVICE_NAME" --query defaultHostName -o tsv)
FULL_URL="https://$APP_URL"

echo ""
echo "========================================"
echo "Deploy Concluído!"
echo "========================================"
echo ""
echo "URL da API: $FULL_URL"
echo "Documentação: $FULL_URL/docs"
echo "Health Check: $FULL_URL/health"
echo ""
echo "Comandos úteis:"
echo "  Ver logs: az webapp log tail --resource-group $RESOURCE_GROUP_NAME --name $APP_SERVICE_NAME"
echo "  Ver configurações: az webapp config appsettings list --resource-group $RESOURCE_GROUP_NAME --name $APP_SERVICE_NAME"
echo "  Reiniciar app: az webapp restart --resource-group $RESOURCE_GROUP_NAME --name $APP_SERVICE_NAME"
echo ""

