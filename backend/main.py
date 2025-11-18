"""
Aprenda Plus - AI Course Recommendation API
Backend FastAPI com integração de IA Generativa para recomendações personalizadas de cursos
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import logging
import unicodedata
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

from services.servico_ia import AIService
from services.servico_recomendacoes import ServicoRecomendacoes
from services.analisador_perfil import AnalisadorPerfil
from models.perfil_usuario import PerfilUsuario, AreaInteresse
from models.curso import Curso
from data.banco_cursos import BancoCursos

# Manter aliases para compatibilidade
UserProfile = PerfilUsuario
AreaInterest = AreaInteresse
Course = Curso
RecommendationService = ServicoRecomendacoes
ProfileAnalyzer = AnalisadorPerfil

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="Aprenda Plus - AI Course Recommendation API",
    description="API de recomendações personalizadas de cursos usando IA Generativa",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requisições do app mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar serviços
ai_service = AIService()
banco_cursos = BancoCursos()
recommendation_service = ServicoRecomendacoes(ai_service)
profile_analyzer = AnalisadorPerfil(ai_service)


# ==================== FUNÇÕES AUXILIARES ====================

def normalize_area_name(area: str) -> str:
    """
    Normaliza o nome da área removendo acentos e convertendo para minúsculas.
    Também mapeia nomes amigáveis para IDs de áreas.
    """
    # Mapeamento de nomes amigáveis para IDs
    area_mapping = {
        # IA
        "ia": "ia",
        "inteligencia artificial": "ia",
        "inteligência artificial": "ia",
        "ai": "ia",
        
        # Ciência de Dados
        "ciencia de dados": "ciencia_dados",
        "ciência de dados": "ciencia_dados",
        "ciencia_dados": "ciencia_dados",
        "data science": "ciencia_dados",
        "cienciadados": "ciencia_dados",
        
        # Sustentabilidade
        "sustentabilidade": "sustentabilidade",
        "sustentavel": "sustentabilidade",
        "sustentável": "sustentabilidade",
        "meio ambiente": "sustentabilidade",
        "ambiental": "sustentabilidade",
        
        # Programação
        "programacao": "programacao",
        "programação": "programacao",
        "desenvolvimento": "programacao",
        "software": "programacao",
        "dev": "programacao",
        
        # Design
        "design": "design",
        "design grafico": "design",
        "design gráfico": "design",
        "ui/ux": "design",
        "ui": "design",
        "ux": "design",
        
        # Marketing Digital
        "marketing digital": "marketing_digital",
        "marketing_digital": "marketing_digital",
        "marketing": "marketing_digital",
        "digital marketing": "marketing_digital",
        "marketingdigital": "marketing_digital",
        
        # Gestão
        "gestao": "gestao",
        "gestão": "gestao",
        "administracao": "gestao",
        "administração": "gestao",
        "management": "gestao",
        "gerenciamento": "gestao",
        
        # Vendas
        "vendas": "vendas",
        "vendas consultivas": "vendas",
        "vendasconsultivas": "vendas",
        "sales": "vendas",
        "negociacao": "vendas",
        "negociação": "vendas",
        
        # RH
        "rh": "rh",
        "recursos humanos": "rh",
        "recursoshumanos": "rh",
        "gestao de pessoas": "rh",
        "gestão de pessoas": "rh",
        "hr": "rh",
        "human resources": "rh",
        
        # Finanças
        "financas": "financas",
        "finanças": "financas",
        "financeiro": "financas",
        "contabilidade": "financas",
        "finance": "financas",
        
        # Saúde
        "saude": "saude",
        "saúde": "saude",
        "saude e bem estar": "saude",
        "saúde e bem estar": "saude",
        "health": "saude",
        "saudebemestar": "saude",
        
        # Educação
        "educacao": "educacao",
        "educação": "educacao",
        "pedagogia": "educacao",
        "ensino": "educacao",
        "education": "educacao",
        "ead": "educacao",
    }
    
    # Normalizar: remover acentos e converter para minúsculas
    area_normalized = unicodedata.normalize('NFD', area.lower().strip())
    area_normalized = ''.join(char for char in area_normalized if unicodedata.category(char) != 'Mn')
    
    # Remover espaços extras e caracteres especiais
    area_normalized = area_normalized.replace(' ', '_').replace('/', '').replace('-', '')
    
    # Verificar no mapeamento
    if area_normalized in area_mapping:
        return area_mapping[area_normalized]
    
    # Verificar também com espaços
    area_with_spaces = area.lower().strip()
    if area_with_spaces in area_mapping:
        return area_mapping[area_with_spaces]
    
    # Se não está no mapeamento, retornar normalizado
    return area_normalized


def get_available_areas() -> List[str]:
    """Retorna lista de IDs de áreas disponíveis no banco"""
    todos_cursos = banco_cursos.get_all_courses()
    return sorted(set(curso.area for curso in todos_cursos))


# ==================== MODELOS DE DADOS ====================

class AreaInterest(BaseModel):
    """Modelo para área de interesse do usuário"""
    area: str = Field(
        ..., 
        description="ID da área de interesse (programacao, ia, iot, seguranca)",
        examples=["programacao"]
    )
    nivel: str = Field(
        ..., 
        description="Nível de conhecimento (iniciante, intermediario, avancado)",
        examples=["intermediario"]
    )


class UserProfile(BaseModel):
    """Modelo para perfil do usuário"""
    user_id: str = Field(
        ..., 
        description="ID único do usuário (DEVE ser igual ao user_id da URL)",
        examples=["121344"]
    )
    name: Optional[str] = Field(None, description="Nome do usuário", examples=["João Silva"])
    email: Optional[str] = Field(None, description="Email do usuário", examples=["joao@example.com"])
    areas_interesse: List[AreaInterest] = Field(
        ..., 
        description="Lista de áreas de interesse com níveis (mínimo 1 área)",
        examples=[[{"area": "programacao", "nivel": "intermediario"}]]
    )
    cursos_completos: Optional[List[str]] = Field(default=[], description="IDs de cursos completados", examples=[["1", "5"]])
    cursos_em_andamento: Optional[List[str]] = Field(default=[], description="IDs de cursos em andamento", examples=[["2"]])
    progresso_cursos: Optional[Dict[str, int]] = Field(default={}, description="Progresso por curso (curso_id: porcentagem)", examples=[{"2": 45}])


class Course(BaseModel):
    """Modelo para curso"""
    id: str
    titulo: str
    descricao: str
    area: str
    nivel: str
    duracao: str
    icone: Optional[str] = None


class RecommendationRequest(BaseModel):
    """Modelo para requisição de recomendações"""
    user_profile: UserProfile
    limit: Optional[int] = Field(default=10, ge=1, le=20, description="Número máximo de recomendações")


class RecommendedCourse(BaseModel):
    """Modelo para curso recomendado pela IA"""
    course: Course
    score: float = Field(..., description="Score de relevância (0-1)")
    reason: str = Field(..., description="Explicação gerada pela IA sobre por que o curso foi recomendado")
    compatibility: str = Field(..., description="Análise de compatibilidade com o perfil")
    suggested_learning_path: Optional[str] = Field(None, description="Sugestão de trilha de aprendizado")


class RecommendationResponse(BaseModel):
    """Modelo para resposta de recomendações"""
    user_id: str
    recommendations: List[RecommendedCourse]
    profile_analysis: Dict[str, Any] = Field(..., description="Análise do perfil pelo modelo de IA")
    generated_at: str
    model_used: str = Field(..., description="Modelo de IA utilizado (ex: gemini-pro)")


class HealthCheck(BaseModel):
    """Modelo para health check"""
    status: str
    service: str
    timestamp: str
    ai_service_status: Optional[str] = None


class ExplanationRequest(BaseModel):
    """Modelo para requisição de explicação de curso"""
    course: Course = Field(..., description="Curso para explicar")
    user_profile: UserProfile = Field(..., description="Perfil do usuário")


# ==================== ENDPOINTS ====================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "Aprenda Plus - AI Course Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check da API e serviços de IA"""
    try:
        ai_status = await ai_service.check_health()
        return HealthCheck(
            status="healthy" if ai_status else "degraded",
            service="course-recommendation-api",
            timestamp=datetime.now().isoformat(),
            ai_service_status="connected" if ai_status else "disconnected"
        )
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return HealthCheck(
            status="unhealthy",
            service="course-recommendation-api",
            timestamp=datetime.now().isoformat(),
            ai_service_status="error"
        )


@app.post("/api/courses/suggested/{user_id}", response_model=RecommendationResponse)
async def get_suggested_courses(
    user_id: str,
    request: RecommendationRequest,
    limit: Optional[int] = None
):
    """
    Endpoint principal para obter recomendações personalizadas de cursos
    
    Este endpoint utiliza IA Generativa para:
    - Analisar o perfil completo do usuário
    - Gerar recomendações personalizadas baseadas em interesses, níveis e histórico
    - Criar explicações contextuais para cada recomendação
    - Analisar compatibilidade e pré-requisitos
    """
    try:
        # Normalizar user_id removendo aspas extras (problema do Swagger UI)
        normalized_path_user_id = user_id.strip('"').strip("'")
        normalized_body_user_id = str(request.user_profile.user_id).strip('"').strip("'")
        
        logger.info(f"Processing recommendation request for user: {normalized_path_user_id}, limit={limit}")
        logger.info(f"Path user_id (normalized): {normalized_path_user_id}")
        logger.info(f"Body user_id (normalized): {normalized_body_user_id}")
        logger.info(f"Request body areas_interesse: {len(request.user_profile.areas_interesse or [])} areas")
        
        # Validar que user_id corresponde ao perfil (comparação normalizada)
        if normalized_body_user_id != normalized_path_user_id:
            logger.warning(f"User ID mismatch: path={normalized_path_user_id}, body={normalized_body_user_id}")
            raise HTTPException(
                status_code=400,
                detail=f"User ID no caminho da URL ({normalized_path_user_id}) deve ser igual ao user_id no JSON do body ({normalized_body_user_id}). "
                       f"Altere o 'user_id' no JSON para '{normalized_path_user_id}' ou use a URL: /api/courses/suggested/{normalized_body_user_id}"
            )
        
        # Usar user_id normalizado para o resto do código
        user_id = normalized_path_user_id
        
        # Validar que há pelo menos uma área de interesse
        if not request.user_profile.areas_interesse or len(request.user_profile.areas_interesse) == 0:
            logger.warning(f"No areas of interest provided for user: {user_id}")
            raise HTTPException(
                status_code=400,
                detail="É necessário fornecer pelo menos uma área de interesse (areas_interesse)"
            )
        
        # Determinar o limite (prioridade: query param > body > default)
        final_limit = limit if limit is not None else (request.limit if request.limit else 10)
        final_limit = max(1, min(20, final_limit))  # Garantir entre 1 e 20
        
        logger.info(f"Using limit: {final_limit} for user: {user_id}")
        
        # Analisar perfil do usuário com IA
        logger.info(f"Starting profile analysis for user: {user_id}")
        profile_analysis = await profile_analyzer.analisar_perfil(request.user_profile)
        logger.info(f"Profile analysis completed for user: {user_id}")
        
        # Gerar recomendações usando IA Generativa
        logger.info(f"Starting recommendations generation for user: {user_id}")
        recommendations = await recommendation_service.gerar_recomendacoes(
            perfil_usuario=request.user_profile,
            analise_perfil=profile_analysis,
            limit=final_limit
        )
        
        logger.info(f"Generated {len(recommendations)} recommendations for user: {user_id}")
        
        return RecommendationResponse(
            user_id=user_id,
            recommendations=recommendations,
            profile_analysis=profile_analysis,
            generated_at=datetime.now().isoformat(),
            model_used=ai_service.get_model_name()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (como 400)
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations for user {user_id}: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


@app.post("/api/ai/analyze-profile", response_model=Dict[str, Any])
async def analyze_profile(profile: UserProfile):
    """
    Endpoint para análise detalhada do perfil usando IA Generativa
    
    Retorna uma análise estruturada do perfil do usuário incluindo:
    - Pontos fortes identificados
    - Áreas de crescimento sugeridas
    - Compatibilidade com diferentes áreas
    - Sugestões de desenvolvimento profissional
    """
    try:
        logger.info(f"Analyzing profile for user: {profile.user_id}")
        analysis = await profile_analyzer.analisar_perfil(profile)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing profile: {str(e)}"
        )


@app.post("/api/ai/generate-explaination")
async def generate_explanation(request: ExplanationRequest):
    """
    Endpoint para gerar explicação personalizada de por que um curso foi recomendado
    
    Usa IA Generativa para criar uma explicação contextual baseada no perfil do usuário
    
    **Body (JSON):**
    ```json
    {
      "course": {
        "id": "1",
        "titulo": "Python Básico",
        "descricao": "Curso introdutório de Python",
        "area": "programacao",
        "nivel": "iniciante",
        "duracao": "40 horas"
      },
      "user_profile": {
        "user_id": "123",
        "areas_interesse": [
          {"area": "programacao", "nivel": "iniciante"}
        ]
      }
    }
    ```
    """
    try:
        logger.info(f"Generating explanation for course {request.course.id} and user {request.user_profile.user_id}")
        
        explanation = await recommendation_service.gerar_explicacao_curso(
            curso=request.course,
            perfil_usuario=request.user_profile
        )
        
        logger.info(f"Explanation generated successfully for course {request.course.id}")
        
        return {
            "course_id": request.course.id,
            "explanation": explanation,
            "generated_at": datetime.now().isoformat(),
            "model_used": ai_service.get_model_name()
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating explanation: {str(e)}"
        )


@app.get("/api/areas", response_model=List[Dict[str, Any]])
async def get_areas():
    """
    Retorna todas as áreas de cursos disponíveis no sistema.
    Útil para o app mobile mostrar as categorias disponíveis.
    """
    try:
        todos_cursos = banco_cursos.get_all_courses()
        areas = {}
        
        # Áreas com nomes amigáveis e ícones
        areas_info = {
            "ia": {"nome": "Inteligência Artificial", "icone": "🤖", "descricao": "IA, Machine Learning e Deep Learning"},
            "ciencia_dados": {"nome": "Ciência de Dados", "icone": "📊", "descricao": "Análise de dados, Big Data e Data Science"},
            "sustentabilidade": {"nome": "Sustentabilidade", "icone": "🌱", "descricao": "Meio ambiente, energia limpa e práticas sustentáveis"},
            "programacao": {"nome": "Programação", "icone": "💻", "descricao": "Cursos de desenvolvimento de software"},
            "design": {"nome": "Design", "icone": "🎨", "descricao": "Design gráfico, UI/UX e design thinking"},
            "marketing_digital": {"nome": "Marketing Digital", "icone": "📱", "descricao": "Marketing digital, redes sociais e SEO"},
            "gestao": {"nome": "Gestão", "icone": "📋", "descricao": "Administração, liderança e gestão de projetos"},
            "vendas": {"nome": "Vendas", "icone": "💼", "descricao": "Técnicas de vendas, negociação e CRM"},
            "rh": {"nome": "Recursos Humanos", "icone": "👤", "descricao": "Gestão de pessoas, recrutamento e desenvolvimento"},
            "financas": {"nome": "Finanças", "icone": "💰", "descricao": "Finanças pessoais, empresariais e investimentos"},
            "saude": {"nome": "Saúde", "icone": "💚", "descricao": "Saúde, bem-estar e nutrição"},
            "educacao": {"nome": "Educação", "icone": "📖", "descricao": "Pedagogia, metodologias de ensino e EAD"}
        }
        
        # Contar cursos por área
        for curso in todos_cursos:
            if curso.area not in areas:
                area_info = areas_info.get(curso.area, {
                    "nome": curso.area.title(),
                    "icone": "📚",
                    "descricao": f"Cursos de {curso.area}"
                })
                areas[curso.area] = {
                    "id": curso.area,
                    "nome": area_info["nome"],
                    "icone": area_info["icone"],
                    "descricao": area_info["descricao"],
                    "total_cursos": 0
                }
            areas[curso.area]["total_cursos"] += 1
        
        return list(areas.values())
    except Exception as e:
        logger.error(f"Error getting areas: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error getting areas: {str(e)}"
        )


