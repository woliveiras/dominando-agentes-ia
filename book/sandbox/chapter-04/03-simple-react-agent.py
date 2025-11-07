"""
Exercício 3: Simple ReAct Agent

Implementa agente ReAct básico com ferramentas simples (calculadora, 
temperatura, conversor de moeda).

Dependências:
    uv pip install openai anthropic

Uso:
    python 03-simple-react-agent.py
"""

import re
from typing import Callable, Dict, List, Optional


class Tool:
    """
    Representa uma ferramenta que o agente pode usar.
    """
    
    def __init__(self, name: str, description: str, func: Callable[[str], str]):
        """
        Args:
            name: Nome da ferramenta
            description: Descrição do que a ferramenta faz
            func: Função que implementa a ferramenta
        """
        self.name = name
        self.description = description
        self.func = func
    
    def run(self, input_str: str) -> str:
        """
        Executa a ferramenta com o input fornecido.
        
        Args:
            input_str: String de input para a ferramenta
        
        Returns:
            Resultado da execução
        """
        try:
            return self.func(input_str)
        except Exception as e:
            return f"Erro ao executar ferramenta: {str(e)}"


# Implementação das ferramentas

def calculator(expression: str) -> str:
    """
    Calculadora simples que avalia expressões matemáticas.
    
    ATENÇÃO: Uso de eval() é perigoso em produção!
    Use uma biblioteca de parsing segura como simpleeval.
    
    Args:
        expression: Expressão matemática (ex: "2 + 2")
    
    Returns:
        Resultado da computação
    """
    try:
        # Permitir apenas operações matemáticas básicas
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Erro: expressão contém caracteres não permitidos"
        
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Erro no cálculo: {str(e)}"


def get_temperature(city: str) -> str:
    """
    Retorna temperatura de uma cidade (mock).
    
    Em produção, conectaria a uma API de clima real.
    
    Args:
        city: Nome da cidade
    
    Returns:
        Temperatura em Celsius
    """
    # Database mock de temperaturas
    temps = {
        "paris": 18,
        "londres": 15,
        "london": 15,
        "tokyo": 22,
        "tóquio": 22,
        "são paulo": 25,
        "sao paulo": 25,
        "nova york": 12,
        "new york": 12
    }
    
    city_normalized = city.lower().strip()
    temp = temps.get(city_normalized, 20)  # Default 20°C
    
    return f"A temperatura em {city} é {temp}°C"


def convert_currency(conversion_str: str) -> str:
    """
    Converte entre moedas (mock).
    
    Args:
        conversion_str: String no formato "100 USD to EUR"
    
    Returns:
        Valor convertido
    """
    # Parse do formato "X FROM to TO"
    pattern = r"([0-9.]+)\s+([A-Z]{3})\s+to\s+([A-Z]{3})"
    match = re.search(pattern, conversion_str, re.IGNORECASE)
    
    if not match:
        return "Erro: formato deve ser 'VALOR MOEDA_ORIGEM to MOEDA_DESTINO'"
    
    amount = float(match.group(1))
    from_currency = match.group(2).upper()
    to_currency = match.group(3).upper()
    
    # Taxas de câmbio mock (relativo a USD)
    rates = {
        "USD": 1.0,
        "EUR": 0.85,
        "BRL": 5.0,
        "GBP": 0.73,
        "JPY": 110.0
    }
    
    if from_currency not in rates or to_currency not in rates:
        return f"Erro: moeda não suportada. Suportadas: {', '.join(rates.keys())}"
    
    # Converter para USD primeiro, depois para moeda destino
    amount_usd = amount / rates[from_currency]
    amount_converted = amount_usd * rates[to_currency]
    
    return f"{amount} {from_currency} = {amount_converted:.2f} {to_currency}"


class ReactAgent:
    """
    Agente ReAct que alterna entre raciocínio e ação.
    """
    
    def __init__(self, tools: List[Tool], max_iterations: int = 5):
        """
        Args:
            tools: Lista de ferramentas disponíveis
            max_iterations: Limite de iterações para evitar loops infinitos
        """
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations
    
    def run(self, question: str, verbose: bool = True) -> str:
        """
        Executa o agente para responder uma pergunta.
        
        Args:
            question: Pergunta a responder
            verbose: Se True, imprime pensamentos e ações
        
        Returns:
            Resposta final
        """
        tools_desc = "\n".join([
            f"- {name}: {tool.description}" 
            for name, tool in self.tools.items()
        ])
        
        history = []
        history.append(f"Pergunta: {question}")
        
        if verbose:
            print("=" * 60)
            print("EXECUÇÃO DO AGENTE ReAct")
            print("=" * 60)
            print(f"Pergunta: {question}\n")
        
        for iteration in range(self.max_iterations):
            # Simular pensamento do LLM
            thought, action, action_input = self._simulate_reasoning(
                question, 
                history, 
                tools_desc
            )
            
            if verbose:
                print(f"Iteração {iteration + 1}:")
                print(f"  Pensamento: {thought}")
            
            # Verificar se chegou à resposta final
            if action == "FINAL_ANSWER":
                if verbose:
                    print(f"  Resposta Final: {action_input}\n")
                return action_input
            
            if verbose:
                print(f"  Ação: {action}")
                print(f"  Input: {action_input}")
            
            # Executar ferramenta
            if action not in self.tools:
                observation = f"Erro: ferramenta '{action}' não existe"
            else:
                tool = self.tools[action]
                observation = tool.run(action_input)
            
            if verbose:
                print(f"  Observação: {observation}\n")
            
            # Adicionar ao histórico
            history.append(f"Pensamento: {thought}")
            history.append(f"Ação: {action}")
            history.append(f"Input da Ação: {action_input}")
            history.append(f"Observação: {observation}")
        
        return "Erro: limite de iterações atingido sem resposta final"
    
    def _simulate_reasoning(
        self, 
        question: str, 
        history: List[str],
        tools_desc: str
    ) -> tuple[str, str, str]:
        """
        Simula raciocínio do LLM (em produção seria chamada à API).
        
        Returns:
            Tupla (pensamento, ação, input_da_ação)
        """
        # Heurística simples baseada em palavras-chave
        question_lower = question.lower()
        
        # Caso 1: Perguntas sobre temperatura
        if "temperatura" in question_lower or "clima" in question_lower:
            # Extrair nome da cidade
            cities = ["paris", "londres", "london", "tokyo", "são paulo", "nova york"]
            city_found = None
            for city in cities:
                if city in question_lower:
                    city_found = city
                    break
            
            if city_found and not any("get_temperature" in h for h in history):
                return (
                    f"Preciso obter a temperatura de {city_found}.",
                    "get_temperature",
                    city_found.title()
                )
            elif len(history) > 3:
                # Já executou, formular resposta
                for line in reversed(history):
                    if line.startswith("Observação:"):
                        return (
                            "Já tenho a informação necessária.",
                            "FINAL_ANSWER",
                            line.replace("Observação: ", "")
                        )
        
        # Caso 2: Cálculos matemáticos
        elif any(op in question_lower for op in ["+", "-", "*", "/", "calcule", "quanto é"]):
            # Extrair expressão numérica
            match = re.search(r"([0-9]+\s*[+\-*/]\s*[0-9]+)", question_lower)
            if match and not any("calculator" in h for h in history):
                expression = match.group(1)
                return (
                    f"Preciso calcular {expression}.",
                    "calculator",
                    expression
                )
            elif len(history) > 3:
                for line in reversed(history):
                    if line.startswith("Observação:"):
                        result = line.replace("Observação: ", "")
                        return (
                            "Já calculei o resultado.",
                            "FINAL_ANSWER",
                            f"O resultado é {result}"
                        )
        
        # Caso 3: Conversão de moeda
        elif "converter" in question_lower or "to" in question_lower:
            # Extrair padrão de conversão
            match = re.search(r"([0-9.]+)\s+([A-Z]{3})\s+(?:para|to)\s+([A-Z]{3})", question, re.IGNORECASE)
            if match and not any("convert_currency" in h for h in history):
                amount, from_curr, to_curr = match.groups()
                input_str = f"{amount} {from_curr} to {to_curr}"
                return (
                    f"Preciso converter {amount} {from_curr} para {to_curr}.",
                    "convert_currency",
                    input_str
                )
            elif len(history) > 3:
                for line in reversed(history):
                    if line.startswith("Observação:"):
                        return (
                            "Já fiz a conversão.",
                            "FINAL_ANSWER",
                            line.replace("Observação: ", "")
                        )
        
        # Caso padrão: resposta genérica
        return (
            "Não tenho certeza de como proceder com esta pergunta.",
            "FINAL_ANSWER",
            "Desculpe, não consigo responder a essa pergunta com as ferramentas disponíveis."
        )


def main():
    """
    Função principal que demonstra o agente ReAct.
    """
    # Criar ferramentas
    tools = [
        Tool(
            name="calculator",
            description="Calcula expressões matemáticas (ex: '2 + 2')",
            func=calculator
        ),
        Tool(
            name="get_temperature",
            description="Retorna a temperatura de uma cidade",
            func=get_temperature
        ),
        Tool(
            name="convert_currency",
            description="Converte entre moedas (formato: '100 USD to EUR')",
            func=convert_currency
        )
    ]
    
    # Criar agente
    agent = ReactAgent(tools, max_iterations=5)
    
    # Testes
    test_questions = [
        "Qual é a temperatura em Paris?",
        "Quanto é 25 * 4?",
        "Converta 100 USD para EUR",
        "Qual a temperatura em Londres e Paris? Compare-as.",
    ]
    
    print("DEMONSTRAÇÃO DO AGENTE ReAct")
    print("=" * 60)
    print()
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'=' * 60}")
        print(f"TESTE {i}")
        print(f"{'=' * 60}\n")
        
        answer = agent.run(question, verbose=True)
        
        print(f"Resultado Final: {answer}")
        print()


if __name__ == "__main__":
    main()
