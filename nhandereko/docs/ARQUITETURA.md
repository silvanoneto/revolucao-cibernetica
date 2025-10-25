# 🏗️ Arquitetura: Orquestrador de Conhecimento

## 📐 Conceito

Este sistema implementa um **orquestrador de consultas multi-camadas** para LLMs, inspirado no funcionamento da cognição humana e no princípio de **feedback loop**.

---

## 🎯 As 4 Camadas do Conhecimento

Cada camada representa um tipo diferente de conhecimento e processamento, trabalhando em sinergia através de **conexões bidirecionais** que criam um sistema de aprendizado contínuo:

```mermaid
graph TB
    subgraph L4["🧠 CAMADA 4: MEMÓRIA (Semântica)"]
        M1["Vector Database<br/>📦 Embeddings"]
        M2["Busca Semântica<br/>🔍 Similaridade"]
        M3["Associações Livres<br/>💭 Contexto"]
        M1 -->|"vetoriza"| M2
        M2 -->|"descobre"| M3
        M3 -->|"refina embeddings"| M1
    end
    
    subgraph L3["🕸️ CAMADA 3: RELACIONAL (Grafo)"]
        G1["Graph Database<br/>🔗 Neo4j/NetworkX"]
        G2["Relações Tipadas<br/>↔️ Arestas"]
        G3["Navegação<br/>🧭 Caminhos"]
        G1 -->|"conecta"| G2
        G2 -->|"permite"| G3
        G3 -->|"expande grafo"| G1
    end
    
    subgraph L2["📊 CAMADA 2: HISTÓRICA (Fatos)"]
        H1["SQL - Fatos<br/>📈 Eventos"]
        H2["Log de Consultas<br/>📝 Trajetória"]
        H3["Análise Temporal<br/>⏱️ Padrões"]
        H1 -->|"registra"| H2
        H2 -->|"revela"| H3
        H3 -->|"alimenta métricas"| H1
    end
    
    subgraph L1["🏛️ CAMADA 1: ESTRUTURAL (Dimensões)"]
        S1["SQL - Dimensões<br/>🗂️ Entidades"]
        S2["Taxonomia Base<br/>🌳 Hierarquias"]
        S3["Metadados<br/>🏷️ Descritores"]
        S1 -->|"organiza"| S2
        S2 -->|"classifica"| S3
        S3 -->|"valida estrutura"| S1
    end
    
    %% Conexões DESCENDENTES (Síntese)
    M1 -.->|"⬇️ SINTETIZAR<br/>extrai conceitos"| G1
    M3 -.->|"enriquece relações"| G2
    
    G1 -.->|"⬇️ SINTETIZAR<br/>identifica padrões"| H1
    G2 -.->|"correlaciona eventos"| H2
    
    H1 -.->|"⬇️ SINTETIZAR<br/>consolida fatos"| S1
    H3 -.->|"define taxonomia"| S2
    
    %% Conexões ASCENDENTES (Expansão)
    S1 ==>|"⬆️ EXPANDIR<br/>valida entidades"| H1
    S2 ==>|"estrutura consultas"| H2
    
    H1 ==>|"⬆️ EXPANDIR<br/>cria relações"| G1
    H2 ==>|"descobre conexões"| G2
    
    G1 ==>|"⬆️ EXPANDIR<br/>gera embeddings"| M1
    G3 ==>|"contextualiza busca"| M2
    
    %% Estilos
    style L4 fill:#e1f5ff,stroke:#01579b,stroke-width:4px
    style L3 fill:#f3e5f5,stroke:#4a148c,stroke-width:4px
    style L2 fill:#fff3e0,stroke:#e65100,stroke-width:4px
    style L1 fill:#e8f5e9,stroke:#1b5e20,stroke-width:4px
    
    style M1 fill:#b3e5fc,stroke:#01579b
    style M2 fill:#b3e5fc,stroke:#01579b
    style M3 fill:#b3e5fc,stroke:#01579b
    
    style G1 fill:#e1bee7,stroke:#4a148c
    style G2 fill:#e1bee7,stroke:#4a148c
    style G3 fill:#e1bee7,stroke:#4a148c
    
    style H1 fill:#ffe0b2,stroke:#e65100
    style H2 fill:#ffe0b2,stroke:#e65100
    style H3 fill:#ffe0b2,stroke:#e65100
    
    style S1 fill:#c8e6c9,stroke:#1b5e20
    style S2 fill:#c8e6c9,stroke:#1b5e20
    style S3 fill:#c8e6c9,stroke:#1b5e20
```

### 🔄 Dinâmica das Conexões

#### ⬇️ Fluxo DESCENDENTE (Sintetizar)
**Da abstração para o concreto**

```text
🧠 Memória → 🕸️ Grafo → 📊 Histórico → 🏛️ Estrutura

• Embeddings identificam conceitos → criam nós no grafo
• Grafo detecta padrões → registra no histórico
• Histórico consolida fatos → define entidades estruturais
```

#### ⬆️ Fluxo ASCENDENTE (Expandir)
**Do concreto para a abstração**

```text
🏛️ Estrutura → 📊 Histórico → 🕸️ Grafo → 🧠 Memória

• Entidades validam consultas → alimentam histórico
• Histórico revela conexões → expande grafo
• Grafo contextualiza busca → enriquece embeddings
```

#### 🌀 Feedback Loop Completo

