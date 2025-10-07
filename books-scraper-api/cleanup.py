#!/usr/bin/env python3
"""
Script de Limpeza do Projeto Books Scraper API
================================================
Remove arquivos duplicados e organiza a estrutura do projeto.

Uso:
    python cleanup.py           # Modo simulação (dry-run)
    python cleanup.py --execute # Executa a limpeza de verdade
"""

import os
import shutil
import sys
from pathlib import Path
from typing import List, Tuple


class ProjectCleaner:
    """Limpa e organiza o projeto"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.project_root = Path(__file__).parent
        self.removed_count = 0
        self.errors = []
        
    def print_header(self):
        """Imprime cabeçalho"""
        print("\n" + "="*70)
        print("🧹 BOOKS SCRAPER API - SCRIPT DE LIMPEZA")
        print("="*70)
        
        if self.dry_run:
            print("⚠️  MODO SIMULAÇÃO - Nenhum arquivo será deletado")
            print("   Execute com --execute para aplicar as mudanças")
        else:
            print("🔴 MODO EXECUÇÃO - Arquivos SERÃO deletados!")
            print("   Certifique-se de ter backup se necessário")
        
        print("="*70 + "\n")
    
    def confirm_execution(self) -> bool:
        """Solicita confirmação do usuário"""
        if self.dry_run:
            return True
            
        print("⚠️  ATENÇÃO: Esta operação vai DELETAR arquivos permanentemente!")
        print("   Tem certeza que deseja continuar?")
        
        response = input("\n   Digite 'SIM' para confirmar: ").strip()
        
        if response != "SIM":
            print("\n❌ Operação cancelada pelo usuário.")
            return False
        
        print("\n✅ Confirmado. Iniciando limpeza...\n")
        return True
    
    def remove_directory(self, path: Path) -> bool:
        """Remove um diretório"""
        try:
            if not path.exists():
                print(f"   ⏭️  Não existe: {path}")
                return True
            
            if self.dry_run:
                print(f"   🗑️  Seria removido: {path}/")
            else:
                shutil.rmtree(path)
                print(f"   ✅ Removido: {path}/")
            
            self.removed_count += 1
            return True
            
        except Exception as e:
            error_msg = f"Erro ao remover {path}: {e}"
            self.errors.append(error_msg)
            print(f"   ❌ {error_msg}")
            return False
    
    def remove_file(self, path: Path) -> bool:
        """Remove um arquivo"""
        try:
            if not path.exists():
                print(f"   ⏭️  Não existe: {path}")
                return True
            
            if self.dry_run:
                print(f"   🗑️  Seria removido: {path}")
            else:
                path.unlink()
                print(f"   ✅ Removido: {path}")
            
            self.removed_count += 1
            return True
            
        except Exception as e:
            error_msg = f"Erro ao remover {path}: {e}"
            self.errors.append(error_msg)
            print(f"   ❌ {error_msg}")
            return False
    
    def create_gitignore(self) -> bool:
        """Cria novo arquivo .gitignore"""
        gitignore_content = """# ========================================
# Books Scraper API - .gitignore
# ========================================

# ==================== PYTHON ====================

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Virtual environments
env/
venv/
ENV/
env.bak/
venv.bak/

# ==================== LOGS ====================

