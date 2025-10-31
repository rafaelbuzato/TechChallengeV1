"""
Script para iniciar a API
==========================
"""

import uvicorn
from app.config import API_HOST, API_PORT, DEBUG

if __name__ == "__main__":
    print("🚀 Iniciando Books Scraper API...")
    print(f"📡 Host: {API_HOST}:{API_PORT}")
    print(f"📖 Docs: http://{API_HOST}:{API_PORT}/docs")
    print("="*50)
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG
    )