```text
┌──────────────────────────────────────────────────┐
│  CICLO DE APRENDIZADO ENTRE CAMADAS              │
└──────────────────────────────────────────────────┘

1️⃣ Consulta semântica (🧠 Memória)
   ↓ sintetiza conceitos
   
2️⃣ Identifica relações (🕸️ Grafo)
   ↓ detecta padrões
   
3️⃣ Registra evento (📊 Histórico)
   ↓ consolida fato
   
4️⃣ Valida/cria entidade (🏛️ Estrutura)
   ↑ valida taxonomia
   
5️⃣ Estrutura expande histórico (📊 Histórico)
   ↑ descobre conexões
   
6️⃣ Histórico enriquece grafo (🕸️ Grafo)
   ↑ contextualiza busca
   
7️⃣ Grafo refina embeddings (🧠 Memória)
   → Próxima consulta é mais inteligente! ✨
```

### 📝 Características de Cada Camada

| Camada | Tecnologia | Função Principal | Conecta com | Analogia Humana |
|--------|-----------|------------------|-------------|-----------------|
| 🧠 **Memória** | Vector DB (ChromaDB) | Busca semântica, similaridade | ⬇️ Grafo: extrai conceitos<br/>⬆️ Grafo: recebe contexto | Intuição e associações livres |
| 🕸️ **Relacional** | Graph DB (NetworkX) | Relações tipadas, navegação | ⬇️ Histórico: identifica padrões<br/>⬆️ Memória: contextualiza busca | Rede neural de conceitos |
| 📊 **Histórica** | SQL Fatos (SQLite) | Eventos temporais, trajetória | ⬇️ Estrutura: consolida fatos<br/>⬆️ Grafo: descobre conexões | Memória episódica |
| 🏛️ **Estrutural** | SQL Dimensões (SQLite) | Taxonomia, entidades | ⬆️ Histórico: valida consultas<br/>⬇️ Histórico: define classes | Conhecimento declarativo |

### 🔗 Tipos de Conexões Entre Camadas

| Direção | Nome | Função | Exemplo Prático |
|---------|------|--------|-----------------|
| ⬇️ **Descendente** | **SINTETIZAR** | Condensar abstrato → concreto | Embedding "Apache Spark" → cria entidade `spark` |
| ⬆️ **Ascendente** | **EXPANDIR** | Ampliar concreto → abstrato | Entidade `spark` validada → enriquece busca vetorial |
| 🔄 **Circular** | **FEEDBACK LOOP** | Aprendizado contínuo | Consulta gera fato → fato cria relação → relação melhora próxima consulta |

---

## 🔄 Feedback Loop: Como o Agente Aprende

### 🎬 Ciclo Completo de Aprendizado (Com Conexões Entre Camadas)

```mermaid
sequenceDiagram
    participant A as 🤖 Agente
    participant M as 🧠 Memória<br/>(Vector)
    participant G as 🕸️ Grafo<br/>(Relações)
    participant H as 📊 Histórico<br/>(Fatos)
    participant S as 🏛️ Estrutura<br/>(Dimensões)
    
    rect rgb(225, 245, 255)
        Note over A,M: FASE 1: Consulta Semântica (Camada 4)
        A->>M: 1️⃣ "Como usar Apache Spark?"
        M->>M: Busca vetorial por similaridade
        M-->>A: Top 5 documentos relevantes
    end
    
    rect rgb(255, 243, 224)
        Note over A,H: FASE 2: Registro Histórico (Camada 2)
        A->>H: 2️⃣ Registra consulta
        Note over H: tipo: embedding<br/>qualidade: 0.7<br/>tempo: 145ms
    end
    
    rect rgb(243, 229, 245)
        Note over A,G: FASE 3: Análise de Padrões (Camada 3)
        A->>A: 3️⃣ Analisa documentos
        Note over A: Detecta: "Spark + Python"<br/>em 85% dos docs
        
        A->>H: 4️⃣ Registra descoberta
        Note over H: confiança: 0.85<br/>evidências: 3 docs
    end
    
    rect rgb(232, 245, 233)
        Note over H,S: FASE 4: Estruturação (Camadas 1 ⬆️ 2 ⬆️ 3)
        H->>S: ⬆️ EXPANDIR: Valida entidades
        S-->>H: spark, python existem
        
        alt Confiança > 0.8
            H->>G: ⬆️ EXPANDIR: Cria relação
            G->>G: Adiciona aresta<br/>spark → usa → python<br/>peso: 0.85
            Note over G: Grafo expandido!
        end
    end
    
    rect rgb(225, 245, 255)
        Note over G,M: FASE 5: Enriquecimento (Camadas 3 ⬆️ 4)
        G->>M: ⬆️ EXPANDIR: Contextualiza embeddings
        M->>M: Reforça associação<br/>spark ↔ python
        Note over M: Próximas buscas mais precisas!
    end
    
    rect rgb(210, 255, 210)
        Note over A,M: FASE 6: Consulta Evoluída ✨
        A->>M: 7️⃣ "Como processar dados em Python?"
        M->>G: ⬇️ SINTETIZAR: Busca relações
        G-->>M: spark usa python (0.85)
        M->>H: ⬇️ SINTETIZAR: Busca descobertas
        H-->>M: "PySpark comum" (0.85)
        M-->>A: Resposta ENRIQUECIDA com contexto! ✨
        Note over A: Qualidade: 0.95 (+35%!)
    end
    
    Note over A,S: 🌀 Loop completo: Sistema aprendeu e melhorou!
```

### 💡 Exemplo Prático: Aprendizado em 4 Fases

#### 🔵 Fase 1: Consulta Inicial (Camada 4 → 2)

```python
query = "Como usar Apache Spark?"

# 🧠 Camada 4 (Memória): Busca vetorial semântica
docs = buscar_embeddings(query)
# Retorna: ["Apache Spark...", "PySpark...", "Spark Streaming..."]

# ⬇️ SINTETIZAR: Extrai conceitos da busca
conceitos_detectados = extrair_conceitos(docs)
# ["spark", "python", "big-data", "processamento"]

# 📊 Camada 2 (Histórico): Registra consulta
registrar_consulta(
    agente="claude-dev",
    tipo="embedding",
    query=query,
    resultados=len(docs),
    tempo_ms=145,
    qualidade_score=0.7,  # Primeira tentativa - baseline
    conceitos=conceitos_detectados
)
```

