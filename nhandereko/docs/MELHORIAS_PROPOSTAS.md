# 🚀 Melhorias Propostas: Projeto Nhandereko

**Data**: 25 de Outubro de 2025  
**Versão Atual**: 1.0.0  
**Status**: Análise Estratégica e Roadmap

---

## 📊 Análise do Estado Atual

### ✅ Pontos Fortes

1. **Arquitetura Conceitual Sólida**
   - 4 camadas bem definidas (Estrutural, Histórica, Relacional, Memória)
   - Feedback loops implementados
   - Filosofia sistêmica clara (Nhandereko)

2. **Documentação Excelente**
   - TRES_LOOPS.md com modelo fractal
   - ARQUITETURA.md detalhada
   - README.md completo
   - EXEMPLOS.md práticos

3. **Fundação Técnica**
   - FastAPI para API REST
   - SQLite para dados estruturados/históricos
   - ChromaDB para embeddings
   - NetworkX para grafo

### ⚠️ Gaps Identificados

1. **Servidor (main.py)**
   - Endpoints desconectados da filosofia sistêmica
   - Faltam endpoints híbridos (4 camadas)
   - Não implementa auto-regularização
   - Ausência de métricas em tempo real

2. **Banco de Dados**
   - Schema não totalmente implementado conforme ARQUITETURA.md
   - Falta tabela `fato_interacao`
   - Sem tracking de pesos dinâmicos
   - Ausência de histórico de evolução

3. **Grafo**
   - Pesos estáticos (não evoluem com uso)
   - Sem decaimento temporal
   - Falta normalização automática
   - Não rastreia "último uso"

4. **Síntese/Expansão**
   - Módulo `sintese_expansao.py` existe mas não integrado aos endpoints
   - Faltam métricas de qualidade de síntese
   - Ausência de score de expansão

5. **Agentes**
   - Não há separação por agente nos pesos (visão de mundo única)
   - Falta tracking de trajetória epistêmica individual
   - Sem consenso coletivo vs. delta pessoal

---

## 🎯 Melhorias Prioritárias

### FASE 1: Fundação Sistêmica (Crítico - 2-3 semanas)

#### 1.1 Refatorar Endpoints para Arquitetura Híbrida

**Problema**: Endpoints atuais são isolados por camada. Sistema híbrido não existe na prática.

**Solução**:

```python
# server/main.py - NOVO endpoint híbrido

@app.post("/consultar/hibrida")
async def consultar_hibrida(
    query: str,
    agente_id: str,
    ordem: Literal["primeira", "segunda", "terceira"],
    top_k: int = 10
):
    """
    Consulta híbrida que usa as 4 camadas de forma integrada.
    
    Primeira Ordem: Read-only, sintetiza conhecimento
    Segunda Ordem: Write-only, expande conhecimento
    Terceira Ordem: Read-write, evolui conhecimento
    """
    inicio = datetime.now()
    
    # 1. 🧠 Camada 4: Busca semântica
    docs_memoria = await embeddings_manager.buscar(query, top_k)
    
    # 2. 🕸️ Camada 3: Expande com grafo
    entidades = extrair_entidades(docs_memoria)
    relacoes_grafo = graph_manager.expandir_contexto(entidades)
    
    # 3. 📊 Camada 2: Consulta descobertas históricas
    descobertas = db_manager.buscar_descobertas(
        entidades=entidades,
        min_confianca=0.8
    )
    
    # 4. 🏛️ Camada 1: Valida e enriquece com estrutura
    contexto_estrutural = db_manager.obter_contexto_entidades(entidades)
    
    # 5. SINTETIZAR resposta integrada
    resposta = SinteseManager.sintetizar_hibrida(
        memoria=docs_memoria,
        grafo=relacoes_grafo,
        historico=descobertas,
        estrutura=contexto_estrutural
    )
    
    # 6. Calcular qualidade
    qualidade = calcular_qualidade_sintese(resposta)
    
    # 7. REGISTRAR (se Segunda ou Terceira Ordem)
    if ordem in ["segunda", "terceira"]:
        tempo_ms = (datetime.now() - inicio).total_seconds() * 1000
        
        consulta_id = db_manager.registrar_consulta(
            agente=agente_id,
            tipo="hibrida",
            query=query,
            qualidade=qualidade,
            tempo_ms=tempo_ms,
            camadas_usadas="memoria,grafo,historico,estrutural"
        )
        
        # FEEDBACK LOOP: Fortalecer relações usadas
        if ordem == "terceira":
            graph_manager.fortalecer_relacoes_usadas(
                relacoes=relacoes_grafo,
                qualidade=qualidade
            )
    
    return {
        "sintese": resposta,
        "qualidade": qualidade,
        "camadas_usadas": 4,
        "ordem": ordem,
        "meta": {
            "docs_encontrados": len(docs_memoria),
            "relacoes_expandidas": len(relacoes_grafo),
            "descobertas_aplicadas": len(descobertas)
        }
    }
```

