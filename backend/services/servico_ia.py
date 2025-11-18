"""
Serviço de integração com IA Generativa (Google Gemini)
Implementa técnicas de Prompt Engineering para recomendações educacionais
"""

import os
import logging
from typing import Dict, Any, List, Optional

# Import opcional para google.generativeai (funciona em modo mock sem ela)
try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    # Criar stubs para desenvolvimento sem a biblioteca
    class HarmCategory:
        HARM_CATEGORY_HATE_SPEECH = None
        HARM_CATEGORY_HARASSMENT = None
        HARM_CATEGORY_SEXUALLY_EXPLICIT = None
        HARM_CATEGORY_DANGEROUS_CONTENT = None
    
    class HarmBlockThreshold:
        BLOCK_NONE = None

logger = logging.getLogger(__name__)


class AIService:
    """Serviço para interação com Google Gemini API"""
    
    def __init__(self):
        """Inicializa o serviço de IA com as configurações"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # Verificar se google.generativeai está disponível
        if not GEMINI_AVAILABLE:
            logger.warning("google.generativeai não está instalado. Usando modo mock.")
            self.api_key = None
            self.mock_mode = True
            self.model_name = "gemini-pro (mock)"
            self.model = None
        elif not self.api_key:
            # Em desenvolvimento, pode usar uma chave padrão ou simular
            logger.warning("GEMINI_API_KEY not found. Using mock mode for development.")
            self.api_key = None
            self.mock_mode = True
            self.model_name = "gemini-pro"
            self.model = None
        else:
            self.mock_mode = False
            genai.configure(api_key=self.api_key)
            self.model_name = "gemini-pro"
            self.model = genai.GenerativeModel(self.model_name)
        
        # Configurações de segurança do conteúdo (apenas se gemini estiver disponível)
        if GEMINI_AVAILABLE and not self.mock_mode:
            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        else:
            self.safety_settings = {}
        
        # Configurações de geração
        self.generation_config = {
            "temperature": 0.7,  # Criatividade nas respostas
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
    
    def get_model_name(self) -> str:
        """Retorna o nome do modelo utilizado"""
        return self.model_name
    
    async def check_health(self) -> bool:
        """Verifica se o serviço de IA está disponível"""
        if self.mock_mode:
            return True  # Em modo mock, sempre disponível
        
        try:
            # Teste simples para verificar conexão
            response = self.model.generate_content(
                "Responda apenas 'OK'",
                safety_settings=self.safety_settings,
                generation_config=self.generation_config
            )
            return response.text is not None
        except Exception as e:
            logger.error(f"AI service health check failed: {str(e)}")
            return False
    
    async def generate_text(
        self,
        prompt: str,
        system_context: Optional[str] = None
    ) -> str:
        """
        Gera texto usando IA Generativa com Prompt Engineering
        
        Args:
            prompt: Prompt principal para geração
            system_context: Contexto adicional do sistema
            
        Returns:
            Texto gerado pela IA
        """
        if self.mock_mode:
            # Modo mock para desenvolvimento/testes sem API key
            logger.info("Mock mode: Generating simulated response")
            return self._mock_response(prompt)
        
        try:
            # Construir prompt completo com contexto
            full_prompt = self._build_prompt(prompt, system_context)
            
            # Gerar resposta usando Gemini
            response = self.model.generate_content(
                full_prompt,
                safety_settings=self.safety_settings,
                generation_config=self.generation_config
            )
            
            if not response.text:
                raise ValueError("Empty response from AI model")
            
            logger.info(f"Generated text successfully (length: {len(response.text)})")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}", exc_info=True)
            raise Exception(f"Failed to generate text: {str(e)}")
    
    async def analyze_with_structured_output(
        self,
        prompt: str,
        output_format: Dict[str, Any],
        system_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analisa dados e retorna saída estruturada
        
        Args:
            prompt: Prompt de análise
            output_format: Formato esperado da saída
            system_context: Contexto adicional
            
        Returns:
            Dicionário com dados estruturados
        """
        format_description = self._describe_format(output_format)
        
        structured_prompt = f"""
{system_context or ""}

{prompt}

IMPORTANTE: Retorne APENAS um objeto JSON válido no seguinte formato:
{format_description}

Não inclua markdown, não inclua ```json, apenas o JSON puro.
"""
        
        response_text = await self.generate_text(structured_prompt)
        
        # Tentar extrair JSON da resposta
        import json
        import re
        
        # Remover markdown se presente
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        response_text = response_text.strip()
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON, returning raw text: {str(e)}")
            # Se falhar, retornar como texto simples
            return {"raw_response": response_text}
    
    def _build_prompt(self, prompt: str, system_context: Optional[str] = None) -> str:
        """Constrói prompt completo com contexto do sistema"""
        if system_context:
            return f"{system_context}\n\n{prompt}"
        return prompt
    
    def _describe_format(self, format_dict: Dict[str, Any]) -> str:
        """Descreve formato de saída esperado"""
        import json
        return json.dumps(format_dict, indent=2, ensure_ascii=False)
    
    def _mock_response(self, prompt: str) -> str:
        """Gera resposta simulada para desenvolvimento sem API key"""
        if "análise" in prompt.lower() or "analyze" in prompt.lower():
            return """
            {
                "pontos_fortes": ["Interesse em programação e IA"],
                "areas_crescimento": ["Desenvolvimento de projetos práticos"],
                "perfil_aprendizado": "Aprendiz ativo que combina teoria e prática",
                "compatibilidade_areas": {
                    "programacao": 0.9,
                    "ia": 0.85
                }
            }
            """
        elif "recomendação" in prompt.lower() or "recommend" in prompt.lower():
            return """
            Baseado no seu perfil de interesse em programação (intermediário) e inteligência artificial, 
            recomendo este curso porque ele combina conceitos práticos de desenvolvimento com aplicações 
            de IA, perfeito para seu nível atual de conhecimento e interesses.
            """
        else:
            return "Resposta simulada para desenvolvimento. Configure GEMINI_API_KEY para usar IA real."