#### 🟢 Fase 2: Análise e Descoberta (Camada 2 → 3)

```python
# 🤖 Agente analisa padrões nos documentos
padroes = analisar_coocorrencia(docs)
# Detecta: "spark" + "python" aparecem juntos em 85% dos docs

# 💡 Sistema descobre correlação forte
descoberta = {
    "tipo": "correlacao",
    "descricao": "Spark frequentemente usado com Python (PySpark)",
    "entidade_origem": "spark",
    "entidade_destino": "python",
    "confianca": 0.85,
    "evidencias": ["doc_spark_1", "doc_pyspark_2", "tutorial_3"]
}

# 📊 Camada 2: Registra descoberta
if descoberta["confianca"] > 0.8:
    registrar_descoberta(**descoberta)
    
    # ⬆️ EXPANDIR: Descoberta valida criação de relação
    criar_relacao_grafo = True
```

#### 🟣 Fase 3: Estruturação do Conhecimento (Camadas 1 ⬆️ 2 ⬆️ 3)

```python
# 🏛️ Camada 1 (Estrutural): Garante existência das entidades
if not existe_entidade("spark"):
    criar_entidade(
        chave="spark",
        nome="Apache Spark",
        tipo="ferramenta",
        categoria="big-data"
    )

if not existe_entidade("python"):
    criar_entidade(
        chave="python",
        nome="Python",
        tipo="linguagem",
        categoria="programacao"
    )

# ⬆️ EXPANDIR: Estrutura valida e alimenta o grafo
# 🕸️ Camada 3 (Grafo): Adiciona relação descoberta
adicionar_aresta(
    origem="spark",
    destino="python",
    relacao="usa",
    peso=0.85,  # Baseado na confiança da descoberta
    evidencias=descoberta["evidencias"]
)

# 📊 Camada 2 (Histórico): Registra interação
registrar_interacao(
    origem="spark",
    destino="python",
    tipo="usa",
    intensidade=0.85,
    contexto="descoberto via análise de coocorrência"
)

# ⬆️ EXPANDIR: Grafo enriquece embeddings futuros
# 🧠 Camada 4 (Memória): Reforça associação
reforcar_associacao_vetorial(
    termo1="spark",
    termo2="python",
    forca=0.85
)
```

#### ✨ Fase 4: Consulta Evoluída (Sistema Aprendeu!)

```python
# 🚀 Próxima consulta - Sistema é mais inteligente!
query = "Como processar dados em Python?"

# 🧠 Camada 4: Busca na memória (embeddings)
docs_memoria = buscar_embeddings(query)

# ⬇️ SINTETIZAR: Busca relações estruturadas
# 🕸️ Camada 3: Expande com o grafo
relacoes = buscar_vizinhos_grafo("python", profundidade=2)
# 💡 Descobre automaticamente: 
# python ← usa ← spark (0.85)
# python → processa → big-data (0.78)

# ⬇️ SINTETIZAR: Consulta aprendizados passados
# 📊 Camada 2: Busca descobertas históricas
descobertas = buscar_descobertas(
    conceito="python",
    tipo="correlacao",
    min_confianca=0.8
)
# Retorna: ["PySpark comum para big-data", "Pandas para análise"]

# 🏛️ Camada 1: Valida entidades mencionadas
entidades_validadas = validar_entidades(
    ["python", "spark", "big-data"]
)

# ✨ Contexto ENRIQUECIDO para o LLM
contexto = {
    "documentos": docs_memoria,           # Camada 4
    "relacoes_grafo": relacoes,           # Camada 3
    "descobertas_previas": descobertas,   # Camada 2
    "entidades_validadas": entidades_validadas  # Camada 1
}

# 📊 Registra nova consulta com qualidade superior
registrar_consulta(
    agente="claude-dev",
    tipo="hibrida",  # Usa todas as 4 camadas!
    query=query,
    qualidade_score=0.95,  # +35% de melhoria! 🎉
    tempo_ms=187,
    contexto_enriquecido=True
)

# 🌀 RESULTADO: Resposta muito mais contextualizada e precisa!
# O sistema APRENDEU com a interação anterior.
```

---

## 🎯 Casos de Uso: Aprendizado em Ação

### 1️⃣ Sistema de Q&A que Aprende Continuamente

O sistema não apenas responde - ele **evolui** a cada interação:

```mermaid
graph LR
    Q1["❓ Pergunta 1<br/>O que é Spark?"] --> R1["📄 Resposta Básica<br/>qualidade: 0.7"]
    R1 --> F1["📊 Feedback<br/>registrado"]
    
    F1 --> Q2["❓ Pergunta 2<br/>Spark com Python?"]
    Q2 --> R2["📄 Resposta Enriquecida<br/>qualidade: 0.85"]
    R2 --> D1["💡 DESCOBERTA<br/>Spark ↔ Python"]
    
    D1 --> Q3["❓ Pergunta 3<br/>Spark é rápido?"]
    Q3 --> R3["✨ Auto-contexto<br/>qualidade: 0.95<br/>+PySpark grátis!"]
    
    style Q1 fill:#fff3cd,stroke:#856404,stroke-width:2px
    style Q2 fill:#fff3cd,stroke:#856404,stroke-width:2px
    style Q3 fill:#fff3cd,stroke:#856404,stroke-width:2px
    style R1 fill:#f8d7da,stroke:#721c24,stroke-width:2px
    style R2 fill:#d1ecf1,stroke:#0c5460,stroke-width:2px
    style R3 fill:#d4edda,stroke:#155724,stroke-width:3px
    style D1 fill:#d4edda,stroke:#155724,stroke-width:2px
    style F1 fill:#e2e3e5,stroke:#383d41
```