**Benefício**: Sistema funciona como documentado - 4 camadas integradas, não isoladas.

---

#### 1.2 Implementar Pesos Dinâmicos no Grafo

**Problema**: Pesos são estáticos. "Visão de mundo" não evolui.

**Solução**:

```python
# server/graph.py - ADICIONAR

class GraphManager:
    
    def fortalecer_relacoes_usadas(self, relacoes: List[Tuple], qualidade: float):
        """
        Fortalecer pesos de relações que foram úteis em uma consulta.
        
        Implementa: feedback positivo → peso aumenta
        """
        for (origem, destino, tipo) in relacoes:
            aresta = self.graph[origem][destino][tipo]
            
            # Peso atual
            peso_atual = aresta.get('peso', 0.5)
            
            # Incremento baseado em qualidade
            incremento = qualidade * 0.05  # Max 5% por consulta
            
            # Novo peso (limitado a 1.0)
            novo_peso = min(1.0, peso_atual + incremento)
            
            # Atualizar
            aresta['peso'] = novo_peso
            aresta['ultimo_uso'] = datetime.now().isoformat()
            aresta['contador_uso'] = aresta.get('contador_uso', 0) + 1
            
            # Registrar no histórico
            self.db.registrar_interacao(
                origem=origem,
                destino=destino,
                tipo=tipo,
                intensidade=novo_peso,
                contexto=f"fortalecido_por_uso_qualidade_{qualidade}"
            )
    
    def decaimento_temporal_pesos(self, dias_inatividade: int = 30):
        """
        Aplicar decaimento exponencial em arestas não usadas.
        
        Implementa: auto-regularização - conhecimento não usado enfraquece
        """
        hoje = datetime.now()
        arestas_removidas = 0
        
        for origem, destinos in self.graph.adj.items():
            for destino, tipos in destinos.items():
                for tipo, aresta in tipos.items():
                    
                    # Calcular dias sem uso
                    ultimo_uso = datetime.fromisoformat(
                        aresta.get('ultimo_uso', hoje.isoformat())
                    )
                    dias_sem_uso = (hoje - ultimo_uso).days
                    
                    if dias_sem_uso > 0:
                        # Decaimento: 2% por semana (0.98^(dias/7))
                        fator = 0.98 ** (dias_sem_uso / 7)
                        peso_atual = aresta.get('peso', 0.5)
                        novo_peso = peso_atual * fator
                        
                        # Remover se muito fraco
                        if novo_peso < 0.1:
                            self.graph.remove_edge(origem, destino, tipo)
                            arestas_removidas += 1
                            
                            self.db.registrar_evento(
                                tipo="aresta_esquecida",
                                detalhes={
                                    "origem": origem,
                                    "destino": destino,
                                    "tipo_relacao": tipo,
                                    "dias_sem_uso": dias_sem_uso,
                                    "peso_final": novo_peso
                                }
                            )
                        else:
                            aresta['peso'] = novo_peso
        
        return {
            "arestas_removidas": arestas_removidas,
            "executado_em": hoje.isoformat()
        }
```

**Benefício**: Grafo se auto-regula, refletindo uso real. Pesos = visão de mundo emergente.

---

#### 1.3 Adicionar Métricas em Tempo Real

**Problema**: Sistema não sabe como está performando.

**Solução**:

```python
# server/main.py - NOVOS endpoints de métricas

@app.get("/metricas/qualidade-sintese")
async def metricas_qualidade_sintese(
    periodo: Literal["hoje", "semana", "mes"] = "semana",
    agente_id: Optional[str] = None
):
    """
    Métricas de qualidade de síntese (Primeira Ordem).
    """
    return db_manager.calcular_metricas_sintese(periodo, agente_id)

@app.get("/metricas/expansao-conhecimento")
async def metricas_expansao(
    periodo: Literal["hoje", "semana", "mes"] = "semana"
):
    """
    Métricas de expansão do grafo (Segunda Ordem).
    
    - Novas entidades criadas
    - Novas relações descobertas
    - Taxa de crescimento do grafo
    - Densidade do grafo
    """
    return {
        "novas_entidades": db_manager.contar_entidades_periodo(periodo),
        "novas_relacoes": graph_manager.contar_arestas_periodo(periodo),
        "densidade_grafo": graph_manager.calcular_densidade(),
        "taxa_crescimento": graph_manager.calcular_taxa_crescimento(periodo),
        "descobertas_aplicadas": db_manager.contar_descobertas_aplicadas(periodo)
    }

@app.get("/metricas/evolucao-agente/{agente_id}")
async def metricas_evolucao_agente(agente_id: str):
    """
    Trajetória epistêmica de um agente específico.
    
    Mostra como a "visão de mundo" do agente evoluiu.
    """
    return {
        "total_consultas": db_manager.contar_consultas(agente_id),
        "qualidade_media": db_manager.qualidade_media(agente_id),
        "evolucao_temporal": db_manager.qualidade_ao_longo_tempo(agente_id),
        "descobertas_realizadas": db_manager.listar_descobertas(agente_id),
        "entidades_mais_consultadas": db_manager.entidades_top(agente_id, top=10),
        "relacoes_mais_fortes": graph_manager.relacoes_top_agente(agente_id, top=10)
    }

@app.get("/metricas/saude-sistema")
async def metricas_saude():
    """
    Saúde geral do sistema Nhandereko.
    """
    return {
        "camadas": {
            "estrutural": {
                "entidades": db_manager.contar_entidades(),
                "conceitos": db_manager.contar_conceitos()
            },
            "historico": {
                "consultas_total": db_manager.contar_consultas_total(),
                "descobertas_total": db_manager.contar_descobertas_total(),
                "qualidade_media_geral": db_manager.qualidade_media_geral()
            },
            "grafo": {
                "nos": graph_manager.contar_nos(),
                "arestas": graph_manager.contar_arestas(),
                "densidade": graph_manager.calcular_densidade(),
                "componentes_conectados": graph_manager.contar_componentes()
            },
            "memoria": {
                "documentos": embeddings_manager.contar_documentos(),
                "dimensao_vetor": embeddings_manager.dimensao_vetor()
            }
        },
        "feedback_loops": {
            "taxa_aprendizado_semanal": db_manager.taxa_aprendizado_semanal(),
            "descobertas_aplicadas_percentual": db_manager.percentual_descobertas_aplicadas(),
            "consultas_hibridas_percentual": db_manager.percentual_hibridas()
        }
    }
```

**Benefício**: Visibilidade total do sistema. Permite monitorar se está realmente aprendendo.

---

### FASE 2: Epistemologias Múltiplas (Importante - 3-4 semanas)

#### 2.1 Implementar Pesos por Agente (Delta Pessoal)

**Problema**: Todos os agentes compartilham mesmo grafo. Não respeita diversidade epistêmica.

**Solução**: Modelo híbrido (base coletiva + delta individual)