@app.get("/api/courses", response_model=List[Course])
async def get_all_courses(area: Optional[str] = None, nivel: Optional[str] = None):
    """
    Retorna todos os cursos disponíveis.
    Pode filtrar por área ou nível.
    
    Query parameters:
    - area: Filtrar por área (ia, ciencia_dados, sustentabilidade, programacao, design, 
      marketing_digital, gestao, vendas, rh, financas, saude, educacao)
    - nivel: Filtrar por nível (iniciante, intermediario, avancado)
    """
    try:
        if area:
            cursos = banco_cursos.get_courses_by_area(area)
        elif nivel:
            cursos = banco_cursos.get_courses_by_level(nivel)
        else:
            cursos = banco_cursos.get_all_courses()
        
        # Filtrar por nível se especificado e não foi o filtro principal
        if nivel and area:
            cursos = [c for c in cursos if c.nivel == nivel]
        
        return [Course(
            id=curso.id,
            titulo=curso.titulo,
            descricao=curso.descricao,
            area=curso.area,
            nivel=curso.nivel,
            duracao=curso.duracao,
            icone=curso.icone
        ) for curso in cursos]
    except Exception as e:
        logger.error(f"Error getting courses: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error getting courses: {str(e)}"
        )


@app.get("/api/courses/{course_id}", response_model=Course)
async def get_course_by_id(course_id: str):
    """
    Busca um curso específico por ID.
    """
    try:
        curso = banco_cursos.get_course_by_id(course_id)
        if not curso:
            raise HTTPException(
                status_code=404,
                detail=f"Course with ID {course_id} not found"
            )
        
        return Course(
            id=curso.id,
            titulo=curso.titulo,
            descricao=curso.descricao,
            area=curso.area,
            nivel=curso.nivel,
            duracao=curso.duracao,
            icone=curso.icone
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting course: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error getting course: {str(e)}"
        )


