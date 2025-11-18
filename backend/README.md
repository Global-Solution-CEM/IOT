# Aprenda Plus - AI Course Recommendation API

Sistema de recomendações personalizadas de cursos usando **IA Generativa (Google Gemini)** integrado com o app mobile React Native "Aprenda Plus".

## 🎯 Visão Geral

Esta API utiliza **Deep Learning** através de modelos de IA Generativa para:
- Analisar perfis de usuários em detalhes
- Gerar recomendações personalizadas de cursos
- Criar explicações contextuais para cada recomendação
- Analisar compatibilidade e sugerir trilhas de aprendizado

## 🚀 Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **Google Gemini API**: IA Generativa para análise e geração de conteúdo
- **Python 3.10+**: Linguagem base
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI

## 📋 Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Google Gemini API Key ([obtenha aqui](https://makersuite.google.com/app/apikey))

## 🔧 Instalação

### 1. Clone o repositório ou navegue até a pasta backend

```bash
cd backend
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API:

```
GEMINI_API_KEY=sua_chave_aqui
PORT=8000
```

**Nota**: Se você não tiver uma chave da API do Gemini, o sistema funcionará em modo mock para desenvolvimento/testes.

## 🏃 Executando o Servidor

### Desenvolvimento

```bash
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --reload --port 8000
```

O servidor estará disponível em: `http://localhost:8000`

### Documentação Interativa

Acesse a documentação automática da API:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 Endpoints Principais

### 1. Health Check
```
GET /health
```
Verifica se a API e o serviço de IA estão funcionando.

### 2. Recomendações de Cursos (Principal)
```
POST /api/courses/suggested/{user_id}
```
Endpoint principal que usa IA Generativa para gerar recomendações personalizadas.

**Body (JSON):**
```json
{
  "user_profile": {
    "user_id": "123",
    "name": "João Silva",
    "email": "joao@email.com",
    "areas_interesse": [
      {
        "area": "programacao",
        "nivel": "intermediario"
      },
      {
        "area": "ia",
        "nivel": "iniciante"
      }
    ],
    "cursos_completos": ["1", "5"],
    "cursos_em_andamento": ["2"],
    "progresso_cursos": {
      "2": 45
    }
  },
  "limit": 10
}
```

**Resposta:**
```json
{
  "user_id": "123",
  "recommendations": [
    {
      "course": {
        "id": "3",
        "titulo": "Desenvolvimento Web Full Stack",
        "descricao": "...",
        "area": "programacao",
        "nivel": "intermediario",
        "duracao": "80 horas",
        "icone": "💻"
      },
      "score": 0.95,
      "reason": "Recomendado porque combina seu interesse em programação...",
      "compatibility": "Compatível com seu nível intermediário...",
      "suggested_learning_path": "Complete este curso após finalizar Análise de Dados"
    }
  ],
  "profile_analysis": {
    "pontos_fortes": [...],
    "areas_crescimento": [...],
    ...
  },
  "generated_at": "2024-01-01T12:00:00",
  "model_used": "gemini-pro"
}
```

### 3. Análise de Perfil
```
POST /api/ai/analyze-profile
```
Analisa o perfil do usuário usando IA Generativa.

### 4. Explicação de Recomendação
```
POST /api/ai/generate-explaination
```
Gera explicação personalizada de por que um curso foi recomendado.

## 🔗 Integração com App Mobile

O app React Native já está preparado para consumir esta API:

1. **Endpoint configurado**: O app usa `/api/courses/suggested/{user_id}` (ver `endpoints.js`)

2. **Atualizar URL da API**: No arquivo `services/api/config.js` do app mobile:
```javascript
BASE_URL: __DEV__ 
  ? 'http://localhost:8000/api'  // Para desenvolvimento local
  : 'https://sua-api-em-producao.com/api'
```

3. **Ativar integração**: No arquivo `CoursesService.js`, alterar:
```javascript
const USE_API = true;  // Mudar de false para true
```

## 🧠 Como Funciona a IA

### Prompt Engineering

O sistema utiliza técnicas avançadas de **Prompt Engineering**:

1. **Análise de Perfil**:
   - Analisa áreas de interesse, níveis e histórico
   - Identifica pontos fortes e áreas de crescimento
   - Calcula compatibilidade com diferentes áreas

2. **Geração de Recomendações**:
   - Combina análise de perfil com catálogo de cursos
   - Gera explicações personalizadas para cada recomendação
   - Calcula scores de relevância
   - Sugere trilhas de aprendizado

3. **Explicações Contextuais**:
   - Cada recomendação inclui uma explicação gerada pela IA
   - Análise de compatibilidade específica
   - Sugestões de sequência de aprendizado

### Modelo Utilizado

- **Google Gemini Pro**: Modelo de IA Generativa da Google
- **Configurações**:
  - Temperature: 0.7 (balance entre criatividade e precisão)
  - Max tokens: 2048
  - Safety settings: Configurados para permitir conteúdo educacional

## 📁 Estrutura do Projeto

```
backend/
├── main.py                      # Aplicação FastAPI principal
├── run.py                       # Script alternativo de execução
├── requirements.txt             # Dependências Python
├── .env.example                 # Exemplo de configuração
├── README.md                    # Este arquivo
│
├── services/
│   ├── servico_ia.py           # Serviço de integração com Gemini
│   ├── servico_recomendacoes.py # Geração de recomendações
│   └── analisador_perfil.py    # Análise de perfis
│
├── models/
│   ├── perfil_usuario.py       # Modelos de perfil
│   └── curso.py                # Modelos de curso
│
└── data/
    └── banco_cursos.py         # Base de dados de cursos
```

## 🧪 Testando a API

### Usando cURL

```bash
curl -X POST "http://localhost:8000/api/courses/suggested/123" \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {
      "user_id": "123",
      "areas_interesse": [
        {"area": "programacao", "nivel": "intermediario"},
        {"area": "ia", "nivel": "iniciante"}
      ]
    },
    "limit": 5
  }'
```

### Usando Python

```python
import requests

url = "http://localhost:8000/api/courses/suggested/123"
data = {
    "user_profile": {
        "user_id": "123",
        "areas_interesse": [
            {"area": "programacao", "nivel": "intermediario"}
        ]
    }
}

response = requests.post(url, json=data)
print(response.json())
```

### Usando a Interface Swagger

Acesse http://localhost:8000/docs e use a interface interativa para testar todos os endpoints.

## 🐛 Modo Mock (Desenvolvimento sem API Key)

Se você não tiver uma chave da API do Gemini, o sistema funcionará em **modo mock**:
- Respostas simuladas para desenvolvimento
- Permite testar a integração sem custos
- Para produção, é necessário configurar a API key real

## 🔒 Segurança

- **CORS**: Configurado para permitir requisições do app mobile
- **Validação**: Todos os dados são validados com Pydantic
- **Error Handling**: Tratamento robusto de erros
- **Logging**: Sistema de logs para monitoramento

## 📊 Monitoramento

O sistema inclui:
- Health check endpoint
- Logging detalhado
- Tratamento de erros centralizado
- Métricas de uso (expandível)

## 🚀 Deploy em Produção

### Opções de Deploy

1. **Heroku**: Deploy direto com Procfile
2. **Railway**: Deploy simples via GitHub
3. **AWS/DigitalOcean**: Usando Docker
4. **Vercel/Netlify**: Para funções serverless

### Variáveis de Ambiente em Produção

Certifique-se de configurar:
- `GEMINI_API_KEY`: Chave da API do Gemini
- `PORT`: Porta do servidor
- `ENVIRONMENT`: production

## 📝 Notas Importantes

- **Custos da API**: O Google Gemini tem limites gratuitos generosos. Consulte [preços](https://ai.google.dev/pricing)
- **Rate Limiting**: Considere implementar rate limiting para produção
- **Cache**: Para melhor performance, considere cachear análises de perfil

## 🤝 Contribuindo

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais acadêmicos.

## 📧 Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Consulte a documentação em `/docs`
- Verifique os logs do servidor

---

**Desenvolvido com ❤️ para o projeto Aprenda Plus**

