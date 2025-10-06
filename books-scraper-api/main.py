"""
Main Application Entry Point for Render
========================================
Este arquivo resolve o problema de ModuleNotFoundError
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao Python path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Importar a aplicação FastAPI
from app.main import app

# Exportar para uvicorn
__all__ = ['app']

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    
    print("="*60)
    print(f"🚀 Starting Books Scraper API")
    print(f"📡 Host: 0.0.0.0:{port}")
    print(f"📖 Docs: http://0.0.0.0:{port}/docs")
    print("="*60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
