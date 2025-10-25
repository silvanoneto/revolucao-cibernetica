# 📋 Exemplo de Uso: Como Passar Tarefas ao Agente

Este documento mostra exemplos práticos de como estruturar o prompt completo para o agente, incluindo o guia (README do Nhandereko) e a tarefa.

---

## 🎯 Processo de Refinamento

Antes de executar qualquer tarefa, o agente deve fazer uma **troca interna de perguntas e respostas** para refinar seu plano de ação:

### Template de Refinamento

```text
📋 REFINAMENTO DA TAREFA

1️⃣ Qual é o objetivo da tarefa?
   → [Descreva o objetivo claramente]

2️⃣ Qual ordem operacional é apropriada?
   → 🔵 Primeira (apenas consultar/sintetizar)
   → 🟢 Segunda (registrar/expandir conhecimento)
   → 🟣 Terceira (consultar + aprender + expandir)

3️⃣ Quais camadas do sistema preciso usar?
   → 🏛️ SQL (fatos estruturados)
   → 🕸️ Graph (relações e navegação)
   → 🧠 Vector (busca semântica)

4️⃣ Quais endpoints vou chamar e em que ordem?
   → [Liste os endpoints específicos]

5️⃣ Como vou sintetizar/processar os resultados?
   → [Descreva a estratégia de síntese]

6️⃣ (Se 3ª ordem) Que feedback vou registrar?
   → Consultas, descobertas, novas relações
```

---

## Estrutura Geral

### Básica (Mínima)

```text
[README DO NHANDEREKO]
---
[DESCRIÇÃO DA TAREFA]
---
[CONTEXTO ADICIONAL (opcional)]
```

### Completa (Recomendada para início do loop)

```text
[README DO PROJETO]
---
[README DO NHANDEREKO]
---
[DESCRIÇÃO DA TAREFA]
---
[CONTEXTO ADICIONAL (opcional)]
```

> **💡 Dica**: Para a **primeira interação** ou para dar **contexto completo ao agente**, inclua o README do projeto principal (`revolucao-cibernetica/README.md`) antes do README do Nhandereko. Isso ajuda o agente a entender o propósito filosófico e conceitual antes de trabalhar com a API técnica.

---

## Exemplo 1: Consulta Simples (Primeira Ordem - Consultar/Sintetizar)

### 🎯 Objetivo da Primeira Ordem

Não apenas **buscar dados brutos**, mas **sintetizar conhecimento** - processar e condensar informação em insights úteis.

```markdown
=== GUIA DO AGENTE ===
[Todo o conteúdo do nhandereko/README.md]

===================================

=== TAREFA ===

**Query do usuário**: "O que é Polars?"

===================================

=== REFINAMENTO (Interno do Agente) ===

1️⃣ Qual é o objetivo da tarefa?
   → Fornecer uma síntese clara e contextualizada sobre Polars

2️⃣ Qual ordem operacional é apropriada?
   → 🔵 PRIMEIRA (apenas consultar/sintetizar - não registrar feedback)

3️⃣ Quais camadas do sistema preciso usar?
   → 🏛️ SQL (buscar entidade "polars")
   → 🧠 Vector (busca semântica "O que é Polars")
   → 🕸️ Graph (relações de "polars" com outras entidades)

4️⃣ Quais endpoints vou chamar e em que ordem?
   → GET /sql/entidade/polars
   → POST /buscar (query: "O que é Polars?", top_k: 5)
   → GET /grafo/vizinhos/polars

5️⃣ Como vou sintetizar/processar os resultados?
   → Combinar informações estruturadas + semânticas + relacionais
   → Condensar em: definição, características-chave, relações, contexto de uso
   → Apresentar resposta coerente e útil (não dump de dados)

6️⃣ Que feedback vou registrar?
   → NENHUM (Primeira Ordem é read-only)

===================================

=== EXECUÇÃO ===

[Agente executa os endpoints planejados]

===================================

=== SÍNTESE PARA O USUÁRIO ===
```

**Exemplo de resposta sintetizada** (não apenas dump de dados):

```text
Polars é uma biblioteca moderna de processamento de dados escrita em Rust, 
posicionada como alternativa ao Pandas. Principais características:

- Performance: até 10x mais rápida que Pandas em operações grandes
- Memória eficiente: lazy evaluation e streaming
- API familiar: sintaxe similar ao Pandas
- Conexão: Rust → Python via PyO3

Contexto: Ideal para big data, ETL pipelines, e análises que excedem 
memória RAM. Complementa (não substitui) o ecossistema pandas/numpy.
```