logs/*.log
*.log
*.log.*

# ==================== DADOS TEMPORÁRIOS ====================

*.tmp
*.bak
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# ==================== AMBIENTE ====================

.env
.env.local
.env.*.local

# ==================== IDE ====================

# VSCode
.vscode/
*.code-workspace

# PyCharm
.idea/
*.iml
*.iws
.idea_modules/

# Sublime Text
*.sublime-project
*.sublime-workspace

# Vim
[._]*.s[a-v][a-z]
[._]*.sw[a-p]
[._]s[a-rt-v][a-z]
[._]ss[a-gi-z]
[._]sw[a-p]

# ==================== SISTEMA OPERACIONAL ====================

# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon
._*

# Windows
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db
[Dd]esktop.ini
$RECYCLE.BIN/
*.lnk

# Linux
*~
.directory
.Trash-*

# ==================== DIVERSOS ====================

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Celery
celerybeat-schedule
celerybeat.pid

# mkdocs
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre
.pyre/
"""
        
        gitignore_path = self.project_root / ".gitignore"
        
        try:
            if self.dry_run:
                print(f"   📝 Seria criado/atualizado: .gitignore")
            else:
                with open(gitignore_path, 'w', encoding='utf-8') as f:
                    f.write(gitignore_content)
                print(f"   ✅ Criado/atualizado: .gitignore")
            
            return True
            
        except Exception as e:
            error_msg = f"Erro ao criar .gitignore: {e}"
            self.errors.append(error_msg)
            print(f"   ❌ {error_msg}")
            return False
    
    def clean_directories(self):
        """Remove diretórios duplicados"""
        print("📁 Removendo diretórios duplicados:")
        print("-" * 70)
        
        directories_to_remove = [
            "app_backup"
        ]
        
        for dir_name in directories_to_remove:
            dir_path = self.project_root / dir_name
            self.remove_directory(dir_path)
        
        print()
    
    def clean_duplicate_files(self):
        """Remove arquivos duplicados da raiz"""
        print("📄 Removendo arquivos duplicados da raiz:")
        print("-" * 70)
        
        duplicate_files = [
            "auth.py",
            "config.py",
            "database.py",
            "main.py",
            "models.py",
            "middleware.py",
            "logging_config.py"
        ]
        
        for filename in duplicate_files:
            file_path = self.project_root / filename
            self.remove_file(file_path)
        
        print()
    
    def clean_temp_files(self):
        """Remove arquivos temporários"""
        print("🗑️  Removendo arquivos temporários:")
        print("-" * 70)
        
        temp_files = [
            "test_imports.py"
        ]
        
        for filename in temp_files:
            file_path = self.project_root / filename
            self.remove_file(file_path)
        
        print()
    
    def update_gitignore(self):
        """Atualiza arquivo .gitignore"""
        print("📝 Atualizando .gitignore:")
        print("-" * 70)
        
        self.create_gitignore()
        
        print()
    
    def verify_structure(self):
        """Verifica se a estrutura final está correta"""
        print("🔍 Verificando estrutura final:")
        print("-" * 70)
        
        required_dirs = [
            "app",
            "scraper",
            "data",
            "logs",
            "tests"
        ]
        
        required_files = [
            "app/__init__.py",
            "app/main.py",
            "app/config.py",
            "app/models.py",
            "app/auth.py",
            "app/database.py",
            "scraper/__init__.py",
            "scraper/scraper.py",
            "tests/__init__.py",
            "tests/test_api.py",
            "requirements.txt",
            "README.md",
            "run.py",
            "server.py"
        ]
        
        all_ok = True
        
        # Verificar diretórios
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                print(f"   ✅ Diretório OK: {dir_name}/")
            else:
                print(f"   ❌ Diretório ausente: {dir_name}/")
                all_ok = False
        
        # Verificar arquivos
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists() and full_path.is_file():
                print(f"   ✅ Arquivo OK: {file_path}")
            else:
                print(f"   ⚠️  Arquivo ausente: {file_path}")
                # Alguns arquivos podem não existir, não é erro crítico
        
        print()
        return all_ok
    
    def test_imports(self):
        """Testa se os imports funcionam"""
        print("🧪 Testando imports:")
        print("-" * 70)
        
        if self.dry_run:
            print("   ⏭️  Pulando testes (modo simulação)")
            print()
            return True
        
        try:
            # Adiciona diretório raiz ao path
            sys.path.insert(0, str(self.project_root))
            
            # Testa import principal
            from app.main import app
            print("   ✅ from app.main import app")
            
            from app.config import PROJECT_NAME
            print(f"   ✅ from app.config import PROJECT_NAME ({PROJECT_NAME})")
            
            from app.models import Book
            print("   ✅ from app.models import Book")
            
            from app.database import get_books
            print("   ✅ from app.database import get_books")
            
            print("\n   🎉 Todos os imports funcionam!")
            print()
            return True
            
        except Exception as e:
            print(f"   ❌ Erro nos imports: {e}")
            print()
            return False
    
    def print_summary(self):
        """Imprime resumo da operação"""
        print("\n" + "="*70)
        print("📊 RESUMO DA LIMPEZA")
        print("="*70)
        
        if self.dry_run:
            print(f"🔍 Modo Simulação: {self.removed_count} itens seriam removidos")
        else:
            print(f"✅ Modo Execução: {self.removed_count} itens removidos")
        
        if self.errors:
            print(f"\n❌ Erros encontrados: {len(self.errors)}")
            for error in self.errors:
                print(f"   • {error}")
        else:
            print("\n✅ Nenhum erro encontrado")
        
        print("\n" + "="*70)
        
        if self.dry_run:
            print("\n💡 Para executar a limpeza de verdade:")
            print("   python cleanup.py --execute")
        else:
            print("\n🎉 Limpeza concluída com sucesso!")
            print("\n📋 Próximos passos:")
            print("   1. Verificar se tudo está funcionando:")
            print("      python run.py")
            print("   2. Fazer commit das mudanças:")
            print("      git add .")
            print('      git commit -m "Simplificar estrutura do projeto"')
            print("      git push")
        
        print()
    
    def run(self):
        """Executa a limpeza completa"""
        self.print_header()
        
        if not self.confirm_execution():
            return
        
        # Executar limpezas
        self.clean_directories()
        self.clean_duplicate_files()
        self.clean_temp_files()
        self.update_gitignore()
        
        # Verificações
        self.verify_structure()
        self.test_imports()
        
        # Resumo
        self.print_summary()


def main():
    """Função principal"""
    # Verifica argumentos
    execute = "--execute" in sys.argv or "-e" in sys.argv
    dry_run = not execute
    
    # Cria e executa cleaner
    cleaner = ProjectCleaner(dry_run=dry_run)
    cleaner.run()


if __name__ == "__main__":
    main()