```python
# server/graph.py - REFATORAR

class GraphManagerMultiAgente:
    """
    Grafo com dois níveis de pesos:
    1. Base coletiva (consenso de todos os agentes)
    2. Delta por agente (ajuste individual)
    """
    
    def __init__(self, db_manager):
        self.graph_base = nx.MultiDiGraph()  # Grafo coletivo
        self.deltas_agentes = {}  # {agente_id: {(o,d,t): delta_peso}}
        self.db = db_manager
    
    def get_peso(self, origem: str, destino: str, tipo: str, agente_id: str) -> float:
        """
        Retorna peso personalizado para um agente.
        
        peso_final = peso_base + delta_agente
        """
        # Peso base (consenso coletivo)
        try:
            peso_base = self.graph_base[origem][destino][tipo].get('peso', 0.5)
        except KeyError:
            peso_base = 0.5
        
        # Delta do agente
        if agente_id not in self.deltas_agentes:
            self.deltas_agentes[agente_id] = {}
        
        chave = (origem, destino, tipo)
        delta = self.deltas_agentes[agente_id].get(chave, 0.0)
        
        # Peso final (limitado entre 0 e 1)
        return max(0.0, min(1.0, peso_base + delta))
    
    def atualizar_peso_uso(self, origem, destino, tipo, agente_id, qualidade):
        """
        Atualiza peso baseado em uso.
        
        70% vai para base coletiva (consenso)
        30% vai para delta do agente (individual)
        """
        incremento_total = qualidade * 0.05
        
        # 70% para base coletiva
        incremento_base = incremento_total * 0.7
        peso_base_atual = self.graph_base[origem][destino][tipo].get('peso', 0.5)
        novo_peso_base = min(1.0, peso_base_atual + incremento_base)
        self.graph_base[origem][destino][tipo]['peso'] = novo_peso_base
        
        # 30% para delta do agente
        incremento_delta = incremento_total * 0.3
        chave = (origem, destino, tipo)
        
        if agente_id not in self.deltas_agentes:
            self.deltas_agentes[agente_id] = {}
        
        delta_atual = self.deltas_agentes[agente_id].get(chave, 0.0)
        novo_delta = min(0.5, max(-0.5, delta_atual + incremento_delta))  # Delta limitado ±0.5
        self.deltas_agentes[agente_id][chave] = novo_delta
        
        # Persistir no banco
        self.db.salvar_delta_agente(agente_id, origem, destino, tipo, novo_delta)
    
    def exportar_visao_mundo_agente(self, agente_id: str) -> Dict:
        """
        Exporta grafo personalizado de um agente.
        
        Mostra como aquele agente específico "vê o mundo".
        """
        grafo_agente = nx.MultiDiGraph()
        
        for origem, destino, tipo, dados in self.graph_base.edges(keys=True, data=True):
            peso_personalizado = self.get_peso(origem, destino, tipo, agente_id)
            
            if peso_personalizado > 0.1:  # Só incluir relações significativas
                grafo_agente.add_edge(
                    origem, destino, tipo,
                    peso=peso_personalizado,
                    peso_base=dados.get('peso', 0.5),
                    delta_agente=self.deltas_agentes.get(agente_id, {}).get((origem, destino, tipo), 0.0)
                )
        
        return {
            "agente_id": agente_id,
            "nos": list(grafo_agente.nodes()),
            "arestas": [
                {
                    "origem": u,
                    "destino": v,
                    "tipo": k,
                    "peso_final": d['peso'],
                    "peso_base": d['peso_base'],
                    "delta_pessoal": d['delta_agente']
                }
                for u, v, k, d in grafo_agente.edges(keys=True, data=True)
            ],
            "estatisticas": {
                "total_nos": grafo_agente.number_of_nodes(),
                "total_arestas": grafo_agente.number_of_edges(),
                "densidade": nx.density(grafo_agente),
                "divergencia_do_consenso": self._calcular_divergencia(agente_id)
            }
        }
    
    def _calcular_divergencia(self, agente_id: str) -> float:
        """
        Mede o quanto a visão do agente diverge do consenso coletivo.
        
        0.0 = idêntico ao consenso
        1.0 = completamente diferente
        """
        if agente_id not in self.deltas_agentes:
            return 0.0
        
        deltas = list(self.deltas_agentes[agente_id].values())
        if not deltas:
            return 0.0
        
        # Desvio médio absoluto dos deltas
        divergencia = sum(abs(d) for d in deltas) / len(deltas)
        return divergencia
```

**Benefício**: Sistema respeita que cada agente tem sua própria experiência, mas mantém conhecimento coletivo como base.

---

#### 2.2 Endpoint de Comparação Epistêmica

```python
@app.get("/epistemologia/comparar-agentes")
async def comparar_visoes_mundo(
    agente_a: str,
    agente_b: str
):
    """
    Compara visões de mundo de dois agentes.
    
    Mostra onde concordam e onde divergem.
    """
    grafo_a = graph_manager.exportar_visao_mundo_agente(agente_a)
    grafo_b = graph_manager.exportar_visao_mundo_agente(agente_b)
    
    # Relações comuns
    arestas_a = {(a['origem'], a['destino'], a['tipo']) for a in grafo_a['arestas']}
    arestas_b = {(a['origem'], a['destino'], a['tipo']) for a in grafo_b['arestas']}
    
    comuns = arestas_a & arestas_b
    apenas_a = arestas_a - arestas_b
    apenas_b = arestas_b - arestas_a
    
    # Diferenças de peso nas comuns
    diferencas_peso = []
    for origem, destino, tipo in comuns:
        peso_a = next(a['peso_final'] for a in grafo_a['arestas'] 
                      if (a['origem'], a['destino'], a['tipo']) == (origem, destino, tipo))
        peso_b = next(a['peso_final'] for a in grafo_b['arestas']
                      if (a['origem'], a['destino'], a['tipo']) == (origem, destino, tipo))
        
        if abs(peso_a - peso_b) > 0.2:  # Diferença significativa
            diferencas_peso.append({
                "relacao": f"{origem} → {destino} ({tipo})",
                "peso_agente_a": peso_a,
                "peso_agente_b": peso_b,
                "diferenca": peso_a - peso_b
            })
    
    return {
        "convergencia": {
            "relacoes_comuns": len(comuns),
            "percentual_comum": len(comuns) / len(arestas_a | arestas_b) * 100
        },
        "divergencia": {
            "apenas_agente_a": len(apenas_a),
            "apenas_agente_b": len(apenas_b),
            "pesos_divergentes": len(diferencas_peso)
        },
        "detalhes_divergencia": diferencas_peso[:10],  # Top 10
        "interpretacao": interpretar_divergencia(
            len(comuns), len(apenas_a), len(apenas_b), diferencas_peso
        )
    }
```

