# 📊 Métricas de Síntese e Expansão

Este documento define as métricas para medir a qualidade das três ordens operacionais do Nhandereko.

## 🔵 Métricas de Primeira Ordem (Consultar/Sintetizar)

### Qualidade de Síntese

**Definição**: Mede quão bem o sistema sintetiza conhecimento (não apenas retorna dados brutos).

**Fórmula**:
```
score_sintese = (
    0.3 * completude +      # Informação está completa?
    0.3 * coerencia +        # Síntese é coerente?
    0.2 * contexto +         # Contexto adequado fornecido?
    0.2 * utilidade          # Resposta é útil/acionável?
)
```

**Componentes**:

1. **Completude** (0-1):
   - Tem descrição? +0.3
   - Tem relações mapeadas? +0.3
   - Tem contexto semântico? +0.4

2. **Coerência** (0-1):
   - Informações consistentes entre fontes
   - Sem contradições
   - Organização lógica

3. **Contexto** (0-1):
   - Quantas camadas foram consultadas (estrutural, grafo, vetorial)
   - Profundidade das relações mapeadas

4. **Utilidade** (0-1):
   - Resposta diretamente aplicável?
   - Insights identificados?
   - Próximos passos sugeridos?

**Threshold**: score_sintese >= 0.75 indica síntese de alta qualidade

---

## 🟢 Métricas de Segunda Ordem (Registrar/Expandir)

### Grau de Expansão

**Definição**: Mede quanto o conhecimento foi expandido (não apenas acumulado).

**Fórmula**:
```
grau_expansao = (
    0.4 * taxa_conectividade +     # Novas conexões criadas
    0.3 * enriquecimento +          # Entidades existentes enriquecidas
    0.2 * profundidade_rede +       # Conexões indiretas fortalecidas
    0.1 * diversidade               # Tipos de relações variadas
)
```

**Componentes**:

1. **Taxa de Conectividade** (0-1):
   ```
   taxa = conexoes_criadas / (entidades_novas + entidades_enriquecidas)
   ```
   - Ideal: cada entidade tem 2-3 conexões
   - < 0.5: acumulação (ruim)
   - >= 0.5: expansão (bom)
   - > 1.0: hiperconectividade (ótimo)

2. **Enriquecimento** (0-1):
   ```
   taxa = entidades_enriquecidas / total_entidades_processadas
   ```
   - Alto: conhecimento novo conecta com existente
   - Baixo: conhecimento isolado

3. **Profundidade de Rede** (0-1):
   - Conexões indiretas criadas (A→B, B→C implica A→C)
   - Triângulos formados (A→B, B→C, C→A)
   - Comunidades detectadas

4. **Diversidade** (0-1):
   - Quantidade de tipos de relações diferentes
   - Evita rede monótona

**Threshold**: grau_expansao >= 0.6 indica expansão saudável

---

## 🟣 Métricas de Terceira Ordem (Sintetizar + Expandir)

### Equilíbrio Síntese-Expansão

**Definição**: Mede o equilíbrio entre processar conhecimento (síntese) e criar conhecimento (expansão).

**Fórmula**:
```
score_terceira = sqrt(score_sintese * grau_expansao) * fator_feedback
```

Onde:
- `sqrt()` = média geométrica (requer que ambos sejam bons)
- `fator_feedback` = qualidade do feedback loop (0.8-1.2)

**Fator de Feedback** (0.8-1.2):
```
fator = 1.0 + (
    0.1 * descobertas_registradas +    # Novas descobertas?
    0.1 * metricas_coletadas -         # Métricas foram coletadas?
    0.1 * tempo_excessivo              # Penaliza se muito lento
)
```

**Características da Terceira Ordem de Qualidade**:

1. **Síntese >= 0.75** (Primeira Ordem bem executada)
2. **Expansão >= 0.6** (Segunda Ordem bem executada)
3. **Feedback Loop Completo**:
   - Consulta registrada em `fato_consulta`
   - Descobertas em `fato_descoberta` (se houver)
   - Relações criadas/fortalecidas no grafo
   - Métricas de qualidade coletadas

**Threshold**: score_terceira >= 0.7 indica terceira ordem de excelência

---

## 📈 Métricas Agregadas (Sistema como um Todo)

### Evolução do Sistema (Loop Nível 2)

**Taxa de Aprendizado**:
```
taxa_aprendizado = (
    delta_conhecimento_semana / conhecimento_total
)
```

Onde:
- `delta_conhecimento_semana` = entidades + relações + documentos novos
- `conhecimento_total` = base atual

