## 📚 Sumário

### **Visão Geral do Livro**

- **Como este livro funciona**
  - Objetivos e público-alvo
  - Pré-requisitos técnicos
- **Estrutura do livro e como navegar pelos capítulos**
  - Divisão em partes e capítulos
  - Como aproveitar ao máximo o conteúdo

### **Introdução: O Universo dos AI Agents**

- **Evolução dos Agentes de IA**
- **O Despertar da Era dos Agentes Inteligentes**
- **O que são AI Agents?**
  - Definição formal e características essenciais
  - Autonomia, reatividade e proatividade
  - Capacidade de interação com o ambiente
- **Agentes vs. Chatbots Simples**
  - Limitações dos chatbots tradicionais
  - O salto qualitativo dos agentes autônomos
  - Quando usar cada abordagem
- **Taxonomia de Agentes**
  - Agentes reativos (stimulus-response)
  - Agentes deliberativos (goal-driven)
  - Agentes híbridos
  - Agentes de aprendizado
- **O Ciclo Percepção-Ação**
  - Observação do ambiente
  - Processamento e raciocínio
  - Tomada de decisão
  - Execução de ações
  - Feedback loop
- **Panorama do Livro: O que você vai aprender**

---

### **PARTE I: Fundamentos e Componentes Base**

#### Capítulo 1: Foundation Models: A Base dos Agentes Inteligentes
- Arquitetura de modelos Transformer
- Como os LLMs aprendem e representam conhecimento
- Treinamento e fine-tuning de foundation models
- Seleção do modelo certo para cada tarefa

#### Capítulo 2: Dominando Large Language Models
- Configuração de parâmetros (temperature, top-p, top-k, max tokens)
- Estratégias de sampling e geração de texto
- Context window e gerenciamento de memória
- Otimização de custo e latência

#### Capítulo 3: Fundamentos de Prompting e Raciocínio
- **Prompt Engineering Essencial**
  - Anatomia de um bom prompt
  - System prompts, user prompts e assistant responses
  - Técnicas de estruturação (markdown, XML, JSON)
- **In-Context Learning (ICL)**
  - Zero-shot: quando o modelo já sabe
  - Few-shot: aprendendo com exemplos
  - Many-shot: maximizando o context window
  - Seleção e ordenação estratégica de exemplos
  - Dynamic example selection
- **Chain-of-Thought (CoT) Prompting**
  - Fundamentos do raciocínio passo-a-passo
  - Zero-shot CoT: "Let's think step by step"
  - Few-shot CoT: ensinando com exemplos de raciocínio
  - Self-consistency: múltiplos caminhos para uma resposta
  - Quando CoT funciona melhor (e quando não funciona)
- **Técnicas Fundamentais de Reasoning**
  - ReAct: Reasoning + Acting (introdução básica)
  - Self-reflection patterns
  - Analogical prompting

#### Capítulo 4: Embeddings e Representação Semântica
- Fundamentos de embeddings
- Modelos de embedding e fine-tuning
- Similarity measures e semantic search
- Técnicas de chunking inteligente
- Vector databases na prática

---

### **PARTE II: Construindo Sistemas de Agentes**

#### Capítulo 5: Retrieval-Augmented Generation (RAG)
- Por que RAG é essencial para agentes
- Arquitetura de pipeline RAG completo
- Estratégias de retrieval (híbrido, reranking, GraphRAG)
- Query rewriting e optimization
- RAG vs. Long Context vs. Fine-tuning

#### Capítulo 6: Tools e Function Calling
- **Fundamentos de Tools**
  - O que são tools e por que são essenciais
  - Anatomia de uma tool definition
- **Design de Tools Efetivas**
  - Schemas e validação de ferramentas
  - Naming conventions e descrições claras
  - Parâmetros obrigatórios vs. opcionais
  - Type safety e validation
- **Exemplos de Tools Específicas**
  - **Web Search Tools**
    - Integração com APIs de busca
    - Parsing e estruturação de resultados
    - Rate limiting e caching
  - **Code Execution Tools**
    - Sandboxing e segurança
    - Ambientes isolados (Docker, containers)
    - Timeouts e resource limits
  - **Database Access Tools**
    - Query generation segura (SQL injection prevention)
    - Read-only vs. write operations
    - Transaction management
  - **API Integration Tools**
    - REST, GraphQL, gRPC
    - Authentication e credentials management
    - Retry strategies
- **Tool Execution e Error Handling**
  - **Patterns de Error Handling Robustos**
    - Graceful degradation
    - Fallback strategies
    - Error classification (transient vs. permanent)
    - Retry with exponential backoff
    - Circuit breaker pattern
  - Logging e debugging de tool calls
  - Timeout management
  - Partial results handling
- **Tool Chaining e Composition**
  - Sequential tool execution
  - Parallel tool execution
  - Conditional tool chains
  - Tool dependencies e orchestration
  - Composing complex workflows from simple tools