**Benefício**: Visibilidade de como diferentes agentes "enxergam" o mesmo conhecimento. Permite identificar visões complementares ou conflitantes.

---

### FASE 3: Auto-Regularização e Homeostase (Importante - 2 semanas)

#### 3.1 Job Automático de Manutenção

```python
# server/maintenance.py - NOVO ARQUIVO

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

class SystemMaintenance:
    """
    Manutenção automática do sistema Nhandereko.
    
    Executa tarefas de auto-regularização sem intervenção humana.
    """
    
    def __init__(self, graph_manager, db_manager, embeddings_manager):
        self.graph = graph_manager
        self.db = db_manager
        self.embeddings = embeddings_manager
        self.scheduler = AsyncIOScheduler()
    
    def start(self):
        """Inicia jobs automáticos."""
        
        # Job 1: Decaimento temporal de pesos (diário às 3h)
        self.scheduler.add_job(
            self.executar_decaimento_pesos,
            'cron',
            hour=3,
            minute=0,
            id='decaimento_pesos'
        )
        
        # Job 2: Limpeza de descobertas obsoletas (semanal, domingo 4h)
        self.scheduler.add_job(
            self.limpar_descobertas_obsoletas,
            'cron',
            day_of_week='sun',
            hour=4,
            minute=0,
            id='limpeza_descobertas'
        )
        
        # Job 3: Consolidação de descobertas similares (semanal, domingo 5h)
        self.scheduler.add_job(
            self.consolidar_descobertas_similares,
            'cron',
            day_of_week='sun',
            hour=5,
            minute=0,
            id='consolidacao_descobertas'
        )
        
        # Job 4: Normalização de pesos (mensal, dia 1 às 2h)
        self.scheduler.add_job(
            self.normalizar_pesos_grafo,
            'cron',
            day=1,
            hour=2,
            minute=0,
            id='normalizacao_pesos'
        )
        
        # Job 5: Cálculo de métricas consolidadas (diário às 6h)
        self.scheduler.add_job(
            self.calcular_metricas_consolidadas,
            'cron',
            hour=6,
            minute=0,
            id='metricas_consolidadas'
        )
        
        self.scheduler.start()
        print("🌀 Sistema de auto-regularização iniciado!")
    
    async def executar_decaimento_pesos(self):
        """Decaimento temporal - conhecimento não usado enfraquece."""
        print("⏱️  Executando decaimento temporal de pesos...")
        resultado = self.graph.decaimento_temporal_pesos(dias_inatividade=30)
        
        self.db.registrar_evento_sistema(
            tipo="decaimento_temporal",
            detalhes=resultado
        )
        
        print(f"✅ Decaimento concluído: {resultado['arestas_removidas']} arestas removidas")
    
    async def limpar_descobertas_obsoletas(self):
        """Remove descobertas que nunca foram aplicadas ao grafo."""
        print("🧹 Limpando descobertas obsoletas...")
        
        descobertas_obsoletas = self.db.buscar_descobertas(
            aplicada_grafo=False,
            dias_antigas=90,
            uso_contagem=0
        )
        
        arquivadas = 0
        for descoberta in descobertas_obsoletas:
            self.db.arquivar_descoberta(descoberta['id'])
            arquivadas += 1
        
        print(f"✅ {arquivadas} descobertas arquivadas")
    
    async def consolidar_descobertas_similares(self):
        """Mescla descobertas redundantes."""
        print("🔄 Consolidando descobertas similares...")
        
        # Buscar grupos de descobertas similares
        grupos = self.db.agrupar_descobertas_similares(
            threshold_similaridade=0.85
        )
        
        consolidadas = 0
        for grupo in grupos:
            if len(grupo) >= 2:
                # Consolidar em uma única descoberta mais forte
                descoberta_consolidada = self._consolidar_grupo(grupo)
                self.db.salvar_descoberta_consolidada(descoberta_consolidada)
                
                # Marcar originais como consolidadas
                for orig in grupo:
                    self.db.marcar_consolidada(orig['id'], descoberta_consolidada['id'])
                
                consolidadas += 1
        
        print(f"✅ {consolidadas} grupos de descobertas consolidados")
    
    async def normalizar_pesos_grafo(self):
        """Normaliza pesos para evitar inflação."""
        print("⚖️  Normalizando pesos do grafo...")
        
        nos_normalizados = 0
        for no in self.graph.graph_base.nodes():
            arestas_saida = list(self.graph.graph_base.out_edges(no, keys=True, data=True))
            
            if not arestas_saida:
                continue
            
            soma_pesos = sum(d.get('peso', 0.5) for _, _, _, d in arestas_saida)
            
            # Se soma > 10.0, normaliza
            if soma_pesos > 10.0:
                fator = 10.0 / soma_pesos
                for origem, destino, tipo, dados in arestas_saida:
                    peso_atual = dados.get('peso', 0.5)
                    dados['peso'] = peso_atual * fator
                
                nos_normalizados += 1
        
        print(f"✅ {nos_normalizados} nós normalizados")
    
    async def calcular_metricas_consolidadas(self):
        """Calcula e persiste métricas diárias."""
        print("📊 Calculando métricas consolidadas...")
        
        metricas = {
            "data": datetime.now().date().isoformat(),
            "consultas_dia": self.db.contar_consultas_periodo("hoje"),
            "qualidade_media_dia": self.db.qualidade_media_periodo("hoje"),
            "descobertas_dia": self.db.contar_descobertas_periodo("hoje"),
            "entidades_total": self.db.contar_entidades(),
            "arestas_total": self.graph.contar_arestas(),
            "densidade_grafo": self.graph.calcular_densidade(),
            "documentos_total": self.embeddings.contar_documentos()
        }
        
        self.db.salvar_metricas_consolidadas(metricas)
        print("✅ Métricas consolidadas salvas")
    
    def _consolidar_grupo(self, grupo: List[Dict]) -> Dict:
        """Consolida múltiplas descobertas em uma."""
        # Média ponderada de confiança
        confianca_consolidada = sum(d['confianca'] for d in grupo) / len(grupo)
        
        # Combina evidências
        evidencias_combinadas = []
        for d in grupo:
            evidencias_combinadas.extend(json.loads(d.get('evidencias_json', '[]')))
        
        # Descrição mais completa
        descricao = max(grupo, key=lambda d: len(d['descricao']))['descricao']
        
        return {
            "tipo_descoberta": grupo[0]['tipo_descoberta'],
            "descricao": f"{descricao} (consolidada de {len(grupo)} descobertas)",
            "confianca": min(1.0, confianca_consolidada * 1.1),  # Bônus por consenso
            "evidencias_json": json.dumps(list(set(evidencias_combinadas))),
            "entidade_origem": grupo[0].get('entidade_origem'),
            "entidade_destino": grupo[0].get('entidade_destino'),
            "descobertas_originais": [d['id'] for d in grupo]
        }
```

