#!/usr/bin/env python3
"""
Script para extrair e validar blocos de código Python dos arquivos .qmd
Valida apenas a sintaxe, sem executar o código (evita problemas com dependências)
"""

import re
import os
import sys
import ast
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
        all_files = list(self.book_dir.rglob("*.qmd"))
        
        # Filtra arquivos do diretório _book (gerado pelo Quarto)
        filtered_files = [
            f for f in all_files 
            if '_book' not in str(f)
        ]
        
        return filtered_files
    
    def extract_python_blocks(self, filepath: Path) -> List[Tuple[int, str]]:
        """Extrai blocos de código Python de um arquivo .qmd"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Para arquivos de exercícios, testa todos os blocos
        is_exercise_file = 'exercises' in str(filepath)
        
        # Para capítulos normais, só testa blocos na seção "Exemplos Completos"
        if not is_exercise_file:
            # Procura pela seção de exemplos completos (várias variações possíveis)
            # Exemplos: "## Exemplos de Código Completos", "## Exemplos Completos de Código", etc.
            examples_pattern = r'##\s+Exemplos\s+(?:de\s+Código\s+)?(?:Completos|Completos\s+de\s+Código)\s*(?:\{[^}]*\})?\s*\n(.*)'
            examples_match = re.search(examples_pattern, content, re.IGNORECASE | re.DOTALL)
            
            if not examples_match:
                # Não encontrou seção de exemplos completos, não testa nenhum bloco
                return []
            
            # Extrai apenas a parte depois da seção de exemplos
            examples_content = examples_match.group(1)
            examples_start_pos = examples_match.start(1)
        else:
            examples_content = content
            examples_start_pos = 0
        
        # Pattern para encontrar blocos de código Python
        pattern = r'```python\n(.*?)\n```'
        matches = re.finditer(pattern, examples_content, re.DOTALL)
        
        code_blocks = []
        for match in matches:
            # Calcula número da linha no arquivo original
            line_num = content[:examples_start_pos + match.start()].count('\n') + 1
            code = match.group(1)
            
            # Ignora blocos que são apenas comentários ou muito curtos
            if code.strip() and len(code.strip()) > 10:
                code_blocks.append((line_num, code))
        
        return code_blocks
    
    def test_code_block(self, code: str, filepath: Path, line_num: int) -> dict:
        """Valida a sintaxe de um bloco de código"""
        result = {
            "file": str(filepath),
            "line": line_num,
            "status": "success",
            "error": None
        }
        
        try:
            # Valida apenas a sintaxe usando ast.parse
            # Não executa o código para evitar problemas com dependências
            ast.parse(code)
            
        except SyntaxError as e:
            result["status"] = "failed"
            result["error"] = f"Erro de sintaxe: {e.msg} (linha {e.lineno})"
            self.failed_tests.append(result)
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = f"Erro ao validar: {str(e)}"
            self.failed_tests.append(result)
            
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
        """Executa a extração e validação de todos os códigos"""
        qmd_files = self.find_qmd_files()
        
        print(f"🔍 Encontrados {len(qmd_files)} arquivos .qmd")
        print("=" * 60)
        
        for filepath in qmd_files:
            print(f"\n📄 Processando: {filepath}")
            code_blocks = self.extract_python_blocks(filepath)
            
            if not code_blocks:
                print("   Sem blocos de código para validar (não está na seção de exemplos)")
                continue
                
            print(f"   Encontrados {len(code_blocks)} blocos de código")
            
            for line_num, code in code_blocks:
                # Valida dependências
                missing_deps = self.validate_dependencies(code)
                if missing_deps:
                    print(f"   ⚠️  Linha {line_num}: Dependências não documentadas: {missing_deps}")
                
                # Valida sintaxe do código
                result = self.test_code_block(code, filepath, line_num)
                self.results.append(result)
                
                if result["status"] == "success":
                    print(f"   ✅ Linha {line_num}: Sintaxe OK")
                else:
                    print(f"   ❌ Linha {line_num}: Erro de sintaxe")
                    if result["error"]:
                        print(f"      {result['error'][:150]}...")
        
        # Relatório final
        self.print_summary()
        
        # Salva relatório JSON
        self.save_report()
        
        # Retorna código de saída
        return 1 if self.failed_tests else 0
    
    def print_summary(self):
        """Imprime resumo da validação"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DA VALIDAÇÃO")
        print("=" * 60)
        
        total = len(self.results)
        if total == 0:
            print("Nenhum bloco de código encontrado para validar")
            return
            
        success = sum(1 for r in self.results if r["status"] == "success")
        failed = sum(1 for r in self.results if r["status"] == "failed")
        error = sum(1 for r in self.results if r["status"] == "error")
        
        print(f"Total de blocos validados: {total}")
        print(f"✅ Sintaxe OK: {success} ({success/total*100:.1f}%)")
        print(f"❌ Erros de sintaxe: {failed} ({failed/total*100:.1f}%)")
        print(f"🔥 Erros de validação: {error} ({error/total*100:.1f}%)")
        
        if self.failed_tests:
            print(f"\n⚠️  CÓDIGOS COM ERROS DE SINTAXE ({len(self.failed_tests)}):")
            for test in self.failed_tests[:10]:  # Mostra apenas os 10 primeiros
                print(f"  - {test['file']}:{test['line']}")
                if test['error']:
                    print(f"    {test['error'][:100]}")
        
        print("\n💡 Nota: Este script valida apenas a sintaxe Python.")
        print("   Erros de imports ou execução são esperados e não impedem o uso do código.")
    
    def save_report(self):
        """Salva relatório detalhado em JSON"""
        os.makedirs("test-results", exist_ok=True)
        
        report = {
            "summary": {
                "total": len(self.results),
                "success": sum(1 for r in self.results if r["status"] == "success"),
                "failed": sum(1 for r in self.results if r["status"] == "failed"),
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