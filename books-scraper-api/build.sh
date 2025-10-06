#!/usr/bin/env bash
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