**Benefício**: Sistema se auto-mantém. "Respira" como organismo vivo - fortalece o útil, enfraquece o obsoleto.

---

### FASE 4: Dashboard e Visualização (Desejável - 3-4 semanas)

#### 4.1 Frontend Web para Visualização

```python
# server/main.py - ADICIONAR

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Servir frontend
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard de monitoramento do sistema."""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/epistemologia/{agente_id}", response_class=HTMLResponse)
async def visualizar_visao_mundo(request: Request, agente_id: str):
    """Visualização interativa da visão de mundo de um agente."""
    grafo = graph_manager.exportar_visao_mundo_agente(agente_id)
    return templates.TemplateResponse(
        "grafo_agente.html",
        {"request": request, "agente": agente_id, "grafo": grafo}
    )
```

Frontend sugerido:
- **D3.js** para visualização do grafo
- **Chart.js** para métricas temporais
- **Tailwind CSS** para UI responsiva
- **Alpine.js** para interatividade leve

---

## 📋 Schema de Banco de Dados Atualizado

```sql
-- ADICIONAR às tabelas existentes

-- Tracking de pesos por agente
CREATE TABLE IF NOT EXISTS delta_peso_agente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_agente TEXT NOT NULL,
    chave_origem TEXT NOT NULL,
    chave_destino TEXT NOT NULL,
    tipo_relacao TEXT NOT NULL,
    delta_peso REAL NOT NULL,  -- Ajuste individual (-0.5 a +0.5)
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_agente) REFERENCES dim_agente(chave_negocio),
    FOREIGN KEY (chave_origem) REFERENCES dim_entidade(chave_negocio),
    FOREIGN KEY (chave_destino) REFERENCES dim_entidade(chave_negocio),
    UNIQUE(id_agente, chave_origem, chave_destino, tipo_relacao)
);

-- Fato de interação (já previsto em ARQUITETURA.md, mas faltando)
CREATE TABLE IF NOT EXISTS fato_interacao (
    id_interacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tempo INTEGER NOT NULL,
    id_entidade_origem INTEGER NOT NULL,
    id_entidade_destino INTEGER NOT NULL,
    tipo_interacao TEXT NOT NULL,
    intensidade REAL NOT NULL,
    contexto TEXT,
    contador_uso INTEGER DEFAULT 1,
    FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
    FOREIGN KEY (id_entidade_origem) REFERENCES dim_entidade(id_entidade),
    FOREIGN KEY (id_entidade_destino) REFERENCES dim_entidade(id_entidade)
);

-- Eventos do sistema (para tracking de auto-regularização)
CREATE TABLE IF NOT EXISTS evento_sistema (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_evento TEXT NOT NULL,  -- 'decaimento_temporal', 'consolidacao', etc
    detalhes_json TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Métricas consolidadas diárias
CREATE TABLE IF NOT EXISTS metricas_consolidadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL UNIQUE,
    consultas_dia INTEGER,
    qualidade_media_dia REAL,
    descobertas_dia INTEGER,
    entidades_total INTEGER,
    arestas_total INTEGER,
    densidade_grafo REAL,
    documentos_total INTEGER,
    calculado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Descobertas consolidadas (tracking de quais foram mescladas)
CREATE TABLE IF NOT EXISTS descoberta_consolidacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_descoberta_original INTEGER NOT NULL,
    id_descoberta_consolidada INTEGER NOT NULL,
    consolidado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_descoberta_original) REFERENCES fato_descoberta(id_descoberta),
    FOREIGN KEY (id_descoberta_consolidada) REFERENCES fato_descoberta(id_descoberta)
);

-- Índices para performance
CREATE INDEX idx_delta_agente ON delta_peso_agente(id_agente);
CREATE INDEX idx_interacao_tempo ON fato_interacao(id_tempo);
CREATE INDEX idx_evento_tipo ON evento_sistema(tipo_evento);
CREATE INDEX idx_metricas_data ON metricas_consolidadas(data);
```

