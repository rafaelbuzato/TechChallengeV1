"""
FastAPI Application - API Completa
===================================
"""

from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess
import sys
import logging

# ==================== SETUP LOGGING BÁSICO (SEMPRE PRIMEIRO) ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== IMPORTS ====================

from app.config import (
    PROJECT_NAME, VERSION, DESCRIPTION, API_V1_PREFIX, 
    ALLOWED_ORIGINS, DATA_FILE, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models import (
    Book, LoginRequest, TokenResponse, RefreshTokenRequest,
    HealthResponse, CategoryResponse, ScrapingResponse,
    StatsOverview, CategoriesStatsResponse,
    MLFeaturesResponse, MLTrainingData, PredictionRequest, PredictionResponse
)
from app.auth import authenticate_user, create_access_token, create_refresh_token, get_admin_user
from app.database import (
    get_books, find_book_by_id, search_books, get_categories, clear_cache,
    get_stats_overview, get_category_stats, get_top_rated_books, get_books_by_price_range,
    get_ml_features, get_ml_training_data, predict_rating
)

# ==================== MIDDLEWARE (OPCIONAL) ====================

MIDDLEWARE_AVAILABLE = False
try:
    from app.middleware import (
        RequestLoggingMiddleware, MetricsMiddleware, 
        get_metrics_instance, set_metrics_instance
    )
    MIDDLEWARE_AVAILABLE = True
    logger.info("Middleware modules loaded")
except ImportError:
    logger.warning("Middleware not available. Running without advanced monitoring.")

# ==================== CRIAR APP ====================

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{API_V1_PREFIX}/openapi.json"
)

# Adicionar middlewares se disponíveis
if MIDDLEWARE_AVAILABLE:
    try:
        metrics_middleware = MetricsMiddleware(app)
        set_metrics_instance(metrics_middleware)
        app.add_middleware(MetricsMiddleware)
        app.add_middleware(RequestLoggingMiddleware)
        logger.info("✅ Middlewares enabled")
    except Exception as e:
        logger.error(f"Error loading middlewares: {e}")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== ROOT ====================

@app.get("/", tags=["Root"])
async def root():
    """Informações da API"""
    return {
        "name": PROJECT_NAME,
        "version": VERSION,
        "docs": "/docs",
        "health": f"{API_V1_PREFIX}/health"
    }


# ==================== AUTENTICAÇÃO ====================

