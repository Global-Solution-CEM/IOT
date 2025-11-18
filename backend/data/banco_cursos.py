"""
Base de dados de cursos
Em produção, isso seria substituído por um banco de dados real
"""

from typing import List, Optional
from models.curso import Curso


class BancoCursos:
    """Base de dados de cursos disponíveis"""
    
    def __init__(self):
        """Inicializa com cursos de exemplo"""
        self._courses = self._load_courses()
    
    def _load_courses(self) -> List[Curso]:
        """Carrega cursos disponíveis"""
        return [
            Curso(
                id="1",
                titulo="Introdução à Inteligência Artificial",
                descricao="Aprenda os fundamentos da IA, incluindo machine learning, redes neurais e aplicações práticas.",
                area="ia",
                nivel="iniciante",
                duracao="40 horas",
                icone="🤖"
            ),
            Curso(
                id="2",
                titulo="Análise de Dados com Python",
                descricao="Domine Python para análise de dados com pandas, numpy e visualização de dados.",
                area="programacao",
                nivel="intermediario",
                duracao="50 horas",
                icone="📊"
            ),
            Curso(
                id="3",
                titulo="Desenvolvimento Web Full Stack",
                descricao="Aprenda a criar aplicações web completas com React, Node.js e bancos de dados.",
                area="programacao",
                nivel="intermediario",
                duracao="80 horas",
                icone="💻"
            ),
            Curso(
                id="4",
                titulo="Deep Learning Avançado",
                descricao="Redes neurais profundas, CNNs, RNNs e aplicações práticas de deep learning.",
                area="ia",
                nivel="avancado",
                duracao="60 horas",
                icone="🧠"
            ),
            Curso(
                id="5",
                titulo="Fundamentos de Programação",
                descricao="Conceitos básicos de programação, lógica, algoritmos e estruturas de dados.",
                area="programacao",
                nivel="iniciante",
                duracao="30 horas",
                icone="📝"
            ),
            Curso(
                id="6",
                titulo="Machine Learning com Python",
                descricao="Implemente algoritmos de machine learning do zero usando scikit-learn e TensorFlow.",
                area="ia",
                nivel="intermediario",
                duracao="55 horas",
                icone="🎯"
            ),
            Curso(
                id="7",
                titulo="Desenvolvimento Mobile com React Native",
                descricao="Crie aplicativos mobile multiplataforma usando React Native e Expo.",
                area="programacao",
                nivel="intermediario",
                duracao="70 horas",
                icone="📱"
            ),
            Curso(
                id="8",
                titulo="Visão Computacional",
                descricao="Processamento de imagens, reconhecimento de padrões e aplicações de CV.",
                area="ia",
                nivel="avancado",
                duracao="45 horas",
                icone="👁️"
            ),
            Curso(
                id="9",
                titulo="Arquitetura de Software",
                descricao="Padrões de design, arquitetura limpa e boas práticas de desenvolvimento.",
                area="programacao",
                nivel="avancado",
                duracao="50 horas",
                icone="🏗️"
            ),
            Curso(
                id="10",
                titulo="Processamento de Linguagem Natural",
                descricao="NLP, transformers, BERT e aplicações práticas de processamento de texto.",
                area="ia",
                nivel="intermediario",
                duracao="50 horas",
                icone="💬"
            ),
            Curso(
                id="11",
                titulo="JavaScript Moderno",
                descricao="ES6+, async/await, promises e recursos modernos do JavaScript.",
                area="programacao",
                nivel="iniciante",
                duracao="35 horas",
                icone="⚡"
            ),
            Curso(
                id="12",
                titulo="Robótica e Automação",
                descricao="Fundamentos de robótica, sistemas embarcados e IoT.",
                area="iot",
                nivel="intermediario",
                duracao="60 horas",
                icone="🤖"
            ),
            Curso(
                id="13",
                titulo="Sistemas Embarcados",
                descricao="Programação de microcontroladores, sensores e sistemas IoT.",
                area="iot",
                nivel="avancado",
                duracao="55 horas",
                icone="🔌"
            ),
            Curso(
                id="14",
                titulo="Fundamentos de IoT",
                descricao="Internet das Coisas: conceitos, protocolos e aplicações práticas.",
                area="iot",
                nivel="iniciante",
                duracao="40 horas",
                icone="🌐"
            ),
            Curso(
                id="15",
                titulo="Segurança da Informação",
                descricao="Cibersegurança, criptografia e boas práticas de segurança.",
                area="seguranca",
                nivel="intermediario",
                duracao="45 horas",
                icone="🔒"
            ),
        ]
    
    def get_all_courses(self) -> List[Curso]:
        """Retorna todos os cursos disponíveis"""
        return self._courses.copy()
    
    def get_course_by_id(self, course_id: str) -> Optional[Curso]:
        """Busca curso por ID"""
        for course in self._courses:
            if course.id == course_id:
                return course
        return None
    
    def get_courses_by_area(self, area: str) -> List[Curso]:
        """Busca cursos por área"""
        return [course for course in self._courses if course.area == area]
    
    def get_courses_by_level(self, nivel: str) -> List[Curso]:
        """Busca cursos por nível"""
        return [course for course in self._courses if course.nivel == nivel]


