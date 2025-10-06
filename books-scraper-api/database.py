"""
Acesso aos Dados e Cache
=========================
"""

from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import openpyxl

from config import DATA_FILE, CACHE_TIMEOUT

# Cache global
_cache: Optional[List[Dict]] = None
_cache_time: Optional[datetime] = None


def load_books() -> List[Dict]:
    """Carrega livros do Excel"""
    if not Path(DATA_FILE).exists():
        return []
    
    try:
        wb = openpyxl.load_workbook(DATA_FILE, read_only=True)
        ws = wb.active
        
        books = []
        for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=1):
            if row[0]:
                books.append({
                    'id': idx,
                    'titulo': row[0] or '',
                    'preco': row[1] or '',
                    'rating': int(row[2]) if row[2] else 0,
                    'disponibilidade': row[3] or '',
                    'categoria': row[4] or '',
                    'imagem': row[5] or ''
                })
        
        wb.close()
        return books
    except Exception as e:
        print(f"Erro ao carregar livros: {e}")
        return []


def get_books() -> List[Dict]:
    """Obtém livros do cache ou carrega"""
    global _cache, _cache_time
    
    # Verifica se cache é válido
    if _cache and _cache_time:
        elapsed = (datetime.now() - _cache_time).total_seconds()
        if elapsed < CACHE_TIMEOUT:
            return _cache
    
    # Carrega e atualiza cache
    _cache = load_books()
    _cache_time = datetime.now()
    return _cache


def clear_cache():
    """Limpa o cache"""
    global _cache, _cache_time
    _cache = None
    _cache_time = None


def find_book_by_id(book_id: int) -> Optional[Dict]:
    """Busca livro por ID"""
    books = get_books()
    return next((b for b in books if b['id'] == book_id), None)


def search_books(
    title: Optional[str] = None,
    category: Optional[str] = None,
    min_rating: Optional[int] = None,
    max_price: Optional[float] = None
) -> List[Dict]:
    """Busca livros com filtros"""
    books = get_books()
    
    if title:
        books = [b for b in books if title.lower() in b['titulo'].lower()]
    
    if category:
        books = [b for b in books if category.lower() in b['categoria'].lower()]
    
    if min_rating is not None:
        books = [b for b in books if b['rating'] >= min_rating]
    
    if max_price is not None:
        try:
            books = [
                b for b in books 
                if float(b['preco'].replace('£', '').replace(',', '')) <= max_price
            ]
        except:
            pass
    
    return books


def get_categories() -> List[str]:
    """Obtém categorias únicas"""
    books = get_books()
    categories = set(b['categoria'] for b in books if b['categoria'])
    return sorted(list(categories))


def parse_price(price: str) -> float:
    """Converte string de preço para float"""
    try:
        return float(price.replace('£', '').replace(',', '').strip())
    except:
        return 0.0


def get_stats_overview() -> dict:
    """Calcula estatísticas gerais da coleção"""
    books = get_books()
    
    if not books:
        return {
            "total_livros": 0,
            "preco_medio": 0.0,
            "preco_minimo": 0.0,
            "preco_maximo": 0.0,
            "distribuicao_ratings": {},
            "total_categorias": 0
        }
    
    # Preços
    prices = [parse_price(b['preco']) for b in books]
    prices = [p for p in prices if p > 0]
    
    # Ratings
    ratings_count = {}
    for b in books:
        rating = b.get('rating', 0)
        ratings_count[str(rating)] = ratings_count.get(str(rating), 0) + 1
    
    return {
        "total_livros": len(books),
        "preco_medio": round(sum(prices) / len(prices), 2) if prices else 0.0,
        "preco_minimo": round(min(prices), 2) if prices else 0.0,
        "preco_maximo": round(max(prices), 2) if prices else 0.0,
        "distribuicao_ratings": ratings_count,
        "total_categorias": len(get_categories())
    }


def get_category_stats() -> List[dict]:
    """Calcula estatísticas por categoria"""
    books = get_books()
    categories = get_categories()
    
    stats = []
    
    for category in categories:
        # Filtra livros da categoria
        cat_books = [b for b in books if b['categoria'] == category]
        
        if not cat_books:
            continue
        
        # Calcula preços
        prices = [parse_price(b['preco']) for b in cat_books]
        prices = [p for p in prices if p > 0]
        
        # Calcula ratings
        ratings = [b.get('rating', 0) for b in cat_books]
        
        stats.append({
            "categoria": category,
            "total_livros": len(cat_books),
            "preco_medio": round(sum(prices) / len(prices), 2) if prices else 0.0,
            "preco_minimo": round(min(prices), 2) if prices else 0.0,
            "preco_maximo": round(max(prices), 2) if prices else 0.0,
            "rating_medio": round(sum(ratings) / len(ratings), 2) if ratings else 0.0
        })
    
    # Ordena por total de livros (decrescente)
    stats.sort(key=lambda x: x['total_livros'], reverse=True)
    
    return stats


