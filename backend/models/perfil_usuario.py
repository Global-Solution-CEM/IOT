"""Modelos de dados para perfil do usuário"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class AreaInteresse(BaseModel):
    """Área de interesse do usuário com nível"""
    area: str = Field(..., description="ID da área de interesse")
    nivel: str = Field(..., description="Nível de conhecimento (iniciante, intermediario, avancado)")


class PerfilUsuario(BaseModel):
    """Perfil completo do usuário"""
    user_id: str = Field(..., description="ID único do usuário")
    name: Optional[str] = Field(None, description="Nome do usuário")
    email: Optional[str] = Field(None, description="Email do usuário")
    areas_interesse: List[AreaInteresse] = Field(..., description="Lista de áreas de interesse com níveis")
    cursos_completos: Optional[List[str]] = Field(default=[], description="IDs de cursos completados")
    cursos_em_andamento: Optional[List[str]] = Field(default=[], description="IDs de cursos em andamento")
    progresso_cursos: Optional[Dict[str, int]] = Field(default={}, description="Progresso por curso (curso_id: porcentagem)")


