"""
Modelos Pydantic
================
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any


# ========== BOOK MODELS ==========

class Book(BaseModel):
    """Modelo de livro"""
    id: int
    titulo: str
    preco: str
    rating: int = Field(ge=0, le=5)
    disponibilidade: str
    categoria: str
    imagem: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "titulo": "A Light in the Attic",
                "preco": "£51.77",
                "rating": 3,
                "disponibilidade": "In stock",
                "categoria": "Poetry",
                "imagem": "https://books.toscrape.com/..."
            }
        }


# ========== AUTH MODELS ==========

class LoginRequest(BaseModel):
    """Requisição de login"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }


class TokenResponse(BaseModel):
    """Resposta com tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Requisição de refresh token"""
    refresh_token: str


# ========== RESPONSE MODELS ==========

class HealthResponse(BaseModel):
    """Resposta de health check"""
    status: str
    timestamp: str
    database: Dict[str, Any]


class CategoryResponse(BaseModel):
    """Resposta de categorias"""
    total: int
    categorias: List[str]


class ScrapingResponse(BaseModel):
    """Resposta de scraping"""
    message: str
    status: str
    timestamp: str


# ========== STATS MODELS ==========

class StatsOverview(BaseModel):
    """Estatísticas gerais da coleção"""
    total_livros: int = Field(..., description="Total de livros")
    preco_medio: float = Field(..., description="Preço médio em £")
    preco_minimo: float = Field(..., description="Menor preço")
    preco_maximo: float = Field(..., description="Maior preço")
    distribuicao_ratings: Dict[str, int] = Field(..., description="Distribuição por rating")
    total_categorias: int = Field(..., description="Total de categorias")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_livros": 60,
                "preco_medio": 35.50,
                "preco_minimo": 10.00,
                "preco_maximo": 60.00,
                "distribuicao_ratings": {
                    "1": 5,
                    "2": 10,
                    "3": 20,
                    "4": 15,
                    "5": 10
                },
                "total_categorias": 15
            }
        }


class CategoryStats(BaseModel):
    """Estatísticas de uma categoria"""
    categoria: str
    total_livros: int
    preco_medio: float
    preco_minimo: float
    preco_maximo: float
    rating_medio: float


class CategoriesStatsResponse(BaseModel):
    """Resposta com estatísticas por categoria"""
    total_categorias: int
    estatisticas: List[CategoryStats]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_categorias": 3,
                "estatisticas": [
                    {
                        "categoria": "Fiction",
                        "total_livros": 20,
                        "preco_medio": 35.50,
                        "preco_minimo": 20.00,
                        "preco_maximo": 55.00,
                        "rating_medio": 3.5
                    }
                ]
            }
        }


# ========== ML MODELS ==========

class MLFeature(BaseModel):
    """Feature de um livro para ML"""
    id: int
    preco_numerico: float = Field(..., description="Preço em formato numérico")
    rating: int = Field(..., ge=0, le=5)
    categoria_encoded: int = Field(..., description="Categoria codificada")
    categoria_nome: str = Field(..., description="Nome da categoria")
    em_estoque: bool = Field(..., description="Se está em estoque")
    titulo_length: int = Field(..., description="Comprimento do título")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "preco_numerico": 51.77,
                "rating": 3,
                "categoria_encoded": 5,
                "categoria_nome": "Poetry",
                "em_estoque": True,
                "titulo_length": 21
            }
        }


class MLFeaturesResponse(BaseModel):
    """Resposta com features para ML"""
    total_registros: int
    features: List[MLFeature]
    categorias_mapping: Dict[str, int] = Field(..., description="Mapeamento categoria -> código")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_registros": 60,
                "features": [{"id": 1, "preco_numerico": 51.77, "rating": 3, "categoria_encoded": 5, "categoria_nome": "Poetry", "em_estoque": True, "titulo_length": 21}],
                "categorias_mapping": {"Poetry": 5, "Fiction": 1}
            }
        }


class MLTrainingData(BaseModel):
    """Dados formatados para treinamento de ML"""
    X: List[List[float]] = Field(..., description="Features (matriz)")
    y: List[int] = Field(..., description="Target (ratings)")
    feature_names: List[str] = Field(..., description="Nomes das features")
    total_samples: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "X": [[51.77, 5, 1, 21], [35.50, 2, 1, 18]],
                "y": [3, 4],
                "feature_names": ["preco", "categoria_encoded", "em_estoque", "titulo_length"],
                "total_samples": 2
            }
        }


class PredictionRequest(BaseModel):
    """Requisição de predição"""
    titulo: str = Field(..., description="Título do livro")
    preco: float = Field(..., ge=0, description="Preço do livro")
    categoria: str = Field(..., description="Categoria do livro")
    
    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "The Great Gatsby",
                "preco": 25.50,
                "categoria": "Fiction"
            }
        }


class PredictionResponse(BaseModel):
    """Resposta de predição"""
    rating_previsto: int = Field(..., ge=0, le=5, description="Rating previsto")
    confianca: float = Field(..., ge=0, le=1, description="Confiança da predição")
    features_usadas: Dict[str, float] = Field(..., description="Features utilizadas")
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "rating_previsto": 4,
                "confianca": 0.85,
                "features_usadas": {
                    "preco_numerico": 25.50,
                    "categoria_encoded": 1,
                    "titulo_length": 16
                },
                "timestamp": "2025-01-04T15:30:00"
            }
        }