@app.post("/api/v1/auth/login", response_model=TokenResponse, tags=["Authentication"])
async def login(data: LoginRequest):
    """Login - Retorna tokens JWT"""
    user = authenticate_user(data.username, data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = create_access_token(user["username"], user["role"])
    refresh_token = create_refresh_token(user["username"])
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@app.post("/api/v1/auth/refresh", response_model=TokenResponse, tags=["Authentication"])
async def refresh(data: RefreshTokenRequest):
    """Renova access token"""
    from jose import jwt, JWTError
    from app.config import SECRET_KEY, ALGORITHM
    
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        
        if not username or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido")
        
        from app.auth import USERS_DB
        user = USERS_DB.get(username)
        
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        access_token = create_access_token(user["username"], user["role"])
        refresh_token = create_refresh_token(user["username"])
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


# ==================== LIVROS ====================

@app.get("/api/v1/books", response_model=List[Book], tags=["Books"])
async def get_all_books(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Lista todos os livros com paginação"""
    books = get_books()
    return books[offset:offset + limit]


@app.get("/api/v1/books/search", response_model=List[Book], tags=["Books"])
async def search_books_endpoint(
    title: str = None,
    category: str = None,
    min_rating: int = Query(None, ge=0, le=5),
    max_price: float = Query(None, ge=0)
):
    """Busca livros com filtros"""
    books = search_books(title, category, min_rating, max_price)
    return books


@app.get("/api/v1/books/top-rated", response_model=List[Book], tags=["Books"])
async def get_top_rated(
    limit: int = Query(10, ge=1, le=100)
):
    """Lista livros com melhor avaliação"""
    books = get_top_rated_books(limit)
    return books


@app.get("/api/v1/books/price-range", response_model=List[Book], tags=["Books"])
async def get_books_in_price_range(
    min: float = Query(..., ge=0),
    max: float = Query(..., ge=0)
):
    """Filtra livros por faixa de preço"""
    if min > max:
        raise HTTPException(status_code=400, detail="Preço mínimo não pode ser maior que o máximo")
    
    books = get_books_by_price_range(min, max)
    return books


@app.get("/api/v1/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book(book_id: int):
    """Busca livro por ID"""
    book = find_book_by_id(book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail=f"Livro {book_id} não encontrado")
    
    return book


# ==================== CATEGORIAS ====================

@app.get("/api/v1/categories", response_model=CategoryResponse, tags=["Categories"])
async def get_categories_endpoint():
    """Lista todas as categorias"""
    categories = get_categories()
    return {
        "total": len(categories),
        "categorias": categories
    }


# ==================== ESTATÍSTICAS ====================

@app.get("/api/v1/stats/overview", response_model=StatsOverview, tags=["Statistics"])
async def get_overview_stats():
    """Estatísticas gerais da coleção"""
    stats = get_stats_overview()
    return stats


@app.get("/api/v1/stats/categories", response_model=CategoriesStatsResponse, tags=["Statistics"])
async def get_categories_stats():
    """Estatísticas detalhadas por categoria"""
    stats = get_category_stats()
    return {
        "total_categorias": len(stats),
        "estatisticas": stats
    }


# ==================== HEALTH ====================

@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Verifica status da API"""
    books = get_books()
    
    database_status = {
        "connected": len(books) > 0,
        "total_books": len(books),
        "file_path": str(DATA_FILE),
        "file_exists": DATA_FILE.exists(),
        "cache_valid": True
    }
    
    status_value = "healthy" if database_status["connected"] else "unhealthy"
    
    return {
        "status": status_value,
        "timestamp": datetime.now().isoformat(),
        "database": database_status
    }


# ==================== MÉTRICAS E MONITORAMENTO ====================

@app.get("/api/v1/metrics", tags=["Monitoring"])
async def get_metrics():
    """Métricas de Performance da API"""
    if not MIDDLEWARE_AVAILABLE:
        return {
            "error": "Metrics middleware not available",
            "message": "Create app/middleware.py to enable metrics"
        }
    
    metrics_instance = get_metrics_instance()
    if metrics_instance:
        return metrics_instance.get_metrics()
    return {"error": "Metrics not available"}


@app.get("/api/v1/logs/recent", tags=["Monitoring"])
async def get_recent_logs(
    lines: int = Query(50, ge=1, le=1000)
):
    """Logs Recentes"""
    from pathlib import Path
    import json
    
    log_file = Path("logs/api.log")
    
    if not log_file.exists():
        return {"logs": [], "total": 0}
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:]
            
            logs = []
            for line in recent_lines:
                try:
                    logs.append(json.loads(line))
                except:
                    logs.append({"raw": line.strip()})
            
            return {
                "logs": logs,
                "total": len(logs),
                "file": str(log_file)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== MACHINE LEARNING ====================

@app.get("/api/v1/ml/features", response_model=MLFeaturesResponse, tags=["Machine Learning"])
async def get_ml_features_endpoint():
    """Retorna dados formatados como features para ML"""
    features_data = get_ml_features()
    return features_data


@app.get("/api/v1/ml/training-data", response_model=MLTrainingData, tags=["Machine Learning"])
async def get_training_data_endpoint():
    """Retorna dataset formatado para treinamento de modelos ML"""
    training_data = get_ml_training_data()
    return training_data


@app.post("/api/v1/ml/predictions", response_model=PredictionResponse, tags=["Machine Learning"])
async def predict_book_rating(request: PredictionRequest):
    """Predição de rating para um novo livro"""
    try:
        prediction = predict_rating(
            titulo=request.titulo,
            preco=request.preco,
            categoria=request.categoria
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer predição: {str(e)}")


# ==================== ADMIN - SCRAPING ====================

@app.post("/api/v1/scraping/trigger", response_model=ScrapingResponse, tags=["Admin"])
async def trigger_scraping(
    max_pages: int = Query(3, ge=1, le=50),
    current_user: dict = Depends(get_admin_user)
):
    """🔒 ADMIN - Executa scraping"""
    try:
        logger.info(f"Scraping triggered by {current_user['username']}")
        
        result = subprocess.run(
            [sys.executable, "scraper/scraper.py"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            clear_cache()
            books_count = len(get_books())
            
            return {
                "message": f"Scraping concluído! {books_count} livros carregados.",
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail=f"Erro: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Timeout (>5 min)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/scraping/reload", response_model=ScrapingResponse, tags=["Admin"])
async def reload_data(current_user: dict = Depends(get_admin_user)):
    """🔒 ADMIN - Recarrega dados do arquivo"""
    try:
        clear_cache()
        books_count = len(get_books())
        
        return {
            "message": f"Dados recarregados! {books_count} livros.",
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== EVENTOS ====================

@app.on_event("startup")
async def startup():
    """Inicialização"""
    books_count = len(get_books())
    
    logger.info(f"API started with {books_count} books")
    
    print("\n" + "="*60)
    print(f"✅ API iniciada com {books_count} livros")
    print(f"📚 Docs: http://localhost:8000/docs")
    print(f"📊 Metrics: http://localhost:8000/api/v1/metrics")
    if MIDDLEWARE_AVAILABLE:
        print("🔍 Monitoring: ENABLED")
    else:
        print("⚠️  Monitoring: DISABLED")
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown():
    """Finalização"""
    logger.info("API shutdown")
    print("\n🔴 API finalizada\n")


if __name__ == "__main__":
    import uvicorn
    from app.config import API_HOST, API_PORT, DEBUG
    
    uvicorn.run(
        "app.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG
    )