#### 📈 Evolução da Qualidade

| Iteração | Consulta | Camadas Usadas | Qualidade | Aprendizado Capturado |
|----------|----------|----------------|-----------|----------------------|
| **1ª** | "O que é Apache Spark?" | 🧠 Memória apenas | ⭐⭐⭐ 70% | Baseline - resposta dos embeddings |
| **2ª** | "Como usar Spark com Python?" | 🧠 Memória + 📊 Histórico | ⭐⭐⭐⭐ 85% | 💡 Descobre correlação Spark-Python (0.85) |
| **3ª** | "Spark é rápido?" | 🧠🕸️📊🏛️ Todas! | ⭐⭐⭐⭐⭐ 95% | ✨ Auto-inclui contexto PySpark + big-data |

**Ganho**: +35% de qualidade em 3 interações! 🚀

### 2️⃣ Análise de Padrões de Consulta (Camada Histórica)

Identifica **gaps de conhecimento** analisando consultas com baixa qualidade:

```sql
-- 📉 Query: Consultas problemáticas por tipo
SELECT 
    tipo_consulta,
    AVG(qualidade_score) as qualidade_media,
    COUNT(*) as total_consultas,
    AVG(tempo_execucao_ms) as tempo_medio,
    STRING_AGG(DISTINCT query_texto, '; ') as exemplos
FROM fato_consulta
WHERE qualidade_score < 0.7
GROUP BY tipo_consulta
ORDER BY qualidade_media ASC
LIMIT 10;

-- 💡 Resultado: "consultas sobre 'kubernetes' têm qualidade 0.55"
-- 🎯 Ação: melhorar documentação e indexação sobre Kubernetes
```

#### 💡 Resultado Exemplo

```text
┌──────────────────┬──────────────┬──────────────┬──────────────┬────────────────────────┐
│ tipo_consulta    │ qualidade_   │ total_       │ tempo_medio  │ exemplos               │
│                  │ media        │ consultas    │              │                        │
├──────────────────┼──────────────┼──────────────┼──────────────┼────────────────────────┤
│ embedding        │ 0.55         │ 47           │ 234 ms       │ "O que é Kubernetes?"  │
│ sql              │ 0.61         │ 23           │ 89 ms        │ "Listar conceitos X"   │
│ grafo            │ 0.68         │ 15           │ 156 ms       │ "Relações com Docker"  │
└──────────────────┴──────────────┴──────────────┴──────────────┴────────────────────────┘
```

**🎯 Ação Recomendada**: Sistema identifica que documentação sobre "Kubernetes" precisa ser melhorada ou expandida (qualidade 0.55 < threshold 0.7).

### 3️⃣ Descoberta Automática de Relações (Todas as Camadas)

O sistema **detecta padrões** e **cria relações estruturadas** automaticamente:

```mermaid
flowchart TD
    A["📚 Agente consulta documentos<br/>(🧠 Camada 4)"] --> B{{"🤔 Co-ocorrência<br/>detectada?"}}
    
    B -->|"Kafka + Streaming<br/>em 88% dos docs"| C["💡 DESCOBERTA<br/>(📊 Camada 2)"]
    
    C --> D["🏛️ Valida/cria entidades<br/>(Camada 1)"]
    D --> E["🕸️ Adiciona ao grafo<br/>Kafka → usa → Streaming<br/>peso: 0.88<br/>(Camada 3)"]
    
    E --> F["📊 Registra interação<br/>histórica<br/>(Camada 2)"]
    
    F --> G["🧠 Reforça embeddings<br/>kafka ↔ streaming<br/>(Camada 4)"]
    
    G --> H["✨ Próximas consultas<br/>AUTO-CONTEXTUALIZADAS"]
    
    style A fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    style C fill:#d4edda,stroke:#155724,stroke-width:3px
    style D fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    style E fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style F fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style G fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    style H fill:#d1ecf1,stroke:#0c5460,stroke-width:3px
    style B fill:#fff3cd,stroke:#856404,stroke-width:2px
```

#### 🔄 Fluxo de Descoberta

1. **🧠 Análise Semântica** (Camada 4): Detecta "kafka" e "streaming" co-ocorrem frequentemente
2. **💡 Descoberta** (Camada 2): Registra padrão com confiança 0.88
3. **🏛️ Validação** (Camada 1): Garante entidades `kafka` e `streaming` existem
4. **🕸️ Estruturação** (Camada 3): Cria aresta `kafka → usa → streaming`
5. **📊 Histórico** (Camada 2): Registra interação para análise futura
6. **🧠 Refinamento** (Camada 4): Reforça associação vetorial
7. **✨ Evolução**: Sistema agora "sabe" automaticamente que Kafka usa streaming!

---

## 📊 Star Schema: Estrutura de Dados (Camadas 1 e 2)

O sistema usa um **modelo dimensional (Star Schema)** para organizar dados estruturados e históricos:

### 🏛️ Dimensões (Camada 1: Contexto Estável)

As dimensões representam **entidades e contextos** que mudam pouco ao longo do tempo:

```mermaid
erDiagram
    DIM_ENTIDADE {
        int id_entidade PK
        string chave_negocio UK "spark, python, kafka"
        string nome "Apache Spark"
        enum tipo "linguagem, ferramenta, conceito"
        string categoria "big-data, ml, web"
        text descricao
        json atributos_json "metadata flexível"
        timestamp criado_em
        timestamp atualizado_em
    }
    
    DIM_CONCEITO {
        int id_conceito PK
        string chave_negocio UK
        string nome "Machine Learning"
        string categoria "tecnologia"
        string hierarquia "tech/ai/ml"
        text descricao
        int nivel_profundidade "3"
    }
    
    DIM_TEMPO {
        int id_tempo PK
        date data UK
        int ano "2025"
        int mes "10"
        int dia "25"
        int dia_semana "5 (sexta)"
        int trimestre "4"
        int semestre "2"
        bool e_feriado
    }
    
    DIM_AGENTE {
        int id_agente PK
        string chave_negocio UK "claude-dev-001"
        string nome "Claude Developer"
        enum tipo "llm, usuario, sistema"
        string modelo "claude-sonnet-4-5"
        json config_json "preferencias, limites"
        timestamp criado_em
    }
```

**📌 Propósito das Dimensões:**
- 🏷️ **DIM_ENTIDADE**: Conceitos, ferramentas, linguagens que estruturam o conhecimento
- 🧩 **DIM_CONCEITO**: Taxonomia hierárquica de ideias
- 📅 **DIM_TEMPO**: Contexto temporal para análises de evolução
- 🤖 **DIM_AGENTE**: Quem interage com o sistema (LLMs, usuários, processos)

### 📈 Fatos (Camada 2: Eventos e Medições)

Os fatos representam **eventos** que acontecem no tempo:

```mermaid
erDiagram
    FATO_CONSULTA {
        int id_consulta PK
        int id_tempo FK
        int id_agente FK
        enum tipo_consulta "embedding, sql, grafo, hibrida"
        text query_texto
        int total_resultados
        int tempo_execucao_ms
        float qualidade_score "0.0 a 1.0"
        json contexto_retornado
        bool usou_grafo "enriquecido?"
        bool usou_historico "contexto previo?"
    }
    
    FATO_DESCOBERTA {
        int id_descoberta PK
        int id_tempo FK
        int id_agente FK
        int id_entidade_origem FK
        int id_entidade_destino FK
        int id_conceito FK
        enum tipo_descoberta "padrao, correlacao, relacao, anomalia"
        text descricao
        float confianca "0.0 a 1.0"
        json evidencias_json "refs a docs"
        bool aplicada_grafo "criou aresta?"
        bool melhorou_qualidade "impacto positivo?"
    }
    
    FATO_INTERACAO {
        int id_interacao PK
        int id_tempo FK
        int id_entidade_origem FK
        int id_entidade_destino FK
        enum tipo_interacao "usa, gera, depende_de, relaciona_com"
        float intensidade "0.0 a 1.0"
        text contexto
        int contador_uso "quantas vezes usado"
    }
    
    DIM_TEMPO ||--o{ FATO_CONSULTA : "registra em"
    DIM_AGENTE ||--o{ FATO_CONSULTA : "executa"
    
    DIM_TEMPO ||--o{ FATO_DESCOBERTA : "ocorre em"
    DIM_AGENTE ||--o{ FATO_DESCOBERTA : "realiza"
    DIM_ENTIDADE }o--o{ FATO_DESCOBERTA : "tem origem"
    DIM_ENTIDADE }o--o{ FATO_DESCOBERTA : "tem destino"
    
    DIM_TEMPO ||--o{ FATO_INTERACAO : "acontece em"
    DIM_ENTIDADE }o--o{ FATO_INTERACAO : "tem origem"
    DIM_ENTIDADE }o--o{ FATO_INTERACAO : "tem destino"
```

**📌 Propósito dos Fatos:**
- 📋 **FATO_CONSULTA**: Rastreia todas as buscas e sua qualidade
- 💡 **FATO_DESCOBERTA**: Registra padrões e correlações encontradas
- 🔗 **FATO_INTERACAO**: Captura uso de relações entre entidades

### 📖 Exemplos de Dados Reais

#### 🏛️ `dim_entidade` (Camada 1)

| id_entidade | chave_negocio | nome | tipo | categoria | criado_em |
|-------------|---------------|------|------|-----------|-----------|
| 1 | spark | Apache Spark | ferramenta | big-data | 2025-10-15 |
| 2 | python | Python | linguagem | programação | 2025-10-15 |
| 3 | pandas | Pandas | biblioteca | data-science | 2025-10-16 |
| 4 | kafka | Apache Kafka | ferramenta | streaming | 2025-10-18 |

#### 📊 `fato_consulta` (Camada 2)

| id_consulta | id_tempo | id_agente | tipo_consulta | query_texto | qualidade_score | usou_grafo |
|-------------|----------|-----------|---------------|-------------|-----------------|------------|
| 101 | 20251018 | 1 | embedding | "O que é Spark?" | 0.72 | false |
| 102 | 20251019 | 1 | **hibrida** | "Spark vs Pandas" | 0.88 | **true** |
| 103 | 20251019 | 1 | **hibrida** | "Como usar Kafka?" | 0.91 | **true** |

**💡 Observação**: Consultas híbridas (que usam grafo) têm qualidade ~20% superior!

#### 💡 `fato_descoberta` (Camada 2)

| id | descricao | confianca | evidencias | origem | destino | aplicada_grafo |
|----|-----------|-----------|------------|--------|---------|----------------|
| 1 | Spark frequentemente usado com Python (PySpark) | 0.85 | ["doc1", "doc3", "tut3"] | spark | python | **true** ✅ |
| 2 | Spark processa big data melhor que Hadoop | 0.88 | ["doc5", "doc8"] | spark | hadoop | **true** ✅ |
| 3 | Kafka integra com Spark Streaming | 0.91 | ["doc12", "tut7", "doc15"] | kafka | spark | **true** ✅ |

**🌀 Feedback Loop**: Descobertas com confiança > 0.8 são aplicadas ao grafo, melhorando consultas futuras!

