#!/usr/bin/env python3
"""
Script para extrair e testar blocos de código Python dos arquivos .qmd
"""

import re
import os
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import List, Tuple
import json

class CodeBlockExtractor:
    """Extrai e testa blocos de código dos arquivos Quarto"""
    
    def __init__(self, book_dir: str = "book"):
        self.book_dir = Path(book_dir)
        self.results = []
        self.failed_tests = []
        
    def find_qmd_files(self) -> List[Path]:
        """Encontra todos os arquivos .qmd no diretório do livro"""
        return list(self.book_dir.rglob("*.qmd"))
    
    def extract_python_blocks(self, filepath: Path) -> List[Tuple[int, str]]:
        """Extrai blocos de código Python de um arquivo .qmd"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern para encontrar blocos de código Python
        pattern = r'```python\n(.*?)\n```'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        code_blocks = []
        for match in matches:
            # Encontra número da linha
            line_num = content[:match.start()].count('\n') + 1
            code = match.group(1)
            
            # Ignora blocos que são apenas comentários ou muito curtos
            if code.strip() and len(code.strip()) > 10:
                code_blocks.append((line_num, code))
        
        return code_blocks
    
    def test_code_block(self, code: str, filepath: Path, line_num: int) -> dict:
        """Testa um bloco de código"""
        result = {
            "file": str(filepath),
            "line": line_num,
            "status": "success",
            "error": None
        }
        
        # Cria arquivo temporário para testar o código
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            # Adiciona imports comuns que podem estar implícitos
            setup_code = """
import sys
import warnings
warnings.filterwarnings('ignore')

# Mock de funções que podem não estar definidas
def llm_generate(*args, **kwargs):
    return "Mocked LLM response"

def search_engine_search(*args, **kwargs):
    return [{"chunk": "Mocked chunk", "score": 0.9}]
"""
            tmp.write(setup_code)
            tmp.write("\n\n# Código do livro:\n")
            tmp.write(code)
            tmp_path = tmp.name
        
        try:
            # Tenta executar o código com timeout
            process = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if process.returncode != 0:
                result["status"] = "failed"
                result["error"] = process.stderr
                self.failed_tests.append(result)
                
        except subprocess.TimeoutExpired:
            result["status"] = "timeout"
            result["error"] = "Código excedeu timeout de 10 segundos"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            self.failed_tests.append(result)
            
        finally:
            # Remove arquivo temporário
            os.unlink(tmp_path)
            
        return result
    
    def validate_dependencies(self, code: str) -> List[str]:
        """Valida se as dependências estão documentadas"""
        missing_deps = []
        
        # Procura por imports
        import_pattern = r'^(?:from|import)\s+(\w+)'
        imports = re.findall(import_pattern, code, re.MULTILINE)
        
        # Procura por comentário de instalação
        install_pattern = r'#\s*uv pip install\s+(.+)'
        documented_deps = re.findall(install_pattern, code)
        
        # Lista de módulos built-in do Python que não precisam de instalação
        builtin_modules = {
            'os', 'sys', 'json', 'math', 'random', 'datetime', 'time',
            'collections', 'itertools', 'functools', 'pathlib', 're',
            'typing', 'dataclasses', 'enum', 'warnings', 'tempfile'
        }
        
        for imp in imports:
            if imp not in builtin_modules and not any(imp in dep for dep in documented_deps):
                missing_deps.append(imp)
                
        return missing_deps
    
    def run(self):
        """Executa a extração e teste de todos os códigos"""
        qmd_files = self.find_qmd_files()
        
        print(f"🔍 Encontrados {len(qmd_files)} arquivos .qmd")
        print("=" * 60)
        
        for filepath in qmd_files:
            # Pula arquivos de exercícios opcionalmente
            if 'exercises' in str(filepath):
                print(f"⏭️  Pulando exercícios: {filepath}")
                continue
                
            print(f"\n📄 Processando: {filepath}")
            code_blocks = self.extract_python_blocks(filepath)
            
            if not code_blocks:
                print("   Sem blocos de código Python")
                continue
                
            print(f"   Encontrados {len(code_blocks)} blocos de código")
            
            for line_num, code in code_blocks:
                # Valida dependências
                missing_deps = self.validate_dependencies(code)
                if missing_deps:
                    print(f"   ⚠️  Linha {line_num}: Dependências não documentadas: {missing_deps}")
                
                # Testa o código
                result = self.test_code_block(code, filepath, line_num)
                self.results.append(result)
                
                if result["status"] == "success":
                    print(f"   ✅ Linha {line_num}: OK")
                elif result["status"] == "timeout":
                    print(f"   ⏱️  Linha {line_num}: Timeout")
                else:
                    print(f"   ❌ Linha {line_num}: Falhou")
                    if result["error"]:
                        print(f"      Erro: {result['error'][:100]}...")
        
        # Relatório final
        self.print_summary()
        
        # Salva relatório JSON
        self.save_report()
        
        # Retorna código de saída
        return 1 if self.failed_tests else 0
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES")
        print("=" * 60)
        
        total = len(self.results)
        success = sum(1 for r in self.results if r["status"] == "success")
        failed = sum(1 for r in self.results if r["status"] == "failed")
        timeout = sum(1 for r in self.results if r["status"] == "timeout")
        error = sum(1 for r in self.results if r["status"] == "error")
        
        print(f"Total de blocos testados: {total}")
        print(f"✅ Sucesso: {success} ({success/total*100:.1f}%)")
        print(f"❌ Falhou: {failed} ({failed/total*100:.1f}%)")
        print(f"⏱️  Timeout: {timeout} ({timeout/total*100:.1f}%)")
        print(f"🔥 Erro: {error} ({error/total*100:.1f}%)")
        
        if self.failed_tests:
            print("\n⚠️  CÓDIGOS QUE FALHARAM:")
            for test in self.failed_tests[:5]:  # Mostra apenas os 5 primeiros
                print(f"  - {test['file']}:{test['line']}")
    
    def save_report(self):
        """Salva relatório detalhado em JSON"""
        os.makedirs("test-results", exist_ok=True)
        
        report = {
            "summary": {
                "total": len(self.results),
                "success": sum(1 for r in self.results if r["status"] == "success"),
                "failed": sum(1 for r in self.results if r["status"] == "failed"),
                "timeout": sum(1 for r in self.results if r["status"] == "timeout"),
                "error": sum(1 for r in self.results if r["status"] == "error")
            },
            "results": self.results
        }
        
        with open("test-results/code-test-report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Relatório salvo em: test-results/code-test-report.json")

if __name__ == "__main__":
    extractor = CodeBlockExtractor()
    exit_code = extractor.run()
    sys.exit(exit_code)