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
            # ========== INTELIGÊNCIA ARTIFICIAL ==========
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
                titulo="Deep Learning Avançado",
                descricao="Redes neurais profundas, CNNs, RNNs e aplicações práticas de deep learning.",
                area="ia",
                nivel="avancado",
                duracao="60 horas",
                icone="🧠"
            ),
            Curso(
                id="3",
                titulo="Machine Learning com Python",
                descricao="Implemente algoritmos de machine learning do zero usando scikit-learn e TensorFlow.",
                area="ia",
                nivel="intermediario",
                duracao="55 horas",
                icone="🎯"
            ),
            Curso(
                id="4",
                titulo="Processamento de Linguagem Natural",
                descricao="NLP, transformers, BERT e aplicações práticas de processamento de texto.",
                area="ia",
                nivel="intermediario",
                duracao="50 horas",
                icone="💬"
            ),
            
            # ========== CIÊNCIA DE DADOS ==========
            Curso(
                id="5",
                titulo="Fundamentos de Ciência de Dados",
                descricao="Introdução à ciência de dados, estatística descritiva e análise exploratória.",
                area="ciencia_dados",
                nivel="iniciante",
                duracao="45 horas",
                icone="📊"
            ),
            Curso(
                id="6",
                titulo="Análise de Dados com Python",
                descricao="Domine Python para análise de dados com pandas, numpy e visualização de dados.",
                area="ciencia_dados",
                nivel="intermediario",
                duracao="50 horas",
                icone="🐍"
            ),
            Curso(
                id="7",
                titulo="Big Data e Data Engineering",
                descricao="Processamento de grandes volumes de dados, Hadoop, Spark e pipelines de dados.",
                area="ciencia_dados",
                nivel="avancado",
                duracao="70 horas",
                icone="⚡"
            ),
            Curso(
                id="8",
                titulo="Visualização de Dados com Tableau",
                descricao="Crie dashboards e visualizações interativas para análise de negócios.",
                area="ciencia_dados",
                nivel="intermediario",
                duracao="40 horas",
                icone="📈"
            ),
            
            # ========== SUSTENTABILIDADE ==========
            Curso(
                id="9",
                titulo="Fundamentos de Sustentabilidade",
                descricao="Conceitos de sustentabilidade ambiental, social e econômica. Agenda 2030 e ODS.",
                area="sustentabilidade",
                nivel="iniciante",
                duracao="30 horas",
                icone="🌱"
            ),
            Curso(
                id="10",
                titulo="Gestão Ambiental Empresarial",
                descricao="Implementação de práticas sustentáveis em empresas, ISO 14001 e economia circular.",
                area="sustentabilidade",
                nivel="intermediario",
                duracao="45 horas",
                icone="🌍"
            ),
            Curso(
                id="11",
                titulo="Energias Renováveis",
                descricao="Solar, eólica, biomassa e outras fontes de energia limpa. Tecnologias e aplicações.",
                area="sustentabilidade",
                nivel="intermediario",
                duracao="50 horas",
                icone="☀️"
            ),
            
            # ========== PROGRAMAÇÃO ==========
            Curso(
                id="12",
                titulo="Fundamentos de Programação",
                descricao="Conceitos básicos de programação, lógica, algoritmos e estruturas de dados.",
                area="programacao",
                nivel="iniciante",
                duracao="30 horas",
                icone="📝"
            ),
            Curso(
                id="13",
                titulo="Desenvolvimento Web Full Stack",
                descricao="Aprenda a criar aplicações web completas com React, Node.js e bancos de dados.",
                area="programacao",
                nivel="intermediario",
                duracao="80 horas",
                icone="💻"
            ),
            Curso(
                id="14",
                titulo="JavaScript Moderno",
                descricao="ES6+, async/await, promises e recursos modernos do JavaScript.",
                area="programacao",
                nivel="iniciante",
                duracao="35 horas",
                icone="⚡"
            ),
            Curso(
                id="15",
                titulo="Arquitetura de Software",
                descricao="Padrões de design, arquitetura limpa e boas práticas de desenvolvimento.",
                area="programacao",
                nivel="avancado",
                duracao="50 horas",
                icone="🏗️"
            ),
            Curso(
                id="16",
                titulo="Desenvolvimento Mobile com React Native",
                descricao="Crie aplicativos mobile multiplataforma usando React Native e Expo.",
                area="programacao",
                nivel="intermediario",
                duracao="70 horas",
                icone="📱"
            ),
            
            # ========== DESIGN ==========
            Curso(
                id="17",
                titulo="Fundamentos de Design",
                descricao="Princípios de design, tipografia, cores, composição e teoria visual.",
                area="design",
                nivel="iniciante",
                duracao="35 horas",
                icone="🎨"
            ),
            Curso(
                id="18",
                titulo="UI/UX Design",
                descricao="Design de interfaces e experiência do usuário. Ferramentas: Figma, Adobe XD.",
                area="design",
                nivel="intermediario",
                duracao="60 horas",
                icone="✨"
            ),
            Curso(
                id="19",
                titulo="Design Gráfico Profissional",
                descricao="Photoshop, Illustrator e InDesign para criação de materiais gráficos.",
                area="design",
                nivel="intermediario",
                duracao="55 horas",
                icone="🖼️"
            ),
            Curso(
                id="20",
                titulo="Design Thinking",
                descricao="Metodologia de design thinking para inovação e solução de problemas.",
                area="design",
                nivel="intermediario",
                duracao="40 horas",
                icone="💡"
            ),
            
            # ========== MARKETING DIGITAL ==========
            Curso(
                id="21",
                titulo="Marketing Digital Essencial",
                descricao="Fundamentos de marketing digital, redes sociais, SEO e conteúdo digital.",
                area="marketing_digital",
                nivel="iniciante",
                duracao="40 horas",
                icone="📱"
            ),
            Curso(
                id="22",
                titulo="Google Ads e Facebook Ads",
                descricao="Criação e gestão de campanhas pagas no Google e Facebook. Otimização de ROI.",
                area="marketing_digital",
                nivel="intermediario",
                duracao="50 horas",
                icone="📊"
            ),
            Curso(
                id="23",
                titulo="Marketing de Conteúdo e SEO",
                descricao="Estratégias de conteúdo, SEO técnico, link building e ranqueamento orgânico.",
                area="marketing_digital",
                nivel="intermediario",
                duracao="55 horas",
                icone="🔍"
            ),
            Curso(
                id="24",
                titulo="E-mail Marketing e Automação",
                descricao="Campanhas de e-mail, automação de marketing e nutrição de leads.",
                area="marketing_digital",
                nivel="intermediario",
                duracao="35 horas",
                icone="📧"
            ),
            
            # ========== GESTÃO ==========
            Curso(
                id="25",
                titulo="Fundamentos de Gestão",
                descricao="Conceitos básicos de administração, planejamento, organização e liderança.",
                area="gestao",
                nivel="iniciante",
                duracao="35 horas",
                icone="📋"
            ),
            Curso(
                id="26",
                titulo="Gestão de Projetos com PMBOK",
                descricao="Metodologia PMBOK, gerenciamento de escopo, tempo, custos e recursos.",
                area="gestao",
                nivel="intermediario",
                duracao="60 horas",
                icone="📊"
            ),
            Curso(
                id="27",
                titulo="Liderança e Gestão de Equipes",
                descricao="Desenvolvimento de habilidades de liderança, gestão de pessoas e alta performance.",
                area="gestao",
                nivel="intermediario",
                duracao="45 horas",
                icone="👥"
            ),
            Curso(
                id="28",
                titulo="Gestão Estratégica",
                descricao="Planejamento estratégico, análise SWOT, BSC e execução de estratégias.",
                area="gestao",
                nivel="avancado",
                duracao="50 horas",
                icone="🎯"
            ),
            
            # ========== VENDAS ==========
            Curso(
                id="29",
                titulo="Técnicas de Vendas",
                descricao="Fundamentos de vendas, prospecção, apresentação e fechamento de negócios.",
                area="vendas",
                nivel="iniciante",
                duracao="30 horas",
                icone="💼"
            ),
            Curso(
                id="30",
                titulo="Vendas Consultivas",
                descricao="Metodologia SPIN, identificação de necessidades e vendas de valor.",
                area="vendas",
                nivel="intermediario",
                duracao="40 horas",
                icone="🤝"
            ),
            Curso(
                id="31",
                titulo="Negociação Avançada",
                descricao="Técnicas avançadas de negociação, gestão de objeções e fechamento complexo.",
                area="vendas",
                nivel="avancado",
                duracao="35 horas",
                icone="🎯"
            ),
            Curso(
                id="32",
                titulo="CRM e Gestão de Relacionamento",
                descricao="Gestão de pipeline de vendas, CRM Salesforce e relacionamento com clientes.",
                area="vendas",
                nivel="intermediario",
                duracao="40 horas",
                icone="📈"
            ),
            
            # ========== RECURSOS HUMANOS ==========
            Curso(
                id="33",
                titulo="Fundamentos de RH",
                descricao="Introdução à gestão de pessoas, recrutamento, seleção e desenvolvimento.",
                area="rh",
                nivel="iniciante",
                duracao="35 horas",
                icone="👤"
            ),
            Curso(
                id="34",
                titulo="Recrutamento e Seleção",
                descricao="Processos de recrutamento, entrevistas, testes e seleção de talentos.",
                area="rh",
                nivel="intermediario",
                duracao="45 horas",
                icone="🔍"
            ),
            Curso(
                id="35",
                titulo="Gestão de Pessoas e Cultura Organizacional",
                descricao="Desenvolvimento organizacional, cultura corporativa e engajamento.",
                area="rh",
                nivel="intermediario",
                duracao="50 horas",
                icone="🏢"
            ),
            Curso(
                id="36",
                titulo="Treinamento e Desenvolvimento",
                descricao="Planejamento de treinamentos, desenvolvimento de competências e educação corporativa.",
                area="rh",
                nivel="intermediario",
                duracao="40 horas",
                icone="📚"
            ),
            
            # ========== FINANÇAS ==========
            Curso(
                id="37",
                titulo="Fundamentos de Finanças",
                descricao="Introdução às finanças pessoais e corporativas, orçamento e fluxo de caixa.",
                area="financas",
                nivel="iniciante",
                duracao="30 horas",
                icone="💰"
            ),
            Curso(
                id="38",
                titulo="Análise Financeira e Contabilidade",
                descricao="Demonstrações financeiras, indicadores, análise de investimentos e custos.",
                area="financas",
                nivel="intermediario",
                duracao="50 horas",
                icone="📊"
            ),
            Curso(
                id="39",
                titulo="Gestão Financeira Empresarial",
                descricao="Planejamento financeiro, capital de giro, financiamentos e estrutura de capital.",
                area="financas",
                nivel="avancado",
                duracao="55 horas",
                icone="💼"
            ),
            Curso(
                id="40",
                titulo="Investimentos e Mercado Financeiro",
                descricao="Ações, títulos, fundos de investimento e análise de mercado financeiro.",
                area="financas",
                nivel="intermediario",
                duracao="45 horas",
                icone="📈"
            ),
            
            # ========== SAÚDE ==========
            Curso(
                id="41",
                titulo="Saúde e Bem-estar",
                descricao="Fundamentos de saúde, nutrição, exercícios e qualidade de vida.",
                area="saude",
                nivel="iniciante",
                duracao="30 horas",
                icone="💚"
            ),
            Curso(
                id="42",
                titulo="Nutrição e Alimentação Saudável",
                descricao="Princípios de nutrição, planejamento alimentar e dietas balanceadas.",
                area="saude",
                nivel="intermediario",
                duracao="40 horas",
                icone="🥗"
            ),
            Curso(
                id="43",
                titulo="Gestão em Saúde",
                descricao="Administração hospitalar, sistemas de saúde e gestão de unidades de saúde.",
                area="saude",
                nivel="intermediario",
                duracao="50 horas",
                icone="🏥"
            ),
            Curso(
                id="44",
                titulo="Primeiros Socorros",
                descricao="Técnicas básicas de primeiros socorros e atendimento de emergências.",
                area="saude",
                nivel="iniciante",
                duracao="20 horas",
                icone="🆘"
            ),
            
            # ========== EDUCAÇÃO ==========
            Curso(
                id="45",
                titulo="Metodologias de Ensino",
                descricao="Técnicas de ensino, didática, planejamento de aulas e avaliação.",
                area="educacao",
                nivel="iniciante",
                duracao="35 horas",
                icone="📖"
            ),
            Curso(
                id="46",
                titulo="Educação a Distância (EAD)",
                descricao="Design instrucional, plataformas EAD, produção de conteúdo e tutoria online.",
                area="educacao",
                nivel="intermediario",
                duracao="50 horas",
                icone="💻"
            ),
            Curso(
                id="47",
                titulo="Pedagogia e Psicologia Educacional",
                descricao="Teorias de aprendizagem, desenvolvimento cognitivo e práticas pedagógicas.",
                area="educacao",
                nivel="intermediario",
                duracao="45 horas",
                icone="🧠"
            ),
            Curso(
                id="48",
                titulo="Gestão Educacional",
                descricao="Administração escolar, planejamento pedagógico e gestão de instituições de ensino.",
                area="educacao",
                nivel="avancado",
                duracao="50 horas",
                icone="🏫"
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

