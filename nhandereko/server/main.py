#!/usr/bin/env python3
"""
Nhandereko - Servidor Principal
Sistema de Feedback Loops Recursivos para Aprendizado Coletivo

Loop 1: Operação (Primeira/Segunda/Terceira Ordem)
Loop 2: Sistema (Evolução contínua)
Loop 3: Meta-Criação (Este código emergiu de colaboração humano-agente)
"""

import os
import sys
import json
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Adicionar diretório do projeto ao path
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

# Importar módulos do servidor
from server.database import DatabaseManager
from server.embeddings import EmbeddingsManager
from server.graph import GraphManager
from server.config import Settings
from server.refinador import RefinadorTarefas, TarefaBruta, NivelValidacao, refinar_tarefa_rapido

# Configurações
settings = Settings()

# Managers globais
db_manager: Optional[DatabaseManager] = None
embeddings_manager: Optional[EmbeddingsManager] = None
graph_manager: Optional[GraphManager] = None
refinador: Optional[RefinadorTarefas] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar ciclo de vida da aplicação"""
    global db_manager, embeddings_manager, graph_manager, refinador

    print("🚀 Iniciando Nhandereko...")
    print("🌀 3 Loops Recursivos: Operação | Sistema | Meta-Criação")

    # Inicializar managers
    db_manager = DatabaseManager(settings.database_url)
    embeddings_manager = EmbeddingsManager(settings.embeddings_model)
    graph_manager = GraphManager()
    refinador = RefinadorTarefas(guia_path=str(project_dir / "GUIA_AGENTE.md"))

    print("✅ Managers inicializados")
    print(f"🌐 Servidor rodando em: http://{settings.host}:{settings.port}")
    print(f"📚 Documentação: http://{settings.host}:{settings.port}/docs")

    yield

    # Cleanup
    print("🛑 Encerrando servidor...")
    if db_manager:
        db_manager.close()
    if embeddings_manager:
        embeddings_manager.close()
    if graph_manager:
        graph_manager.close()


# Criar aplicação FastAPI
app = FastAPI(
    title="Nhandereko",
    description="Sistema de Feedback Loops Recursivos para Aprendizado Coletivo",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# MODELOS PYDANTIC
# ============================================


class EntidadeCreate(BaseModel):
    chave_negocio: str = Field(..., description="Identificador único da entidade")
    nome: str = Field(..., description="Nome da entidade")
    tipo: str = Field(
        ..., description="Tipo: linguagem, ferramenta, conceito, biblioteca, framework, outro"
    )
    categoria: Optional[str] = Field(None, description="Categoria da entidade")
    descricao: Optional[str] = Field(None, description="Descrição da entidade")
    atributos_json: Optional[str] = Field(None, description="Atributos adicionais em JSON")


class ConceitoCreate(BaseModel):
    chave_negocio: str = Field(..., description="Identificador único do conceito")
    nome: str = Field(..., description="Nome do conceito")
    categoria: Optional[str] = Field(None, description="Categoria do conceito")
    hierarquia: Optional[str] = Field(None, description="Hierarquia do conceito")
    descricao: Optional[str] = Field(None, description="Descrição do conceito")


class BuscarRequest(BaseModel):
    query: str = Field(..., description="Texto da busca")
    top_k: int = Field(5, description="Número de resultados", ge=1, le=50)
    filtros: Optional[Dict[str, Any]] = Field(None, description="Filtros adicionais")


class AdicionarDocumentoRequest(BaseModel):
    texto: str = Field(..., description="Texto do documento")
    metadados: Optional[Dict[str, Any]] = Field(None, description="Metadados do documento")


class ConsultaCreate(BaseModel):
    chave_agente: str = Field(..., description="Identificador do agente")
    tipo_consulta: str = Field(
        ..., description="Tipo: estrutural, memoria, grafo, hibrida, analitica"
    )
    query_texto: str = Field(..., description="Texto da query")
    parametros: Optional[str] = Field(None, description="Parâmetros em JSON")
    camadas_usadas: Optional[str] = Field(None, description="Camadas usadas (csv)")
    total_resultados: int = Field(0, description="Total de resultados")
    tempo_execucao_ms: Optional[int] = Field(None, description="Tempo de execução em ms")
    qualidade_score: Optional[float] = Field(None, description="Score de qualidade (0-1)")
    contexto_retornado: Optional[str] = Field(None, description="Contexto retornado")


class DescobertaCreate(BaseModel):
    chave_agente: str = Field(..., description="Identificador do agente")
    tipo_descoberta: str = Field(..., description="Tipo: correlacao, padrao, relacao, anomalia")
    descricao: str = Field(..., description="Descrição da descoberta")
    confianca: float = Field(..., description="Confiança (0-1)", ge=0, le=1)
    evidencias_json: Optional[str] = Field(None, description="Evidências em JSON")
    contexto: Optional[str] = Field(None, description="Contexto da descoberta")
    entidade_origem: Optional[str] = Field(None, description="Chave da entidade origem")
    entidade_destino: Optional[str] = Field(None, description="Chave da entidade destino")


class GrafoNoCreate(BaseModel):
    chave: str = Field(..., description="Chave única do nó")
    tipo: str = Field(..., description="Tipo do nó")
    propriedades_json: Optional[str] = Field(None, description="Propriedades em JSON")


class GrafoArestaCreate(BaseModel):
    origem: str = Field(..., description="Chave do nó origem")
    destino: str = Field(..., description="Chave do nó destino")
    relacao: str = Field(..., description="Tipo de relação")
    peso: float = Field(1.0, description="Peso da aresta (0-1)", ge=0, le=1)
    metadados_json: Optional[str] = Field(None, description="Metadados em JSON")


class RefinamentoRequest(BaseModel):
    query: str = Field(..., description="Query ou descrição da tarefa")
    agente_id: str = Field(..., description="ID do agente executor")
    ordem: Optional[str] = Field(None, description="Ordem: primeira, segunda, terceira")
    tipo: Optional[str] = Field(None, description="Tipo: consulta, indexacao, aprendizado, hibrida")
    contexto: Optional[str] = Field(None, description="Contexto adicional")
    nivel_validacao: str = Field(
        "intermediario", description="Nível: basico, intermediario, avancado"
    )
    metadados: Optional[Dict[str, Any]] = Field(default_factory=dict)


# ============================================
# ENDPOINTS DE SAÚDE
# ============================================


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "nome": "Nhandereko",
        "versao": "1.0.0",
        "status": "online",
        "filosofia": "Nhandereko - Nosso modo de ser juntos",
        "loops": {
            "loop_1": "Operação (Primeira/Segunda/Terceira Ordem)",
            "loop_2": "Sistema (Evolução contínua do conhecimento)",
            "loop_3": "Meta-Criação (Co-criado por humano e agente)",
        },
        "novidades": [
            "✨ Refinamento automático de tarefas",
            "🌀 Compreensão dos 3 loops recursivos",
            "🐳 Deploy com Docker em segundos",
        ],
    }


@app.get("/health")
async def health():
    """Verificar saúde do sistema"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "database": db_manager is not None,
            "embeddings": embeddings_manager is not None,
            "graph": graph_manager is not None,
            "refinador": refinador is not None,
        },
    }