---

## 🚀 Roadmap: Evolução Contínua

### 📍 Estado Atual (Outubro 2025)

```mermaid
gantt
    title Evolução do Sistema Nhandereko
    dateFormat YYYY-MM-DD
    
    section ✅ Fase 1: Fundação
    Arquitetura 4 Camadas     :done, f1a, 2025-01-01, 30d
    Star Schema + Dimensões   :done, f1b, 2025-01-15, 45d
    Feedback Loop Básico      :done, f1c, 2025-02-01, 30d
    Vector + Graph DB         :done, f1d, 2025-02-15, 30d
    
    section 🏗️ Fase 2: Inteligência
    Pesos Dinâmicos          :active, f2a, 2025-03-01, 45d
    Aprendizado Ativo        :f2b, 2025-03-20, 50d
    Descoberta Automática    :f2c, 2025-04-01, 40d
    
    section 🔮 Fase 3: Meta-Sistema
    Consolidação Auto        :f3a, 2025-05-10, 35d
    Meta-Aprendizado         :f3b, 2025-06-01, 50d
    Auto-Otimização          :f3c, 2025-06-20, 40d
```

### 🎯 Funcionalidades Planejadas

#### 1️⃣ Pesos Dinâmicos (Fase 2 - Em Desenvolvimento)

**Objetivo**: Relações aprendem sua própria importância através do uso real.

**Como funciona**:

```python
# 🔗 Relação inicial: spark → python (peso 0.85)
# Após 100 consultas bem-sucedidas usando ambos
# Sistema APRENDE que relação é mais importante

ajustar_peso_aresta(
    origem="spark",
    destino="python",
    novo_peso=calcular_peso_dinamico(
        uso_frequencia=100,           # quantas vezes foi útil
        qualidade_media=0.92,          # impacto na qualidade
        feedback_positivo=0.95,        # consultas bem-sucedidas
        tempo_decaimento=30            # relevância temporal
    )
)
# Resultado: peso sobe para 0.93! 📈
```

**💡 Benefício**: Relações mais usadas ficam mais fortes, melhorando contexto automaticamente.

#### 2️⃣ Aprendizado Ativo (Fase 2 - Planejado)

**Objetivo**: Sistema identifica gaps e sugere o que aprender.

**Como funciona**:

```python
# 📊 Sistema analisa histórico de consultas
gaps = identificar_gaps_conhecimento()

# Retorna:
[
    {
        "gap": "Spark + Kubernetes",
        "frequencia_consultas": 23,
        "qualidade_media": 0.45,  # BAIXA!
        "prioridade": "ALTA",
        "sugestao": "Indexar documentação oficial Spark on K8s"
    },
    {
        "gap": "Polars + Machine Learning",
        "frequencia_consultas": 12,
        "qualidade_media": 0.52,
        "prioridade": "MÉDIA",
        "sugestao": "Adicionar exemplos de integração Polars-sklearn"
    }
]

# 🎯 Sistema prioriza documentos para indexação
priorizar_indexacao(gaps, limite_top=5)
```

**💡 Benefício**: Sistema sabe o que NÃO sabe e busca preencher lacunas.

#### 3️⃣ Consolidação Automática (Fase 3 - Futuro)

**Objetivo**: Evitar redundância, mesclar conhecimento similar.

**Como funciona**:

```python
# 🔍 Sistema encontra descobertas similares:
descobertas_similares = [
    {"desc": "Spark usa Python", "confianca": 0.85},
    {"desc": "Python é linguagem para Spark", "confianca": 0.82},
    {"desc": "PySpark é API Python do Spark", "confianca": 0.90}
]

# 🔄 Consolida em uma descoberta mais forte
descoberta_consolidada = consolidar_descobertas(
    descobertas_similares,
    estrategia="media_ponderada"
)

# ✨ Resultado:
{
    "desc": "Spark tem integração nativa com Python via PySpark",
    "confianca": 0.92,  # média ponderada: (0.85*1 + 0.82*1 + 0.90*3)/5
    "evidencias_combinadas": 15,
    "descobertas_originais": [disc1_id, disc2_id, disc3_id]
}
```

**💡 Benefício**: Conhecimento mais limpo, preciso e sem duplicação.

#### 4️⃣ Meta-Aprendizado (Fase 3 - Futuro)

**Objetivo**: Aprender sobre o próprio processo de aprendizado.

**Como funciona**:

```python
# 🧠 Sistema analisa eficácia de seus próprios padrões
meta_analise = analisar_eficacia_descobertas(
    periodo="ultimos_30_dias"
)

# 📊 Descobre meta-padrões:
{
    "insights": [
        {
            "padrao": "Descobertas tipo 'correlacao' com confiança > 0.85",
            "impacto": "+23% qualidade nas próximas 5 consultas",
            "recomendacao": "PRIORIZAR este tipo de descoberta"
        },
        {
            "padrao": "Relações grafo com peso > 0.9",
            "impacto": "+18% velocidade de resposta",
            "recomendacao": "Cache agressivo destas conexões"
        },
        {
            "padrao": "Consultas híbridas (4 camadas)",
            "impacto": "+31% satisfação do agente",
            "recomendacao": "Sugerir modo híbrido por padrão"
        }
    ]
}

# 🎯 Sistema AJUSTA seu comportamento baseado em meta-insights
aplicar_otimizacoes(meta_analise["insights"])
```

**💡 Benefício**: Sistema se otimiza continuamente, ficando mais eficiente com o tempo.

#### 5️⃣ Auto-Regularização Temporal (Fase 3 - Futuro)

**Objetivo**: Sistema se auto-regula sem intervenção externa.

**🌀 Princípio Sistêmico**: Pesos se ajustam pelo **próprio uso**, não por administração manual!

