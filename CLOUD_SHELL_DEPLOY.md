# 🚀 Deploy no Azure Cloud Shell - Guia Rápido

## ⚠️ Problema: Arquivos não encontrados

O Azure Cloud Shell é **efêmero** - os arquivos não persistem entre sessões. Você precisa fazer upload ou clonar o repositório.

## 📦 Opção 1: Upload via Cloud Shell (Mais Rápido)

### Passo 1: Preparar arquivos localmente

No seu computador, crie um ZIP com a pasta `backend`:

```powershell
# Windows PowerShell
cd C:\Users\PC-MURILLO\IOT-3
Compress-Archive -Path backend -DestinationPath backend.zip -Force
```

### Passo 2: Upload no Cloud Shell

1. No Azure Cloud Shell, clique no ícone **📁 Upload/Download files**
2. Selecione **Upload**
3. Faça upload do arquivo `backend.zip`
4. Extraia o arquivo:

```bash
unzip backend.zip
```

### Passo 3: Executar deploy

```bash
chmod +x deploy-azure.sh
export GEMINI_API_KEY="AIzaSyCncDNgwimag2kXDkRafBqeJ4tPlbThE4k"
./deploy-azure.sh
```

## 📦 Opção 2: Clone via Git (Recomendado)

Se seu código está no GitHub/GitLab:

```bash
# 1. Clone o repositório
git clone <seu-repositorio-url>
cd <nome-do-repositorio>

# 2. Executar deploy
chmod +x deploy-azure.sh
export GEMINI_API_KEY="AIzaSyCncDNgwimag2kXDkRafBqeJ4tPlbThE4k"
./deploy-azure.sh
```

## 📦 Opção 3: Deploy direto via ZIP (Sem script)

Se você já tem o ZIP pronto:

```bash
# 1. Fazer upload do backend.zip no Cloud Shell
# 2. Extrair (se necessário)
unzip backend.zip -d backend

# 3. Criar ZIP para deploy
cd backend
zip -r deploy.zip . -x "*.pyc" "__pycache__/*" "*.log" ".env" "venv/*" ".git/*"

# 4. Fazer deploy
az webapp deployment source config-zip \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --src deploy.zip

# 5. Limpar
rm deploy.zip
```

## 🔧 Verificar se funcionou

```bash
# Obter URL
az webapp show --resource-group rg-aprenda-plus --name aprenda-plus-api --query defaultHostName -o tsv

# Ver logs
az webapp log tail --resource-group rg-aprenda-plus --name aprenda-plus-api
```

## ⚡ Solução Rápida Agora

Como você já executou o script e os recursos foram criados, você só precisa fazer o deploy do código:

```bash
# 1. Fazer upload do backend.zip no Cloud Shell
# 2. Extrair
unzip backend.zip

# 3. Criar ZIP e fazer deploy
cd backend
zip -r deploy.zip . -x "*.pyc" "__pycache__/*" "*.log" ".env" "venv/*" ".git/*"
az webapp deployment source config-zip \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --src deploy.zip
rm deploy.zip
```

## ✅ Verificar variáveis de ambiente

As variáveis podem ter aparecido como `null` no output, mas isso é normal. Verifique se estão configuradas:

```bash
az webapp config appsettings list \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --query "[?name=='GEMINI_API_KEY' || name=='PORT' || name=='WEBSITES_PORT']"
```

Se não estiverem configuradas, configure novamente:

```bash
az webapp config appsettings set \
    --resource-group rg-aprenda-plus \
    --name aprenda-plus-api \
    --settings \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true \
        ENABLE_ORYX_BUILD=true \
        PYTHON_VERSION=3.11 \
        PORT=8000 \
        WEBSITES_PORT=8000 \
        GEMINI_API_KEY="AIzaSyCncDNgwimag2kXDkRafBqeJ4tPlbThE4k"
```

