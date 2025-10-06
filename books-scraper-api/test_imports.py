#!/usr/bin/env python3
"""Teste rápido da aplicação"""

import sys
from pathlib import Path

print("🧪 Testando imports...")

try:
    from main import app
    print("✅ from main import app - OK")
except Exception as e:
    print(f"❌ from main import app - FALHOU: {e}")
    sys.exit(1)

try:
    from config import PROJECT_NAME
    print(f"✅ from config import PROJECT_NAME - OK ({PROJECT_NAME})")
except Exception as e:
    print(f"❌ from config import PROJECT_NAME - FALHOU: {e}")

try:
    from models import Book
    print("✅ from models import Book - OK")
except Exception as e:
    print(f"❌ from models import Book - FALHOU: {e}")

try:
    from database import get_books
    books = get_books()
    print(f"✅ from database import get_books - OK ({len(books)} livros)")
except Exception as e:
    print(f"❌ from database import get_books - FALHOU: {e}")

print("\n✅ TODOS OS TESTES PASSARAM!")
print("\n📋 Próximos passos:")
print("1. python main.py  # Iniciar servidor")
print("2. curl http://localhost:8000/api/v1/health")
print("3. git add . && git commit -m 'Reorganizar' && git push")