**Como funciona**:

```python
# ⏱️ AUTO-REGULARIZAÇÃO EMERGENTE
def ciclo_auto_regulacao(frequencia="diario"):
    """
    Sistema mantém homeostase sem intervenção humana.
    Regulação acontece PELO uso, não CONTRA o uso.
    """
    
    hoje = datetime.now()
    
    # 📉 DECAIMENTO NATURAL (conhecimento não usado enfraquece)
    for aresta in grafo.todas_arestas():
        dias_sem_uso = (hoje - aresta.ultimo_uso).days
        
        if dias_sem_uso > 0:
            # Decaimento exponencial baseado em tempo
            fator_decaimento = 0.98 ** (dias_sem_uso / 7)  # ~2% por semana
            novo_peso = aresta.peso * fator_decaimento
            
            # Limiar mínimo: remove se muito fraco
            if novo_peso < 0.1:
                grafo.remover_aresta(aresta)
                registrar_evento("aresta_esquecida", aresta.id)
            else:
                aresta.atualizar(peso=novo_peso)
    
    # 📈 FORTALECIMENTO NATURAL (já acontece no feedback loop!)
    # Consultas que usam relações fortalecem automaticamente o peso
    # (implementado em calcular_peso_dinamico - funcionalidade 1)
    
    # ⚖️ NORMALIZAÇÃO (evita inflação de pesos)
    for nodo in grafo.todos_nodos():
        arestas_saida = nodo.arestas_saindo()
        
        # Se soma dos pesos > 10.0, normaliza
        soma_pesos = sum(a.peso for a in arestas_saida)
        if soma_pesos > 10.0:
            for aresta in arestas_saida:
                aresta.peso = (aresta.peso / soma_pesos) * 10.0
    
    # 🧹 LIMPEZA DE DESCOBERTAS OBSOLETAS
    for descoberta in historico.descobertas_antigas(dias=90):
        # Se descoberta não gerou relação útil em 90 dias, arquiva
        if not descoberta.aplicada_grafo or descoberta.uso_contagem == 0:
            historico.arquivar(descoberta)
    
    # 📊 QUALIDADE: Decaimento de scores antigos
    for consulta in historico.consultas_antigas(dias=30):
        # Scores antigos têm peso menor em análises
        consulta.peso_temporal = 0.5 ** (consulta.idade_dias / 30)

# 🔄 Execução automática (cron job interno)
scheduler.add_job(
    ciclo_auto_regulacao,
    trigger="cron",
    hour=3,  # 3h da manhã
    args=["diario"]
)
```

**🌀 Por que isso é sistêmico?**

| Aspecto | Anti-Sistêmico ❌ | Sistêmico ✅ |
|---------|-------------------|--------------|
| **Quem decide** | Administrador externo | Sistema observa seu próprio uso |
| **Critério** | Regra fixa arbitrária | Padrões emergentes de uso real |
| **Frequência** | Manual, irregular | Automática, rítmica (circadiana) |
| **Objetivo** | "Limpar banco de dados" | Manter homeostase do conhecimento |
| **Efeito** | Quebra feedback loops | Reforça feedback loops |

**💡 Benefício**: Sistema mantém saúde do conhecimento sem intervenção humana - como um organismo vivo que elimina células mortas e fortalece conexões neurais ativas! 🧠

**⚠️ Importante**: Regularização é **consequência** do sistema funcionando, não uma **intervenção** no sistema.

### 🌍 Insight Filosófico: Pesos como Epistemologia

> **Os pesos não são apenas números - eles representam a visão de mundo do agente.** 🧠

Cada agente que interage com o sistema **molda** os pesos através de suas consultas e descobertas. Com o tempo:

- **Pesos altos** = Conexões que o agente considera **fundamentais** (usadas frequentemente, alta qualidade)
- **Pesos baixos** = Conexões **periféricas** ou **experimentais** (pouco usadas ou baixo impacto)
- **Ausência de aresta** = Relação que **não existe** na experiência desse agente

#### 📊 Exemplo: Dois Agentes, Dois Mundos

```python
# AGENTE A: Desenvolvedor Python/Data Science
grafo_agente_a = {
    "spark": {
        "python": 0.95,      # "Spark É Python (PySpark)!"
        "scala": 0.30,       # "Scala? Raramente uso..."
        "java": 0.20         # "Java? Legado..."
    }
}

# AGENTE B: Engenheiro Big Data tradicional
grafo_agente_b = {
    "spark": {
        "scala": 0.92,       # "Spark native em Scala!"
        "java": 0.75,        # "JVM é a base"
        "python": 0.45       # "Python é só API"
    }
}

# MESMA ENTIDADE "spark", VISÕES DE MUNDO DIFERENTES! 🌍
```

#### 🌀 Implicações Sistêmicas

1. **Conhecimento é Situado**: Não existe "verdade absoluta" dos pesos - eles refletem a **experiência situada** do agente

2. **Múltiplas Epistemologias**: Se múltiplos agentes usam o mesmo sistema, cada um deveria ter seu **próprio espaço de pesos**?

3. **Consenso Emergente**: Ou os pesos convergem para um **consenso coletivo** (média ponderada de todas as experiências)?

4. **Evolução Temporal**: Agente hoje pode ter visão diferente do agente amanhã - pesos capturam essa **trajetória epistêmica**

#### 💡 Questão em Aberto

