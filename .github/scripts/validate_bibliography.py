#!/usr/bin/env python3
"""
Script para validar o arquivo references.bib
"""

import sys
import re
from pathlib import Path
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding
from typing import List, Dict, Tuple

class BibliographyValidator:
    """Valida arquivo de bibliografia BibTeX"""
    
    def __init__(self, bib_file: str = "book/references.bib"):
        self.bib_file = Path(bib_file)
        self.errors = []
        self.warnings = []
        
    def parse_bibtex(self) -> List[Dict]:
        """Parseia arquivo BibTeX"""
        if not self.bib_file.exists():
            print(f"❌ Arquivo não encontrado: {self.bib_file}")
            sys.exit(1)
            
        with open(self.bib_file, 'r', encoding='utf-8') as f:
            parser = BibTexParser(common_strings=True)
            parser.customization = homogenize_latex_encoding
            bib_database = bibtexparser.load(f, parser=parser)
            
        return bib_database.entries
    
    def validate_entry(self, entry: Dict) -> Tuple[List[str], List[str]]:
        """Valida uma entrada do BibTeX"""
        errors = []
        warnings = []
        
        # Campos obrigatórios por tipo
        required_fields = {
            'article': ['author', 'title', 'journal', 'year'],
            'inproceedings': ['author', 'title', 'booktitle', 'year'],
            'book': ['author', 'title', 'publisher', 'year'],
            'misc': ['author', 'title', 'year'],
            'techreport': ['author', 'title', 'institution', 'year']
        }
        
        entry_type = entry.get('ENTRYTYPE', '').lower()
        entry_id = entry.get('ID', 'unknown')
        
        # Verifica campos obrigatórios
        if entry_type in required_fields:
            for field in required_fields[entry_type]:
                if field not in entry or not entry[field].strip():
                    errors.append(f"Entry '{entry_id}': campo obrigatório '{field}' faltando")
        
        # Verifica formato do ID (sobrenome+ano+palavra)
        if not re.match(r'^[a-z]+\d{4}[a-z]+$', entry_id.lower()):
            warnings.append(f"Entry '{entry_id}': ID não segue padrão 'sobrenome+ano+palavra'")
        
        # Verifica URL
        if 'url' not in entry:
            warnings.append(f"Entry '{entry_id}': sem URL (recomendado incluir)")
        
        # Verifica formato do autor
        if 'author' in entry:
            authors = entry['author']
            if ' and ...' in authors or '...' in authors:
                errors.append(f"Entry '{entry_id}': use 'and others' ao invés de '...'")
        
        # Verifica ano
        if 'year' in entry:
            year = entry['year']
            if not re.match(r'^\d{4}$', year):
                errors.append(f"Entry '{entry_id}': ano inválido '{year}'")
            else:
                year_int = int(year)
                if year_int < 1900 or year_int > 2030:
                    warnings.append(f"Entry '{entry_id}': ano suspeito '{year}'")
        
        return errors, warnings
    
    def check_url_validity(self, entry: Dict) -> bool:
        """Verifica se a URL é válida (não faz request real no CI)"""
        if 'url' not in entry:
            return True
            
        url = entry['url']
        
        # Valida formato básico da URL
        url_pattern = re.compile(
            r'^https?://'  # http:// ou https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domínio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ou IP
            r'(?::\d+)?'  # porta opcional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            return False
            
        # Verifica domínios preferidos
        preferred_domains = ['arxiv.org', 'doi.org', 'github.com', 'openai.com', 'anthropic.com']
        if any(domain in url.lower() for domain in preferred_domains):
            return True
            
        return True  # Assume válido se passar validação básica
    
    def check_duplicates(self, entries: List[Dict]) -> List[str]:
        """Verifica entradas duplicadas"""
        duplicates = []
        seen_ids = set()
        seen_titles = {}
        
        for entry in entries:
            entry_id = entry.get('ID', '')
            title = entry.get('title', '').lower().strip()
            
            # Verifica ID duplicado
            if entry_id in seen_ids:
                duplicates.append(f"ID duplicado: '{entry_id}'")
            seen_ids.add(entry_id)
            
            # Verifica título similar (pode ser duplicata)
            for seen_title, seen_id in seen_titles.items():
                if self.similar_titles(title, seen_title):
                    duplicates.append(f"Possível duplicata: '{entry_id}' e '{seen_id}' têm títulos similares")
            
            seen_titles[title] = entry_id
            
        return duplicates
    
    def similar_titles(self, title1: str, title2: str) -> bool:
        """Verifica se dois títulos são similares"""
        # Remove pontuação e espaços extras
        clean1 = re.sub(r'[^\w\s]', '', title1).lower().strip()
        clean2 = re.sub(r'[^\w\s]', '', title2).lower().strip()
        
        # Verifica similaridade simples
        if clean1 == clean2:
            return True
            
        # Verifica se um contém o outro (para variações)
        if len(clean1) > 10 and len(clean2) > 10:
            if clean1 in clean2 or clean2 in clean1:
                return True
                
        return False
    
    def run(self) -> int:
        """Executa validação completa"""
        print("📚 Validando arquivo de bibliografia...")
        print(f"📄 Arquivo: {self.bib_file}")
        print("=" * 60)
        
        # Parseia arquivo
        entries = self.parse_bibtex()
        print(f"📖 Encontradas {len(entries)} entradas")
        
        # Valida cada entrada
        for entry in entries:
            entry_errors, entry_warnings = self.validate_entry(entry)
            self.errors.extend(entry_errors)
            self.warnings.extend(entry_warnings)
            
            # Verifica URL
            if not self.check_url_validity(entry):
                self.warnings.append(f"Entry '{entry.get('ID', '')}': URL com formato inválido")
        
        # Verifica duplicatas
        duplicates = self.check_duplicates(entries)
        self.warnings.extend(duplicates)
        
        # Imprime resultados
        print("\n" + "=" * 60)
        print("📊 RESULTADO DA VALIDAÇÃO")
        print("=" * 60)
        
        if self.errors:
            print(f"\n❌ {len(self.errors)} ERROS encontrados:")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✅ Nenhum erro encontrado!")
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} AVISOS:")
            for warning in self.warnings[:10]:  # Mostra apenas 10 primeiros
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... e {len(self.warnings) - 10} avisos adicionais")
        
        print("\n" + "=" * 60)
        
        # Estatísticas
        print("\n📈 ESTATÍSTICAS:")
        
        # Conta tipos de entrada
        entry_types = {}
        for entry in entries:
            entry_type = entry.get('ENTRYTYPE', 'unknown')
            entry_types[entry_type] = entry_types.get(entry_type, 0) + 1
        
        for entry_type, count in sorted(entry_types.items()):
            print(f"  {entry_type}: {count}")
        
        # Conta entradas com URL
        with_url = sum(1 for e in entries if 'url' in e)
        print(f"\n  Com URL: {with_url}/{len(entries)} ({with_url/len(entries)*100:.1f}%)")
        
        # Retorna código de erro se houver erros
        return 1 if self.errors else 0

if __name__ == "__main__":
    validator = BibliographyValidator()
    sys.exit(validator.run())