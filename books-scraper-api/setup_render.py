#!/usr/bin/env python3
"""
Script para preparar projeto para deploy no Render
===================================================
Cria todos os arquivos necessários automaticamente

Uso:
    python setup_render.py
"""

import os
from pathlib import Path


def create_file(filepath, content):
    """Cria arquivo com conteúdo"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Criado: {filepath}")


def main():
    print("="*60)
    print("🚀 CONFIGURANDO PROJETO PARA RENDER")
    print("="*60)
    print()
    
    # 1. render.yaml
    render_yaml = """services:
  - type: web
    name: books-scraper-api
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
      python scraper/scraper.py
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /api/v1/health
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.7
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
      - key: API_HOST
        value: 0.0.0.0
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30
      - key: REFRESH_TOKEN_EXPIRE_DAYS
        value: 7
      - key: RENDER
        value: true
"""
    create_file("render.yaml", render_yaml)
    
    # 2. build.sh
    build_sh = """#!/usr/bin/env bash
# Build script para Render
set -o errexit

echo "🔧 Iniciando build..."

# Atualizar pip
echo "📦 Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p data
mkdir -p logs

# Executar scraper para gerar dados iniciais
echo "🕷️  Executando web scraper..."
python scraper/scraper.py

# Verificar se dados foram gerados
if [ -f "data/books_data.xlsx" ]; then
    echo "✅ Dados gerados com sucesso!"
    ls -lh data/
else
    echo "⚠️  Aviso: Arquivo de dados não encontrado"
fi

echo "✅ Build concluído com sucesso!"
"""
    create_file("build.sh", build_sh)
    
    # Tornar executável
    os.chmod("build.sh", 0o755)
    print("  🔒 Permissões de execução definidas")
    
    # 3. Procfile
    procfile = "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT\n"
    create_file("Procfile", procfile)
    
    # 4. runtime.txt
    runtime = "python-3.11.7\n"
    create_file("runtime.txt", runtime)
    
    # 5. .gitkeep para data e logs
    create_file("data/.gitkeep", "")
    create_file("logs/.gitkeep", "")
    
    # 6. Atualizar requirements.txt
    requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
openpyxl==3.1.2
requests==2.31.0
beautifulsoup4==4.12.2
python-dotenv==1.0.0
pydantic==2.5.0
lxml==5.1.0
"""
    create_file("requirements.txt", requirements)
    
    # 7. .env.example (atualizado)
    env_example = """# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=mude-esta-chave-em-producao

# JWT Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Render Specific (set by Render automatically)
# PORT=10000
# RENDER=true
"""
    create_file(".env.example", env_example)
    
    print()
    print("="*60)
    print("✅ ARQUIVOS CRIADOS COM SUCESSO!")
    print("="*60)
    print()
    print("📝 PRÓXIMOS PASSOS:")
    print()
    print("1. Modifique o código (ver instruções abaixo)")
    print("2. Commit e push:")
    print("   git add .")
    print("   git commit -m 'Deploy: Configuração para Render'")
    print("   git push origin main")
    print()
    print("3. No Render:")
    print("   - New → Web Service")
    print("   - Conectar repositório")
    print("   - Render detecta render.yaml automaticamente")
    print("   - Clicar 'Apply'")
    print()
    print("="*60)
    print("⚠️  MODIFICAÇÕES NECESSÁRIAS NO CÓDIGO:")
    print("="*60)
    print()
    
    print("📄 app/main.py (final do arquivo):")
    print("-" * 60)
    print("""
Encontre: if __name__ == "__main__":

Substitua por:

if __name__ == "__main__":
    import uvicorn
    import os
    from app.config import DEBUG
    
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=DEBUG
    )
""")
    
    print()
    print("📄 app/config.py:")
    print("-" * 60)
    print("""
Adicione no final da seção API:

# Detecta se está rodando no Render
IS_RENDER = os.getenv("RENDER", "False").lower() == "true"

# Porta dinâmica para Render
if IS_RENDER:
    API_PORT = int(os.getenv("PORT", 10000))
""")
    
    print()
    print("="*60)
    print("🎉 CONFIGURAÇÃO COMPLETA!")
    print("="*60)
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Erro: {e}")
        exit(1)