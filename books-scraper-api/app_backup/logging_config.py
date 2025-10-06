"""
Configuração de Logging Estruturado
====================================
"""

import logging
import logging.handlers
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class JSONFormatter(logging.Formatter):
    """
    Formatter para logs em formato JSON estruturado
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Formata log em JSON"""
        
        # Dados base do log
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Adicionar campos extras se existirem
        if hasattr(record, "event"):
            log_data["event"] = record.event
        
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        
        # Adicionar todos os campos extras
        for key, value in record.__dict__.items():
            if key not in [
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "message", "pathname", "process", "processName",
                "relativeCreated", "thread", "threadName", "exc_info",
                "exc_text", "stack_info"
            ]:
                log_data[key] = value
        
        # Adicionar exception info se houver
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, default=str)


class ColoredFormatter(logging.Formatter):
    """
    Formatter com cores para console
    """
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        # Adicionar cor
        color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        
        # Formatar com cores
        return super().format(record)


def setup_logging(
    log_level: str = "INFO",
    log_file: str = "logs/api.log",
    json_logs: bool = True,
    console_logs: bool = True
):
    """
    Configura sistema de logging
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR)
        log_file: Caminho do arquivo de log
        json_logs: Se True, usa formato JSON
        console_logs: Se True, envia logs para console
    """
    
    # Criar diretório de logs
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remover handlers existentes
    root_logger.handlers = []
    
    # Handler para arquivo (JSON estruturado)
    if json_logs:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(JSONFormatter())
        file_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
    
    # Handler para console (colorido)
    if console_logs:
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        root_logger.addHandler(console_handler)
    
    # Configurar loggers específicos
    
    # Logger de requisições API
    api_logger = logging.getLogger("api.requests")
    api_logger.setLevel(logging.INFO)
    
    # Logger de autenticação
    auth_logger = logging.getLogger("api.auth")
    auth_logger.setLevel(logging.INFO)
    
    # Logger de ML
    ml_logger = logging.getLogger("api.ml")
    ml_logger.setLevel(logging.INFO)
    
    # Logger de database
    db_logger = logging.getLogger("api.database")
    db_logger.setLevel(logging.INFO)
    
    # Desabilitar logs muito verbosos
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    logging.info("Logging system configured")


def get_logger(name: str) -> logging.Logger:
    """
    Obtém logger configurado
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


class LoggerAdapter(logging.LoggerAdapter):
    """
    Adapter para adicionar contexto aos logs
    """
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Adiciona contexto extra aos logs"""
        
        # Adicionar contexto do adapter
        extra = kwargs.get("extra", {})
        extra.update(self.extra)
        kwargs["extra"] = extra
        
        return msg, kwargs


def get_request_logger(request_id: str) -> LoggerAdapter:
    """
    Cria logger com contexto de requisição
    
    Args:
        request_id: ID da requisição
        
    Returns:
        Logger com contexto
    """
    logger = logging.getLogger("api.requests")
    return LoggerAdapter(logger, {"request_id": request_id})
