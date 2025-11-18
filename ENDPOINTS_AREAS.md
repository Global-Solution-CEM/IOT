# 📡 Endpoints de Áreas e Cursos - Para o App Mobile

## 🎯 Endpoints Criados

### 1. **Listar Todas as Áreas Disponíveis**
```
GET /api/areas
```

**Resposta:**
```json
[
  {
    "id": "programacao",
    "nome": "Programação",
    "icone": "💻",
    "descricao": "Cursos de desenvolvimento de software",
    "total_cursos": 7
  },
  {
    "id": "ia",
    "nome": "Inteligência Artificial",
    "icone": "🤖",
    "descricao": "IA, Machine Learning e Deep Learning",
    "total_cursos": 5
  },
  {
    "id": "iot",
    "nome": "Internet das Coisas",
    "icone": "🌐",
    "descricao": "IoT, robótica e sistemas embarcados",
    "total_cursos": 3
  },
  {
    "id": "seguranca",
    "nome": "Segurança",
    "icone": "🔒",
    "descricao": "Cibersegurança e segurança da informação",
    "total_cursos": 1
  }
]
```

**Uso no app:** Mostrar as categorias/áreas disponíveis para o usuário escolher.

---

### 2. **Listar Todos os Cursos (com filtros opcionais)**
```
GET /api/courses?area=programacao&nivel=intermediario
```

**Parâmetros opcionais:**
- `area`: Filtrar por área (programacao, ia, iot, seguranca)
- `nivel`: Filtrar por nível (iniciante, intermediario, avancado)

**Exemplos:**
- `GET /api/courses` - Todos os cursos
- `GET /api/courses?area=programacao` - Apenas cursos de programação
- `GET /api/courses?nivel=iniciante` - Apenas cursos iniciantes
- `GET /api/courses?area=ia&nivel=intermediario` - IA intermediária

**Resposta:**
```json
[
  {
    "id": "1",
    "titulo": "Introdução à Inteligência Artificial",
    "descricao": "Aprenda os fundamentos da IA...",
    "area": "ia",
    "nivel": "iniciante",
    "duracao": "40 horas",
    "icone": "🤖"
  },
  ...
]
```

**Uso no app:** Listar cursos, com opção de filtrar por área ou nível.

---

### 3. **Buscar Curso por ID**
```
GET /api/courses/{course_id}
```

**Exemplo:**
```
GET /api/courses/1
```

**Resposta:**
```json
{
  "id": "1",
  "titulo": "Introdução à Inteligência Artificial",
  "descricao": "Aprenda os fundamentos da IA...",
  "area": "ia",
  "nivel": "iniciante",
  "duracao": "40 horas",
  "icone": "🤖"
}
```

**Uso no app:** Mostrar detalhes de um curso específico.

---

### 4. **Listar Cursos por Área**
```
GET /api/courses/area/{area}
```

**Exemplos:**
- `GET /api/courses/area/programacao`
- `GET /api/courses/area/ia`
- `GET /api/courses/area/iot`
- `GET /api/courses/area/seguranca`

**Resposta:**
```json
[
  {
    "id": "2",
    "titulo": "Análise de Dados com Python",
    "descricao": "Domine Python para análise de dados...",
    "area": "programacao",
    "nivel": "intermediario",
    "duracao": "50 horas",
    "icone": "📊"
  },
  ...
]
```

**Uso no app:** Quando o usuário clica em uma área, mostrar todos os cursos dessa área.

---

## 📋 Áreas Disponíveis

1. **programacao** 💻 - Programação
   - Fundamentos, Web, Mobile, Arquitetura

2. **ia** 🤖 - Inteligência Artificial
   - IA Básica, Machine Learning, Deep Learning, NLP, Visão Computacional

3. **iot** 🌐 - Internet das Coisas
   - Fundamentos de IoT, Robótica, Sistemas Embarcados

4. **seguranca** 🔒 - Segurança
   - Cibersegurança e Segurança da Informação

---

## 🎯 Como Usar no App Mobile

### Exemplo 1: Listar Áreas na Tela Inicial
```javascript
// Buscar áreas disponíveis
const areas = await fetch('http://localhost:8000/api/areas')
  .then(res => res.json());

// Mostrar cards com as áreas
areas.forEach(area => {
  // Renderizar card com area.nome, area.icone, area.total_cursos
});
```

### Exemplo 2: Ao Clicar em uma Área
```javascript
// Buscar cursos da área selecionada
const cursos = await fetch(`http://localhost:8000/api/courses/area/${areaId}`)
  .then(res => res.json());

// Mostrar lista de cursos
```

### Exemplo 3: Filtrar Cursos
```javascript
// Cursos de programação nível intermediário
const cursos = await fetch('http://localhost:8000/api/courses?area=programacao&nivel=intermediario')
  .then(res => res.json());
```

---

## ✅ Todos os Endpoints da API

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/health` | GET | Health check |
| `/api/areas` | GET | Lista todas as áreas |
| `/api/courses` | GET | Lista cursos (com filtros) |
| `/api/courses/{id}` | GET | Busca curso por ID |
| `/api/courses/area/{area}` | GET | Cursos por área |
| `/api/courses/suggested/{user_id}` | POST | **Recomendações com IA** |
| `/api/ai/analyze-profile` | POST | Análise de perfil com IA |
| `/api/ai/generate-explaination` | POST | Explicação de recomendação |

---

**Todos os endpoints estão prontos e funcionando!** 🚀