@app.get("/api/courses/area/{area}", response_model=List[Course])
async def get_courses_by_area(area: str):
    """
    Retorna todos os cursos de uma área específica.
    
    A área pode ser informada com ou sem acentos, em maiúsculas ou minúsculas.
    Exemplos válidos:
    - ia, IA, Inteligência Artificial
    - ciencia_dados, ciência de dados, Ciência de Dados
    - sustentabilidade, Sustentabilidade
    - programacao, programação, Programação
    - design, Design
    - marketing_digital, Marketing Digital, marketing digital
    - gestao, gestão, Gestão
    - vendas, Vendas
    - rh, RH, Recursos Humanos
    - financas, finanças, Finanças
    - saude, saúde, Saúde
    - educacao, educação, Educação
    
    Áreas disponíveis: ia, ciencia_dados, sustentabilidade, programacao, design, 
    marketing_digital, gestao, vendas, rh, financas, saude, educacao
    """
    try:
        # Normalizar área (remover acentos, converter para minúsculas, mapear nomes)
        area_normalized = normalize_area_name(area)
        logger.info(f"Requested area: '{area}' -> normalized: '{area_normalized}'")
        
        # Verificar se a área existe
        available_areas = get_available_areas()
        
        # Buscar cursos
        cursos = banco_cursos.get_courses_by_area(area_normalized)
        
        # Se não encontrou cursos e a área normalizada não está na lista de áreas disponíveis
        if not cursos and area_normalized not in available_areas:
            # Mapear IDs para nomes amigáveis para a mensagem de erro
            area_names = {
                "ia": "Inteligência Artificial",
                "ciencia_dados": "Ciência de Dados",
                "sustentabilidade": "Sustentabilidade",
                "programacao": "Programação",
                "design": "Design",
                "marketing_digital": "Marketing Digital",
                "gestao": "Gestão",
                "vendas": "Vendas",
                "rh": "Recursos Humanos",
                "financas": "Finanças",
                "saude": "Saúde",
                "educacao": "Educação"
            }
            available_names = [area_names.get(a, a) for a in available_areas]
            
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Area not found",
                    "message": f"Área '{area}' não encontrada.",
                    "requested_area": area,
                    "normalized_area": area_normalized,
                    "available_areas": available_areas,
                    "available_areas_names": available_names,
                    "hint": f"Use uma das áreas disponíveis: {', '.join(available_areas)}. "
                           f"Você pode usar nomes amigáveis como 'Programação', 'IA', etc."
                }
            )
        
        # Se a área existe mas não tem cursos (caso raro)
        if not cursos:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "No courses found",
                    "message": f"Nenhum curso encontrado para a área '{area_normalized}'.",
                    "area": area_normalized
                }
            )
        
        logger.info(f"Found {len(cursos)} courses for area '{area_normalized}'")
        
        return [Course(
            id=curso.id,
            titulo=curso.titulo,
            descricao=curso.descricao,
            area=curso.area,
            nivel=curso.nivel,
            duracao=curso.duracao,
            icone=curso.icone
        ) for curso in cursos]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting courses by area: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting courses by area: {str(e)}"
        )


