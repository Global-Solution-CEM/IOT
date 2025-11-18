# Script PowerShell para iniciar PM2 no Windows
# Este script pode ser adicionado ao Task Scheduler para iniciar automaticamente

Set-Location $PSScriptRoot

# Iniciar PM2 e restaurar processos salvos
pm2 resurrect

