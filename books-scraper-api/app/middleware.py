"""
Middleware para Logging e Métricas
===================================
"""

import time
import json
from datetime import datetime
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

# Configurar logger estruturado
logger = logging.getLogger("api.requests")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging estruturado de todas as requisições
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Timestamp de início
        start_time = time.time()
        
        # ID único da requisição
        request_id = f"{int(time.time() * 1000)}-{id(request)}"
        
        # Informações da requisição
        request_info = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_host": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        }
        
        # Adicionar request_id ao state para uso posterior
        request.state.request_id = request_id
        
        # Log da requisição
        logger.info(
            "Request started",
            extra={
                "event": "request_started",
                **request_info
            }
        )
        
        # Processar requisição
        try:
            response = await call_next(request)
            
            # Calcular tempo de processamento
            process_time = time.time() - start_time
            
            # Informações da resposta
            response_info = {
                **request_info,
                "status_code": response.status_code,
                "process_time": round(process_time, 4),
            }
            
            # Log da resposta
            logger.info(
                f"{request.method} {request.url.path} - {response.status_code}",
                extra={
                    "event": "request_completed",
                    **response_info
                }
            )
            
            # Adicionar headers customizados
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Tempo até o erro
            process_time = time.time() - start_time
            
            # Log de erro
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "event": "request_failed",
                    **request_info,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "process_time": round(process_time, 4),
                },
                exc_info=True
            )
            
            raise


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware para coletar métricas de performance
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.metrics = {
            "total_requests": 0,
            "total_errors": 0,
            "requests_by_method": {},
            "requests_by_endpoint": {},
            "response_times": [],
            "status_codes": {},
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Incrementar total de requisições
        self.metrics["total_requests"] += 1
        
        # Contar por método
        method = request.method
        self.metrics["requests_by_method"][method] = \
            self.metrics["requests_by_method"].get(method, 0) + 1
        
        # Contar por endpoint
        endpoint = request.url.path
        self.metrics["requests_by_endpoint"][endpoint] = \
            self.metrics["requests_by_endpoint"].get(endpoint, 0) + 1
        
        try:
            response = await call_next(request)
            
            # Tempo de processamento
            process_time = time.time() - start_time
            
            # Armazenar tempo de resposta (últimos 1000)
            self.metrics["response_times"].append(process_time)
            if len(self.metrics["response_times"]) > 1000:
                self.metrics["response_times"].pop(0)
            
            # Contar status codes
            status = response.status_code
            self.metrics["status_codes"][status] = \
                self.metrics["status_codes"].get(status, 0) + 1
            
            return response
            
        except Exception as e:
            # Incrementar erros
            self.metrics["total_errors"] += 1
            
            # Log do erro
            logger.error(f"Metrics middleware error: {e}", exc_info=True)
            
            raise
    
    def get_metrics(self) -> dict:
        """Retorna métricas coletadas"""
        import statistics
        
        response_times = self.metrics["response_times"]
        
        return {
            "total_requests": self.metrics["total_requests"],
            "total_errors": self.metrics["total_errors"],
            "error_rate": round(
                (self.metrics["total_errors"] / max(self.metrics["total_requests"], 1)) * 100,
                2
            ),
            "requests_by_method": self.metrics["requests_by_method"],
            "requests_by_endpoint": dict(
                sorted(
                    self.metrics["requests_by_endpoint"].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]  # Top 10
            ),
            "status_codes": self.metrics["status_codes"],
            "response_times": {
                "count": len(response_times),
                "mean": round(statistics.mean(response_times), 4) if response_times else 0,
                "median": round(statistics.median(response_times), 4) if response_times else 0,
                "min": round(min(response_times), 4) if response_times else 0,
                "max": round(max(response_times), 4) if response_times else 0,
                "p95": round(
                    statistics.quantiles(response_times, n=20)[18], 4
                ) if len(response_times) > 1 else 0,
                "p99": round(
                    statistics.quantiles(response_times, n=100)[98], 4
                ) if len(response_times) > 1 else 0,
            }
        }


# Instância global de métricas
metrics_middleware_instance = None


def get_metrics_instance():
    """Retorna instância do middleware de métricas"""
    global metrics_middleware_instance
    return metrics_middleware_instance


def set_metrics_instance(instance):
    """Define instância do middleware de métricas"""
    global metrics_middleware_instance
    metrics_middleware_instance = instance