def get_top_rated_books(limit: int = 10) -> List[Dict]:
    """Obtém livros com melhor avaliação"""
    books = get_books()
    
    # Ordena por rating (decrescente) e depois por título
    sorted_books = sorted(
        books,
        key=lambda x: (-x.get('rating', 0), x.get('titulo', ''))
    )
    
    return sorted_books[:limit]


def get_books_by_price_range(min_price: float, max_price: float) -> List[Dict]:
    """Filtra livros por faixa de preço"""
    books = get_books()
    
    filtered = []
    for book in books:
        price = parse_price(book['preco'])
        if min_price <= price <= max_price:
            filtered.append(book)
    
    # Ordena por preço
    filtered.sort(key=lambda x: parse_price(x['preco']))
    
    return filtered


# ========== ML FUNCTIONS ==========

def get_ml_features() -> dict:
    """Retorna dados formatados como features para ML"""
    books = get_books()
    
    if not books:
        return {
            "total_registros": 0,
            "features": [],
            "categorias_mapping": {}
        }
    
    # Criar mapeamento de categorias
    categories = sorted(list(set(b['categoria'] for b in books if b['categoria'])))
    categorias_mapping = {cat: idx for idx, cat in enumerate(categories)}
    
    # Extrair features
    features = []
    for book in books:
        # Verifica disponibilidade
        em_estoque = 'in stock' in book.get('disponibilidade', '').lower()
        
        feature = {
            "id": book['id'],
            "preco_numerico": parse_price(book['preco']),
            "rating": book.get('rating', 0),
            "categoria_encoded": categorias_mapping.get(book['categoria'], 0),
            "categoria_nome": book['categoria'],
            "em_estoque": em_estoque,
            "titulo_length": len(book.get('titulo', ''))
        }
        features.append(feature)
    
    return {
        "total_registros": len(features),
        "features": features,
        "categorias_mapping": categorias_mapping
    }


def get_ml_training_data() -> dict:
    """Retorna dados formatados para treinamento de ML"""
    books = get_books()
    
    if not books:
        return {
            "X": [],
            "y": [],
            "feature_names": [],
            "total_samples": 0
        }
    
    # Criar mapeamento de categorias
    categories = sorted(list(set(b['categoria'] for b in books if b['categoria'])))
    categorias_mapping = {cat: idx for idx, cat in enumerate(categories)}
    
    # Preparar dados
    X = []
    y = []
    
    for book in books:
        # Features (X)
        em_estoque = 1 if 'in stock' in book.get('disponibilidade', '').lower() else 0
        
        features = [
            parse_price(book['preco']),                    # Preço
            categorias_mapping.get(book['categoria'], 0),  # Categoria codificada
            em_estoque,                                     # Em estoque (0 ou 1)
            len(book.get('titulo', ''))                    # Tamanho do título
        ]
        
        X.append(features)
        
        # Target (y) - Rating
        y.append(book.get('rating', 0))
    
    return {
        "X": X,
        "y": y,
        "feature_names": ["preco", "categoria_encoded", "em_estoque", "titulo_length"],
        "total_samples": len(X)
    }


def predict_rating(titulo: str, preco: float, categoria: str) -> dict:
    """
    Predição simples de rating baseada em regras
    (Em produção, use um modelo ML treinado)
    """
    from datetime import datetime
    
    # Obter estatísticas para fazer predição baseada em regras
    books = get_books()
    
    # Criar mapeamento de categorias
    categories = sorted(list(set(b['categoria'] for b in books if b['categoria'])))
    categorias_mapping = {cat: idx for idx, cat in enumerate(categories)}
    
    # Features
    categoria_encoded = categorias_mapping.get(categoria, 0)
    titulo_length = len(titulo)
    
    # Lógica simples de predição (substituir por modelo ML real)
    rating_base = 3  # Rating médio base
    
    # Ajusta baseado no preço (livros mais caros tendem a ter ratings melhores)
    if preco > 50:
        rating_base += 1
    elif preco < 20:
        rating_base -= 1
    
    # Ajusta baseado na categoria (exemplo)
    if categoria in ["Classics", "Poetry"]:
        rating_base += 0.5
    
    # Garante que está entre 1-5
    rating_previsto = max(1, min(5, int(round(rating_base))))
    
    # Confiança baseada em quão perto está de casos conhecidos
    confianca = 0.75  # Valor fixo (em produção calcular baseado no modelo)
    
    return {
        "rating_previsto": rating_previsto,
        "confianca": confianca,
        "features_usadas": {
            "preco_numerico": float(preco),
            "categoria_encoded": float(categoria_encoded),
            "titulo_length": float(titulo_length)
        },
        "timestamp": datetime.now().isoformat()
    }