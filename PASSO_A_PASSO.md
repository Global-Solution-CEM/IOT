# 🧪 Teste Passo a Passo - Do Zero

Guia simples para testar o projeto desde o início.

## 📋 Pré-requisitos

- Python 3.10 ou superior instalado
- Terminal/PowerShell aberto

## 🚀 Passo 1: Verificar Python

```bash
python --version
```

**Deve mostrar:** `Python 3.10.x` ou superior

## 🔧 Passo 2: Navegar até a Pasta Backend

```bash
cd backend
```

**Você deve estar em:** `C:\Users\PC-MURILLO\IOT\backend`

## 📦 Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

**Aguarde a instalação.** Deve instalar:
- fastapi
- uvicorn
- pydantic
- python-dotenv
- etc.

## ✅ Passo 4: Verificar Instalação (Opcional)

```bash
python -c "import fastapi, uvicorn, pydantic; print('OK - Dependencias instaladas')"
```

**Deve mostrar:** `OK - Dependencias instaladas`

## 🏃 Passo 5: Iniciar o Servidor

```bash
python main.py
```

**Você deve ver:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**⚠️ IMPORTANTE:** Mantenha este terminal aberto! O servidor precisa ficar rodando.

## 🧪 Passo 6: Testar a API

**Abra OUTRO terminal** (mantenha o servidor rodando no primeiro).

### 6.1. Teste Rápido - Health Check

**No navegador:**
```
http://localhost:8000/health
```

**Ou no terminal:**
```bash
python -c "import requests; r = requests.get('http://localhost:8000/health'); print(r.json())"
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "service": "course-recommendation-api",
  "timestamp": "...",
  "ai_service_status": "connected"
}
```

### 6.2. Teste Completo - Script de Testes

```bash
cd C:\Users\PC-MURILLO\IOT\examples
python testar_api.py
```

**Todos os testes devem passar!**

### 6.3. Documentação Interativa (Swagger)

**No navegador:**
```
http://localhost:8000/docs
```

Aqui você pode testar todos os endpoints clicando em "Try it out"!

## ✅ Checklist de Testes

Marque conforme testar:

- [ ] Python instalado e funcionando
- [ ] Dependências instaladas
- [ ] Servidor iniciado sem erros
- [ ] Health check funcionando (http://localhost:8000/health)
- [ ] Documentação Swagger acessível (http://localhost:8000/docs)
- [ ] Script de testes passou (python examples/testar_api.py)
- [ ] Endpoint de recomendações funcionando

## 🐛 Problemas Comuns

### Erro: "ModuleNotFoundError"
**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Address already in use"
**Solução:** A porta 8000 está em uso. Pare o servidor anterior (Ctrl+C) ou feche o processo.

### Erro: "Connection refused"
**Solução:** O servidor não está rodando. Execute `python main.py` no passo 5.

## 🎯 Próximos Passos

Quando todos os testes passarem:

1. ✅ API testada e funcionando
2. 📱 Pronto para integração com app mobile
3. 🚀 Pronto para deploy em produção

---

**Vamos começar! Execute os passos acima.** 🚀


