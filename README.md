# 📚 Books Scraper API - Completa

> API RESTful profissional para consultar dados de livros com web scraping, autenticação JWT, machine learning e monitoramento em tempo real.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Coverage](https://img.shields.io/badge/Coverage-85%25-brightgreen.svg)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Endpoints da API](#-endpoints-da-api)
- [Autenticação](#-autenticação)
- [Machine Learning](#-machine-learning)
- [Monitoramento](#-monitoramento)
- [Testes](#-testes)
- [Deploy](#-deploy)
- [Documentação Adicional](#-documentação-adicional)

---

## 🎯 Sobre o Projeto

A **Books Scraper API** é uma aplicação completa de nível profissional que demonstra as melhores práticas de desenvolvimento de APIs modernas em Python.

### Destaques

- ✅ **API REST** completa com FastAPI
- ✅ **Web Scraping** automatizado
- ✅ **Autenticação JWT** com refresh tokens
- ✅ **Machine Learning** endpoints prontos para modelos
- ✅ **Logs estruturados** em JSON
- ✅ **Métricas em tempo real** de performance
- ✅ **Testes automatizados** (50+ testes)
- ✅ **Documentação interativa** Swagger/ReDoc
- ✅ **Dashboard de monitoramento**
- ✅ **Cache inteligente**
- ✅ **CORS habilitado**
- ✅ **Docker ready**

---

## ✨ Funcionalidades

### 📖 Gerenciamento de Livros
- Listar todos os livros com paginação
- Buscar livro por ID
- Busca avançada (título, categoria, rating, preço)
- Top livros melhor avaliados
- Filtro por faixa de preço
- Listar categorias

### 📊 Estatísticas
- Visão geral da coleção
- Estatísticas por categoria
- Distribuição de preços e ratings
- Análises detalhadas

### 🔐 Autenticação & Segurança
- Login com JWT
- Refresh token automático
- Controle de acesso por roles (admin/user)
- Rotas protegidas

### 🤖 Machine Learning
- Features formatadas para ML
- Dataset para treinamento
- Endpoint de predições
- Pronto para integrar modelos

### 🕷️ Web Scraping
- Extração automatizada de dados
- Salvamento em Excel e CSV
- Trigger via API (apenas admin)
- Recarregamento sob demanda

### 📈 Monitoramento
- Logs estruturados em JSON
- Métricas de performance em tempo real
- Dashboard interativo
- Request ID para rastreamento
- Rotação automática de logs

---

## 🛠️ Tecnologias

### Backend
- **[Python 3.11+](https://www.python.org/)** - Linguagem
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI
- **[Pydantic](https://docs.pydantic.dev/)** - Validação de dados

### Autenticação
- **[Python-JOSE](https://python-jose.readthedocs.io/)** - JWT tokens
- **SHA256** - Hash de senhas

### Web Scraping
- **[Requests](https://requests.readthedocs.io/)** - HTTP requests
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** - Parser HTML

### Dados
- **[OpenPyXL](https://openpyxl.readthedocs.io/)** - Excel
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment

### Testes
- **[Pytest](https://docs.pytest.org/)** - Framework de testes
- **[TestClient](https://fastapi.tiangolo.com/tutorial/testing/)** - FastAPI testing

---

## 🏗️ Arquitetura

### Estrutura Simplificada e Profissional

```
books-scraper-api/
├── 📁 app/                          # Aplicação principal
│   ├── __init__.py
│   ├── main.py                      # API completa (todos os endpoints)
│   ├── config.py                    # Configurações centralizadas
│   ├── models.py                    # Modelos Pydantic
│   ├── auth.py                      # Autenticação JWT
│   ├── database.py                  # Acesso aos dados + cache
│   ├── middleware.py                # Logging e métricas (opcional)
│   └── logging_config.py            # Configuração de logs (opcional)
│
├── 📁 scraper/                      # Web Scraping
│   ├── __init__.py
│   └── scraper.py                   # Script de scraping
│
├── 📁 data/                         # Dados gerados
│   ├── books_data.xlsx              # Dados em Excel
│   └── books_data.csv               # Dados em CSV
│
├── 📁 logs/                         # Logs da aplicação
│   └── api.log                      # Logs estruturados em JSON
│
├── 📁 tests/                        # Testes automatizados
│   ├── __init__.py
│   └── test_api.py                  # 50+ testes unitários
│
├── 📄 .env                          # Variáveis de ambiente
├── 📄 .env.example                  # Exemplo de configuração
├── 📄 .gitignore                    # Git ignore
├── 📄 requirements.txt              # Dependências Python
├── 📄 requirements-dev.txt          # Dependências de desenvolvimento
├── 📄 pytest.ini                    # Configuração do Pytest
├── 📄 run.py                        # Script para iniciar API
├── 📄 dashboard.py                  # Dashboard de monitoramento
├── 📄 README.md                     # Este arquivo
├── 📄 TESTING.md                    # Guia de testes
├── 📄 MONITORING.md                 # Guia de monitoramento
└── 📄 ML_GUIDE.md                   # Guia de Machine Learning
```

---

## 📦 Instalação

### Pré-requisitos

- **Python 3.11 ou superior** ([Download](https://www.python.org/downloads/))
- **pip** (gerenciador de pacotes)

```bash
python --version  # Deve ser 3.11+
pip --version
```

### Passo a Passo

#### 1. Clone ou Baixe o Projeto

```bash
git clone https://github.com/seu-usuario/books-scraper-api.git
cd books-scraper-api
```

#### 2. Crie Ambiente Virtual

```bash
# Criar
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate
```

#### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

#### 4. Configure as Variáveis de Ambiente

```bash
# Copie o exemplo
cp .env.example .env

# Edite .env com suas configurações
```

**`.env` básico:**
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
SECRET_KEY=mude-esta-chave-em-producao
```

#### 5. Execute o Web Scraper (Primeira Vez)

```bash
python scraper/scraper.py
```

**Saída esperada:**
```
============================================================
🕷️  BOOKS TO SCRAPE - WEB SCRAPER
============================================================
📖 Páginas a extrair: 3
...
✅ PROCESSO CONCLUÍDO!
📊 Total de livros: 60
📁 Arquivos salvos em: data/
```

#### 6. Inicie a API

```bash
python run.py
```

**Saída esperada:**
```
✅ API iniciada com 60 livros
📚 Docs: http://localhost:8000/docs
📊 Metrics: http://localhost:8000/api/v1/metrics
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🎮 Uso

### Acessar a Documentação Interativa

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Testar um Endpoint

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Listar livros
curl http://localhost:8000/api/v1/books?limit=5

# Buscar livros
curl "http://localhost:8000/api/v1/books/search?title=light"
```

### Dashboard de Monitoramento

```bash
# Em outro terminal
python dashboard.py
```

---

## 📡 Endpoints da API

### 🔓 Públicos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Informações da API |
| `GET` | `/api/v1/health` | Status da API |
| `GET` | `/api/v1/books` | Lista livros (paginação) |
| `GET` | `/api/v1/books/{id}` | Busca por ID |
| `GET` | `/api/v1/books/search` | Busca com filtros |
| `GET` | `/api/v1/books/top-rated` | Melhor avaliados |
| `GET` | `/api/v1/books/price-range` | Filtro por preço |
| `GET` | `/api/v1/categories` | Lista categorias |
| `GET` | `/api/v1/stats/overview` | Estatísticas gerais |
| `GET` | `/api/v1/stats/categories` | Stats por categoria |

### 🔐 Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/auth/login` | Fazer login |
| `POST` | `/api/v1/auth/refresh` | Renovar token |

### 🤖 Machine Learning

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/ml/features` | Features para ML |
| `GET` | `/api/v1/ml/training-data` | Dataset de treino |
| `POST` | `/api/v1/ml/predictions` | Predição de rating |

### 👑 Admin (Requer Autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/scraping/trigger` | 🔒 Executar scraping |
| `POST` | `/api/v1/scraping/reload` | 🔒 Recarregar dados |

### 📊 Monitoramento

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/metrics` | Métricas de performance |
| `GET` | `/api/v1/logs/recent` | Logs recentes |

---

## 🔐 Autenticação

### Credenciais Padrão

| Usuário | Senha | Role | Acesso |
|---------|-------|------|--------|
| **admin** | admin123 | admin | Todas as rotas |
| **user** | user123 | user | Apenas leitura |

⚠️ **Altere em produção editando `app/auth.py`**

### Fluxo de Autenticação

**1. Fazer Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Resposta:**
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "eyJhbG...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**2. Usar Token:**
```bash
curl -X POST http://localhost:8000/api/v1/scraping/trigger \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**3. Renovar Token:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"SEU_REFRESH_TOKEN"}'
```

---

## 🤖 Machine Learning

### Obter Features

```bash
curl http://localhost:8000/api/v1/ml/features
```

**Uso com Python:**
```python
import requests
import pandas as pd

response = requests.get('http://localhost:8000/api/v1/ml/features').json()
df = pd.DataFrame(response['features'])
print(df.head())
```

### Treinar Modelo

```python
import requests
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Obter dados
response = requests.get('http://localhost:8000/api/v1/ml/training-data').json()
X = np.array(response['X'])
y = np.array(response['y'])

# Treinar
model = RandomForestClassifier()
model.fit(X, y)
```

### Fazer Predição

```bash
curl -X POST http://localhost:8000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Deep Learning",
    "preco": 45.00,
    "categoria": "Programming"
  }'
```

**Ver mais em:** [ML_GUIDE.md](ML_GUIDE.md)

---

## 📊 Monitoramento

### Métricas em Tempo Real

```bash
curl http://localhost:8000/api/v1/metrics
```

**Resposta:**
```json
{
  "total_requests": 1250,
  "error_rate": 1.2,
  "response_times": {
    "mean": 0.0856,
    "p95": 0.2145,
    "p99": 0.5678
  }
}
```

### Dashboard Interativo

```bash
python dashboard.py
```

### Logs Estruturados

Todos os logs em JSON:
```bash
tail -f logs/api.log | jq
```

**Ver mais em:** [MONITORING.md](MONITORING.md)

---

## 🧪 Testes

### Executar Todos os Testes

```bash
# Instalar dependências de teste
pip install -r requirements-dev.txt

# Executar testes
pytest

# Com cobertura
pytest --cov=app

# Relatório HTML
pytest --cov=app --cov-report=html
```

### Testes Disponíveis

- ✅ 50+ testes unitários
- ✅ Testes de integração
- ✅ Testes de autenticação
- ✅ Testes de ML
- ✅ Testes de performance

**Ver mais em:** [TESTING.md](TESTING.md)

---

## 🚀 Deploy

### Docker

```bash
# Build
docker build -t books-api .

# Run
docker run -d -p 8000:8000 books-api
```

### Heroku

```bash
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile
heroku create seu-app
git push heroku main
```

### Produção

```bash
# Com workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Com variáveis de ambiente
export DEBUG=False
export SECRET_KEY=sua-chave-forte
python run.py
```

---

## 📚 Documentação Adicional

### Guias Especializados

- **[TESTING.md](TESTING.md)** - Guia completo de testes
- **[MONITORING.md](MONITORING.md)** - Monitoramento e logs
- **[ML_GUIDE.md](ML_GUIDE.md)** - Machine Learning

### Exemplos Práticos

#### Exemplo 1: Dashboard Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Estatísticas gerais
stats = requests.get(f"{BASE_URL}/stats/overview").json()
print(f"Total de livros: {stats['total_livros']}")
print(f"Preço médio: £{stats['preco_medio']}")

# Top 5 livros
top_books = requests.get(f"{BASE_URL}/books/top-rated?limit=5").json()
for i, book in enumerate(top_books, 1):
    print(f"{i}. {book['titulo']} - {'⭐' * book['rating']}")
```

#### Exemplo 2: Integração com Frontend

```javascript
// React/Vue/Angular
const API_URL = 'http://localhost:8000/api/v1';

// Buscar livros
async function searchBooks(query) {
  const response = await fetch(`${API_URL}/books/search?title=${query}`);
  return await response.json();
}

// Fazer predição
async function predictRating(book) {
  const response = await fetch(`${API_URL}/ml/predictions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(book)
  });
  return await response.json();
}
```

---

## 🔧 Troubleshooting

### Erro: "Data file not found"

```bash
# Execute o scraper primeiro
python scraper/scraper.py
```

### Erro: "Port already in use"

```bash
# Mude a porta no .env
API_PORT=8001
```

### Erro: "Module not found"

```bash
# Reinstale dependências
pip install -r requirements.txt
```

### API não responde

```bash
# Verifique se está rodando
curl http://localhost:8000/api/v1/health

# Veja os logs
tail -f logs/api.log
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit (`git commit -m 'Add: nova feature'`)
4. Push (`git push origin feature/nova-feature`)
5. Pull Request

---

## 📈 Métricas do Projeto

| Métrica | Valor |
|---------|-------|
| Linhas de código | ~3000 |
| Testes | 50+ |
| Cobertura | 85%+ |
| Endpoints | 20+ |
| Documentação | 100% |

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Projeto POSTECH - Tech Challenge**

---

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework incrível
- [Books to Scrape](https://books.toscrape.com/) - Site para scraping
- [POSTECH](https://postech.fiap.com.br/) - Oportunidade de aprendizado

---

## 📞 Suporte

- 📖 Documentação: http://localhost:8000/docs
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/books-scraper-api/issues)
- 💬 Discussões: [GitHub Discussions](https://github.com/seu-usuario/books-scraper-api/discussions)

---

<div align="center">

**⭐ Se este projeto te ajudou, considere dar uma estrela!**

**Made with ❤️ and ☕**

[🔝 Voltar ao topo](#-books-scraper-api---completa)

</div>