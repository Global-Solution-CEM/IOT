# ☁️ Deploy no Azure (App Service) - Aprenda Plus API

## 📦 Preparar artefato local

No seu computador, prepare a pasta `backend` para upload:

```powershell
# Windows PowerShell
cd C:\Users\PC-MURILLO\IOT-3
Compress-Archive -Path backend -DestinationPath backend.zip -Force
```

## ☁️ Passo a passo no Azure Cloud Shell

Abra o Portal Azure e inicie o Cloud Shell (bash).

### 1. Fazer upload dos arquivos

**Opção A - Upload direto:**
- Clique no ícone **Upload/Download files** no Cloud Shell
- Faça upload do arquivo `backend.zip`
- Extraia: `unzip backend.zip`

**Opção B - Clone do repositório:**
```bash
git clone <seu-repositorio-url>
cd <nome-do-repositorio>
```

### 2. Executar script de deploy

```bash
# Dar permissão de execução
chmod +x deploy-azure.sh

# Deploy básico (modo mock)
./deploy-azure.sh

# Deploy com GEMINI_API_KEY
export GEMINI_API_KEY="sua_chave_aqui"
./deploy-azure.sh

# Se o nome da app já existe, use um nome diferente:
export WEBAPP_NAME="aprenda-plus-api-unico"
./deploy-azure.sh

# Ou use o Resource Group existente:
export RESOURCE_GROUP="rg-aprenda-plus"
./deploy-azure.sh
```

## 📋 O que o script faz

1. ✅ Cria Resource Group (`AprendaPlusRG`)
2. ✅ Cria App Service Plan (Free tier)
3. ✅ Cria Web App com Python 3.11
4. ✅ Configura variáveis de ambiente
5. ✅ Configura startup command
6. ✅ Faz deploy do código via ZIP

## 🔧 Comandos manuais (alternativa)

Se preferir executar passo a passo:

```bash
# Definir variáveis
export RESOURCE_GROUP=AprendaPlusRG
export LOCATION=brazilsouth
export APP_SERVICE_PLAN=aprenda-plus-plan
export WEBAPP_NAME=aprenda-plus-api
export GEMINI_API_KEY="sua_chave_aqui"

# Criar Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Criar App Service Plan
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku FREE \
  --is-linux

# Criar Web App
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $WEBAPP_NAME \
  --runtime "PYTHON:3.11"

# Configurar variáveis de ambiente
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEBAPP_NAME \
  --settings \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    ENABLE_ORYX_BUILD=true \
    PYTHON_VERSION=3.11 \
    PORT=8000 \
    WEBSITES_PORT=8000 \
    GEMINI_API_KEY="$GEMINI_API_KEY"

# Configurar startup
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $WEBAPP_NAME \
  --startup-file "startup.sh"

# Fazer deploy
cd backend
zip -r app.zip . -x "*.pyc" "__pycache__/*" "*.log" ".env" "venv/*" ".git/*"
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $WEBAPP_NAME \
  --src app.zip
rm app.zip
```

## 🔄 Atualizar deploy

Após fazer mudanças no código:

```bash
# 1. Fazer upload da nova versão ou fazer pull
# 2. Executar o script novamente
./deploy-azure.sh

# Ou fazer deploy manual do ZIP
cd backend
zip -r app.zip . -x "*.pyc" "__pycache__/*" "*.log" ".env" "venv/*" ".git/*"
az webapp deployment source config-zip \
  --resource-group AprendaPlusRG \
  --name aprenda-plus-api \
  --src app.zip
rm app.zip
```

## 📊 Monitoramento

```bash
# Ver logs em tempo real
az webapp log tail --resource-group AprendaPlusRG --name aprenda-plus-api

# Reiniciar aplicação
az webapp restart --resource-group AprendaPlusRG --name aprenda-plus-api

# Ver status
az webapp show --resource-group AprendaPlusRG --name aprenda-plus-api --query state

# Obter URL
az webapp show --resource-group AprendaPlusRG --name aprenda-plus-api --query defaultHostName -o tsv
```

## 🗑️ Remover recursos

```bash
az group delete --name AprendaPlusRG --yes --no-wait
```

## ⚠️ Notas

- O tier **FREE** pode deixar a app inativa após 20min de inatividade
- A API funciona em **modo mock** sem `GEMINI_API_KEY`
- Para produção, considere usar um tier pago (B1 ou superior)

