"""
Serviço de Recomendações usando IA Generativa
Gera recomendações personalizadas de cursos baseadas no perfil do usuário
"""

import logging
from typing import List, Dict, Any
from models.perfil_usuario import PerfilUsuario, AreaInteresse
from models.curso import Curso
from services.servico_ia import AIService
from data.banco_cursos import BancoCursos

logger = logging.getLogger(__name__)


class ServicoRecomendacoes:
    """Serviço para gerar recomendações de cursos usando IA Generativa"""
    
    SYSTEM_CONTEXT = """Você é um especialista em recomendações educacionais personalizadas. 
Sua função é recomendar cursos ideais para cada usuário baseado em:
- Áreas de interesse e níveis de conhecimento
- Histórico de cursos completados e em andamento
- Compatibilidade e pré-requisitos
- Progresso atual e objetivos de aprendizado

Seja específico, explique claramente por que cada curso foi recomendado e forneça 
análises de compatibilidade detalhadas."""

    def __init__(self, ai_service: AIService):
        """Inicializa o serviço de recomendações"""
        self.ai_service = ai_service
        self.banco_cursos = BancoCursos()
    
    async def gerar_recomendacoes(
        self,
        perfil_usuario: PerfilUsuario,
        analise_perfil: Dict[str, Any],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Gera recomendações personalizadas de cursos usando IA Generativa
        
        Args:
            perfil_usuario: Perfil do usuário
            analise_perfil: Análise do perfil gerada pela IA
            limit: Número máximo de recomendações
            
        Returns:
            Lista de cursos recomendados com explicações personalizadas
        """
        logger.info(f"Generating recommendations for user: {perfil_usuario.user_id}")
        
        # Obter cursos disponíveis filtrados por áreas de interesse
        cursos_disponiveis = self._filtrar_cursos_por_interesses(perfil_usuario)
        
        if not cursos_disponiveis:
            logger.warning(f"No courses found for user interests: {perfil_usuario.user_id}")
            return []
        
        # Construir prompt para IA gerar recomendações
        prompt_recomendacao = self._construir_prompt_recomendacao(
            perfil_usuario,
            analise_perfil,
            cursos_disponiveis,
            limit
        )
        
        # Gerar recomendações usando IA
        try:
            recomendacoes_ia = await self._obter_recomendacoes_ia(
                prompt_recomendacao,
                cursos_disponiveis,
                limit
            )
            
            # Processar e enriquecer recomendações
            recomendacoes = await self._processar_recomendacoes(
                recomendacoes_ia,
                perfil_usuario,
                cursos_disponiveis
            )
            
            logger.info(f"Generated {len(recomendacoes)} recommendations")
            return recomendacoes[:limit]
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}", exc_info=True)
            # Retornar recomendações baseadas em filtros simples
            return self._recomendacoes_fallback(perfil_usuario, cursos_disponiveis, limit)
    
    async def gerar_explicacao_curso(
        self,
        curso: Curso,
        perfil_usuario: PerfilUsuario
    ) -> str:
        """
        Gera explicação personalizada de por que um curso foi recomendado
        
        Args:
            curso: Curso para explicar
            perfil_usuario: Perfil do usuário
            
        Returns:
            Explicação gerada pela IA
        """
        prompt = f"""
Explique de forma personalizada por que este curso foi recomendado para este usuário.

CURSO:
- Título: {curso.titulo}
- Descrição: {curso.descricao}
- Área: {curso.area}
- Nível: {curso.nivel}

PERFIL DO USUÁRIO:
- Áreas de interesse: {', '.join([f"{a.area} ({a.nivel})" for a in perfil_usuario.areas_interesse])}
- Cursos completos: {len(perfil_usuario.cursos_completos or [])}
- Cursos em andamento: {len(perfil_usuario.cursos_em_andamento or [])}

Gere uma explicação clara, específica e motivadora (máximo 150 palavras) explicando:
1. Por que este curso se encaixa no perfil do usuário
2. Como ele se relaciona com os interesses e nível atual
3. Benefícios específicos para o desenvolvimento do usuário

Seja direto, pessoal e encorajador.
"""
        
        try:
            explicacao = await self.ai_service.generate_text(prompt, self.SYSTEM_CONTEXT)
            return explicacao.strip()
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return f"Este curso foi recomendado porque se alinha com suas áreas de interesse ({curso.area}) e seu nível atual ({curso.nivel})."
    
    def _filtrar_cursos_por_interesses(self, perfil: PerfilUsuario) -> List[Curso]:
        """Filtra cursos disponíveis pelas áreas de interesse do usuário"""
        areas_interesse = {area.area for area in perfil.areas_interesse}
        
        todos_cursos = self.banco_cursos.get_all_courses()
        
        # Filtrar cursos que correspondem às áreas de interesse
        filtrados = [
            curso for curso in todos_cursos
            if curso.area in areas_interesse
        ]
        
        # Se não houver cursos nas áreas exatas, incluir cursos relacionados
        if not filtrados:
            filtrados = todos_cursos[:10]  # Retornar top 10 como fallback
        
        return filtrados
    
    def _construir_prompt_recomendacao(
        self,
        perfil: PerfilUsuario,
        analise: Dict[str, Any],
        cursos: List[Curso],
        limit: int
    ) -> str:
        """Constrói prompt para gerar recomendações"""
        
        # Lista de cursos disponíveis
        lista_cursos = "\n".join([
            f"{i+1}. ID: {c.id} | {c.titulo} | {c.area} | {c.nivel} | {c.descricao[:100]}"
            for i, c in enumerate(cursos)
        ])
        
        # Informações do perfil
        areas_info = "\n".join([
            f"- {area.area} (nível: {area.nivel})"
            for area in perfil.areas_interesse
        ])
        
        prompt = f"""
Com base na análise do perfil do usuário e nos cursos disponíveis, gere recomendações personalizadas.

PERFIL DO USUÁRIO:
Áreas de interesse:
{areas_info}

Cursos completos: {len(perfil.cursos_completos or [])}
Cursos em andamento: {len(perfil.cursos_em_andamento or [])}

ANÁLISE DO PERFIL:
Pontos fortes: {', '.join(analise.get('pontos_fortes', []))}
Áreas de crescimento: {', '.join(analise.get('areas_crescimento', []))}
Nível geral: {analise.get('nivel_geral', 'intermediario')}

CURSOS DISPONÍVEIS:
{lista_cursos}

INSTRUÇÕES:
1. Selecione os {limit} melhores cursos para este usuário
2. Ordene por relevância (do mais relevante para o menos relevante)
3. Para cada curso, gere:
   - Score de relevância (0.0 a 1.0)
   - Explicação personalizada de por que foi recomendado (máximo 100 palavras)
   - Análise de compatibilidade com o perfil (breve, máximo 50 palavras)
   - Sugestão de trilha de aprendizado se aplicável

Retorne APENAS um JSON no formato:
{{
    "recommendations": [
        {{
            "course_id": "id_do_curso",
            "score": 0.95,
            "reason": "explicação personalizada",
            "compatibility": "análise de compatibilidade",
            "learning_path": "sugestão de trilha (opcional)"
        }}
    ]
}}

Priorize cursos que:
- Combinam múltiplas áreas de interesse do usuário
- Estão no nível adequado (ou ligeiramente acima para desafio)
- Complementam cursos já completados ou em andamento
- Alinham com áreas de crescimento identificadas
"""
        return prompt
    
    async def _obter_recomendacoes_ia(
        self,
        prompt: str,
        cursos: List[Curso],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Obtém recomendações da IA"""
        
        output_format = {
            "recommendations": [
                {
                    "course_id": "string",
                    "score": "float",
                    "reason": "string",
                    "compatibility": "string",
                    "learning_path": "string (opcional)"
                }
            ]
        }
        
        try:
            result = await self.ai_service.analyze_with_structured_output(
                prompt=prompt,
                output_format=output_format,
                system_context=self.SYSTEM_CONTEXT
            )
            
            return result.get("recommendations", [])
            
        except Exception as e:
            logger.error(f"Error getting AI recommendations: {str(e)}")
            return []
    
    async def _processar_recomendacoes(
        self,
        recomendacoes_ia: List[Dict[str, Any]],
        perfil_usuario: PerfilUsuario,
        cursos_disponiveis: List[Curso]
    ) -> List[Dict[str, Any]]:
        """Processa e enriquece recomendações da IA"""
        
        recomendacoes = []
        
        # Criar mapa de cursos por ID
        mapa_cursos = {curso.id: curso for curso in cursos_disponiveis}
        
        for rec_ia in recomendacoes_ia:
            curso_id = rec_ia.get("course_id")
            curso = mapa_cursos.get(curso_id)
            
            if not curso:
                continue  # Pular se curso não encontrado
            
            # Enriquecer com explicação personalizada se não vier completa da IA
            motivo = rec_ia.get("reason", "")
            if not motivo or len(motivo) < 50:
                try:
                    motivo = await self.gerar_explicacao_curso(curso, perfil_usuario)
                except:
                    motivo = rec_ia.get("reason", "Curso recomendado baseado no seu perfil.")
            
            recomendacao = {
                "course": {
                    "id": curso.id,
                    "titulo": curso.titulo,
                    "descricao": curso.descricao,
                    "area": curso.area,
                    "nivel": curso.nivel,
                    "duracao": curso.duracao,
                    "icone": curso.icone
                },
                "score": float(rec_ia.get("score", 0.8)),
                "reason": motivo,
                "compatibility": rec_ia.get("compatibility", "Compatível com seu perfil de aprendizado."),
                "suggested_learning_path": rec_ia.get("learning_path")
            }
            
            recomendacoes.append(recomendacao)
        
        # Ordenar por score
        recomendacoes.sort(key=lambda x: x["score"], reverse=True)
        
        return recomendacoes
    
    def _recomendacoes_fallback(
        self,
        perfil: PerfilUsuario,
        cursos: List[Curso],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Recomendações básicas em caso de erro na IA"""
        
        # Ordenar por nível e área de interesse
        areas_interesse = {area.area for area in perfil.areas_interesse}
        
        cursos_com_score = []
        for curso in cursos:
            score = 0.7  # Score base
            
            # Aumentar score se estiver nas áreas de interesse
            if curso.area in areas_interesse:
                score += 0.2
            
            cursos_com_score.append({
                "course": {
                    "id": curso.id,
                    "titulo": curso.titulo,
                    "descricao": curso.descricao,
                    "area": curso.area,
                    "nivel": curso.nivel,
                    "duracao": curso.duracao,
                    "icone": curso.icone
                },
                "score": score,
                "reason": f"Recomendado baseado no seu interesse em {curso.area}.",
                "compatibility": f"Compatível com seu nível de conhecimento.",
                "suggested_learning_path": None
            })
        
        cursos_com_score.sort(key=lambda x: x["score"], reverse=True)
        return cursos_com_score[:limit]


