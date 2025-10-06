#!/usr/bin/env bash
set -o errexit

echo "🔧 Build starting..."
echo "📁 Current directory: $(pwd)"

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Criar diretórios
mkdir -p data logs

# Garantir __init__.py
echo "📝 Creating __init__.py files..."
touch app/__init__.py
touch scraper/__init__.py

# Verificar estrutura
echo "📂 Project structure:"
ls -la

# Executar scraper
echo "🕷️  Running web scraper..."
python scraper/scraper.py

# Verificar dados
if [ -f "data/books_data.xlsx" ]; then
    echo "✅ Data generated successfully!"
    ls -lh data/
else
    echo "⚠️  Warning: Data file not found"
fi

echo "✅ Build complete!"
