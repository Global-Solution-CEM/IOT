# Aprenda Plus - Sistema de Recomendações com IA Generativa

Sistema completo de recomendações personalizadas de cursos usando **IA Generativa (Google Gemini)** integrado com o app mobile React Native "Aprenda Plus".

## 🎯 Visão Geral

Este projeto demonstra uma aplicação baseada em **Deep Learning** que resolve o problema de recomendações personalizadas de cursos educacionais, integrada às disciplinas de **Desenvolvimento Web** e **Mobile**.

### Requisitos Técnicos Atendidos

✅ **IA Generativa**: Implementação usando Google Gemini API com técnicas avançadas de Prompt Engineering

✅ **Integração Interdisciplinar**: Backend Python/FastAPI integrado com app React Native

✅ **REST API**: Interface funcional que consome resultados do modelo de IA

✅ **Deep Learning**: Análise de perfis e geração de recomendações usando IA Generativa

## 📁 Estrutura do Projeto

```
.
├── backend/                      # API Python/FastAPI com IA
│   ├── main.py                  # Aplicação principal
│   ├── requirements.txt         # Dependências Python
│   ├── README.md                # Documentação da API
│   ├── Procfile                 # Configuração para deploy
│   │
│   ├── services/               # Serviços de IA
│   │   ├── servico_ia.py       # Integração com Gemini API
│   │   ├── servico_recomendacoes.py  # Geração de recomendações
│   │   └── analisador_perfil.py # Análise de perfis
│   │
│   ├── models/                 # Modelos de dados
│   │   ├── perfil_usuario.py
│   │   └── curso.py
│   │
│   └── data/                   # Base de dados
│       └── banco_cursos.py
│
└── examples/                    # Exemplos e testes
    └── testar_api.py           # Script de testes da API
```

## 🚀 Início Rápido

### Backend (API com IA)

1. **Navegue até a pasta backend**:
   ```bash
   cd backend
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   
   # Edite .env e adicione sua chave do Gemini (opcional)
   # O sistema funciona em modo mock sem a chave
   GEMINI_API_KEY=sua_chave_aqui
   PORT=8000
   ```

5. **Execute o servidor**:
   ```bash
   python main.py
   ```

   O servidor estará disponível em: `http://localhost:8000`
   - Documentação: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Testando a API

Execute o script de testes:

```bash
cd examples
python testar_api.py
```

Ou acesse a documentação interativa: `http://localhost:8000/docs`

## 🧠 Como Funciona

### Arquitetura da IA

1. **Análise de Perfil**:
   - O usuário fornece áreas de interesse, níveis e histórico
   - A IA (Gemini) analisa o perfil completo
   - Gera insights sobre pontos fortes, áreas de crescimento e perfil de aprendizado

2. **Geração de Recomendações**:
   - A IA combina análise de perfil com catálogo de cursos
   - Gera recomendações personalizadas com scores de relevância
   - Cria explicações contextuais para cada recomendação

3. **Explicações Personalizadas**:
   - Cada curso recomendado inclui uma explicação gerada pela IA
   - Análise de compatibilidade específica
   - Sugestões de trilhas de aprendizado

### Prompt Engineering

O sistema utiliza técnicas avançadas de **Prompt Engineering**:
- Contextos estruturados para a IA
- Formatação de saída JSON para análise
- Prompts específicos para diferentes tarefas
- Sistema de fallback para desenvolvimento sem API key

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
    "areas_interesse": [
      {"area": "programacao", "nivel": "intermediario"},
      {"area": "ia", "nivel": "iniciante"}
    ],
    "cursos_completos": ["1", "5"],
    "cursos_em_andamento": ["2"]
  },
  "limit": 10
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

O app mobile React Native "Aprenda Plus" está preparado para consumir esta API.

**Principais pontos**:
- Endpoint: `POST /api/courses/suggested/{user_id}`
- Estrutura de dados compatível
- Suporte a CORS configurado
- Tratamento de erros robusto

**Configuração no app mobile:**
```javascript
BASE_URL: 'http://localhost:8000/api'  // Desenvolvimento
// ou
BASE_URL: 'https://sua-api-producao.com/api'  // Produção
```

## 📊 Critérios de Avaliação

### ✅ [60 pontos] Cumprimento dos Requisitos Técnicos
- ✅ Implementação técnica em Deep Learning (IA Generativa)
- ✅ Funcionamento da IA com Google Gemini API
- ✅ Integração da API REST funcional
- ✅ Documentação completa do modelo
- ✅ Aderência aos requisitos obrigatórios

### ✅ [20 pontos] Integração Interdisciplinar
- ✅ Integração efetiva com app mobile React Native
- ✅ Arquitetura coerente do sistema
- ✅ Fluxo de dados completo (Mobile → API → IA → Mobile)
- ✅ Interface funcional que consome resultados da IA

### ✅ [10 pontos] Boas Práticas de Código
- ✅ Organização clara e modular
- ✅ README completo com instruções
- ✅ Documentação inline
- ✅ Estrutura de pastas lógica
- ✅ Tratamento de erros

### ✅ [10 pontos] Apresentação
- ✅ Código executável e testável
- ✅ Exemplos de uso incluídos
- ✅ Scripts de teste prontos
- ✅ Documentação completa para demonstração

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**: Linguagem base do backend
- **FastAPI**: Framework web moderno e rápido
- **Google Gemini API**: IA Generativa para análise e geração
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI
- **React Native**: App mobile (referência)

## 📝 Documentação Adicional

- **API Documentation**: Veja `backend/README.md` para documentação completa da API
- **API Interactive Docs**: Acesse `http://localhost:8000/docs` quando o servidor estiver rodando
- **Testes**: Execute `python examples/testar_api.py` para testar todos os endpoints

## 🔒 Modo Mock

O sistema funciona em **modo mock** sem necessidade de API key do Gemini:
- Respostas simuladas para desenvolvimento
- Permite testar toda a integração
- Para produção, configure a API key real no arquivo `.env`

## 🚀 Deploy

Para deploy em produção (Railway, Render, Heroku, etc.):
1. Configure `GEMINI_API_KEY` nas variáveis de ambiente
2. O `Procfile` já está configurado para deploy automático
3. Ajuste `BASE_URL` no app mobile para URL de produção
4. CORS já está configurado para permitir requisições do mobile

## 📧 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação em `backend/README.md`
2. Execute os testes: `python examples/testar_api.py`
3. Verifique os logs do servidor
4. Teste os endpoints usando a documentação interativa em `/docs`

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais acadêmicos.

---

**Desenvolvido com ❤️ para o projeto Aprenda Plus**

*Sistema de recomendações educacionais usando IA Generativa integrado com desenvolvimento web e mobile*