---

## 🧪 Testes Necessários

```python
# tests/test_feedback_loops.py - NOVO

import pytest
from server.graph import GraphManagerMultiAgente
from server.database import DatabaseManager

def test_peso_evolui_com_uso():
    """Testa se peso aumenta quando relação é usada."""
    graph = GraphManagerMultiAgente(db_mock)
    
    # Peso inicial
    graph.graph_base.add_edge("spark", "python", "usa", peso=0.5)
    
    # Simular 10 consultas de qualidade 0.9
    for _ in range(10):
        graph.atualizar_peso_uso("spark", "python", "usa", "agente-1", qualidade=0.9)
    
    peso_final = graph.get_peso("spark", "python", "usa", "agente-1")
    
    # Peso deve ter aumentado
    assert peso_final > 0.5
    assert peso_final <= 1.0

def test_decaimento_temporal():
    """Testa se peso diminui sem uso."""
    graph = GraphManagerMultiAgente(db_mock)
    graph.graph_base.add_edge("spark", "hadoop", "compara", peso=0.8, ultimo_uso="2025-01-01")
    
    # Simular 60 dias sem uso
    resultado = graph.decaimento_temporal_pesos(dias_inatividade=30)
    
    # Aresta deve ter sido removida ou muito enfraquecida
    assert resultado['arestas_removidas'] >= 1

def test_agentes_diferentes_visoes_diferentes():
    """Testa se agentes diferentes podem ter visões diferentes."""
    graph = GraphManagerMultiAgente(db_mock)
    graph.graph_base.add_edge("spark", "python", "usa", peso=0.5)
    
    # Agente A usa muito
    for _ in range(20):
        graph.atualizar_peso_uso("spark", "python", "usa", "agente-a", qualidade=0.9)
    
    # Agente B usa pouco
    for _ in range(2):
        graph.atualizar_peso_uso("spark", "python", "usa", "agente-b", qualidade=0.5)
    
    peso_a = graph.get_peso("spark", "python", "usa", "agente-a")
    peso_b = graph.get_peso("spark", "python", "usa", "agente-b")
    
    # Agente A deve ter peso mais alto
    assert peso_a > peso_b

def test_consulta_hibrida_usa_4_camadas():
    """Testa se consulta híbrida realmente usa todas as camadas."""
    # Mock das camadas
    resultado = consultar_hibrida_mock(
        query="Como usar Spark?",
        agente_id="teste",
        ordem="terceira"
    )
    
    assert resultado['camadas_usadas'] == 4
    assert 'memoria' in resultado['meta']
    assert 'grafo' in resultado['meta']
    assert 'historico' in resultado['meta']
    assert 'estrutural' in resultado['meta']
```