- **Melhores Práticas de Tool Orchestration**
  - Tool selection strategies
  - Context passing entre tools
  - State management
  - Performance optimization

#### Capítulo 7: Workflows e Orquestração de Agentes
- **Task Decomposition e Planning**
  - Quebrando problemas complexos
  - Planejamento hierárquico
  - Adaptive planning
- **Agent Loop e Reasoning Patterns**
  - O ciclo observe-think-act
  - Agent loop system prompts
  - Managing state através de iterações
- **ReAct em Profundidade**
  - Implementação completa do padrão ReAct
  - Interleaving reasoning e acting
  - Tool selection e execution
  - Error recovery e replanning
- **Técnicas Avançadas de Raciocínio**
  - **Tree-of-Thought (ToT)**
    - Exploração de múltiplos caminhos de raciocínio
    - Search strategies (BFS, DFS, beam search)
    - State evaluation e pruning
    - Trade-offs de custo computacional
  - **Graph-of-Thought**
  - **Program-of-Thought (PoT)**
    - Gerando código para raciocínio
    - Execução segura de código
  - **Self-Refine e Reflexion**
    - Crítica e melhoria iterativa
    - Learning from mistakes
- **Stateful Agents e Memory Management**
  - Short-term vs. long-term memory
  - Memory stores e retrieval
  - Conversational context management
- **Frameworks de Orquestração**
  - LangGraph, CrewAI, AutoGen
  - Prós, contras e quando usar cada um
  - Building your own orchestration layer

#### Capítulo 8: Comunicação Entre Agentes
- **Padrões de Comunicação Multi-Agente**
  - Message passing fundamentals
  - Synchronous vs. asynchronous communication
  - Broadcast, unicast, multicast
- **Agent-to-Agent (A2A) Protocols**
  - Protocol design principles
  - Message formats e serialization
  - Handshaking e session management
- **Model Context Protocol (MCP)**
  - Arquitetura do MCP
  - Implementação prática
  - Use cases e benefícios
- **Coordination Patterns**
  - Request-response patterns
  - Pub-sub patterns
  - Event-driven architectures
- **Delegation e Role Assignment**
  - Task delegation strategies
  - Role-based agent organization
  - Dynamic role assignment
- **Conflict Resolution Entre Agentes**
  - Identifying conflicts
  - Conflict types (resource, goal, priority)
  - Resolution strategies
    - Voting mechanisms
    - Priority-based resolution
    - Mediator patterns
    - Negotiation protocols
- **Consensus Mechanisms**
  - Distributed consensus basics
  - Majority voting
  - Weighted voting
  - Byzantine fault tolerance considerations
  - Practical consensus for agent systems
- **Load Balancing Entre Agentes**
  - Work distribution strategies
  - Round-robin vs. weighted distribution
  - Dynamic load balancing
  - Queue-based task distribution
  - Monitoring agent capacity e health

---

### **PARTE III: Arquitetura e Produção**

#### Capítulo 9: Arquiteturas de Sistemas Multi-Agentes
- Design patterns para sistemas multi-LLM
- Cascade architectures e routing
- Task-specialized agents
- Hierarchical agent systems
- Hybrid approaches (embeddings + LLMs + symbolic AI)
- Trade-offs de custo, latência e performance

#### Capítulo 10: Verificação, Guardrails e Qualidade
- Safety guardrails (input/output validation)
- Verification modules e self-correction
- Fact-checking e hallucination mitigation
- Human-in-the-loop patterns
- Quality assurance em produção

#### Capítulo 11: Segurança em Sistemas de AI Agents
- Threat model para aplicações com LLMs
- Prompt injection e adversarial attacks
- Proteção de dados sensíveis (PII, secrets)
- Guardrails comerciais vs. open source
- Zero trust architecture para agentes
- Supply chain security (ML-BOMs, model cards)

#### Capítulo 12: LLMOps e Deploy em Produção
- CI/CD para aplicações com LLMs
- Monitoring e observability
- Logging de prompts e respostas
- Gerenciamento de custos
- A/B testing e evaluation metrics
- Incident response e rollback strategies

#### Capítulo 13: Avaliação e Iteração de Agentes
- Métricas de sucesso para agentes
- Offline vs. online evaluation
- Building test suites e benchmarks
- Red teaming para agentes
- Continuous improvement loops

---

### **Apêndices**

#### Apêndice A: Guia de Ferramentas e Frameworks
- Overview de frameworks populares
- Comparação de vector databases
- LLM providers e suas características
- Tools de desenvolvimento recomendadas

#### Apêndice B: Datasets e Recursos
- Datasets para fine-tuning
- Benchmarks importantes
- Comunidades e recursos de aprendizado

#### Apêndice C: Exercícios Práticos Avançados
- Projetos completos end-to-end
- Desafios de implementação
- Soluções e discussões

#### Apêndice D: Glossário de Termos Técnicos
- Definições de termos-chave
- Siglas e abreviações comuns
- Referências cruzadas para capítulos relevantes

