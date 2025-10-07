# server.py
"""
Server Entry Point for Render
==============================
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao Python path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

print("="*70)
print("🚀 Books Scraper API - Starting on Render")
print("="*70)
print(f"📁 Project root: {project_root}")
print(f"🐍 Python version: {sys.version}")
print(f"📍 Current dir: {os.getcwd()}")
print("="*70)

# Verificar se app/ existe
app_dir = project_root / "app"
if not app_dir.exists():
    print(f"❌ ERROR: Directory 'app/' not found")
    sys.exit(1)

# Criar __init__.py se não existir
app_init = app_dir / "__init__.py"
if not app_init.exists():
    app_init.write_text('"""Books Scraper API"""\n')
    print("✅ Created app/__init__.py")

scraper_dir = project_root / "scraper"
if scraper_dir.exists():
    scraper_init = scraper_dir / "__init__.py"
    if not scraper_init.exists():
        scraper_init.write_text('"""Web Scraper"""\n')
        print("✅ Created scraper/__init__.py")

# Importar a aplicação
try:
    print("📦 Importing app...")
    from app.main import app
    print("✅ App imported successfully!")
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Executar servidor
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🌐 Starting server on 0.0.0.0:{port}")
    print("="*70)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )