# 🚀 Deploy no Azure - Aprenda Plus API

Este guia explica como fazer deploy da API Aprenda Plus no Azure App Service.

## 📋 Pré-requisitos

1. **Conta Azure** com subscription ativa
2. **Azure CLI** instalado ([Download](https://aka.ms/InstallAzureCLIWindows))
3. **Git** (opcional, para deploy via GitHub)

## 🎯 Opções de Deploy

### Opção 1: Script PowerShell (Windows Local)

Execute o script PowerShell diretamente no seu computador:

```powershell
# Deploy básico
.\deploy-azure.ps1

# Deploy com configurações personalizadas
.\deploy-azure.ps1 `
    -ResourceGroupName "rg-aprenda-plus" `
    -AppServiceName "aprenda-plus-api" `
    -Location "brazilsouth" `
    -GeminiApiKey "sua_chave_gemini_aqui"
```

**Parâmetros:**
- `ResourceGroupName`: Nome do Resource Group (padrão: `rg-aprenda-plus`)
- `AppServiceName`: Nome da aplicação (padrão: `aprenda-plus-api`)
- `Location`: Região do Azure (padrão: `brazilsouth`)
- `SubscriptionId`: ID da subscription (opcional)
- `GeminiApiKey`: Chave da API Gemini (opcional, funciona em modo mock sem ela)

### Opção 2: Azure Cloud Shell (Recomendado)

1. Acesse o [Azure Cloud Shell](https://shell.azure.com)
2. Faça upload do arquivo `deploy-azure.sh` ou clone o repositório
3. Execute:

```bash
# Dar permissão de execução
chmod +x deploy-azure.sh

# Deploy básico
./deploy-azure.sh

# Deploy com GEMINI_API_KEY
export GEMINI_API_KEY="sua_chave_aqui"
./deploy-azure.sh
```

### Opção 3: Deploy Manual via Azure CLI

```bash
# 1. Login
az login

# 2. Criar Resource Group
az group create --name rg-aprenda-plus --location brazilsouth

# 3. Criar App Service Plan (Free tier)
az appservice plan create \
    --name aprenda-plus-plan \
    --resource-group rg-aprenda-plus \
    --sku FREE \
    --is-linux

# 4. Criar Web App
az webapp create \
    --resource-group rg-aprenda-plus \
    --plan aprenda-plus-plan \
    --name aprenda-plus-api \
    --runtime "PYTHON:3.11"

# 5. Configurar variáveis de ambiente
az webapp config appsettings set \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --settings \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true \
        ENABLE_ORYX_BUILD=true \
        PYTHON_VERSION=3.11 \
        PORT=8000 \
        WEBSITES_PORT=8000 \
        GEMINI_API_KEY=sua_chave_aqui

# 6. Configurar startup
az webapp config set \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --startup-file "startup.sh"

# 7. Fazer deploy (via ZIP)
cd backend
zip -r deploy.zip . -x "*.pyc" "__pycache__/*" "*.log" ".env" "venv/*" ".git/*"
az webapp deployment source config-zip \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --src deploy.zip
rm deploy.zip
```

## 🔧 Configuração Pós-Deploy

### Configurar GEMINI_API_KEY

Se você não configurou a chave durante o deploy:

```bash
az webapp config appsettings set \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --settings GEMINI_API_KEY=sua_chave_aqui
```

### Verificar Logs

```bash
# Ver logs em tempo real
az webapp log tail \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api

# Baixar logs
az webapp log download \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --log-file logs.zip
```

### Reiniciar Aplicação

```bash
az webapp restart \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api
```

## 📊 Monitoramento

### Verificar Status

```bash
# Status da aplicação
az webapp show \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --query state

# URL da aplicação
az webapp show \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --query defaultHostName -o tsv
```

### Testar Endpoints

Após o deploy, teste os endpoints:

- **Health Check**: `https://seu-app.azurewebsites.net/health`
- **Documentação**: `https://seu-app.azurewebsites.net/docs`
- **API Root**: `https://seu-app.azurewebsites.net/`

## 🔄 Atualizar Deploy

Para atualizar a aplicação após mudanças:

### Via Script

```powershell
# PowerShell
.\deploy-azure.ps1 -AppServiceName "aprenda-plus-api"
```

```bash
# Bash/Cloud Shell
./deploy-azure.sh
```

### Via ZIP Manual

```bash
cd backend
zip -r deploy.zip . -x "*.pyc" "__pycache__/*" "*.log" ".env" "venv/*" ".git/*"
az webapp deployment source config-zip \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --src deploy.zip
rm deploy.zip
```

## 🗑️ Remover Recursos

Para remover todos os recursos criados:

```bash
az group delete --name rg-aprenda-plus --yes --no-wait
```

## ⚠️ Troubleshooting

### Aplicação não inicia

1. Verificar logs:
   ```bash
   az webapp log tail --resource-group rg-aprenda-plus --name aprenda-plus-api
   ```

2. Verificar configurações:
   ```bash
   az webapp config appsettings list --resource-group rg-aprenda-plus --name aprenda-plus-api
   ```

3. Verificar startup command:
   ```bash
   az webapp config show --resource-group rg-aprenda-plus --name aprenda-plus-api --query linuxFxVersion
   ```

### Erro 500 Internal Server Error

- Verificar se todas as dependências estão no `requirements.txt`
- Verificar logs para erros específicos
- Verificar se `GEMINI_API_KEY` está configurada (se necessário)

### Porta não configurada

Certifique-se de que as variáveis de ambiente estão configuradas:
- `PORT=8000`
- `WEBSITES_PORT=8000`

## 📝 Notas Importantes

1. **Tier Gratuito**: O Azure App Service Free tier tem limitações:
   - Aplicação pode ficar inativa após 20 minutos de inatividade
   - Recursos limitados (CPU, memória)
   - Para produção, considere usar um tier pago

2. **CORS**: A API já está configurada para aceitar requisições de qualquer origem. Em produção, considere restringir.

3. **Variáveis de Ambiente**: Nunca commite arquivos `.env` com chaves reais no repositório.

4. **Custos**: O tier Free é gratuito, mas recursos adicionais podem gerar custos.

## 🔗 Links Úteis

- [Azure App Service Documentation](https://docs.microsoft.com/azure/app-service/)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)
- [Python no Azure App Service](https://docs.microsoft.com/azure/app-service/quickstart-python)

## 📧 Suporte

Para problemas ou dúvidas:
1. Verifique os logs da aplicação
2. Consulte a documentação do Azure
3. Verifique se todas as dependências estão instaladas

---

**Desenvolvido para o projeto Aprenda Plus**

