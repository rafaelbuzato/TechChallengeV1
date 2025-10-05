"""
Testes Unitários para Books Scraper API
========================================
Execute: pytest tests/test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Cliente de testes
client = TestClient(app)


# ==================== TESTES ROOT ====================

class TestRoot:
    """Testes para endpoints raiz"""
    
    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["version"] == "1.0.0"


# ==================== TESTES HEALTH ====================

class TestHealth:
    """Testes para health check"""
    
    def test_health_check(self):
        """Testa health check"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "database" in data
        assert data["status"] in ["healthy", "unhealthy"]
    
    def test_health_database_info(self):
        """Testa informações do banco de dados no health"""
        response = client.get("/api/v1/health")
        data = response.json()
        db_info = data["database"]
        assert "connected" in db_info
        assert "total_books" in db_info
        assert "file_path" in db_info
        assert "file_exists" in db_info


# ==================== TESTES BOOKS ====================

class TestBooks:
    """Testes para endpoints de livros"""
    
    def test_get_all_books(self):
        """Testa listagem de todos os livros"""
        response = client.get("/api/v1/books")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_books_with_limit(self):
        """Testa listagem com limite"""
        response = client.get("/api/v1/books?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5
    
    def test_get_books_with_offset(self):
        """Testa listagem com offset"""
        response = client.get("/api/v1/books?limit=10&offset=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 10
    
    def test_get_books_invalid_limit(self):
        """Testa limite inválido"""
        response = client.get("/api/v1/books?limit=0")
        assert response.status_code == 422
    
    def test_get_book_by_id(self):
        """Testa busca por ID"""
        response = client.get("/api/v1/books/1")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "titulo" in data
            assert "preco" in data
            assert "rating" in data
    
    def test_get_book_invalid_id(self):
        """Testa ID inexistente"""
        response = client.get("/api/v1/books/99999")
        assert response.status_code == 404
    
    def test_book_model_structure(self):
        """Testa estrutura do modelo de livro"""
        response = client.get("/api/v1/books?limit=1")
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                book = data[0]
                required_fields = [
                    "id", "titulo", "preco", "rating",
                    "disponibilidade", "categoria", "imagem"
                ]
                for field in required_fields:
                    assert field in book


# ==================== TESTES SEARCH ====================

class TestSearch:
    """Testes para busca de livros"""
    
    def test_search_by_title(self):
        """Testa busca por título"""
        response = client.get("/api/v1/books/search?title=the")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_by_category(self):
        """Testa busca por categoria"""
        response = client.get("/api/v1/books/search?category=fiction")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_by_min_rating(self):
        """Testa busca por rating mínimo"""
        response = client.get("/api/v1/books/search?min_rating=4")
        assert response.status_code == 200
        data = response.json()
        for book in data:
            assert book["rating"] >= 4
    
    def test_search_by_max_price(self):
        """Testa busca por preço máximo"""
        response = client.get("/api/v1/books/search?max_price=30")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_multiple_filters(self):
        """Testa busca com múltiplos filtros"""
        response = client.get(
            "/api/v1/books/search?title=the&min_rating=3&max_price=50"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_no_results(self):
        """Testa busca sem resultados"""
        response = client.get(
            "/api/v1/books/search?title=xyznonexistent"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


# ==================== TESTES TOP RATED ====================

class TestTopRated:
    """Testes para livros melhor avaliados"""
    
    def test_get_top_rated_default(self):
        """Testa top rated com limite padrão"""
        response = client.get("/api/v1/books/top-rated")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
    
    def test_get_top_rated_custom_limit(self):
        """Testa top rated com limite customizado"""
        response = client.get("/api/v1/books/top-rated?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5
    
    def test_top_rated_sorted(self):
        """Testa se está ordenado por rating"""
        response = client.get("/api/v1/books/top-rated?limit=10")
        data = response.json()
        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["rating"] >= data[i + 1]["rating"]


# ==================== TESTES PRICE RANGE ====================

class TestPriceRange:
    """Testes para filtro por faixa de preço"""
    
    def test_price_range_valid(self):
        """Testa faixa de preço válida"""
        response = client.get("/api/v1/books/price-range?min=10&max=30")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_price_range_min_greater_than_max(self):
        """Testa min > max"""
        response = client.get("/api/v1/books/price-range?min=50&max=20")
        assert response.status_code == 400
    
    def test_price_range_negative(self):
        """Testa preço negativo"""
        response = client.get("/api/v1/books/price-range?min=-10&max=50")
        assert response.status_code == 422


# ==================== TESTES CATEGORIES ====================

class TestCategories:
    """Testes para categorias"""
    
    def test_get_categories(self):
        """Testa listagem de categorias"""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "categorias" in data
        assert isinstance(data["categorias"], list)
    
    def test_categories_structure(self):
        """Testa estrutura das categorias"""
        response = client.get("/api/v1/categories")
        data = response.json()
        assert data["total"] == len(data["categorias"])


# ==================== TESTES STATISTICS ====================

class TestStatistics:
    """Testes para estatísticas"""
    
    def test_stats_overview(self):
        """Testa estatísticas gerais"""
        response = client.get("/api/v1/stats/overview")
        assert response.status_code == 200
        data = response.json()
        required_fields = [
            "total_livros", "preco_medio", "preco_minimo",
            "preco_maximo", "distribuicao_ratings", "total_categorias"
        ]
        for field in required_fields:
            assert field in data
    
    def test_stats_overview_values(self):
        """Testa valores das estatísticas"""
        response = client.get("/api/v1/stats/overview")
        data = response.json()
        assert data["total_livros"] >= 0
        assert data["preco_medio"] >= 0
        assert data["preco_minimo"] >= 0
        assert data["preco_maximo"] >= 0
        assert isinstance(data["distribuicao_ratings"], dict)
    
    def test_stats_categories(self):
        """Testa estatísticas por categoria"""
        response = client.get("/api/v1/stats/categories")
        assert response.status_code == 200
        data = response.json()
        assert "total_categorias" in data
        assert "estatisticas" in data
        assert isinstance(data["estatisticas"], list)
    
    def test_stats_categories_structure(self):
        """Testa estrutura das estatísticas por categoria"""
        response = client.get("/api/v1/stats/categories")
        data = response.json()
        if len(data["estatisticas"]) > 0:
            cat_stat = data["estatisticas"][0]
            required_fields = [
                "categoria", "total_livros", "preco_medio",
                "preco_minimo", "preco_maximo", "rating_medio"
            ]
            for field in required_fields:
                assert field in cat_stat


# ==================== TESTES AUTHENTICATION ====================

class TestAuthentication:
    """Testes para autenticação"""
    
    def test_login_success(self):
        """Testa login com credenciais válidas"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "invalid", "password": "wrong"}
        )
        assert response.status_code == 401
    
    def test_login_missing_fields(self):
        """Testa login com campos faltando"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin"}
        )
        assert response.status_code == 422
    
    def test_refresh_token(self):
        """Testa refresh token"""
        # Primeiro faz login
        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Tenta renovar
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
    
    def test_refresh_invalid_token(self):
        """Testa refresh com token inválido"""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )
        assert response.status_code == 401


# ==================== TESTES MACHINE LEARNING ====================

class TestMachineLearning:
    """Testes para endpoints de ML"""
    
    def test_get_ml_features(self):
        """Testa obtenção de features"""
        response = client.get("/api/v1/ml/features")
        assert response.status_code == 200
        data = response.json()
        assert "total_registros" in data
        assert "features" in data
        assert "categorias_mapping" in data
    
    def test_ml_features_structure(self):
        """Testa estrutura das features"""
        response = client.get("/api/v1/ml/features")
        data = response.json()
        if len(data["features"]) > 0:
            feature = data["features"][0]
            required_fields = [
                "id", "preco_numerico", "rating",
                "categoria_encoded", "categoria_nome",
                "em_estoque", "titulo_length"
            ]
            for field in required_fields:
                assert field in feature
    
    def test_get_training_data(self):
        """Testa obtenção de dados de treinamento"""
        response = client.get("/api/v1/ml/training-data")
        assert response.status_code == 200
        data = response.json()
        assert "X" in data
        assert "y" in data
        assert "feature_names" in data
        assert "total_samples" in data
    
    def test_training_data_consistency(self):
        """Testa consistência dos dados de treinamento"""
        response = client.get("/api/v1/ml/training-data")
        data = response.json()
        assert len(data["X"]) == len(data["y"])
        assert len(data["X"]) == data["total_samples"]
        if len(data["X"]) > 0:
            assert len(data["X"][0]) == len(data["feature_names"])
    
    def test_ml_prediction_success(self):
        """Testa predição bem-sucedida"""
        response = client.post(
            "/api/v1/ml/predictions",
            json={
                "titulo": "Test Book",
                "preco": 25.50,
                "categoria": "Fiction"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "rating_previsto" in data
        assert "confianca" in data
        assert "features_usadas" in data
        assert "timestamp" in data
    
    def test_ml_prediction_rating_range(self):
        """Testa se rating previsto está no range correto"""
        response = client.post(
            "/api/v1/ml/predictions",
            json={
                "titulo": "Another Book",
                "preco": 30.00,
                "categoria": "History"
            }
        )
        data = response.json()
        assert 1 <= data["rating_previsto"] <= 5
        assert 0 <= data["confianca"] <= 1
    
    def test_ml_prediction_missing_fields(self):
        """Testa predição com campos faltando"""
        response = client.post(
            "/api/v1/ml/predictions",
            json={"titulo": "Test", "preco": 20.0}
        )
        assert response.status_code == 422
    
    def test_ml_prediction_invalid_price(self):
        """Testa predição com preço negativo"""
        response = client.post(
            "/api/v1/ml/predictions",
            json={
                "titulo": "Test",
                "preco": -10.0,
                "categoria": "Fiction"
            }
        )
        assert response.status_code == 422


# ==================== TESTES ADMIN ====================

class TestAdmin:
    """Testes para endpoints admin (protegidos)"""
    
    def get_admin_token(self):
        """Obtém token de admin para testes"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        return response.json()["access_token"]
    
    def test_scraping_without_auth(self):
        """Testa scraping sem autenticação"""
        response = client.post("/api/v1/scraping/trigger")
        assert response.status_code == 403
    
    def test_scraping_with_user_token(self):
        """Testa scraping com token de usuário comum"""
        # Login como user
        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": "user", "password": "user123"}
        )
        token = login_response.json()["access_token"]
        
        # Tenta acessar endpoint admin
        response = client.post(
            "/api/v1/scraping/trigger",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
    
    def test_reload_without_auth(self):
        """Testa reload sem autenticação"""
        response = client.post("/api/v1/scraping/reload")
        assert response.status_code == 403
    
    def test_reload_with_admin_token(self):
        """Testa reload com token admin"""
        token = self.get_admin_token()
        response = client.post(
            "/api/v1/scraping/reload",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data


# ==================== TESTES DE INTEGRAÇÃO ====================

class TestIntegration:
    """Testes de integração entre endpoints"""
    
    def test_search_and_get_by_id(self):
        """Testa busca e depois obtenção por ID"""
        # Busca livros
        search_response = client.get("/api/v1/books/search?title=the")
        if search_response.status_code == 200:
            books = search_response.json()
            if len(books) > 0:
                book_id = books[0]["id"]
                
                # Busca pelo ID
                get_response = client.get(f"/api/v1/books/{book_id}")
                assert get_response.status_code == 200
                book = get_response.json()
                assert book["id"] == book_id
    
    def test_stats_match_books(self):
        """Testa se estatísticas batem com livros"""
        books_response = client.get("/api/v1/books")
        stats_response = client.get("/api/v1/stats/overview")
        
        if books_response.status_code == 200 and stats_response.status_code == 200:
            books = books_response.json()
            stats = stats_response.json()
            
            # Total deve bater
            assert stats["total_livros"] >= len(books)
    
    def test_ml_features_match_books(self):
        """Testa se features de ML batem com livros"""
        books_response = client.get("/api/v1/books?limit=1000")
        ml_response = client.get("/api/v1/ml/features")
        
        if books_response.status_code == 200 and ml_response.status_code == 200:
            books = books_response.json()
            ml_data = ml_response.json()
            
            assert ml_data["total_registros"] == len(books)


# ==================== TESTES DE PERFORMANCE ====================

class TestPerformance:
    """Testes básicos de performance"""
    
    def test_response_time_books(self):
        """Testa tempo de resposta para listagem"""
        import time
        start = time.time()
        response = client.get("/api/v1/books?limit=100")
        end = time.time()
        
        assert response.status_code == 200
        assert (end - start) < 2.0  # Deve responder em menos de 2 segundos
    
    def test_response_time_stats(self):
        """Testa tempo de resposta para estatísticas"""
        import time
        start = time.time()
        response = client.get("/api/v1/stats/overview")
        end = time.time()
        
        assert response.status_code == 200
        assert (end - start) < 2.0


# ==================== CONFIGURAÇÃO PYTEST ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])