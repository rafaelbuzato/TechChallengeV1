"""
Server Entry Point for Render
==============================
Este arquivo resolve o ModuleNotFoundError definitivamente
"""

import sys
import os
from pathlib import Path

# CRÍTICO: Adicionar diretório raiz ao Python path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

print("="*70)
print("🚀 Books Scraper API - Starting on Render")
print("="*70)
print(f"📁 Project root: {project_root}")
print(f"🐍 Python version: {sys.version}")
print(f"📍 Current dir: {os.getcwd()}")
print(f"🔧 PYTHONPATH: {sys.path[0]}")
print("="*70)

# Verificar se app/ existe
app_dir = project_root / "app"
if not app_dir.exists():
    print(f"❌ ERROR: Directory 'app/' not found at {app_dir}")
    sys.exit(1)

# Verificar __init__.py
app_init = app_dir / "__init__.py"
if not app_init.exists():
    print(f"⚠️  Creating app/__init__.py...")
    app_init.write_text('"""Books Scraper API"""\n')

scraper_init = project_root / "scraper" / "__init__.py"
if scraper_init.parent.exists() and not scraper_init.exists():
    print(f"⚠️  Creating scraper/__init__.py...")
    scraper_init.write_text('"""Web Scraper"""\n')

# Importar a aplicação FastAPI
try:
    print("📦 Importing FastAPI app...")
    from app.main import app
    print("✅ App imported successfully!")
except Exception as e:
    print(f"❌ FAILED to import app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Executar apenas quando chamado diretamente
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🌐 Starting server on {host}:{port}")
    print(f"📖 Docs will be available at: http://{host}:{port}/docs")
    print("="*70)
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )