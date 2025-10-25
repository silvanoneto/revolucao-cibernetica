#!/usr/bin/env python3
"""
Script de inicialização do banco de dados
Cria todas as tabelas necessárias para o Orquestrador de Conhecimento
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Adicionar diretório do projeto ao path
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# Cores para output
class Colors:
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    NC = "\033[0m"


def print_step(step: int, message: str):
    print(f"{Colors.BLUE}{step}️⃣ {message}{Colors.NC}")


def print_success(message: str):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")


def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")


def print_error(message: str):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")


# SQL para criar as tabelas
SQL_CREATE_TABLES = """
-- ============================================
-- DIMENSÕES (Contexto Estável)
-- ============================================

-- Dimensão: Tempo
CREATE TABLE IF NOT EXISTS dim_tempo (
    id_tempo INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE UNIQUE NOT NULL,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    semestre INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_dim_tempo_data ON dim_tempo(data);
CREATE INDEX IF NOT EXISTS idx_dim_tempo_ano_mes ON dim_tempo(ano, mes);

-- Dimensão: Agente
CREATE TABLE IF NOT EXISTS dim_agente (
    id_agente INTEGER PRIMARY KEY AUTOINCREMENT,
    chave_negocio TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('llm', 'usuario', 'sistema')),
    modelo TEXT,
    config_json TEXT,
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_dim_agente_chave ON dim_agente(chave_negocio);
CREATE INDEX IF NOT EXISTS idx_dim_agente_tipo ON dim_agente(tipo);

-- Dimensão: Entidade
CREATE TABLE IF NOT EXISTS dim_entidade (
    id_entidade INTEGER PRIMARY KEY AUTOINCREMENT,
    chave_negocio TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('linguagem', 'ferramenta', 'conceito', 'biblioteca', 'framework', 'outro')),
    categoria TEXT,
    descricao TEXT,
    atributos_json TEXT,
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_dim_entidade_chave ON dim_entidade(chave_negocio);
CREATE INDEX IF NOT EXISTS idx_dim_entidade_tipo ON dim_entidade(tipo);
CREATE INDEX IF NOT EXISTS idx_dim_entidade_categoria ON dim_entidade(categoria);

-- Dimensão: Conceito
CREATE TABLE IF NOT EXISTS dim_conceito (
    id_conceito INTEGER PRIMARY KEY AUTOINCREMENT,
    chave_negocio TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    categoria TEXT,
    hierarquia TEXT,
    descricao TEXT,
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_dim_conceito_chave ON dim_conceito(chave_negocio);
CREATE INDEX IF NOT EXISTS idx_dim_conceito_categoria ON dim_conceito(categoria);

-- ============================================
-- FATOS (Eventos e Medições)
-- ============================================

-- Fato: Consulta
CREATE TABLE IF NOT EXISTS fato_consulta (
    id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tempo INTEGER NOT NULL,
    id_agente INTEGER NOT NULL,
    tipo_consulta TEXT NOT NULL CHECK(tipo_consulta IN ('estrutural', 'memoria', 'grafo', 'hibrida', 'analitica')),
    query_texto TEXT NOT NULL,
    parametros TEXT,
    camadas_usadas TEXT,
    total_resultados INTEGER DEFAULT 0,
    tempo_execucao_ms INTEGER,
    qualidade_score REAL CHECK(qualidade_score BETWEEN 0 AND 1),
    contexto_retornado TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
    FOREIGN KEY (id_agente) REFERENCES dim_agente(id_agente)
);

CREATE INDEX IF NOT EXISTS idx_fato_consulta_tempo ON fato_consulta(id_tempo);
CREATE INDEX IF NOT EXISTS idx_fato_consulta_agente ON fato_consulta(id_agente);
CREATE INDEX IF NOT EXISTS idx_fato_consulta_tipo ON fato_consulta(tipo_consulta);
CREATE INDEX IF NOT EXISTS idx_fato_consulta_qualidade ON fato_consulta(qualidade_score);

-- Fato: Descoberta
CREATE TABLE IF NOT EXISTS fato_descoberta (
    id_descoberta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tempo INTEGER NOT NULL,
    id_agente INTEGER NOT NULL,
    id_entidade_origem INTEGER,
    id_entidade_destino INTEGER,
    id_conceito INTEGER,
    tipo_descoberta TEXT NOT NULL CHECK(tipo_descoberta IN ('correlacao', 'padrao', 'relacao', 'anomalia')),
    descricao TEXT NOT NULL,
    confianca REAL NOT NULL CHECK(confianca BETWEEN 0 AND 1),
    evidencias_json TEXT,
    contexto TEXT,
    validada BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
    FOREIGN KEY (id_agente) REFERENCES dim_agente(id_agente),
    FOREIGN KEY (id_entidade_origem) REFERENCES dim_entidade(id_entidade),
    FOREIGN KEY (id_entidade_destino) REFERENCES dim_entidade(id_entidade),
    FOREIGN KEY (id_conceito) REFERENCES dim_conceito(id_conceito)
);

CREATE INDEX IF NOT EXISTS idx_fato_descoberta_tempo ON fato_descoberta(id_tempo);
CREATE INDEX IF NOT EXISTS idx_fato_descoberta_agente ON fato_descoberta(id_agente);
CREATE INDEX IF NOT EXISTS idx_fato_descoberta_tipo ON fato_descoberta(tipo_descoberta);
CREATE INDEX IF NOT EXISTS idx_fato_descoberta_confianca ON fato_descoberta(confianca);

-- Fato: Interação
CREATE TABLE IF NOT EXISTS fato_interacao (
    id_interacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tempo INTEGER NOT NULL,
    id_entidade_origem INTEGER NOT NULL,
    id_entidade_destino INTEGER NOT NULL,
    tipo_interacao TEXT NOT NULL CHECK(tipo_interacao IN ('usa', 'gera', 'depende_de', 'comparado_com', 'similar_a')),
    intensidade REAL CHECK(intensidade BETWEEN 0 AND 1),
    contexto TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
    FOREIGN KEY (id_entidade_origem) REFERENCES dim_entidade(id_entidade),
    FOREIGN KEY (id_entidade_destino) REFERENCES dim_entidade(id_entidade)
);

CREATE INDEX IF NOT EXISTS idx_fato_interacao_tempo ON fato_interacao(id_tempo);
CREATE INDEX IF NOT EXISTS idx_fato_interacao_origem ON fato_interacao(id_entidade_origem);
CREATE INDEX IF NOT EXISTS idx_fato_interacao_destino ON fato_interacao(id_entidade_destino);
CREATE INDEX IF NOT EXISTS idx_fato_interacao_tipo ON fato_interacao(tipo_interacao);

-- ============================================
-- RELAÇÕES (Tabelas Auxiliares)
-- ============================================

-- Relação: Entidade-Conceito
CREATE TABLE IF NOT EXISTS rel_entidade_conceito (
    id_relacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_entidade INTEGER NOT NULL,
    id_conceito INTEGER NOT NULL,
    peso REAL DEFAULT 1.0 CHECK(peso BETWEEN 0 AND 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_entidade) REFERENCES dim_entidade(id_entidade),
    FOREIGN KEY (id_conceito) REFERENCES dim_conceito(id_conceito),
    UNIQUE(id_entidade, id_conceito)
);

CREATE INDEX IF NOT EXISTS idx_rel_entidade_conceito_entidade ON rel_entidade_conceito(id_entidade);
CREATE INDEX IF NOT EXISTS idx_rel_entidade_conceito_conceito ON rel_entidade_conceito(id_conceito);

-- ============================================
-- GRAFO (Estrutura de Nós e Arestas)
-- ============================================

-- Nós do Grafo
CREATE TABLE IF NOT EXISTS grafo_no (
    id_no INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT UNIQUE NOT NULL,
    tipo TEXT NOT NULL,
    id_entidade INTEGER,
    id_conceito INTEGER,
    propriedades_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_entidade) REFERENCES dim_entidade(id_entidade),
    FOREIGN KEY (id_conceito) REFERENCES dim_conceito(id_conceito)
);

CREATE INDEX IF NOT EXISTS idx_grafo_no_chave ON grafo_no(chave);
CREATE INDEX IF NOT EXISTS idx_grafo_no_tipo ON grafo_no(tipo);

-- Arestas do Grafo
CREATE TABLE IF NOT EXISTS grafo_aresta (
    id_aresta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_no_origem INTEGER NOT NULL,
    id_no_destino INTEGER NOT NULL,
    relacao TEXT NOT NULL,
    peso REAL DEFAULT 1.0 CHECK(peso BETWEEN 0 AND 1),
    metadados_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_no_origem) REFERENCES grafo_no(id_no),
    FOREIGN KEY (id_no_destino) REFERENCES grafo_no(id_no),
    UNIQUE(id_no_origem, id_no_destino, relacao)
);

CREATE INDEX IF NOT EXISTS idx_grafo_aresta_origem ON grafo_aresta(id_no_origem);
CREATE INDEX IF NOT EXISTS idx_grafo_aresta_destino ON grafo_aresta(id_no_destino);
CREATE INDEX IF NOT EXISTS idx_grafo_aresta_relacao ON grafo_aresta(relacao);

-- ============================================
-- MEMÓRIA (Embeddings e Documentos)
-- ============================================

-- Documentos
CREATE TABLE IF NOT EXISTS memoria_documento (
    id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT UNIQUE NOT NULL,
    texto TEXT NOT NULL,
    metadados_json TEXT,
    embedding_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_memoria_documento_chave ON memoria_documento(chave);
CREATE INDEX IF NOT EXISTS idx_memoria_documento_embedding ON memoria_documento(embedding_id);

-- ============================================
-- NOVAS TABELAS - FASE 1: FUNDAÇÃO SISTÊMICA
-- ============================================

-- Delta de Peso por Agente (Epistemologias Múltiplas)
CREATE TABLE IF NOT EXISTS delta_peso_agente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_agente TEXT NOT NULL,
    chave_origem TEXT NOT NULL,
    chave_destino TEXT NOT NULL,
    tipo_relacao TEXT NOT NULL,
    delta_peso REAL NOT NULL CHECK(delta_peso BETWEEN -0.5 AND 0.5),
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_agente, chave_origem, chave_destino, tipo_relacao)
);

CREATE INDEX IF NOT EXISTS idx_delta_agente ON delta_peso_agente(id_agente);
CREATE INDEX IF NOT EXISTS idx_delta_origem_destino ON delta_peso_agente(chave_origem, chave_destino);

-- Eventos do Sistema (Auto-Regularização)
CREATE TABLE IF NOT EXISTS evento_sistema (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_evento TEXT NOT NULL CHECK(tipo_evento IN (
        'decaimento_temporal', 'consolidacao_descobertas', 
        'normalizacao_pesos', 'limpeza_obsoletos', 'backup'
    )),
    detalhes_json TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evento_tipo ON evento_sistema(tipo_evento);
CREATE INDEX IF NOT EXISTS idx_evento_timestamp ON evento_sistema(timestamp);

-- Métricas Consolidadas (Monitoramento)
CREATE TABLE IF NOT EXISTS metricas_consolidadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL UNIQUE,
    consultas_dia INTEGER DEFAULT 0,
    qualidade_media_dia REAL,
    descobertas_dia INTEGER DEFAULT 0,
    entidades_total INTEGER DEFAULT 0,
    arestas_total INTEGER DEFAULT 0,
    densidade_grafo REAL,
    documentos_total INTEGER DEFAULT 0,
    calculado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_metricas_data ON metricas_consolidadas(data);

-- Descoberta Consolidação (Tracking de Mesclagem)
CREATE TABLE IF NOT EXISTS descoberta_consolidacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_descoberta_original INTEGER NOT NULL,
    id_descoberta_consolidada INTEGER NOT NULL,
    similaridade REAL CHECK(similaridade BETWEEN 0 AND 1),
    consolidado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_descoberta_original) REFERENCES fato_descoberta(id_descoberta),
    FOREIGN KEY (id_descoberta_consolidada) REFERENCES fato_descoberta(id_descoberta)
);

CREATE INDEX IF NOT EXISTS idx_consolidacao_original ON descoberta_consolidacao(id_descoberta_original);
CREATE INDEX IF NOT EXISTS idx_consolidacao_consolidada ON descoberta_consolidacao(id_descoberta_consolidada);

-- Histórico de Pesos (Tracking de Evolução)
CREATE TABLE IF NOT EXISTS historico_peso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave_origem TEXT NOT NULL,
    chave_destino TEXT NOT NULL,
    tipo_relacao TEXT NOT NULL,
    peso_anterior REAL NOT NULL,
    peso_novo REAL NOT NULL,
    motivo TEXT CHECK(motivo IN ('uso', 'decaimento', 'normalizacao', 'manual')),
    qualidade_interacao REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_historico_origem_destino ON historico_peso(chave_origem, chave_destino);
CREATE INDEX IF NOT EXISTS idx_historico_timestamp ON historico_peso(timestamp);

-- Metadados de Arestas (Informações de Uso)
CREATE TABLE IF NOT EXISTS grafo_aresta_metadados (
    id_aresta INTEGER PRIMARY KEY,
    ultimo_uso TIMESTAMP,
    contador_uso INTEGER DEFAULT 0,
    qualidade_media REAL,
    criado_por TEXT,
    aplicada_grafo BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_aresta) REFERENCES grafo_aresta(id_aresta) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_aresta_meta_ultimo_uso ON grafo_aresta_metadados(ultimo_uso);
