"""
Analisador de Perfil usando IA Generativa
Analisa o perfil do usuário para extrair insights e características de aprendizado
"""

import logging
from typing import Dict, Any
from models.perfil_usuario import PerfilUsuario
from services.servico_ia import AIService

logger = logging.getLogger(__name__)


class AnalisadorPerfil:
    """Analisador de perfil do usuário usando IA Generativa"""
    
    SYSTEM_CONTEXT = """Você é um especialista em educação e análise de perfis de aprendizado. 
Sua função é analisar perfis de usuários em plataformas educacionais e identificar:
- Pontos fortes e áreas de interesse
- Nível de conhecimento atual em cada área
- Padrões de aprendizado e preferências
- Compatibilidade com diferentes áreas de conhecimento
- Sugestões de desenvolvimento profissional

Seja específico, construtivo e focado em ajudar o usuário a alcançar seus objetivos educacionais."""

    def __init__(self, ai_service: AIService):
        """Inicializa o analisador com serviço de IA"""
        self.ai_service = ai_service
    
    async def analisar_perfil(self, perfil: PerfilUsuario) -> Dict[str, Any]:
        """
        Analisa o perfil completo do usuário usando IA Generativa
        
        Args:
            perfil: Perfil do usuário para análise
            
        Returns:
            Dicionário com análise estruturada do perfil
        """
        logger.info(f"Analyzing profile for user: {perfil.user_id}")
        
        # Construir prompt de análise
        analysis_prompt = self._build_analysis_prompt(perfil)
        
        # Formato esperado da resposta
        output_format = {
            "pontos_fortes": ["string"],
            "areas_crescimento": ["string"],
            "perfil_aprendizado": "string",
            "compatibilidade_areas": {
                "area_id": "float (0-1)"
            },
            "sugestoes_desenvolvimento": ["string"],
            "nivel_geral": "string (iniciante/intermediario/avancado)",
            "areas_destaque": ["string"],
            "insights_personalizados": "string"
        }
        
        # Gerar análise usando IA
        try:
            analysis = await self.ai_service.analyze_with_structured_output(
                prompt=analysis_prompt,
                output_format=output_format,
                system_context=self.SYSTEM_CONTEXT
            )
            
            # Adicionar metadados
            analysis["user_id"] = perfil.user_id
            analysis["analyzed_at"] = "now"  # Será formatado no endpoint
            analysis["total_areas"] = len(perfil.areas_interesse)
            analysis["cursos_completos_count"] = len(perfil.cursos_completos or [])
            analysis["cursos_em_andamento_count"] = len(perfil.cursos_em_andamento or [])
            
            logger.info(f"Profile analysis completed for user: {perfil.user_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing profile: {str(e)}", exc_info=True)
            # Retornar análise básica em caso de erro
            return self._fallback_analysis(perfil)
    
    def _build_analysis_prompt(self, perfil: PerfilUsuario) -> str:
        """Constrói prompt de análise do perfil"""
        
        # Informações das áreas de interesse
        areas_info = "\n".join([
            f"- {area.area} (nível: {area.nivel})"
            for area in perfil.areas_interesse
        ])
        
        # Histórico de cursos
        cursos_info = ""
        if perfil.cursos_completos:
            cursos_info += f"\nCursos completos ({len(perfil.cursos_completos)}): {', '.join(perfil.cursos_completos)}"
        if perfil.cursos_em_andamento:
            cursos_info += f"\nCursos em andamento ({len(perfil.cursos_em_andamento)}): {', '.join(perfil.cursos_em_andamento)}"
        
        # Progresso dos cursos
        progresso_info = ""
        if perfil.progresso_cursos:
            progresso_info = "\nProgresso em cursos:\n"
            for curso_id, progresso in perfil.progresso_cursos.items():
                progresso_info += f"- {curso_id}: {progresso}%\n"
        
        prompt = f"""
Analise o seguinte perfil de usuário em uma plataforma educacional:

INFORMAÇÕES DO USUÁRIO:
- Nome: {perfil.name or 'Não informado'}
- Email: {perfil.email or 'Não informado'}
- ID: {perfil.user_id}

ÁREAS DE INTERESSE E NÍVEIS:
{areas_info}
{cursos_info}
{progresso_info}

Com base nessas informações, forneça uma análise estruturada do perfil incluindo:
1. Pontos fortes identificados (baseado nas áreas escolhidas e níveis)
2. Áreas de crescimento (oportunidades de desenvolvimento)
3. Perfil de aprendizado (tipo de aprendiz, preferências identificadas)
4. Compatibilidade com diferentes áreas (scores de 0 a 1 para cada área mencionada)
5. Sugestões de desenvolvimento profissional
6. Nível geral de conhecimento estimado
7. Áreas de destaque (quais áreas o usuário tem maior afinidade)
8. Insights personalizados (análise única e específica deste perfil)

Seja específico e base suas análises nas informações fornecidas.
"""
        return prompt
    
    def _fallback_analysis(self, perfil: PerfilUsuario) -> Dict[str, Any]:
        """Análise básica em caso de erro na IA"""
        areas = [area.area for area in perfil.areas_interesse]
        niveis = [area.nivel for area in perfil.areas_interesse]
        
        return {
            "user_id": perfil.user_id,
            "pontos_fortes": [f"Interesse em {', '.join(areas)}"],
            "areas_crescimento": ["Desenvolvimento de habilidades práticas"],
            "perfil_aprendizado": "Aprendiz ativo",
            "compatibilidade_areas": {area: 0.8 for area in areas},
            "sugestoes_desenvolvimento": ["Explorar projetos práticos nas áreas de interesse"],
            "nivel_geral": "intermediario" if "intermediario" in niveis else "iniciante",
            "areas_destaque": areas[:2] if len(areas) >= 2 else areas,
            "insights_personalizados": f"Usuário interessado em {len(areas)} área(s) principal(is).",
            "analyzed_at": "now",
            "total_areas": len(areas),
            "cursos_completos_count": len(perfil.cursos_completos or []),
            "cursos_em_andamento_count": len(perfil.cursos_em_andamento or [])
        }


