# 🧪 Guia Completo de Testes - Books Scraper API

Documentação completa sobre testes unitários, integração e automação.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Instalação](#-instalação)
- [Estrutura de Testes](#-estrutura-de-testes)
- [Executando Testes](#-executando-testes)
- [Cobertura de Código](#-cobertura-de-código)
- [Tipos de Testes](#-tipos-de-testes)
- [Guia de Escrita](#-guia-de-escrita)
- [CI/CD](#-cicd)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Visão Geral

O projeto possui **50+ testes automatizados** cobrindo todos os endpoints e funcionalidades.

### Estatísticas

| Métrica | Valor |
|---------|-------|
| Total de Testes | 50+ |
| Cobertura de Código | 85%+ |
| Classes de Teste | 13 |
| Tempo de Execução | ~5 segundos |
| Frameworks | Pytest, httpx |

### Tipos de Testes Incluídos

✅ **Testes Unitários** - Funções individuais  
✅ **Testes de Integração** - Fluxos completos  
✅ **Testes de API** - Todos os endpoints  
✅ **Testes de Autenticação** - JWT e permissões  
✅ **Testes de ML** - Endpoints de Machine Learning  
✅ **Testes de Performance** - Tempo de resposta  

---

## 📦 Instalação

### 1. Instalar Dependências de Teste

```bash
# Instalar dependências principais
pip install -r requirements.txt

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### 2. Verificar Instalação

```bash
pytest --version
# pytest 7.4.3

python -m pytest --version
```

---

## 📁 Estrutura de Testes

```
tests/
├── __init__.py                  # Inicialização do pacote
├── conftest.py                  # Fixtures compartilhadas (opcional)
├── test_api.py                  # ⭐ Testes principais (50+ testes)
├── test_auth.py                 # Testes de autenticação (opcional)
├── test_ml.py                   # Testes de ML (opcional)
└── test_integration.py          # Testes de integração (opcional)
```

### Classes de Teste Disponíveis

```python
# test_api.py

class TestRoot:              # 1 teste  - Endpoint raiz
class TestHealth:            # 2 testes - Health check
class TestBooks:             # 7 testes - CRUD de livros
class TestSearch:            # 6 testes - Busca e filtros
class TestTopRated:          # 3 testes - Top livros
class TestPriceRange:        # 3 testes - Faixa de preço
class TestCategories:        # 2 testes - Categorias
class TestStatistics:        # 4 testes - Estatísticas
class TestAuthentication:    # 5 testes - Auth JWT
class TestMachineLearning:   # 8 testes - ML endpoints
class TestAdmin:             # 4 testes - Rotas admin
class TestIntegration:       # 3 testes - Testes integrados
class TestPerformance:       # 2 testes - Performance
```

---

## 🚀 Executando Testes

### Comandos Básicos

```bash
# Executar todos os testes
pytest

# Com output verbose
pytest -v

# Com output detalhado
pytest -vv

# Modo quiet (apenas sumário)
pytest -q
```

### Executar Testes Específicos

```bash
# Um arquivo
pytest tests/test_api.py

# Uma classe específica
pytest tests/test_api.py::TestBooks

# Um teste específico
pytest tests/test_api.py::TestBooks::test_get_all_books

# Múltiplos arquivos
pytest tests/test_api.py tests/test_auth.py
```

### Executar por Marcador

```bash
# Criar marcadores no pytest.ini primeiro
pytest -m unit           # Apenas testes unitários
pytest -m integration    # Apenas integração
pytest -m auth          # Apenas autenticação
pytest -m ml            # Apenas ML
pytest -m slow          # Apenas testes lentos
```

### Opções Úteis

```bash
# Parar no primeiro erro
pytest -x

# Parar após N falhas
pytest --maxfail=3

# Executar apenas testes que falharam
pytest --lf

# Executar testes que falharam primeiro
pytest --ff

# Ver print statements
pytest -s

# Ver variáveis locais em falhas
pytest -l

# Traceback curto
pytest --tb=short

# Traceback longo
pytest --tb=long

# Sem traceback
pytest --tb=no
```

---

## 📊 Cobertura de Código

### Executar com Cobertura

```bash
# Cobertura simples
pytest --cov=app

# Com report detalhado
pytest --cov=app --cov-report=term-missing

# Relatório HTML
pytest --cov=app --cov-report=html

# Abrir relatório HTML
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
xdg-open htmlcov/index.html  # Linux
```

### Cobertura por Módulo

```bash
# Apenas um módulo
pytest --cov=app.main

# Múltiplos módulos
pytest --cov=app.main --cov=app.auth
```

### Configuração de Cobertura Mínima

```bash
# Falhar se cobertura < 80%
pytest --cov=app --cov-fail-under=80

# Falhar se cobertura < 85%
pytest --cov=app --cov-fail-under=85
```

### Exemplo de Saída

```
----------- coverage: platform win32, python 3.11.0 -----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/__init__.py            0      0   100%
app/auth.py               45      3    93%   78-80
app/config.py             35      2    94%   45, 67
app/database.py          120     12    90%   89-95, 134-138
app/main.py              180     15    92%   245-250, 312-318
app/models.py             85      0   100%
-----------------------------------------------------
TOTAL                    465     32    93%
```

---

## 🔬 Tipos de Testes

### 1. Testes Unitários

Testam funções individuais isoladamente.

```python
def test_parse_price():
    """Testa função de parse de preço"""
    from app.database import parse_price
    
    assert parse_price("£25.50") == 25.50
    assert parse_price("£100.00") == 100.00
    assert parse_price("invalid") == 0.0
```

### 2. Testes de API

Testam endpoints HTTP.

```python
def test_get_all_books():
    """Testa listagem de livros"""
    response = client.get("/api/v1/books")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### 3. Testes de Autenticação

```python
def test_login_success():
    """Testa login com credenciais válidas"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
```

### 4. Testes de Integração

```python
def test_full_flow():
    """Testa fluxo completo: login → busca → detalhes"""
    # 1. Login
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    token = login.json()["access_token"]
    
    # 2. Buscar livros
    search = client.get("/api/v1/books/search?title=light")
    books = search.json()
    assert len(books) > 0
    
    # 3. Obter detalhes
    book_id = books[0]["id"]
    details = client.get(f"/api/v1/books/{book_id}")
    assert details.status_code == 200
```

### 5. Testes Parametrizados

```python
import pytest

@pytest.mark.parametrize("username,password,expected", [
    ("admin", "admin123", 200),
    ("user", "user123", 200),
    ("invalid", "wrong", 401),
    ("", "", 422),
])
def test_login_cases(username, password, expected):
    """Testa múltiplos casos de login"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password}
    )
    assert response.status_code == expected
```

### 6. Testes com Fixtures

```python
import pytest

@pytest.fixture
def admin_token():
    """Fixture para obter token admin"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]

def test_admin_endpoint(admin_token):
    """Testa endpoint protegido"""
    response = client.post(
        "/api/v1/scraping/reload",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
```

### 7. Testes de Performance

```python
import time

def test_response_time():
    """Testa tempo de resposta"""
    start = time.time()
    response = client.get("/api/v1/books")
    end = time.time()
    
    assert response.status_code == 200
    assert (end - start) < 1.0  # Menos de 1 segundo
```

---

## ✍️ Guia de Escrita de Testes

### Padrão AAA (Arrange-Act-Assert)

```python
def test_create_book():
    """Testa criação de livro"""
    
    # Arrange - preparar dados
    book_data = {
        "titulo": "Test Book",
        "preco": 20.0,
        "categoria": "Fiction"
    }
    
    # Act - executar ação
    response = client.post("/api/v1/books", json=book_data)
    
    # Assert - verificar resultado
    assert response.status_code == 201
    assert response.json()["titulo"] == "Test Book"
```

### Nomeação de Testes

```python
# ✅ Bom - descritivo e claro
def test_login_with_invalid_credentials_returns_401():
    pass

def test_search_books_by_title_filters_correctly():
    pass

# ❌ Ruim - vago
def test_login():
    pass

def test_search():
    pass
```

### Organização por Cenário

```python
class TestBookSearch:
    """Testes de busca de livros"""
    
    def test_search_by_title_returns_matches(self):
        """Busca por título retorna correspondências"""
        pass
    
    def test_search_by_category_filters_correctly(self):
        """Busca por categoria filtra corretamente"""
        pass
    
    def test_search_with_no_results_returns_empty_list(self):
        """Busca sem resultados retorna lista vazia"""
        pass
    
    def test_search_with_multiple_filters_combines_correctly(self):
        """Busca com múltiplos filtros combina corretamente"""
        pass
```

### Boas Práticas

#### ✅ Fazer

- Testes independentes (não dependem de ordem)
- Um assert por conceito
- Nomes descritivos
- Testar casos de sucesso e erro
- Usar fixtures para setup comum
- Documentar testes complexos

#### ❌ Evitar

- Testes dependentes
- Múltiplos conceitos em um teste
- Nomes vagos
- Testar apenas happy path
- Duplicação de código
- Testes sem documentação

---

## 📈 Relatórios e Métricas

### Relatório de Testes

```bash
# Sumário simples
pytest --tb=no --no-header -q

# Relatório detalhado
pytest -v --tb=line

# Com duração dos testes
pytest --durations=10

# Top 20 testes mais lentos
pytest --durations=20
```

### Exemplo de Saída

```
==================== test session starts ====================
collected 50 items

tests/test_api.py::TestRoot::test_root_endpoint PASSED    [  2%]
tests/test_api.py::TestHealth::test_health_check PASSED   [  4%]
tests/test_api.py::TestBooks::test_get_all_books PASSED   [  6%]
tests/test_api.py::TestBooks::test_get_book_by_id PASSED  [  8%]
...
tests/test_api.py::TestPerformance::test_response_time PASSED [100%]

==================== 50 passed in 4.52s ====================
```

### Relatório HTML

```bash
# Gerar relatório
pytest --html=report.html --self-contained-html

# Abrir relatório
start report.html
```

### Relatório JSON

```bash
# Instalar plugin
pip install pytest-json-report

# Gerar relatório
pytest --json-report --json-report-file=report.json
```

---

## 🔄 CI/CD

### GitHub Actions

Crie `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Run scraper to generate data
      run: |
        python scraper/scraper.py
    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml --cov-report=term
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### GitLab CI

Crie `.gitlab-ci.yml`:

```yaml
image: python:3.11

stages:
  - test

test:
  stage: test
  before_script:
    - pip install -r requirements-dev.txt
  script:
    - python scraper/scraper.py
    - pytest --cov=app --cov-report=term --cov-report=html
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

### Pre-commit Hooks

Crie `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

---

## 🐛 Troubleshooting

### Erro: "No module named 'app'"

**Causa:** PYTHONPATH incorreto

**Solução:**
```bash
# Adicione o diretório raiz ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Ou execute de forma diferente
python -m pytest
```

### Erro: "Database not available"

**Causa:** Arquivo de dados não existe

**Solução:**
```bash
# Execute o scraper primeiro
python scraper/scraper.py

# Verifique se o arquivo foi criado
ls -la data/books_data.xlsx
```

### Testes Muito Lentos

**Solução:**
```bash
# Use pytest-xdist para paralelização
pip install pytest-xdist

# Execute em paralelo
pytest -n auto
```

### Conflito de Cache

**Solução:**
```bash
# Limpar cache do pytest
pytest --cache-clear

# Remover diretório de cache
rm -rf .pytest_cache
```

### Falhas Intermitentes

**Causa:** Testes dependentes de ordem

**Solução:**
```bash
# Execute em ordem aleatória
pip install pytest-randomly
pytest
```

---

## 📚 Recursos e Plugins

### Plugins Úteis

```bash
# Melhor UI
pip install pytest-sugar

# Relatório HTML
pip install pytest-html

# Paralelização
pip install pytest-xdist

# Ordem aleatória
pip install pytest-randomly

# Mock
pip install pytest-mock

# Asyncio
pip install pytest-asyncio

# Timeout
pip install pytest-timeout
```

### Uso de Plugins

```bash
# pytest-sugar (UI melhorada)
pytest

# pytest-html (relatório HTML)
pytest --html=report.html

# pytest-xdist (paralelo)
pytest -n 4  # 4 workers

# pytest-timeout (timeout)
pytest --timeout=10  # 10s por teste
```

---

## 📋 Checklist de Testes

Antes de fazer commit/deploy:

- [ ] Todos os testes passam (`pytest`)
- [ ] Cobertura > 80% (`pytest --cov=app --cov-fail-under=80`)
- [ ] Sem warnings (`pytest -W error`)
- [ ] Code style ok (`black app/ tests/`)
- [ ] Linting ok (`flake8 app/ tests/`)
- [ ] Type checking ok (`mypy app/`)
- [ ] Testes de integração ok
- [ ] Performance aceitável
- [ ] Documentação atualizada

---

## 🎯 Comandos Rápidos

```bash
# Desenvolvimento diário
pytest -v                                    # Executar testes
pytest --lf                                  # Apenas falhas
pytest -k "test_login"                       # Por nome
pytest tests/test_api.py::TestAuth          # Classe específica

# Cobertura
pytest --cov=app --cov-report=html          # Relatório HTML
pytest --cov=app --cov-report=term-missing  # Missing lines

# CI/CD
pytest --cov=app --cov-report=xml           # Para Codecov
pytest --junitxml=junit.xml                  # JUnit XML

# Debug
pytest -s                                    # Ver prints
pytest -l                                    # Ver variáveis locais
pytest --pdb                                 # Debugger em falha
pytest -x --pdb                             # Para + debug

# Performance
pytest --durations=10                        # Top 10 lentos
pytest -n auto                               # Paralelo
```

---

## 📊 Exemplo Completo de Saída

```bash
$ pytest -v --cov=app --cov-report=term

==================== test session starts ====================
platform win32 -- Python 3.11.0
cachedir: .pytest_cache
plugins: cov-4.1.0, asyncio-0.21.1
collected 50 items

tests/test_api.py::TestRoot::test_root_endpoint PASSED                    [  2%]
tests/test_api.py::TestHealth::test_health_check PASSED                   [  4%]
tests/test_api.py::TestHealth::test_health_database_info PASSED           [  6%]
tests/test_api.py::TestBooks::test_get_all_books PASSED                   [  8%]
tests/test_api.py::TestBooks::test_get_books_with_limit PASSED            [ 10%]
tests/test_api.py::TestBooks::test_get_book_by_id PASSED                  [ 12%]
tests/test_api.py::TestSearch::test_search_by_title PASSED                [ 14%]
tests/test_api.py::TestSearch::test_search_by_category PASSED             [ 16%]
tests/test_api.py::TestAuth::test_login_success PASSED                    [ 18%]
tests/test_api.py::TestAuth::test_login_invalid_credentials PASSED        [ 20%]
tests/test_api.py::TestML::test_ml_prediction_success PASSED              [ 22%]
...
tests/test_api.py::TestPerformance::test_response_time_books PASSED       [100%]

---------- coverage: platform win32, python 3.11.0 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
app/__init__.py            0      0   100%
app/auth.py               45      3    93%
app/config.py             35      2    94%
app/database.py          120     12    90%
app/main.py              180     15    92%
app/models.py             85      0   100%
-------------------------------------------
TOTAL                    465     32    93%

==================== 50 passed in 4.52s ====================
```

---

<div align="center">

**✅ Testes são essenciais para código confiável! 🚀**

[🔝 Voltar ao README](README.md)

</div>