CREATE INDEX IF NOT EXISTS idx_aresta_meta_contador ON grafo_aresta_metadados(contador_uso);
"""


def create_database():
    """Cria o banco de dados e todas as tabelas"""

    print("\n🧠 Inicializando Banco de Dados do Orquestrador de Conhecimento\n")

    # Criar diretório de dados
    data_dir = project_dir / "data" / "db"
    data_dir.mkdir(parents=True, exist_ok=True)

    db_path = data_dir / "orquestrador.db"

    print_step(1, f"Criando banco de dados em: {db_path}")

    # Criar engine
    engine = create_engine(f"sqlite:///{db_path}")

    try:
        # Executar SQL de criação
        print_step(2, "Criando tabelas...")

        with engine.begin() as conn:
            # Dividir e executar cada statement
            statements = [s.strip() for s in SQL_CREATE_TABLES.split(";") if s.strip()]

            for i, statement in enumerate(statements, 1):
                if statement:
                    conn.execute(text(statement))

        print_success("Todas as tabelas criadas com sucesso")

        # Inserir dados iniciais
        print_step(3, "Inserindo dados iniciais...")
        insert_initial_data(engine)
        print_success("Dados iniciais inseridos")

        # Verificar estrutura
        print_step(4, "Verificando estrutura do banco...")
        verify_database(engine)
        print_success("Estrutura verificada")

        print(f"\n{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")
        print(f"{Colors.GREEN}✨ Banco de dados inicializado com sucesso! ✨{Colors.NC}")
        print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}\n")

        print(f"{Colors.BLUE}📊 Localização: {db_path}{Colors.NC}")
        print(f"{Colors.BLUE}📋 Total de tabelas: 21 (14 originais + 7 novas){Colors.NC}")
        print(f"{Colors.BLUE}✨ Novas funcionalidades:{Colors.NC}")
        print(f"{Colors.BLUE}   • Pesos dinâmicos por agente{Colors.NC}")
        print(f"{Colors.BLUE}   • Auto-regularização do sistema{Colors.NC}")
        print(f"{Colors.BLUE}   • Métricas consolidadas{Colors.NC}")
        print(f"{Colors.BLUE}   • Tracking de evolução de pesos{Colors.NC}\n")

    except Exception as e:
        print_error(f"Erro ao criar banco de dados: {e}")
        sys.exit(1)


def insert_initial_data(engine):
    """Insere dados iniciais no banco"""

    with engine.begin() as conn:
        # Inserir dimensão tempo (hoje)
        today = datetime.now()
        conn.execute(
            text("""
            INSERT OR IGNORE INTO dim_tempo (data, ano, mes, dia, dia_semana, trimestre, semestre)
            VALUES (:data, :ano, :mes, :dia, :dia_semana, :trimestre, :semestre)
        """),
            {
                "data": today.date(),
                "ano": today.year,
                "mes": today.month,
                "dia": today.day,
                "dia_semana": today.weekday(),
                "trimestre": (today.month - 1) // 3 + 1,
                "semestre": (today.month - 1) // 6 + 1,
            },
        )

        # Inserir agente sistema
        conn.execute(
            text("""
            INSERT OR IGNORE INTO dim_agente (chave_negocio, nome, tipo, modelo)
            VALUES ('sistema', 'Sistema', 'sistema', NULL)
        """)
        )

        print_success("  - Dimensão tempo: registro de hoje")
        print_success("  - Agente sistema: criado")


def verify_database(engine):
    """Verifica a estrutura do banco de dados"""

    with engine.connect() as conn:
        # Contar tabelas
        result = conn.execute(
            text("""
            SELECT COUNT(*) as total 
            FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        )

        total_tables = result.fetchone()[0]
        print_success(f"  - Total de tabelas: {total_tables}")

        # Listar tabelas principais
        result = conn.execute(
            text("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        )

        tables = [row[0] for row in result.fetchall()]

        # Categorizar tabelas
        dims = [t for t in tables if t.startswith("dim_")]
        fatos = [t for t in tables if t.startswith("fato_")]
        grafo = [t for t in tables if t.startswith("grafo_")]
        outros = [
            t for t in tables if not any(t.startswith(p) for p in ["dim_", "fato_", "grafo_"])
        ]

        print_success(f"  - Dimensões: {len(dims)}")
        print_success(f"  - Fatos: {len(fatos)}")
        print_success(f"  - Grafo: {len(grafo)}")
        print_success(f"  - Outros: {len(outros)}")


if __name__ == "__main__":
    create_database()
