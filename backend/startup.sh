#!/bin/bash
# Script de inicialização para Azure App Service
# Este script é executado quando a aplicação inicia no Azure

# Ativar modo não-bufferizado do Python para logs em tempo real
export PYTHONUNBUFFERED=1

# Navegar para o diretório da aplicação
cd /home/site/wwwroot

# Instalar dependências se necessário (Azure faz isso automaticamente, mas garantimos)
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
fi

# Executar a aplicação FastAPI
# O Azure App Service define a variável PORT automaticamente
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1

