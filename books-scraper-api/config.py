"""
Configurações da Aplicação
===========================

"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

# ==================== DIRETÓRIOS ====================

# Diretório base do projeto (raiz)
BASE_DIR = Path(__file__).parent

# Diretório de dados
DATA_DIR = BASE_DIR / "data"

# Diretório de logs
LOGS_DIR = BASE_DIR / "logs"

# Cria diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


# ==================== API ====================

# Configurações do servidor
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Informações da API
PROJECT_NAME = "Books Scraper API"
VERSION = "1.0.0"
DESCRIPTION = "API RESTful para consultar livros com autenticação JWT"

# Prefixo da API
API_V1_PREFIX = "/api/v1"


# ==================== SEGURANÇA ====================

# Chave secreta para JWT (MUDE EM PRODUÇÃO!)
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key-in-production-use-a-random-string"
)

# Algoritmo de criptografia JWT
ALGORITHM = "HS256"

# Tempo de expiração dos tokens
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


# ==================== DADOS ====================

# Arquivo de dados Excel
DATA_FILE = DATA_DIR / "books_data.xlsx"

# Arquivo de dados CSV (opcional)
CSV_FILE = DATA_DIR / "books_data.csv"

# Tempo de cache em segundos (10 minutos)
CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT_SECONDS", 600))


# ==================== WEB SCRAPING ====================

# URL alvo para scraping
SCRAPER_URL = os.getenv("SCRAPER_TARGET_URL", "https://books.toscrape.com/")

# Número máximo de páginas para scraping
SCRAPER_MAX_PAGES = int(os.getenv("SCRAPER_MAX_PAGES", 50))

# Delay entre requisições (segundos)
SCRAPER_DELAY = float(os.getenv("SCRAPER_DELAY", 0.5))

# User-Agent para requisições
SCRAPER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Timeout para requisições (segundos)
SCRAPER_TIMEOUT = int(os.getenv("SCRAPER_TIMEOUT", 10))

# Caminho do script do scraper
SCRAPER_SCRIPT = BASE_DIR / "scraper" / "scraper.py"


# ==================== CORS ====================

# Origens permitidas para CORS
# Em produção, especifique domínios específicos
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

# Em desenvolvimento, permite todas as origens
if DEBUG:
    ALLOWED_ORIGINS = ["*"]


# ==================== LOGGING ====================

# Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Formato do log
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Arquivo de log
LOG_FILE = LOGS_DIR / "app.log"


# ==================== PAGINAÇÃO ====================

# Limite padrão de resultados
DEFAULT_PAGE_LIMIT = 100

# Limite máximo de resultados por página
MAX_PAGE_LIMIT = 1000


# ==================== VALIDAÇÕES ====================

def validate_config():
    """
    Valida as configurações críticas
    Levanta exceções se houver problemas
    """
    errors = []
    
    # Valida SECRET_KEY em produção
    if not DEBUG and SECRET_KEY == "change-this-secret-key-in-production-use-a-random-string":
        errors.append("⚠️  SECRET_KEY padrão detectada! Altere em produção!")
    
    # Valida diretório de dados
    if not DATA_DIR.exists():
        errors.append(f"⚠️  Diretório de dados não existe: {DATA_DIR}")
    
    # Valida arquivo de dados
    if not DATA_FILE.exists():
        print(f"⚠️  Arquivo de dados não encontrado: {DATA_FILE}")
        print("💡 Execute o scraper primeiro: python scraper/scraper.py")
    
    # Exibe avisos
    if errors:
        print("\n" + "="*60)
        print("⚠️  AVISOS DE CONFIGURAÇÃO:")
        for error in errors:
            print(f"   {error}")
        print("="*60 + "\n")


# ==================== INFORMAÇÕES DO SISTEMA ====================

def get_system_info() -> dict:
    """
    Retorna informações sobre a configuração atual
    Útil para debugging
    """
    return {
        "project_name": PROJECT_NAME,
        "version": VERSION,
        "debug": DEBUG,
        "api_host": API_HOST,
        "api_port": API_PORT,
        "data_file": str(DATA_FILE),
        "data_file_exists": DATA_FILE.exists(),
        "cache_timeout": CACHE_TIMEOUT,
        "log_level": LOG_LEVEL,
    }


# Executa validação ao importar
validate_config()


# ==================== EXPORTAÇÃO ====================

__all__ = [
    # Diretórios
    "BASE_DIR",
    "DATA_DIR",
    "LOGS_DIR",
    
    # API
    "API_HOST",
    "API_PORT",
    "DEBUG",
    "PROJECT_NAME",
    "VERSION",
    "DESCRIPTION",
    "API_V1_PREFIX",
    
    # Segurança
    "SECRET_KEY",
    "ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS",
    
    # Dados
    "DATA_FILE",
    "CSV_FILE",
    "CACHE_TIMEOUT",
    
    # Scraper
    "SCRAPER_URL",
    "SCRAPER_MAX_PAGES",
    "SCRAPER_DELAY",
    "SCRAPER_USER_AGENT",
    "SCRAPER_TIMEOUT",
    "SCRAPER_SCRIPT",
    
    # CORS
    "ALLOWED_ORIGINS",
    
    # Logging
    "LOG_LEVEL",
    "LOG_FORMAT",
    "LOG_FILE",
    
    # Paginação
    "DEFAULT_PAGE_LIMIT",
    "MAX_PAGE_LIMIT",
    
    # Funções
    "validate_config",
    "get_system_info",
]