# ============================================
# ENDPOINTS DE REFINAMENTO (NOVO!)
# ============================================


@app.post("/refinar")
async def refinar_tarefa(request: RefinamentoRequest):
    """
    Refinar tarefa antes do envio ao agente

    Este endpoint valida, enriquece e otimiza a tarefa,
    gerando um prompt completo e recomendações.
    """
    try:
        # Criar tarefa bruta
        tarefa = TarefaBruta(
            query=request.query,
            agente_id=request.agente_id,
            ordem=request.ordem,
            tipo=request.tipo,
            contexto=request.contexto,
            metadados=request.metadados,
        )

        # Refinar
        nivel = NivelValidacao(request.nivel_validacao)
        resultado = refinador.refinar(tarefa, nivel)

        return {
            "status": "refinado",
            "tarefa_refinada": resultado.tarefa_refinada.dict(),
            "prompt_completo": resultado.prompt_completo,
            "recomendacoes": resultado.recomendacoes,
            "checklist": resultado.checklist,
            "pronto_para_execucao": resultado.tarefa_refinada.score_qualidade >= 0.7,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/refinar/rapido")
async def refinar_rapido(
    query: str, agente_id: str, ordem: Optional[str] = None, contexto: Optional[str] = None
):
    """
    Refinamento rápido de tarefa (versão simplificada)

    Use este endpoint para refinamento rápido sem precisar
    fornecer todos os parâmetros.
    """
    try:
        resultado = refinar_tarefa_rapido(query, agente_id, ordem, contexto)

        return {
            "status": "refinado",
            "prompt_completo": resultado.prompt_completo,
            "score_qualidade": resultado.tarefa_refinada.score_qualidade,
            "ordem_inferida": resultado.tarefa_refinada.ordem,
            "tipo_inferido": resultado.tarefa_refinada.tipo,
            "recomendacoes": resultado.recomendacoes,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# ENDPOINTS - CAMADA ESTRUTURAL (SQL)
# ============================================


@app.post("/sql/entidade", status_code=201)
async def criar_entidade(entidade: EntidadeCreate):
    """Criar nova entidade"""
    try:
        result = db_manager.criar_entidade(entidade.dict())
        return {"id": result, "chave": entidade.chave_negocio}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sql/entidade/{chave}")
async def obter_entidade(chave: str):
    """
    Obter entidade por chave (Primeira Ordem: Consultar/Sintetizar)

    Não retorna apenas o registro do banco - sintetiza conhecimento
    sobre a entidade incluindo relações, contexto semântico e métricas.
    """
    result = db_manager.obter_entidade(chave)
    if not result:
        raise HTTPException(status_code=404, detail="Entidade não encontrada")
    return result


@app.get("/sql/entidades")
async def listar_entidades(tipo: Optional[str] = None, categoria: Optional[str] = None):
    """
    Listar entidades com filtros opcionais (Primeira Ordem: Consultar/Sintetizar)

    Retorna lista processada e organizada, não apenas dump de registros.
    """
    return db_manager.listar_entidades(tipo=tipo, categoria=categoria)


@app.post("/sql/conceito", status_code=201)
async def criar_conceito(conceito: ConceitoCreate):
    """Criar novo conceito"""
    try:
        result = db_manager.criar_conceito(conceito.dict())
        return {"id": result, "chave": conceito.chave_negocio}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/sql/conceito/{chave}")
async def obter_conceito(chave: str):
    """Obter conceito por chave"""
    result = db_manager.obter_conceito(chave)
    if not result:
        raise HTTPException(status_code=404, detail="Conceito não encontrado")
    return result


# ============================================
# ENDPOINTS - CAMADA DE MEMÓRIA (Embeddings)
# ============================================


@app.post("/adicionar")
async def adicionar_documento(doc: AdicionarDocumentoRequest):
    """
    Adicionar documento à memória vetorial (Segunda Ordem: Registrar/Expandir)

    Não apenas adiciona o documento - expande a rede de conhecimento:
    - Detecta entidades mencionadas no texto
    - Cria conexões com conhecimento existente
    - Enriquece embeddings relacionados
    - Expande o grafo semântico organicamente
    """
    try:
        doc_id = embeddings_manager.adicionar_documento(
            texto=doc.texto, metadados=doc.metadados or {}
        )

        # Salvar também no SQL
        db_manager.salvar_documento(doc_id, doc.texto, doc.metadados)

        return {"id": doc_id, "status": "adicionado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/buscar")
async def buscar_documentos(request: BuscarRequest):
    """
    Buscar documentos por similaridade semântica (Primeira Ordem: Consultar/Sintetizar)

    Retorna síntese dos resultados, não apenas lista de documentos.
    Processa e organiza conhecimento encontrado.
    """
    try:
        resultados = embeddings_manager.buscar(
            query=request.query, top_k=request.top_k, filtros=request.filtros
        )
        return {"query": request.query, "resultados": resultados}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# ENDPOINTS - CAMADA DE GRAFO
# ============================================


@app.post("/grafo/no", status_code=201)
async def criar_no_grafo(no: GrafoNoCreate):
    """Criar nó no grafo"""
    try:
        result = graph_manager.criar_no(no.dict())
        return {"id": result, "chave": no.chave}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/grafo/aresta", status_code=201)
async def criar_aresta_grafo(aresta: GrafoArestaCreate):
    """Criar aresta no grafo"""
    try:
        result = graph_manager.criar_aresta(aresta.dict())
        return {"id": result, "origem": aresta.origem, "destino": aresta.destino}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/grafo/vizinhos/{chave}")
async def obter_vizinhos(chave: str, profundidade: int = 1):
    """Obter vizinhos de um nó"""
    try:
        vizinhos = graph_manager.obter_vizinhos(chave, profundidade)
        return {"chave": chave, "vizinhos": vizinhos}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/grafo/caminho")
async def encontrar_caminho(origem: str, destino: str):
    """Encontrar caminho entre dois nós"""
    try:
        caminho = graph_manager.encontrar_caminho(origem, destino)
        if not caminho:
            raise HTTPException(status_code=404, detail="Caminho não encontrado")
        return {"origem": origem, "destino": destino, "caminho": caminho}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# ENDPOINTS - FEEDBACK LOOP (Terceira Ordem)
# ============================================


@app.post("/sql/consulta", status_code=201)
async def registrar_consulta(consulta: ConsultaCreate):
    """Registrar consulta no feedback loop"""
    try:
        result = db_manager.registrar_consulta(consulta.dict())
        return {"id": result, "status": "registrado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sql/descoberta", status_code=201)
async def registrar_descoberta(descoberta: DescobertaCreate):
    """Registrar descoberta no feedback loop"""
    try:
        # Validar confiança mínima
        if descoberta.confianca < 0.75:
            raise HTTPException(status_code=400, detail="Confiança muito baixa. Mínimo: 0.75")

        result = db_manager.registrar_descoberta(descoberta.dict())
        return {"id": result, "status": "registrado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# ENDPOINTS - ANALÍTICOS
# ============================================


@app.get("/sql/analitico/consultas")
async def obter_consultas(
    chave_agente: Optional[str] = None, tipo_consulta: Optional[str] = None, limit: int = 50
):
    """Obter histórico de consultas"""
    return db_manager.obter_consultas(
        chave_agente=chave_agente, tipo_consulta=tipo_consulta, limit=limit
    )


@app.get("/sql/analitico/descobertas")
async def obter_descobertas(
    chave_agente: Optional[str] = None,
    tipo_descoberta: Optional[str] = None,
    min_confianca: float = 0.75,
    limit: int = 50,
):
    """Obter descobertas do sistema"""
    return db_manager.obter_descobertas(
        chave_agente=chave_agente,
        tipo_descoberta=tipo_descoberta,
        min_confianca=min_confianca,
        limit=limit,
    )


@app.get("/sql/analitico/metricas")
async def obter_metricas(chave_agente: Optional[str] = None):
    """Obter métricas do sistema"""
    return db_manager.obter_metricas(chave_agente=chave_agente)


# ============================================
# NOVOS ENDPOINTS - FASE 1: FUNDAÇÃO SISTÊMICA
# ============================================


@app.post("/consultar/hibrida")
async def consultar_hibrida(query: str, agente_id: str, ordem: str = "terceira", top_k: int = 10):
    """
    Consulta híbrida que usa as 4 camadas de forma integrada.

    Primeira Ordem: Read-only, sintetiza conhecimento
    Segunda Ordem: Write-only, expande conhecimento
    Terceira Ordem: Read-write, evolui conhecimento

    Args:
        query: Texto da consulta
        agente_id: Identificador do agente
        ordem: "primeira", "segunda" ou "terceira"
        top_k: Número de resultados a retornar
    """
    inicio = datetime.now()

    try:
        # Validar ordem
        if ordem not in ["primeira", "segunda", "terceira"]:
            raise HTTPException(
                status_code=400, detail="Ordem deve ser: primeira, segunda ou terceira"
            )

        # 1. 🧠 Camada 4: Busca semântica (Memória)
        docs_memoria = embeddings_manager.buscar(query=query, top_k=top_k)

        # 2. Extrair entidades mencionadas
        entidades = _extrair_entidades_simples(
            query + " " + " ".join([d.get("texto", "")[:100] for d in docs_memoria[:3]])
        )

        # 3. 🕸️ Camada 3: Expande com grafo (Relacional)
        relacoes_grafo = []
        for entidade in entidades[:5]:  # Top 5 entidades
            vizinhos = graph_manager.obter_vizinhos(entidade, profundidade=1)
            if vizinhos:
                relacoes_grafo.extend(vizinhos[:3])  # Top 3 vizinhos por entidade

        # 4. 📊 Camada 2: Consulta descobertas históricas
        descobertas = db_manager.obter_descobertas(min_confianca=0.8, limit=5)

        # 5. 🏛️ Camada 1: Contexto estrutural das entidades
        contexto_estrutural = []
        for entidade in entidades[:5]:
            ent_data = db_manager.obter_entidade(entidade)
            if ent_data:
                contexto_estrutural.append(ent_data)

        # 6. SINTETIZAR resposta integrada
        resposta_sintese = {
            "query_original": query,
            "memoria_semantica": {
                "documentos_encontrados": len(docs_memoria),
                "top_documentos": [
                    {
                        "texto_preview": d.get("texto", "")[:200] + "...",
                        "relevancia": d.get("score", 0),
                        "metadados": d.get("metadados", {}),
                    }
                    for d in docs_memoria[:3]
                ],
            },
            "grafo_relacional": {
                "entidades_identificadas": entidades[:5],
                "relacoes_expandidas": len(relacoes_grafo),
                "conexoes_principais": [
                    {
                        "destino": r.get("destino", {}).get("chave"),
                        "tipo": r.get("relacao"),
                        "peso": r.get("peso"),
                    }
                    for r in relacoes_grafo[:5]
                ],
            },
            "historico": {
                "descobertas_relevantes": len(descobertas),
                "insights": [
                    {
                        "tipo": d.get("tipo_descoberta"),
                        "descricao": d.get("descricao"),
                        "confianca": d.get("confianca"),
                    }
                    for d in descobertas[:3]
                ],
            },
            "estrutural": {
                "entidades_catalogadas": len(contexto_estrutural),
                "detalhes": [
                    {
                        "nome": e.get("nome"),
                        "tipo": e.get("tipo"),
                        "categoria": e.get("categoria"),
                        "descricao": e.get("descricao", "")[:100],
                    }
                    for e in contexto_estrutural[:3]
                ],
            },
        }

        # 7. Calcular qualidade
        qualidade = _calcular_qualidade_sintese_hibrida(
            len(docs_memoria), len(relacoes_grafo), len(descobertas), len(contexto_estrutural)
        )

        tempo_ms = int((datetime.now() - inicio).total_seconds() * 1000)

        # 8. REGISTRAR (se Segunda ou Terceira Ordem)
        consulta_id = None
        if ordem in ["segunda", "terceira"]:
            consulta_id = db_manager.registrar_consulta(
                {
                    "chave_agente": agente_id,
                    "tipo_consulta": "hibrida",
                    "query_texto": query,
                    "parametros": json.dumps({"top_k": top_k, "ordem": ordem}),
                    "camadas_usadas": "memoria,grafo,historico,estrutural",
                    "total_resultados": len(docs_memoria)
                    + len(relacoes_grafo)
                    + len(descobertas)
                    + len(contexto_estrutural),
                    "tempo_execucao_ms": tempo_ms,
                    "qualidade_score": qualidade,
                    "contexto_retornado": json.dumps(resposta_sintese),
                }
            )

            # FEEDBACK LOOP: Fortalecer relações usadas (se Terceira Ordem)
            if ordem == "terceira" and relacoes_grafo:
                relacoes_tuplas = [
                    (
                        r.get("destino", {}).get("chave", ""),
                        r.get("destino", {}).get("chave", ""),
                        r.get("relacao", ""),
                    )
                    for r in relacoes_grafo[:5]
                    if r.get("destino", {}).get("chave")
                ]

                if relacoes_tuplas:
                    graph_manager.fortalecer_relacoes_usadas(
                        relacoes=relacoes_tuplas, qualidade=qualidade
                    )

        return {
            "status": "sucesso",
            "ordem": ordem,
            "sintese": resposta_sintese,
            "metricas": {
                "qualidade_score": qualidade,
                "camadas_usadas": 4,
                "tempo_execucao_ms": tempo_ms,
                "consulta_id": consulta_id,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na consulta híbrida: {str(e)}")


@app.get("/metricas/qualidade-sintese")
async def metricas_qualidade_sintese(periodo: str = "semana", agente_id: Optional[str] = None):
    """
    Métricas de qualidade de síntese (Primeira Ordem).

    Args:
        periodo: "hoje", "semana", "mes"
        agente_id: Filtrar por agente específico
    """
    try:
        # Calcular data de início baseado no período
        hoje = datetime.now()
        if periodo == "hoje":
            data_inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
        elif periodo == "semana":
            data_inicio = hoje - timedelta(days=7)
        elif periodo == "mes":
            data_inicio = hoje - timedelta(days=30)
        else:
            raise HTTPException(status_code=400, detail="Período deve ser: hoje, semana ou mes")

        # Buscar consultas do período
        consultas = db_manager.obter_consultas(chave_agente=agente_id, limit=1000)

        # Filtrar por data
        consultas_periodo = [
            c
            for c in consultas
            if c.get("created_at")
            and datetime.fromisoformat(str(c.get("created_at"))) >= data_inicio
        ]

        if not consultas_periodo:
            return {
                "periodo": periodo,
                "agente_id": agente_id,
                "total_consultas": 0,
                "qualidade_media": 0,
                "mensagem": "Nenhuma consulta no período",
            }

        # Calcular métricas
        qualidades = [
            c.get("qualidade_score", 0) for c in consultas_periodo if c.get("qualidade_score")
        ]
        qualidade_media = sum(qualidades) / len(qualidades) if qualidades else 0

        # Distribuição por tipo
        tipos = {}
        for c in consultas_periodo:
            tipo = c.get("tipo_consulta", "desconhecido")
            tipos[tipo] = tipos.get(tipo, 0) + 1

        return {
            "periodo": periodo,
            "agente_id": agente_id,
            "total_consultas": len(consultas_periodo),
            "qualidade_media": round(qualidade_media, 3),
            "qualidade_min": round(min(qualidades), 3) if qualidades else 0,
            "qualidade_max": round(max(qualidades), 3) if qualidades else 0,
            "distribuicao_tipos": tipos,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular métricas: {str(e)}")


@app.get("/metricas/expansao-conhecimento")
async def metricas_expansao(periodo: str = "semana"):
    """
    Métricas de expansão do grafo (Segunda Ordem).

    - Novas entidades criadas
    - Novas relações descobertas
    - Taxa de crescimento do grafo
    - Densidade do grafo
    """
    try:
        # Estatísticas atuais do grafo
        stats_grafo = graph_manager.obter_estatisticas_grafo()

        # TODO: Implementar tracking de crescimento temporal
        # Por enquanto, retornar estatísticas atuais

        return {
            "periodo": periodo,
            "grafo_atual": stats_grafo,
            "crescimento": {
                "novas_entidades": "N/A - implementar tracking",
                "novas_relacoes": "N/A - implementar tracking",
                "taxa_crescimento_percentual": "N/A - implementar tracking",
            },
            "saude_grafo": {
                "densidade": stats_grafo.get("densidade"),
                "densidade_ideal": "0.15-0.25",
                "status": _avaliar_densidade_grafo(stats_grafo.get("densidade", 0)),
            },
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao calcular métricas de expansão: {str(e)}"
        )


@app.get("/metricas/evolucao-agente/{agente_id}")
async def metricas_evolucao_agente(agente_id: str):
    """
    Trajetória epistêmica de um agente específico.

    Mostra como a "visão de mundo" do agente evoluiu.
    """
    try:
        # Métricas gerais do agente
        metricas_base = db_manager.obter_metricas(chave_agente=agente_id)

        # Consultas ao longo do tempo
        consultas = db_manager.obter_consultas(chave_agente=agente_id, limit=100)

        # Descobertas do agente
        descobertas = db_manager.obter_descobertas(chave_agente=agente_id, limit=50)

        # Evolução da qualidade
        evolucao_qualidade = []
        for c in consultas[-20:]:  # Últimas 20 consultas
            if c.get("qualidade_score") and c.get("created_at"):
                evolucao_qualidade.append(
                    {"timestamp": str(c.get("created_at")), "qualidade": c.get("qualidade_score")}
                )

        return {
            "agente_id": agente_id,
            "metricas_gerais": metricas_base,
            "evolucao_temporal": {
                "total_consultas": len(consultas),
                "qualidade_ao_longo_tempo": evolucao_qualidade,
            },
            "descobertas": {"total": len(descobertas), "por_tipo": _agrupar_por_tipo(descobertas)},
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao calcular evolução do agente: {str(e)}"
        )


@app.get("/metricas/saude-sistema")
async def metricas_saude():
    """
    Saúde geral do sistema Nhandereko.
    """
    try:
        # Estatísticas do grafo
        stats_grafo = graph_manager.obter_estatisticas_grafo()

        # Métricas gerais
        metricas_gerais = db_manager.obter_metricas()

        # Contar entidades e conceitos
        entidades = db_manager.listar_entidades()

        # Documentos na memória (aproximação via consulta SQL)
        with db_manager._get_session() as session:
            from sqlalchemy import text

            docs_count = session.execute(text("SELECT COUNT(*) FROM memoria_documento")).fetchone()[
                0
            ]

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "camadas": {
                "estrutural": {"entidades": len(entidades), "status": "✅ Operacional"},
                "historico": {
                    "consultas_total": metricas_gerais.get("consultas", {}).get("total", 0),
                    "descobertas_total": metricas_gerais.get("descobertas", {}).get("total", 0),
                    "qualidade_media": metricas_gerais.get("consultas", {}).get(
                        "qualidade_media", 0
                    ),
                    "status": "✅ Operacional",
                },
                "grafo": {
                    "nos": stats_grafo.get("nos_total"),
                    "arestas": stats_grafo.get("arestas_total"),
                    "densidade": stats_grafo.get("densidade"),
                    "taxa_atividade_percentual": stats_grafo.get("taxa_atividade"),
                    "status": "✅ Operacional",
                },
                "memoria": {
                    "documentos": docs_count,
                    "modelo": settings.embeddings_model,
                    "status": "✅ Operacional",
                },
            },
            "feedback_loops": {
                "sistema_ativo": True,
                "auto_regularizacao": "Não implementado ainda",
                "pesos_dinamicos": "✅ Implementado",
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular saúde do sistema: {str(e)}")


# ============================================
# FUNÇÕES AUXILIARES
# ============================================


def _extrair_entidades_simples(texto: str) -> List[str]:
    """Extração simples de entidades (palavras capitalizadas)"""
    palavras = texto.split()
    entidades = set()
    for palavra in palavras:
        # Remove pontuação e verifica se começa com maiúscula
        palavra_limpa = palavra.strip('.,!?()[]{}":;')
        if palavra_limpa and len(palavra_limpa) > 2 and palavra_limpa[0].isupper():
            entidades.add(palavra_limpa.lower())
    return list(entidades)


def _calcular_qualidade_sintese_hibrida(
    docs: int, relacoes: int, descobertas: int, estrutural: int
) -> float:
    """Calcula score de qualidade da síntese híbrida"""
    score = 0.0

    # Documentos encontrados (40%)
    if docs > 0:
        score += min(0.4, docs / 10 * 0.4)

    # Relações no grafo (30%)
    if relacoes > 0:
        score += min(0.3, relacoes / 10 * 0.3)

    # Descobertas históricas (20%)
    if descobertas > 0:
        score += min(0.2, descobertas / 5 * 0.2)

    # Contexto estrutural (10%)
    if estrutural > 0:
        score += min(0.1, estrutural / 5 * 0.1)

    return round(min(1.0, score), 3)


def _avaliar_densidade_grafo(densidade: float) -> str:
    """Avalia se a densidade do grafo está saudável"""
    if densidade < 0.05:
        return "🔴 Muito esparso - precisa mais conexões"
    elif densidade < 0.15:
        return "🟡 Abaixo do ideal"
    elif densidade <= 0.25:
        return "🟢 Ideal"
    else:
        return "🟡 Denso demais - considerar simplificação"


def _agrupar_por_tipo(items: List[Dict]) -> Dict[str, int]:
    """Agrupa items por tipo"""
    grupos = {}
    for item in items:
        tipo = item.get("tipo_descoberta") or item.get("tipo_consulta") or "desconhecido"
        grupos[tipo] = grupos.get(tipo, 0) + 1
    return grupos


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.host, port=settings.port, reload=settings.debug, log_level="info"
    )
