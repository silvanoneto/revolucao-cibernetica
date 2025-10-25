"""
Gerenciador de Banco de Dados
Camada Estrutural e Histórica (SQL)
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import json


class DatabaseManager:
    """Gerencia operações no banco de dados SQL"""

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def _get_session(self):
        """Obter sessão do banco"""
        return self.SessionLocal()

    def close(self):
        """Fechar conexões"""
        self.engine.dispose()

    # ============================================
    # DIMENSÕES
    # ============================================

    def _garantir_tempo(self, data: date = None) -> int:
        """Garantir que a dimensão tempo existe para a data"""
        if data is None:
            data = datetime.now().date()

        with self._get_session() as session:
            # Verificar se já existe
            result = session.execute(
                text("SELECT id_tempo FROM dim_tempo WHERE data = :data"), {"data": data}
            ).fetchone()

            if result:
                return result[0]

            # Criar novo registro
            dt = datetime.combine(data, datetime.min.time())
            session.execute(
                text("""
                INSERT INTO dim_tempo (data, ano, mes, dia, dia_semana, trimestre, semestre)
                VALUES (:data, :ano, :mes, :dia, :dia_semana, :trimestre, :semestre)
            """),
                {
                    "data": data,
                    "ano": dt.year,
                    "mes": dt.month,
                    "dia": dt.day,
                    "dia_semana": dt.weekday(),
                    "trimestre": (dt.month - 1) // 3 + 1,
                    "semestre": (dt.month - 1) // 6 + 1,
                },
            )
            session.commit()

            # Obter ID
            result = session.execute(
                text("SELECT id_tempo FROM dim_tempo WHERE data = :data"), {"data": data}
            ).fetchone()

            return result[0]

    def _garantir_agente(self, chave_agente: str) -> int:
        """Garantir que o agente existe"""
        with self._get_session() as session:
            # Verificar se já existe
            result = session.execute(
                text("SELECT id_agente FROM dim_agente WHERE chave_negocio = :chave"),
                {"chave": chave_agente},
            ).fetchone()

            if result:
                return result[0]

            # Criar novo agente
            session.execute(
                text("""
                INSERT INTO dim_agente (chave_negocio, nome, tipo)
                VALUES (:chave, :nome, :tipo)
            """),
                {"chave": chave_agente, "nome": chave_agente, "tipo": "llm"},
            )
            session.commit()

            # Obter ID
            result = session.execute(
                text("SELECT id_agente FROM dim_agente WHERE chave_negocio = :chave"),
                {"chave": chave_agente},
            ).fetchone()

            return result[0]

    def criar_entidade(self, dados: Dict[str, Any]) -> int:
        """Criar nova entidade"""
        with self._get_session() as session:
            result = session.execute(
                text("""
                INSERT INTO dim_entidade 
                (chave_negocio, nome, tipo, categoria, descricao, atributos_json)
                VALUES (:chave_negocio, :nome, :tipo, :categoria, :descricao, :atributos_json)
            """),
                dados,
            )
            session.commit()
            return result.lastrowid

    def obter_entidade(self, chave: str) -> Optional[Dict[str, Any]]:
        """Obter entidade por chave"""
        with self._get_session() as session:
            result = session.execute(
                text("SELECT * FROM dim_entidade WHERE chave_negocio = :chave"), {"chave": chave}
            ).fetchone()

            if result:
                return dict(result._mapping)
            return None

    def listar_entidades(
        self, tipo: Optional[str] = None, categoria: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Listar entidades com filtros"""
        query = "SELECT * FROM dim_entidade WHERE ativo = 1"
        params = {}

        if tipo:
            query += " AND tipo = :tipo"
            params["tipo"] = tipo

        if categoria:
            query += " AND categoria = :categoria"
            params["categoria"] = categoria

        query += " ORDER BY nome"

        with self._get_session() as session:
            result = session.execute(text(query), params).fetchall()
            return [dict(row._mapping) for row in result]

    def criar_conceito(self, dados: Dict[str, Any]) -> int:
        """Criar novo conceito"""
        with self._get_session() as session:
            result = session.execute(
                text("""
                INSERT INTO dim_conceito 
                (chave_negocio, nome, categoria, hierarquia, descricao)
                VALUES (:chave_negocio, :nome, :categoria, :hierarquia, :descricao)
            """),
                dados,
            )
            session.commit()
            return result.lastrowid

    def obter_conceito(self, chave: str) -> Optional[Dict[str, Any]]:
        """Obter conceito por chave"""
        with self._get_session() as session:
            result = session.execute(
                text("SELECT * FROM dim_conceito WHERE chave_negocio = :chave"), {"chave": chave}
            ).fetchone()

            if result:
                return dict(result._mapping)
            return None

    # ============================================
    # MEMÓRIA (Documentos)
    # ============================================

    def salvar_documento(self, doc_id: str, texto: str, metadados: Optional[Dict] = None) -> int:
        """Salvar documento na memória"""
        with self._get_session() as session:
            result = session.execute(
                text("""
                INSERT INTO memoria_documento (chave, texto, metadados_json, embedding_id)
                VALUES (:chave, :texto, :metadados, :embedding_id)
            """),
                {
                    "chave": doc_id,
                    "texto": texto,
                    "metadados": json.dumps(metadados) if metadados else None,
                    "embedding_id": doc_id,
                },
            )
            session.commit()
            return result.lastrowid

    # ============================================
    # FEEDBACK LOOP
    # ============================================

    def registrar_consulta(self, dados: Dict[str, Any]) -> int:
        """Registrar consulta no feedback loop"""
        id_tempo = self._garantir_tempo()
        id_agente = self._garantir_agente(dados["chave_agente"])

        with self._get_session() as session:
            result = session.execute(
                text("""
                INSERT INTO fato_consulta 
                (id_tempo, id_agente, tipo_consulta, query_texto, parametros, 
                 camadas_usadas, total_resultados, tempo_execucao_ms, 
                 qualidade_score, contexto_retornado)
                VALUES (:id_tempo, :id_agente, :tipo_consulta, :query_texto, 
                        :parametros, :camadas_usadas, :total_resultados, 
                        :tempo_execucao_ms, :qualidade_score, :contexto_retornado)
            """),
                {
                    "id_tempo": id_tempo,
                    "id_agente": id_agente,
                    "tipo_consulta": dados["tipo_consulta"],
                    "query_texto": dados["query_texto"],
                    "parametros": dados.get("parametros"),
                    "camadas_usadas": dados.get("camadas_usadas"),
                    "total_resultados": dados.get("total_resultados", 0),
                    "tempo_execucao_ms": dados.get("tempo_execucao_ms"),
                    "qualidade_score": dados.get("qualidade_score"),
                    "contexto_retornado": dados.get("contexto_retornado"),
                },
            )
            session.commit()
            return result.lastrowid

    def registrar_descoberta(self, dados: Dict[str, Any]) -> int:
        """Registrar descoberta no feedback loop"""
        id_tempo = self._garantir_tempo()
        id_agente = self._garantir_agente(dados["chave_agente"])

        # Obter IDs de entidades se fornecidas
        id_origem = None
        id_destino = None

        if dados.get("entidade_origem"):
            ent = self.obter_entidade(dados["entidade_origem"])
            if ent:
                id_origem = ent["id_entidade"]

        if dados.get("entidade_destino"):
            ent = self.obter_entidade(dados["entidade_destino"])
            if ent:
                id_destino = ent["id_entidade"]

        with self._get_session() as session:
            result = session.execute(
                text("""
                INSERT INTO fato_descoberta 
                (id_tempo, id_agente, id_entidade_origem, id_entidade_destino,
                 tipo_descoberta, descricao, confianca, evidencias_json, contexto)
                VALUES (:id_tempo, :id_agente, :id_origem, :id_destino,
                        :tipo_descoberta, :descricao, :confianca, :evidencias, :contexto)
            """),
                {
                    "id_tempo": id_tempo,
                    "id_agente": id_agente,
                    "id_origem": id_origem,
                    "id_destino": id_destino,
                    "tipo_descoberta": dados["tipo_descoberta"],
                    "descricao": dados["descricao"],
                    "confianca": dados["confianca"],
                    "evidencias": dados.get("evidencias_json"),
                    "contexto": dados.get("contexto"),
                },
            )
            session.commit()
            return result.lastrowid

    # ============================================
    # ANALÍTICOS
    # ============================================

    def obter_consultas(
        self,
        chave_agente: Optional[str] = None,
        tipo_consulta: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Obter histórico de consultas"""
        query = """
            SELECT 
                fc.*,
                da.chave_negocio as agente_chave,
                da.nome as agente_nome,
                dt.data
            FROM fato_consulta fc
            JOIN dim_agente da ON fc.id_agente = da.id_agente
            JOIN dim_tempo dt ON fc.id_tempo = dt.id_tempo
            WHERE 1=1
        """
        params = {}

        if chave_agente:
            query += " AND da.chave_negocio = :chave_agente"
            params["chave_agente"] = chave_agente

        if tipo_consulta:
            query += " AND fc.tipo_consulta = :tipo_consulta"
            params["tipo_consulta"] = tipo_consulta

        query += " ORDER BY fc.created_at DESC LIMIT :limit"
        params["limit"] = limit

        with self._get_session() as session:
            result = session.execute(text(query), params).fetchall()
            return [dict(row._mapping) for row in result]

    def obter_descobertas(
        self,
        chave_agente: Optional[str] = None,
        tipo_descoberta: Optional[str] = None,
        min_confianca: float = 0.75,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Obter descobertas do sistema"""
        query = """
            SELECT 
                fd.*,
                da.chave_negocio as agente_chave,
                da.nome as agente_nome,
                dt.data,
                eo.chave_negocio as entidade_origem_chave,
                ed.chave_negocio as entidade_destino_chave
            FROM fato_descoberta fd
            JOIN dim_agente da ON fd.id_agente = da.id_agente
            JOIN dim_tempo dt ON fd.id_tempo = dt.id_tempo
            LEFT JOIN dim_entidade eo ON fd.id_entidade_origem = eo.id_entidade
            LEFT JOIN dim_entidade ed ON fd.id_entidade_destino = ed.id_entidade
            WHERE fd.confianca >= :min_confianca
        """
        params = {"min_confianca": min_confianca}

        if chave_agente:
            query += " AND da.chave_negocio = :chave_agente"
            params["chave_agente"] = chave_agente

        if tipo_descoberta:
            query += " AND fd.tipo_descoberta = :tipo_descoberta"
            params["tipo_descoberta"] = tipo_descoberta

        query += " ORDER BY fd.confianca DESC, fd.created_at DESC LIMIT :limit"
        params["limit"] = limit

        with self._get_session() as session:
            result = session.execute(text(query), params).fetchall()
            return [dict(row._mapping) for row in result]

    def obter_metricas(self, chave_agente: Optional[str] = None) -> Dict[str, Any]:
        """Obter métricas do sistema"""
        params = {}
        where_clause = ""

        if chave_agente:
            where_clause = "WHERE da.chave_negocio = :chave_agente"
            params["chave_agente"] = chave_agente

        with self._get_session() as session:
            # Métricas de consultas
            consultas = session.execute(
                text(f"""
                SELECT 
                    COUNT(*) as total,
                    AVG(qualidade_score) as qualidade_media,
                    AVG(tempo_execucao_ms) as tempo_medio
                FROM fato_consulta fc
                JOIN dim_agente da ON fc.id_agente = da.id_agente
                {where_clause}
            """),
                params,
            ).fetchone()

            # Métricas de descobertas
            descobertas = session.execute(
                text(f"""
                SELECT 
                    COUNT(*) as total,
                    AVG(confianca) as confianca_media
                FROM fato_descoberta fd
                JOIN dim_agente da ON fd.id_agente = da.id_agente
                {where_clause}
            """),
                params,
            ).fetchone()

            return {
                "consultas": {
                    "total": consultas[0],
                    "qualidade_media": round(consultas[1], 2) if consultas[1] else 0,
                    "tempo_medio_ms": round(consultas[2], 2) if consultas[2] else 0,
                },
                "descobertas": {
                    "total": descobertas[0],
                    "confianca_media": round(descobertas[1], 2) if descobertas[1] else 0,
                },
            }
