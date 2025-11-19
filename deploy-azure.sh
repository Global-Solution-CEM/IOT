#!/bin/bash
# ☁️ Deploy no Azure (App Service) - Aprenda Plus API
# Execute este script no Azure Cloud Shell

set -e

echo "☁️ Deploy no Azure - Aprenda Plus API"
echo "======================================"
echo ""

# 📦 Definir variáveis
export RESOURCE_GROUP=AprendaPlusRG
export LOCATION=brazilsouth
export APP_SERVICE_PLAN=aprenda-plus-plan
export WEBAPP_NAME=aprenda-plus-api
export GEMINI_API_KEY="${GEMINI_API_KEY:-}"

echo "📋 Variáveis configuradas:"
echo "   RESOURCE_GROUP: $RESOURCE_GROUP"
echo "   LOCATION: $LOCATION"
echo "   APP_SERVICE_PLAN: $APP_SERVICE_PLAN"
echo "   WEBAPP_NAME: $WEBAPP_NAME"
echo ""

# 1. Criar Resource Group
echo "🔨 Criando Resource Group..."
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# 2. Criar App Service Plan (Free tier)
echo ""
echo "🔨 Criando App Service Plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku FREE \
  --is-linux

# 3. Criar Web App
echo ""
echo "🔨 Criando Web App..."
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $WEBAPP_NAME \
  --runtime "PYTHON:3.11"

# 4. Configurar variáveis de ambiente
echo ""
echo "⚙️ Configurando variáveis de ambiente..."
SETTINGS="SCM_DO_BUILD_DURING_DEPLOYMENT=true ENABLE_ORYX_BUILD=true PYTHON_VERSION=3.11 PORT=8000 WEBSITES_PORT=8000"

if [ -n "$GEMINI_API_KEY" ]; then
  SETTINGS="$SETTINGS GEMINI_API_KEY=$GEMINI_API_KEY"
  echo "   ✓ GEMINI_API_KEY configurada"
else
  echo "   ⚠ GEMINI_API_KEY não fornecida (API funcionará em modo mock)"
fi

az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEBAPP_NAME \
  --settings $SETTINGS

# 5. Configurar startup command
echo ""
echo "⚙️ Configurando startup command..."
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $WEBAPP_NAME \
  --startup-file "startup.sh"

# 6. Verificar se a pasta backend existe
echo ""
echo "📦 Verificando arquivos do projeto..."
if [ ! -d "backend" ]; then
  echo "⚠ Pasta 'backend' não encontrada!"
  echo ""
  echo "📥 Opções:"
  echo "   1. Faça upload da pasta 'backend' via Cloud Shell (botão Upload)"
  echo "   2. Ou clone o repositório: git clone <seu-repositorio>"
  echo ""
  echo "   Após fazer upload/clone, execute este script novamente."
  exit 1
fi

# 7. Preparar e fazer deploy
echo ""
echo "📦 Preparando artefato para deploy..."
cd backend

# Criar arquivo .deployment se não existir
if [ ! -f ".deployment" ]; then
  cat > .deployment <<EOF
[config]
SCM_DO_BUILD_DURING_DEPLOYMENT=true
EOF
fi

# Criar ZIP para deploy
echo "   Criando ZIP..."
zip -r app.zip . \
  -x "*.pyc" \
  -x "__pycache__/*" \
  -x "*.log" \
  -x "logs/*" \
  -x ".env" \
  -x "venv/*" \
  -x ".git/*" \
  -x "*.zip"

# Fazer deploy
echo ""
echo "🚀 Fazendo deploy..."
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $WEBAPP_NAME \
  --src app.zip

# Limpar
rm -f app.zip
cd ..

# 8. Obter URL e informações
echo ""
echo "✅ Deploy concluído!"
echo ""
APP_URL=$(az webapp show --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME --query defaultHostName -o tsv)
echo "🌐 URL da API: https://$APP_URL"
echo "📚 Documentação: https://$APP_URL/docs"
echo "❤️ Health Check: https://$APP_URL/health"
echo ""

# 9. Comandos úteis
echo "📋 Comandos úteis:"
echo "   Ver logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME"
echo "   Reiniciar: az webapp restart --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME"
echo "   Ver status: az webapp show --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME --query state"
echo ""