# Handler para erros de validação do Pydantic
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "message": "Os dados enviados são inválidos. Verifique o formato da requisição.",
            "details": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )


# Handler para métodos HTTP não permitidos (405)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handler para erros HTTP incluindo 405 Method Not Allowed"""
    if exc.status_code == 405:
        # Ordenar por especificidade (mais específicos primeiro)
        allowed_methods = [
            ("/api/courses/suggested/", ["POST"]),
            ("/api/courses/area/", ["GET"]),
            ("/api/courses/", ["GET"]),  # Para /api/courses/{course_id}
            ("/api/courses", ["GET"]),
            ("/api/ai/analyze-profile", ["POST"]),
            ("/api/ai/generate-explaination", ["POST"]),
            ("/api/areas", ["GET"]),
            ("/health", ["GET"]),
            ("/", ["GET"])
        ]
        
        path = request.url.path
        method = request.method
        
        # Encontrar endpoint similar (verificando do mais específico para o menos específico)
        suggested_method = None
        for endpoint_pattern, methods in allowed_methods:
            # Verificar se o path começa com o padrão
            if path.startswith(endpoint_pattern) or endpoint_pattern.startswith(path):
                suggested_method = methods[0]
                break
            # Verificar padrões com parâmetros
            if "{user_id}" in endpoint_pattern or "{course_id}" in endpoint_pattern or "{area}" in endpoint_pattern:
                pattern_base = endpoint_pattern.replace("{user_id}", "").replace("{course_id}", "").replace("{area}", "").replace("//", "/")
                if path.startswith(pattern_base) and path != pattern_base:
                    suggested_method = methods[0]
                    break
        
        error_msg = {
            "error": "Method Not Allowed",
            "message": f"O método {method} não é permitido para o endpoint {path}",
            "requested_method": method,
            "requested_path": path,
            "timestamp": datetime.now().isoformat()
        }
        
        if suggested_method:
            error_msg["suggestion"] = {
                "correct_method": suggested_method,
                "hint": f"Use {suggested_method} para este endpoint. "
                       f"Exemplo: {suggested_method} {path}"
            }
        
        logger.warning(f"Method not allowed: {method} {path}")
        return JSONResponse(status_code=405, content=error_msg)
    
    # Para outros erros HTTP, retornar padrão
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.now().isoformat()}
    )


# Handler para erros globais
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    import sys
    import os
    
    # Adicionar o diretório backend ao path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    )