---

## Exemplo 2: Indexação de Documento (Segunda Ordem - Registrar/Expandir)

### 🎯 Objetivo da Segunda Ordem

Não apenas **acumular dados**, mas **expandir a rede de conhecimento** - criar conexões e enriquecer o grafo semântico.

```markdown
=== GUIA DO AGENTE ===
[Todo o conteúdo do nhandereko/README.md]

===================================

=== TAREFA ===

**Tipo**: Indexação e Expansão de Conhecimento
**Ordem**: SEGUNDA (Registrar/Expandir)
**Objetivo**: Processar documento e EXPANDIR a rede de conhecimento

**Documento fornecido**:

```text
[Conteúdo do documento ou caminho para o arquivo]
```

**Instruções**:

1. Extraia entidades, conceitos e relações do documento
2. **EXPANDA** o conhecimento existente:
   - Detecte conexões com entidades já existentes no sistema
   - Crie links bidirecionais no grafo
   - Identifique relações implícitas
   - Enriqueça embeddings com contexto expandido
3. Registre todas as informações usando os endpoints POST
4. NÃO apenas consulte (Segunda Ordem - foco em expansão)
5. Reporte ao final:
   - Quantas entidades novas foram adicionadas
   - Quantas conexões foram criadas
   - Grau de expansão da rede (novas arestas/nós)

**Base URL do servidor**: <http://localhost:8000>

**Critérios de qualidade para expansão**:

- Extraia apenas informações com alta confiança (> 0.75)
- Prefira entidades bem definidas a genéricas
- Normalize nomes de entidades (lowercase, slugify)
- **PRIORIZE** criação de relações e conexões
- **ENRIQUEÇA** entidades existentes com novo contexto

**Métricas de Expansão**:

- Novas entidades: X
- Novas relações: Y
- Entidades enriquecidas: Z
- Taxa de conectividade: Y/(X+Z)

```markdown

---

## Exemplo 3: Consulta com Aprendizado (Terceira Ordem - Sintetizar + Expandir)

### 🎯 Objetivo da Terceira Ordem

Fazer **ambos simultaneamente**: sintetizar conhecimento existente E expandir com novas descobertas. A terceira ordem **contém e transcende** as duas primeiras.

```markdown
=== GUIA DO AGENTE ===
[Todo o conteúdo do nhandereko/README.md]

===================================

=== TAREFA ===

**Tipo**: Consulta com Feedback Loop Completo
**Ordem**: TERCEIRA (Sintetizar + Expandir)
**Query do usuário**: "Qual a diferença entre Polars e Pandas?"

**Instruções**:

**Fase 1: SINTETIZAR (Primeira Ordem embutida)**

1. Consulte o servidor nas camadas: estrutural, memória, grafo
2. **Sintetize** os resultados em insights úteis:
   - Processe dados brutos em conhecimento estruturado
   - Identifique conceitos-chave e relações
   - Condense informação em resposta clara

**Fase 2: EXPANDIR (Segunda Ordem embutida)**

3. Durante a análise, **detecte novas conexões**:
   - Padrões que emergem da comparação
   - Relações implícitas entre Polars e Pandas
   - Contextos de uso complementares vs excludentes
4. **Expanda** a rede de conhecimento:
   - Registre descobertas com alta confiança
   - Crie/fortaleça arestas no grafo
   - Enriqueça embeddings com novo contexto

**Fase 3: FEEDBACK LOOP (Integração)**

5. Registre feedback completo que alimenta o sistema:
   - Consulta em `fato_consulta` (métricas de qualidade)
   - Descobertas em `fato_descoberta` (novas relações identificadas)
   - Arestas no grafo (conexões fortalecidas/criadas)
   - Padrões de interação entre entidades

**Identificador do agente**: claude-dev-001

**Base URL do servidor**: http://localhost:8000

**Resultado Esperado**:

- Resposta sintetizada ao usuário (Primeira Ordem)
- Conhecimento expandido no sistema (Segunda Ordem)  
- Feedback que melhora futuras consultas (Terceira Ordem)

**Métricas esperadas**:

- Tempo de execução < 500ms
- Score de síntese > 0.80
- Pelo menos 1 descoberta com confiança > 0.75
- Taxa de expansão: novas conexões / conceitos envolvidos > 0.5
```

**Exemplo de Output Completo**:

