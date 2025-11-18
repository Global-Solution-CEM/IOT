"""
Aprenda Plus - AI Course Recommendation API
Backend FastAPI com integração de IA Generativa para recomendações personalizadas de cursos
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import logging

from services.servico_ia import AIService
from services.servico_recomendacoes import ServicoRecomendacoes
from services.analisador_perfil import AnalisadorPerfil
from models.perfil_usuario import PerfilUsuario, AreaInteresse
from models.curso import Curso

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
recommendation_service = ServicoRecomendacoes(ai_service)
profile_analyzer = AnalisadorPerfil(ai_service)


# ==================== MODELOS DE DADOS ====================

class AreaInterest(BaseModel):
    """Modelo para área de interesse do usuário"""
    area: str = Field(..., description="ID da área de interesse")
    nivel: str = Field(..., description="Nível de conhecimento (iniciante, intermediario, avancado)")


class UserProfile(BaseModel):
    """Modelo para perfil do usuário"""
    user_id: str = Field(..., description="ID único do usuário")
    name: Optional[str] = Field(None, description="Nome do usuário")
    email: Optional[str] = Field(None, description="Email do usuário")
    areas_interesse: List[AreaInterest] = Field(..., description="Lista de áreas de interesse com níveis")
    cursos_completos: Optional[List[str]] = Field(default=[], description="IDs de cursos completados")
    cursos_em_andamento: Optional[List[str]] = Field(default=[], description="IDs de cursos em andamento")
    progresso_cursos: Optional[Dict[str, int]] = Field(default={}, description="Progresso por curso (curso_id: porcentagem)")


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
    limit: Optional[int] = 10
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
        logger.info(f"Processing recommendation request for user: {user_id}")
        
        # Validar que user_id corresponde ao perfil
        if request.user_profile.user_id != user_id:
            raise HTTPException(
                status_code=400,
                detail="User ID in path does not match user_id in profile"
            )
        
        # Analisar perfil do usuário com IA
        profile_analysis = await profile_analyzer.analisar_perfil(request.user_profile)
        logger.info(f"Profile analysis completed for user: {user_id}")
        
        # Gerar recomendações usando IA Generativa
        recommendations = await recommendation_service.gerar_recomendacoes(
            perfil_usuario=request.user_profile,
            analise_perfil=profile_analysis,
            limit=limit or request.limit
        )
        
        logger.info(f"Generated {len(recommendations)} recommendations for user: {user_id}")
        
        return RecommendationResponse(
            user_id=user_id,
            recommendations=recommendations,
            profile_analysis=profile_analysis,
            generated_at=datetime.now().isoformat(),
            model_used=ai_service.get_model_name()
        )
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}", exc_info=True)
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
async def generate_explanation(
    course: Course,
    user_profile: UserProfile
):
    """
    Endpoint para gerar explicação personalizada de por que um curso foi recomendado
    
    Usa IA Generativa para criar uma explicação contextual baseada no perfil do usuário
    """
    try:
        explanation = await recommendation_service.gerar_explicacao_curso(
            course=course,
            user_profile=user_profile
        )
        return {
            "course_id": course.id,
            "explanation": explanation,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error generating explanation: {str(e)}"
        )


# Handler para erros globais
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
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

