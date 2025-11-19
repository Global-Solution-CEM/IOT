# 🚀 Quick Start - Deploy Azure

## Opção 1: PowerShell (Windows)

```powershell
# 1. Login no Azure (se necessário)
az login

# 2. Executar script de deploy
.\deploy-azure.ps1 -GeminiApiKey "sua_chave_aqui"
```

## Opção 2: Azure Cloud Shell

1. Acesse: https://shell.azure.com
2. Faça upload do arquivo `deploy-azure.sh`
3. Execute:

```bash
chmod +x deploy-azure.sh
export GEMINI_API_KEY="sua_chave_aqui"  # Opcional
./deploy-azure.sh
```

## ⚡ Comandos Rápidos

```bash
# Ver logs
az webapp log tail --resource-group rg-aprenda-plus --name aprenda-plus-api

# Ver URL
az webapp show --resource-group rg-aprenda-plus --name aprenda-plus-api --query defaultHostName -o tsv

# Reiniciar
az webapp restart --resource-group rg-aprenda-plus --name aprenda-plus-api
```

## 📝 Notas

- O tier **FREE** pode deixar a app inativa após 20min
- A API funciona em **modo mock** sem GEMINI_API_KEY
- Veja `DEPLOY_AZURE.md` para documentação completa

