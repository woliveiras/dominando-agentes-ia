#!/usr/bin/env python3
"""
Script para verificar consistência entre citações no texto e referências
"""

import re
import sys
from pathlib import Path
from typing import Set, List, Dict

class CitationChecker:
    """Verifica consistência de citações"""
    
    def __init__(self, book_dir: str = "book", bib_file: str = "book/references.bib"):
        self.book_dir = Path(book_dir)
        self.bib_file = Path(bib_file)
        self.citations_in_text = set()
        self.references_in_bib = set()
        self.errors = []
        self.warnings = []
        
    def extract_citations_from_qmd(self, filepath: Path) -> Set[str]:
        """Extrai citações de um arquivo .qmd"""
        citations = set()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern para citações [@author2024] ou [@author2024; @other2023]
        pattern = r'@([a-zA-Z0-9_\-]+)'
        matches = re.findall(pattern, content)
        
        citations.update(matches)
        return citations
    
    def extract_references_from_bib(self) -> Set[str]:
        """Extrai IDs de referências do arquivo .bib"""
        references = set()
        
        if not self.bib_file.exists():
            self.errors.append(f"Arquivo bibliography não encontrado: {self.bib_file}")
            return references
        
        with open(self.bib_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern para entradas BibTeX @type{id,
        pattern = r'@\w+\{([^,]+),'
        matches = re.findall(pattern, content)
        
        references.update(matches)
        return references
    
    def find_all_citations(self) -> None:
        """Encontra todas as citações nos arquivos .qmd"""
        qmd_files = list(self.book_dir.rglob("*.qmd"))
        
        for filepath in qmd_files:
            # Ignora arquivos gerados
            if '_book' in str(filepath):
                continue
                
            citations = self.extract_citations_from_qmd(filepath)
            self.citations_in_text.update(citations)
            
            if citations:
                print(f"📄 {filepath.name}: {len(citations)} citações")
    
    def check_consistency(self) -> None:
        """Verifica consistência entre citações e referências"""
        
        # Citações sem referência
        missing_refs = self.citations_in_text - self.references_in_bib
        if missing_refs:
            for ref in sorted(missing_refs):
                self.errors.append(f"Citação [@{ref}] sem entrada em references.bib")
        
        # Referências não citadas
        unused_refs = self.references_in_bib - self.citations_in_text
        if unused_refs:
            for ref in sorted(unused_refs):
                self.warnings.append(f"Referência '{ref}' em .bib mas não citada no texto")
    
    def check_citation_format(self) -> None:
        """Verifica formato das citações"""
        qmd_files = list(self.book_dir.rglob("*.qmd"))
        
        for filepath in qmd_files:
            if '_book' in str(filepath):
                continue
                
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # Verifica citações mal formadas
                bad_patterns = [
                    (r'\[@([a-zA-Z0-9_\-]+) \]', "Espaço extra antes do ]"),
                    (r'\[ @([a-zA-Z0-9_\-]+)\]', "Espaço extra depois do ["),
                    (r'@([a-zA-Z0-9_\-]+)[,.](?!\s)', "Pontuação colada na citação"),
                    (r'\[@([a-zA-Z0-9_\-]+);([a-zA-Z0-9_\-]+)\]', "Faltando @ na segunda citação"),
                ]
                
                for pattern, description in bad_patterns:
                    if re.search(pattern, line):
                        self.warnings.append(
                            f"{filepath.name}:{line_num}: {description}"
                        )
    
    def generate_citation_stats(self) -> Dict:
        """Gera estatísticas sobre citações"""
        stats = {
            'total_citations': len(self.citations_in_text),
            'total_references': len(self.references_in_bib),
            'missing_references': len(self.citations_in_text - self.references_in_bib),
            'unused_references': len(self.references_in_bib - self.citations_in_text),
            'coverage': len(self.citations_in_text & self.references_in_bib) / len(self.references_in_bib) * 100 if self.references_in_bib else 0
        }
        return stats
    
    def run(self) -> int:
        """Executa verificação completa"""
        print("🔍 Verificando consistência de citações...")
        print("=" * 60)
        
        # Extrai citações e referências
        print("\n📚 Analisando citações nos arquivos...")
        self.find_all_citations()
        
        print(f"\n📖 Analisando references.bib...")
        self.references_in_bib = self.extract_references_from_bib()
        
        # Verifica consistência
        self.check_consistency()
        
        # Verifica formato
        print("\n✏️  Verificando formato das citações...")
        self.check_citation_format()
        
        # Gera estatísticas
        stats = self.generate_citation_stats()
        
        # Imprime resultados
        print("\n" + "=" * 60)
        print("📊 RESULTADO DA VERIFICAÇÃO")
        print("=" * 60)
        
        print("\n📈 ESTATÍSTICAS:")
        print(f"  Total de citações no texto: {stats['total_citations']}")
        print(f"  Total de referências no .bib: {stats['total_references']}")
        print(f"  Taxa de uso das referências: {stats['coverage']:.1f}%")
        
        if self.errors:
            print(f"\n❌ {len(self.errors)} ERROS encontrados:")
            for error in self.errors[:10]:
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... e {len(self.errors) - 10} erros adicionais")
        else:
            print("\n✅ Nenhum erro de citação encontrado!")
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} AVISOS:")
            for warning in self.warnings[:10]:
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... e {len(self.warnings) - 10} avisos adicionais")
        
        # Lista citações mais frequentes
        if self.citations_in_text:
            print("\n📚 Citações únicas encontradas:")
            for citation in sorted(list(self.citations_in_text))[:10]:
                print(f"  - @{citation}")
            if len(self.citations_in_text) > 10:
                print(f"  ... e {len(self.citations_in_text) - 10} citações adicionais")
        
        return 1 if self.errors else 0

if __name__ == "__main__":
    checker = CitationChecker()
    sys.exit(checker.run())