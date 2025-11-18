"""Modelos de dados para cursos"""

from pydantic import BaseModel, Field
from typing import Optional


class Curso(BaseModel):
    """Modelo de curso"""
    id: str = Field(..., description="ID único do curso")
    titulo: str = Field(..., description="Título do curso")
    descricao: str = Field(..., description="Descrição do curso")
    area: str = Field(..., description="Área do curso")
    nivel: str = Field(..., description="Nível do curso (iniciante, intermediario, avancado)")
    duracao: str = Field(..., description="Duração estimada do curso")
    icone: Optional[str] = Field(None, description="Ícone/emoji do curso")