---

## 📊 KPIs de Sucesso

Para medir se as melhorias estão funcionando:

### Fase 1 (Fundação Sistêmica)
- ✅ **80%+ das consultas são híbridas** (usam 4 camadas)
- ✅ **Qualidade média cresce 20-35%** ao longo de 1 mês
- ✅ **Pesos evoluem dinamicamente** (tracking de variação semanal)

### Fase 2 (Epistemologias Múltiplas)
- ✅ **Cada agente tem visão de mundo única** (divergência média > 0.1)
- ✅ **Base coletiva converge** (estabiliza após N interações)
- ✅ **Comparações epistêmicas revelam insights** (identificar especialistas)

### Fase 3 (Auto-Regularização)
- ✅ **Sistema opera 30 dias sem intervenção humana**
- ✅ **Arestas obsoletas são removidas automaticamente** (>10/semana)
- ✅ **Descobertas redundantes são consolidadas** (>5/semana)

### Fase 4 (Dashboard)
- ✅ **Métricas visíveis em tempo real**
- ✅ **Grafo de agente visualizável interativamente**
- ✅ **Relatórios de saúde do sistema acessíveis**

---

## 🔮 Visão de Longo Prazo

### Funcionalidades Avançadas (Futuro)

1. **Meta-Aprendizado**
   - Sistema aprende quais tipos de descoberta são mais eficazes
   - Auto-ajusta thresholds de confiança
   - Prioriza automaticamente padrões valiosos

2. **Federação de Sistemas**
   - Múltiplas instâncias Nhandereko compartilham conhecimento
   - Consenso inter-sistemas
   - Resiliência distribuída

3. **Interface Conversacional**
   - LLM nativo que usa o sistema
   - "Explique sua visão sobre X"
   - "Compare minha visão com do agente Y"

4. **Auditoria Total**
   - Toda decisão é rastreável
   - "Por que você recomendou isso?"
   - Transparência epistêmica completa

---

## 💭 Reflexões Finais

### O Que Torna Nhandereko Único?

1. **Sistêmico de Verdade**
   - Não é só "mais um sistema de IA"
   - É um organismo que aprende, respira, evolui
   - Auto-regularização sem administrador

2. **Epistêmico**
   - Pesos = visão de mundo
   - Respeita pluralidade epistêmica
   - Conhecimento é situado, não universal

3. **Coletivo**
   - "Nosso modo de ser juntos"
   - Base compartilhada + experiência individual
   - Consenso emergente, não imposto

4. **Transparente**
   - Todo conhecimento tem origem
   - Toda decisão tem explicação
   - Trajetória epistêmica auditável

### Próximos Passos Imediatos

1. ✅ **Revisar este documento** com equipe
2. 🔨 **Implementar Fase 1** (fundação sistêmica)
3. 🧪 **Testar feedback loops** em produção
4. 📊 **Monitorar evolução** dos pesos
5. 📝 **Documentar aprendizados** emergentes

---

**Documento vivo** - atualizar conforme sistema evolui! 🌱

**Versão**: 1.0  
**Autor**: Análise colaborativa humano-agente  
**Data**: 25 de Outubro de 2025  
**Status**: 🟢 Pronto para revisão e implementação