```python
# OPÇÃO 1: Pesos compartilhados (consenso coletivo)
# Todos os agentes moldam o MESMO grafo
# Benefício: Conhecimento coletivo convergente
# Risco: Visões minoritárias são suprimidas

# OPÇÃO 2: Pesos por agente (epistemologias múltiplas)  
# Cada agente tem SEU grafo de pesos
# Benefício: Respeita diversidade epistêmica
# Risco: Fragmentação, sem aprendizado coletivo

# OPÇÃO 3: Pesos híbridos (base comum + delta pessoal)
grafo_agente = grafo_base + agente.delta_experiencia
# Benefício: Equilíbrio entre coletivo e individual
# Complexidade: Gestão de duas camadas de pesos
```

**🌱 Para o Nhandereko ("nosso modo de ser juntos")**: A Opção 3 parece mais alinhada - há uma base compartilhada (conhecimento coletivo), mas cada agente tem sua própria lente (experiência situada).

> *"O mapa não é o território, mas os pesos do agente são o mapa que ele carrega."* 🗺️

---

## 📚 Glossário Técnico

### 🗂️ Conceitos de Arquitetura

| Termo | Camada | Definição | Exemplo |
|-------|--------|-----------|---------|
| **🧠 Embedding** | 4 (Memória) | Representação vetorial de texto que captura significado semântico | "spark" → [0.23, -0.45, 0.67, ...] |
| **🕸️ Grafo de Conhecimento** | 3 (Relacional) | Estrutura que conecta conceitos através de relações tipadas | `spark →(usa)→ python` |
| **📊 Star Schema** | 1-2 (Estrutura/Histórico) | Modelo dimensional com fatos centrais e dimensões descritivas | Fatos conectam a dimensões via FK |
| **🔄 Feedback Loop** | Todas | Ciclo onde outputs influenciam inputs futuros, criando aprendizado | Consulta → Descoberta → Melhora próxima consulta |

### 💡 Conceitos de Aprendizado

| Termo | Tipo | Definição | Threshold de Qualidade |
|-------|------|-----------|------------------------|
| **💡 Descoberta** | Evento | Padrão ou correlação identificada automaticamente pelo sistema | Confiança ≥ 0.80 |
| **🎯 Confiança** | Métrica | Score (0-1) que indica certeza sobre uma descoberta | 0.85 = 85% de certeza |
| **⬇️ Sintetizar** | Operação | Condensar conhecimento abstrato em estruturas concretas | Embeddings → Entidades |
| **⬆️ Expandir** | Operação | Ampliar conhecimento concreto para contextos mais amplos | Entidades → Grafo → Embeddings |

### �️ Conceitos de Dados

| Termo | Camada | Definição | Característica |
|-------|--------|-----------|----------------|
| **�🔗 Aresta** | 3 (Grafo) | Conexão direcionada e tipada entre dois nós | Tem peso, tipo e evidências |
| **📈 Fato** | 2 (Histórico) | Registro de evento ou medição que ocorreu no tempo | Imutável, timestampado |
| **🏛️ Dimensão** | 1 (Estrutural) | Contexto descritivo estável (muda pouco) | Entidades, Conceitos, Tempo, Agentes |
| **🔍 Consulta Híbrida** | Todas | Busca que usa as 4 camadas simultaneamente | Qualidade ~20-35% superior |

---

## 🎓 Resumo Executivo

> **Este sistema transforma um banco de dados passivo em um parceiro ativo que aprende com cada interação.** 🧠✨

### ✨ Diferenciais Chave

1. **🔄 Autoaperfeiçoamento Contínuo**
   - Cada consulta alimenta o sistema
   - Descobertas criam novas conexões
   - Relações ficam mais fortes com uso
   - Qualidade cresce ~20-35% ao longo do tempo

2. **🧠 Arquitetura Multi-Camadas Integrada**
   - **4 tipos de conhecimento** trabalhando juntos
   - **Fluxos bidirecionais** (⬇️ Sintetizar ⬆️ Expandir)
   - **Feedback loops** em todos os níveis
   - **Contexto enriquecido** automaticamente

3. **🔍 Transparência e Auditabilidade Total**
   - Todo conhecimento tem origem rastreável
   - Confiança explícita em cada descoberta
   - Histórico completo de aprendizado
   - Evidências linkadas a cada relação

4. **📈 Escalabilidade do Protótipo à Produção**
   - SQLite → PostgreSQL (zero refatoração)
   - NetworkX → Neo4j (mesma interface)
   - ChromaDB → produção ready
   - Spark para processamento paralelo

### 🎯 Resultado Final: Um Orquestrador Que Aprende

```text
╔════════════════════════════════════════════════════════════╗
║  ANTES                  →  DEPOIS                          ║
╠════════════════════════════════════════════════════════════╣
║  🗄️  Database estático    🧠 Parceiro inteligente          ║
║  🔍 Busca passiva         🔮 Contextualização ativa         ║
║  📊 Armazena dados        💡 Descobre padrões               ║
║  ⚡ Responde queries      🌀 Aprende continuamente          ║
║  📋 Lista resultados      ✨ Enriquece conhecimento         ║
╚════════════════════════════════════════════════════════════╝
```

Um orquestrador inteligente que não apenas **busca** informação, mas **aprende**, **estrutura**, **conecta** e **evolui** seu conhecimento de forma autônoma e transparente.

**🌱 O futuro do conhecimento é vivo, recursivo e colaborativo.**

Um orquestrador inteligente que não apenas **busca** informação, mas **aprende**, **estrutura** e **evolui** seu conhecimento de forma autônoma e transparente.

---

## 💖 Créditos

---

## 💖 Créditos

### Construído com ❤️ para sistemas que aprendem

*Porque conhecimento não é estático - ele evolui.* 🚀

**Arquitetura Nhandereko**  
**Versão**: 1.0.0  
**Última atualização**: 25 de Janeiro de 2025  
**Status**: ✅ Fundação completa | 🏗️ Fase 2 em desenvolvimento

---

*"O conhecimento emerge das conexões, não dos dados isolados."* 🌀