**Taxa saudável**: 5-15% de crescimento semanal

**Densidade do Grafo**:
```
densidade = arestas_reais / arestas_possiveis
densidade = arestas / (nós * (nós - 1) / 2)
```

- Baixa (< 0.1): conhecimento fragmentado
- Média (0.1-0.3): rede saudável
- Alta (> 0.3): talvez overconnected

**Qualidade Média das Sínteses**:
```
qualidade_media = sum(scores_sintese) / total_consultas
```

Deve aumentar com o tempo conforme sistema aprende.

---

## 🔬 Endpoints de Métricas

Implementar endpoints para expor essas métricas:

```python
GET /metricas/sintese
{
    "periodo": "ultima_semana",
    "score_medio": 0.82,
    "consultas_analisadas": 147,
    "distribuicao": {
        "excelentes": 89,  # >= 0.8
        "boas": 45,        # 0.6-0.8
        "fracas": 13       # < 0.6
    }
}

GET /metricas/expansao
{
    "periodo": "ultimo_mes",
    "grau_medio": 0.68,
    "entidades_novas": 234,
    "entidades_enriquecidas": 456,
    "conexoes_criadas": 789,
    "taxa_conectividade": 1.14
}

GET /metricas/terceira-ordem
{
    "periodo": "ultimo_mes",
    "score_medio": 0.73,
    "feedback_loops_completos": 89,
    "feedback_loops_parciais": 34,
    "descobertas_registradas": 67,
    "equilibrio": "saudavel"  # ou "desequilibrado_sintese" / "desequilibrado_expansao"
}

GET /metricas/evolucao
{
    "conhecimento_total": {
        "entidades": 1234,
        "relacoes": 3456,
        "documentos": 2345
    },
    "taxa_aprendizado_semanal": 0.12,
    "densidade_grafo": 0.23,
    "qualidade_media_sintese": 0.81,
    "tendencia": "crescimento_saudavel"
}
```

---

## 📊 Dashboard de Visualização

Criar visualizações para:

1. **Gráfico de Evolução Temporal**:
   - Linha do tempo: síntese, expansão, terceira ordem
   - Identificar padrões e anomalias

2. **Mapa de Calor do Grafo**:
   - Nós mais conectados
   - Clusters de conhecimento
   - Áreas isoladas (oportunidades de expansão)

3. **Funil de Qualidade**:
   - Quantas consultas atingem cada threshold
   - Identificar gargalos

4. **Matriz de Equilíbrio**:
   - Eixo X: Score de Síntese
   - Eixo Y: Grau de Expansão
   - Quadrante ideal: alto em ambos

---

## 🎯 Objetivos de Qualidade

### Primeira Ordem (Consultar/Sintetizar)
- **Meta**: 80% das consultas com score >= 0.75
- **Ação se abaixo**: Melhorar algoritmos de síntese, enriquecer fontes

### Segunda Ordem (Registrar/Expandir)
- **Meta**: Taxa de conectividade >= 0.8
- **Ação se abaixo**: Melhorar detecção de relações, enriquecer grafo

### Terceira Ordem (Sintetizar + Expandir)
- **Meta**: 70% dos loops completos com score >= 0.7
- **Ação se abaixo**: Revisar processo de feedback, treinar agentes

### Sistema (Evolução Contínua)
- **Meta**: Taxa de aprendizado 8-12% semanal
- **Meta**: Densidade grafo 0.15-0.25
- **Meta**: Qualidade média síntese > 0.75

---

## 💡 Uso Prático

### Para Agentes

Ao executar tarefas, verificar métricas:

```python
# Após síntese (Primeira Ordem)
if score_sintese < 0.75:
    logging.warning("Síntese de baixa qualidade, considere refinar")

# Após expansão (Segunda Ordem)
if taxa_conectividade < 0.5:
    logging.warning("Conhecimento sendo acumulado, não expandido")

# Após feedback (Terceira Ordem)
if score_terceira < 0.7:
    logging.warning("Loop não está funcionando bem")
```

### Para Desenvolvedores

Monitorar métricas agregadas:

```bash
# Verificar saúde do sistema
curl http://localhost:8000/metricas/evolucao

# Identificar problemas
if qualidade_media < 0.75:
    # Melhorar algoritmos de síntese
    
if taxa_conectividade < 0.5:
    # Melhorar detecção de relações
```

---

**Versão**: 1.0.0  
**Última atualização**: 2025-10-25  
**Filosofia**: Medir não para controlar, mas para aprender e evoluir. 🌱
