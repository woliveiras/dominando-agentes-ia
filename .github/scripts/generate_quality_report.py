#!/usr/bin/env python3
"""
Script para gerar relatório consolidado de qualidade do livro
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import subprocess
import re

class QualityReportGenerator:
    """Gera relatório de qualidade consolidado"""
    
    def __init__(self):
        self.report_data = {
            "timestamp": datetime.now().isoformat(),
            "commit_sha": os.environ.get("GITHUB_SHA", "local")[:7],
            "branch": os.environ.get("GITHUB_REF_NAME", "local"),
            "pr_number": os.environ.get("GITHUB_PR_NUMBER", ""),
            "tests": {},
            "metrics": {},
            "summary": {}
        }
        self.markdown_report = []
        
    def collect_test_results(self):
        """Coleta resultados de todos os testes"""
        
        # Resultados dos testes de código Python
        code_test_file = Path("test-results/code-test-report.json")
        if code_test_file.exists():
            with open(code_test_file, 'r') as f:
                code_results = json.load(f)
                self.report_data["tests"]["python_code"] = code_results["summary"]
        else:
            self.report_data["tests"]["python_code"] = {
                "status": "skipped",
                "message": "Arquivo de resultados não encontrado"
            }
        
        # Resultados do markdown lint (via arquivo de log se existir)
        self.check_markdown_results()
        
        # Resultados da validação de links
        self.check_link_validation()
        
        # Resultados do build
        self.check_build_artifacts()
        
    def check_markdown_results(self):
        """Verifica resultados do markdown linting"""
        # Simula contagem de avisos do markdownlint
        markdown_issues = 0
        
        for qmd_file in Path("book").rglob("*.qmd"):
            try:
                result = subprocess.run(
                    ["markdownlint", str(qmd_file), "--config", ".markdownlint.json"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode != 0:
                    markdown_issues += len(result.stdout.splitlines())
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        self.report_data["tests"]["markdown_lint"] = {
            "issues": markdown_issues,
            "status": "passed" if markdown_issues == 0 else "warning"
        }
    
    def check_link_validation(self):
        """Verifica resultados da validação de links"""
        broken_links = []
        
        # Se houver um arquivo de resultados de links
        link_report = Path("test-results/broken-links.txt")
        if link_report.exists():
            with open(link_report, 'r') as f:
                broken_links = f.readlines()
        
        self.report_data["tests"]["link_check"] = {
            "broken_links": len(broken_links),
            "status": "passed" if len(broken_links) == 0 else "failed"
        }
    
    def check_build_artifacts(self):
        """Verifica artefatos de build gerados"""
        artifacts = {
            "html": False,
            "pdf": False,
            "epub": False
        }
        
        # Verifica se os arquivos foram gerados
        if Path("book/_book/index.html").exists():
            artifacts["html"] = True
            html_size = sum(f.stat().st_size for f in Path("book/_book").rglob("*.html"))
            self.report_data["metrics"]["html_size_mb"] = round(html_size / 1024 / 1024, 2)
        
        if Path("book/_book/Dominando-Agentes-de-IA.pdf").exists():
            artifacts["pdf"] = True
            pdf_size = Path("book/_book/Dominando-Agentes-de-IA.pdf").stat().st_size
            self.report_data["metrics"]["pdf_size_mb"] = round(pdf_size / 1024 / 1024, 2)
        
        if Path("book/_book/Dominando-Agentes-de-IA.epub").exists():
            artifacts["epub"] = True
            epub_size = Path("book/_book/Dominando-Agentes-de-IA.epub").stat().st_size
            self.report_data["metrics"]["epub_size_mb"] = round(epub_size / 1024 / 1024, 2)
        
        self.report_data["tests"]["build"] = artifacts
    
    def calculate_metrics(self):
        """Calcula métricas do livro"""
        metrics = self.report_data["metrics"]
        
        # Conta capítulos
        chapter_count = len(list(Path("book/chapters").rglob("*.qmd")))
        metrics["total_chapters"] = chapter_count
        
        # Conta palavras totais (aproximado)
        total_words = 0
        for qmd_file in Path("book").rglob("*.qmd"):
            if "_book" not in str(qmd_file):
                with open(qmd_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Remove código e markdown
                    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
                    text = re.sub(r'[#*`\[\]()]', '', text)
                    words = len(text.split())
                    total_words += words
        
        metrics["total_words"] = total_words
        metrics["estimated_pages"] = round(total_words / 250)  # ~250 palavras por página
        
        # Conta exemplos de código
        code_examples = 0
        for qmd_file in Path("book").rglob("*.qmd"):
            if "_book" not in str(qmd_file):
                with open(qmd_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    code_examples += len(re.findall(r'```python', content))
        
        metrics["code_examples"] = code_examples
        
        # Conta referências
        if Path("book/references.bib").exists():
            with open("book/references.bib", 'r') as f:
                content = f.read()
                references = len(re.findall(r'@\w+\{', content))
                metrics["total_references"] = references
        
    def calculate_quality_score(self) -> int:
        """Calcula score de qualidade de 0-100"""
        score = 100
        penalties = []
        
        # Penalidades por problemas encontrados
        tests = self.report_data.get("tests", {})
        
        # Testes de código Python
        if "python_code" in tests:
            failed = tests["python_code"].get("failed", 0)
            if failed > 0:
                penalty = min(failed * 5, 30)
                score -= penalty
                penalties.append(f"-{penalty} (código com erros)")
        
        # Markdown linting
        if "markdown_lint" in tests:
            issues = tests["markdown_lint"].get("issues", 0)
            if issues > 0:
                penalty = min(issues * 2, 20)
                score -= penalty
                penalties.append(f"-{penalty} (problemas de formatação)")
        
        # Links quebrados
        if "link_check" in tests:
            broken = tests["link_check"].get("broken_links", 0)
            if broken > 0:
                penalty = min(broken * 10, 30)
                score -= penalty
                penalties.append(f"-{penalty} (links quebrados)")
        
        # Build failures
        if "build" in tests:
            artifacts = tests["build"]
            if not artifacts.get("html", False):
                score -= 10
                penalties.append("-10 (HTML não gerado)")
            if not artifacts.get("pdf", False):
                score -= 10
                penalties.append("-10 (PDF não gerado)")
        
        self.report_data["summary"]["quality_score"] = max(score, 0)
        self.report_data["summary"]["penalties"] = penalties
        
        return max(score, 0)
    
    def determine_status_emoji(self, score: int) -> str:
        """Determina emoji baseado no score"""
        if score >= 90:
            return "✅"
        elif score >= 70:
            return "🟡"
        else:
            return "❌"
    
    def generate_markdown_report(self):
        """Gera relatório em formato Markdown"""
        score = self.calculate_quality_score()
        emoji = self.determine_status_emoji(score)
        
        # Cabeçalho
        self.markdown_report.append(f"# {emoji} Relatório de Qualidade - Score: {score}/100\n")
        
        # Informações do commit
        self.markdown_report.append(f"**Commit:** `{self.report_data['commit_sha']}`")
        self.markdown_report.append(f"**Branch:** `{self.report_data['branch']}`")
        if self.report_data['pr_number']:
            self.markdown_report.append(f"**PR:** #{self.report_data['pr_number']}")
        self.markdown_report.append(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        
        # Resumo dos testes
        self.markdown_report.append("## 📊 Resumo dos Testes\n")
        
        tests = self.report_data.get("tests", {})
        
        # Tabela de resultados
        self.markdown_report.append("| Teste | Status | Detalhes |")
        self.markdown_report.append("|-------|--------|----------|")
        
        # Python Code Tests
        if "python_code" in tests:
            python_tests = tests["python_code"]
            total = python_tests.get("total", 0)
            success = python_tests.get("success", 0)
            if total > 0:
                percent = (success / total) * 100
                status = "✅ Passou" if percent == 100 else f"⚠️ {percent:.0f}%"
                details = f"{success}/{total} blocos OK"
            else:
                status = "⏭️ Pulado"
                details = "Sem blocos de código"
            self.markdown_report.append(f"| Código Python | {status} | {details} |")
        
        # Markdown Linting
        if "markdown_lint" in tests:
            issues = tests["markdown_lint"]["issues"]
            status = "✅ Passou" if issues == 0 else f"⚠️ {issues} avisos"
            self.markdown_report.append(f"| Formatação Markdown | {status} | {issues} problemas encontrados |")
        
        # Link Check
        if "link_check" in tests:
            broken = tests["link_check"]["broken_links"]
            status = "✅ OK" if broken == 0 else f"❌ {broken} quebrados"
            self.markdown_report.append(f"| Verificação de Links | {status} | {broken} links quebrados |")
        
        # Build Status
        if "build" in tests:
            artifacts = tests["build"]
            built = sum(1 for v in artifacts.values() if v)
            total = len(artifacts)
            status = "✅ Completo" if built == total else f"⚠️ {built}/{total}"
            formats = ", ".join(k.upper() for k, v in artifacts.items() if v)
            self.markdown_report.append(f"| Build do Livro | {status} | {formats or 'Nenhum'} |")
        
        # Métricas do livro
        self.markdown_report.append("\n## 📈 Métricas do Livro\n")
        
        metrics = self.report_data.get("metrics", {})
        
        self.markdown_report.append("| Métrica | Valor |")
        self.markdown_report.append("|---------|-------|")
        
        if "total_chapters" in metrics:
            self.markdown_report.append(f"| Total de Capítulos | {metrics['total_chapters']} |")
        
        if "total_words" in metrics:
            words = metrics['total_words']
            self.markdown_report.append(f"| Total de Palavras | {words:,} |")
        
        if "estimated_pages" in metrics:
            self.markdown_report.append(f"| Páginas Estimadas | ~{metrics['estimated_pages']} |")
        
        if "code_examples" in metrics:
            self.markdown_report.append(f"| Exemplos de Código | {metrics['code_examples']} |")
        
        if "total_references" in metrics:
            self.markdown_report.append(f"| Referências Bibliográficas | {metrics['total_references']} |")
        
        # Tamanhos dos artefatos
        if any(k.endswith("_size_mb") for k in metrics):
            self.markdown_report.append("\n### 📦 Tamanho dos Artefatos\n")
            if "html_size_mb" in metrics:
                self.markdown_report.append(f"- **HTML:** {metrics['html_size_mb']} MB")
            if "pdf_size_mb" in metrics:
                self.markdown_report.append(f"- **PDF:** {metrics['pdf_size_mb']} MB")
            if "epub_size_mb" in metrics:
                self.markdown_report.append(f"- **EPUB:** {metrics['epub_size_mb']} MB")
        
        # Detalhamento de penalidades (se houver)
        if score < 100:
            penalties = self.report_data["summary"].get("penalties", [])
            if penalties:
                self.markdown_report.append("\n## ⚠️ Pontos de Atenção\n")
                self.markdown_report.append("Penalidades aplicadas no score:")
                for penalty in penalties:
                    self.markdown_report.append(f"- {penalty}")
        
        # Recomendações
        self.markdown_report.append("\n## 💡 Recomendações\n")
        
        if score == 100:
            self.markdown_report.append("🎉 **Excelente!** Todos os testes passaram com sucesso!")
        else:
            if tests.get("python_code", {}).get("failed", 0) > 0:
                self.markdown_report.append("- 🐍 Revisar e corrigir blocos de código Python com erro")
            
            if tests.get("markdown_lint", {}).get("issues", 0) > 0:
                self.markdown_report.append("- 📝 Corrigir problemas de formatação Markdown")
            
            if tests.get("link_check", {}).get("broken_links", 0) > 0:
                self.markdown_report.append("- 🔗 Atualizar ou remover links quebrados")
            
            if not tests.get("build", {}).get("pdf", False):
                self.markdown_report.append("- 📄 Investigar falha na geração do PDF")
        
        # Rodapé
        self.markdown_report.append("\n---")
        self.markdown_report.append("*Relatório gerado automaticamente pelo CI/CD*")
        self.markdown_report.append(f"*Timestamp: {datetime.now().isoformat()}*")
    
    def save_reports(self):
        """Salva relatórios em diferentes formatos"""
        # Cria diretório se não existir
        os.makedirs("test-results", exist_ok=True)
        
        # Salva JSON detalhado
        with open("test-results/quality-report.json", "w") as f:
            json.dump(self.report_data, f, indent=2)
        
        # Salva Markdown para comentário no PR
        with open("quality-report.md", "w") as f:
            f.write("\n".join(self.markdown_report))
        
        # Salva badge SVG com score
        self.generate_badge_svg()
    
    def generate_badge_svg(self):
        """Gera badge SVG com o score de qualidade"""
        score = self.report_data["summary"]["quality_score"]
        
        # Determina cor baseada no score
        if score >= 90:
            color = "#4c1"  # Verde
        elif score >= 70:
            color = "#dfb317"  # Amarelo
        else:
            color = "#e05d44"  # Vermelho
        
        # Template SVG simples
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="104" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="104" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h63v20H0z"/>
        <path fill="{color}" d="M63 0h41v20H63z"/>
        <path fill="url(#b)" d="M0 0h104v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="31.5" y="15" fill="#010101" fill-opacity=".3">quality</text>
        <text x="31.5" y="14">quality</text>
        <text x="82.5" y="15" fill="#010101" fill-opacity=".3">{score}%</text>
        <text x="82.5" y="14">{score}%</text>
    </g>
</svg>"""
        
        with open("test-results/quality-badge.svg", "w") as f:
            f.write(svg)
    
    def print_summary(self):
        """Imprime resumo no console"""
        score = self.report_data["summary"]["quality_score"]
        emoji = self.determine_status_emoji(score)
        
        print("\n" + "=" * 60)
        print(f"{emoji} RELATÓRIO DE QUALIDADE - Score: {score}/100")
        print("=" * 60)
        
        # Resumo dos testes
        tests = self.report_data.get("tests", {})
        
        if "python_code" in tests:
            python_tests = tests["python_code"]
            total = python_tests.get("total", 0)
            success = python_tests.get("success", 0)
            if total > 0:
                print(f"🐍 Código Python: {success}/{total} blocos OK")
        
        if "markdown_lint" in tests:
            issues = tests["markdown_lint"]["issues"]
            print(f"📝 Markdown: {issues} problemas encontrados")
        
        if "link_check" in tests:
            broken = tests["link_check"]["broken_links"]
            print(f"🔗 Links: {broken} quebrados")
        
        if "build" in tests:
            artifacts = tests["build"]
            built = [k.upper() for k, v in artifacts.items() if v]
            print(f"📚 Build: {', '.join(built) if built else 'Nenhum'}")
        
        # Métricas
        metrics = self.report_data.get("metrics", {})
        if metrics:
            print("\n📊 Métricas:")
            if "total_chapters" in metrics:
                print(f"  Capítulos: {metrics['total_chapters']}")
            if "total_words" in metrics:
                print(f"  Palavras: {metrics['total_words']:,}")
            if "code_examples" in metrics:
                print(f"  Exemplos: {metrics['code_examples']}")
        
        print("\n" + "=" * 60)
        print(f"Relatórios salvos:")
        print("  - quality-report.md (Markdown)")
        print("  - test-results/quality-report.json (JSON)")
        print("  - test-results/quality-badge.svg (Badge)")
    
    def run(self):
        """Executa geração completa do relatório"""
        print("📊 Gerando relatório de qualidade...")
        
        # Coleta resultados
        self.collect_test_results()
        
        # Calcula métricas
        self.calculate_metrics()
        
        # Gera relatório Markdown
        self.generate_markdown_report()
        
        # Salva relatórios
        self.save_reports()
        
        # Imprime resumo
        self.print_summary()
        
        # Retorna código baseado no score
        score = self.report_data["summary"]["quality_score"]
        if score >= 70:
            return 0  # Sucesso se score >= 70
        else:
            return 1  # Falha se score < 70

if __name__ == "__main__":
    generator = QualityReportGenerator()
    sys.exit(generator.run())