```text
=== SÍNTESE PARA O USUÁRIO ===
Polars vs Pandas - Comparação sintetizada:

Performance: Polars 5-10x mais rápido (Rust vs C/Python)
Paradigma: Polars lazy + eager / Pandas apenas eager
API: Sintaxes similares mas filosofias diferentes
Uso: Polars para big data / Pandas para prototipagem

Recomendação: Complementares, não excludentes.

=== EXPANSÃO DO SISTEMA ===
✅ 3 novas relações criadas:
   - Polars ↔ "alternativa_de" → Pandas (peso: 0.85)
   - Polars ↔ "usa_linguagem" → Rust (peso: 0.92)
   - Pandas ↔ "baseado_em" → NumPy (peso: 0.88)

✅ 2 descobertas registradas:
   - "Polars e Pandas têm casos de uso complementares" (conf: 0.87)
   - "Rust é fator-chave de performance do Polars" (conf: 0.91)

✅ Feedback registrado:
   - Consulta #1247 | Qualidade: 0.89 | Tipo: comparação
   - Tempo: 342ms | Camadas: 3 | Descobertas: 2
```

---

## Exemplo 4: Pesquisa Web + Aprendizado (Segunda + Terceira)

```markdown
=== GUIA DO AGENTE ===
[Todo o conteúdo do nhandereko/README.md]

===================================

=== TAREFA ===

**Tipo**: Pesquisa e Aprendizado Híbrido
**Query do usuário**: "Pesquise sobre DuckDB e me diga como se compara ao Polars"

**Fluxo esperado**:

### Fase 1: Pesquisa Externa (Segunda Ordem)
1. Use web_search para buscar informações sobre DuckDB
2. Extraia entidades, conceitos e relações
3. Registre novas informações no servidor

### Fase 2: Consulta e Comparação (Terceira Ordem)
4. Consulte informações sobre Polars no servidor
5. Compare DuckDB e Polars
6. Identifique padrões e relações
7. Responda ao usuário

### Fase 3: Feedback Completo
8. Registre a consulta
9. Registre descobertas (comparação, diferenças, semelhanças)
10. Atualize o grafo com relações entre DuckDB e Polars

**Identificador do agente**: claude-dev-001

**Base URL do servidor**: http://localhost:8000

**Contexto adicional**:
- Foque em aspectos técnicos (performance, sintaxe, casos de uso)
- Priorize fontes oficiais e benchmarks reconhecidos
- Registre a fonte de cada informação nos metadados
```

---

## Estrutura de Arquivos Sugerida

Para facilitar o uso, mantenha:

```text
projeto/
├── README.md                          # Guia completo do agente
├── tarefas/
│   ├── consulta_simples.md            # Templates de tarefas
│   ├── indexacao.md
│   ├── consulta_aprendizado.md
│   └── analise_tendencias.md
└── executar_agente.py                 # Script que combina README + tarefa
```

## Script de Execução (Exemplo Python)

```python
#!/usr/bin/env python3
"""
Script para executar o agente com README + tarefa
"""

def executar_agente(tarefa_path: str):
    """
    Combina o README com a tarefa e envia ao agente
    """
    # Ler o README (guia do agente)
    with open('README.md', 'r') as f:
        readme = f.read()
    
    # Ler a tarefa
    with open(tarefa_path, 'r') as f:
        tarefa = f.read()
    
    # Combinar
    prompt_completo = f"""
{readme}

{'=' * 60}

{tarefa}
"""
    
    # Enviar ao agente (Claude API, por exemplo)
    resposta = enviar_para_agente(prompt_completo)
    
    return resposta

# Uso:
# resposta = executar_agente('tarefas/consulta_aprendizado.md')
```

---

## Checklist de Validação

Antes de executar, verifique:

✅ O guia está completo no prompt?  
✅ A tarefa especifica claramente a ordem?  
✅ A base URL do servidor está correta?  
✅ O identificador do agente está definido?  
✅ As instruções são claras e não ambíguas?  
✅ Os endpoints esperados estão documentados?  
✅ Critérios de sucesso estão definidos?  

---

## Dicas de Uso

1. **Seja específico na tarefa**: Quanto mais clara a instrução, melhor o resultado

2. **Defina sempre a ordem**: Mesmo que seja Terceira Ordem (padrão), explicite

3. **Forneça contexto**: URLs, identificadores, critérios de qualidade

4. **Estabeleça métricas**: Como saber se a tarefa foi bem executada?

5. **Itere**: Use as descobertas de uma tarefa para refinar a próxima

---

**Lembre-se**: O README contém todo o guia do agente, e as tarefas são dinâmicas.  
**Combine-os com sabedoria para desbloquear o poder do Nhandereko.** 🌱

