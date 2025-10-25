"""
Gerenciador de Grafo
Camada de Eventos (Graph Database)
"""

from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import json


class GraphManager:
    """Gerencia o grafo de conhecimento"""

    def __init__(self, db_type: str = "sqlite"):
        """
        Inicializar gerenciador de grafo

        Args:
            db_type: Tipo de banco (sqlite ou neo4j)
        """
        self.db_type = db_type

        if db_type == "sqlite":
            # Usar implementação SQLite (já criada no init-db.py)
            from server.database import DatabaseManager
            from server.config import settings

            self.db = DatabaseManager(settings.database_url)
        elif db_type == "neo4j":
            # TODO: Implementar Neo4j
            raise NotImplementedError("Neo4j ainda não implementado")
        else:
            raise ValueError(f"Tipo de banco não suportado: {db_type}")

    def criar_no(self, dados: Dict[str, Any]) -> int:
        """
        Criar nó no grafo

        Args:
            dados: Dados do nó (chave, tipo, propriedades_json)

        Returns:
            ID do nó criado
        """
        with self.db._get_session() as session:
            from sqlalchemy import text

            result = session.execute(
                text("""
                INSERT INTO grafo_no (chave, tipo, propriedades_json)
                VALUES (:chave, :tipo, :propriedades)
            """),
                {
                    "chave": dados["chave"],
                    "tipo": dados["tipo"],
                    "propriedades": dados.get("propriedades_json"),
                },
            )
            session.commit()
            return result.lastrowid

    def obter_no(self, chave: str) -> Optional[Dict[str, Any]]:
        """
        Obter nó por chave

        Args:
            chave: Chave do nó

        Returns:
            Dados do nó ou None
        """
        with self.db._get_session() as session:
            from sqlalchemy import text

            result = session.execute(
                text("SELECT * FROM grafo_no WHERE chave = :chave"), {"chave": chave}
            ).fetchone()

            if result:
                return dict(result._mapping)
            return None

    def criar_aresta(self, dados: Dict[str, Any]) -> int:
        """
        Criar aresta no grafo

        Args:
            dados: Dados da aresta (origem, destino, relacao, peso, metadados_json)

        Returns:
            ID da aresta criada
        """
        with self.db._get_session() as session:
            from sqlalchemy import text

            # Obter IDs dos nós
            no_origem = self.obter_no(dados["origem"])
            no_destino = self.obter_no(dados["destino"])

            if not no_origem:
                # Criar nó origem se não existir
                id_origem = self.criar_no(
                    {"chave": dados["origem"], "tipo": "auto", "propriedades_json": None}
                )
            else:
                id_origem = no_origem["id_no"]

            if not no_destino:
                # Criar nó destino se não existir
                id_destino = self.criar_no(
                    {"chave": dados["destino"], "tipo": "auto", "propriedades_json": None}
                )
            else:
                id_destino = no_destino["id_no"]

            # Criar aresta
            result = session.execute(
                text("""
                INSERT OR REPLACE INTO grafo_aresta 
                (id_no_origem, id_no_destino, relacao, peso, metadados_json)
                VALUES (:id_origem, :id_destino, :relacao, :peso, :metadados)
            """),
                {
                    "id_origem": id_origem,
                    "id_destino": id_destino,
                    "relacao": dados["relacao"],
                    "peso": dados.get("peso", 1.0),
                    "metadados": dados.get("metadados_json"),
                },
            )
            session.commit()
            return result.lastrowid

    def obter_vizinhos(self, chave: str, profundidade: int = 1) -> List[Dict[str, Any]]:
        """
        Obter vizinhos de um nó

        Args:
            chave: Chave do nó
            profundidade: Profundidade da busca

        Returns:
            Lista de vizinhos
        """
        no = self.obter_no(chave)
        if not no:
            return []

        with self.db._get_session() as session:
            from sqlalchemy import text

            # Buscar arestas saindo do nó
            result = session.execute(
                text("""
                SELECT 
                    ga.relacao,
                    ga.peso,
                    gn.chave as destino_chave,
                    gn.tipo as destino_tipo,
                    gn.propriedades_json as destino_propriedades
                FROM grafo_aresta ga
                JOIN grafo_no gn ON ga.id_no_destino = gn.id_no
                WHERE ga.id_no_origem = :id_no
                ORDER BY ga.peso DESC
            """),
                {"id_no": no["id_no"]},
            ).fetchall()

            vizinhos = []
            for row in result:
                vizinhos.append(
                    {
                        "relacao": row[0],
                        "peso": row[1],
                        "destino": {
                            "chave": row[2],
                            "tipo": row[3],
                            "propriedades": json.loads(row[4]) if row[4] else {},
                        },
                    }
                )

            return vizinhos

    def encontrar_caminho(
        self, origem: str, destino: str, max_profundidade: int = 5
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Encontrar caminho entre dois nós (BFS)

        Args:
            origem: Chave do nó origem
            destino: Chave do nó destino
            max_profundidade: Profundidade máxima de busca

        Returns:
            Lista de nós no caminho ou None se não encontrado
        """
        no_origem = self.obter_no(origem)
        no_destino = self.obter_no(destino)

        if not no_origem or not no_destino:
            return None

        # BFS simples
        visitados = set()
        fila = [(no_origem["id_no"], [origem])]

        with self.db._get_session() as session:
            from sqlalchemy import text

            while fila and len(fila[0][1]) <= max_profundidade:
                id_atual, caminho = fila.pop(0)

                if id_atual in visitados:
                    continue

                visitados.add(id_atual)

                # Verificar se chegamos ao destino
                if id_atual == no_destino["id_no"]:
                    return [{"chave": c} for c in caminho]

                # Buscar vizinhos
                result = session.execute(
                    text("""
                    SELECT gn.id_no, gn.chave
                    FROM grafo_aresta ga
                    JOIN grafo_no gn ON ga.id_no_destino = gn.id_no
                    WHERE ga.id_no_origem = :id_no
                """),
                    {"id_no": id_atual},
                ).fetchall()

                for id_vizinho, chave_vizinho in result:
                    if id_vizinho not in visitados:
                        fila.append((id_vizinho, caminho + [chave_vizinho]))

        return None

    def obter_nos_mais_conectados(self, limite: int = 10) -> List[Dict[str, Any]]:
        """
        Obter nós mais conectados (por grau de saída)

        Args:
            limite: Número de resultados

        Returns:
            Lista de nós mais conectados
        """
        with self.db._get_session() as session:
            from sqlalchemy import text

            result = session.execute(
                text("""
                SELECT 
                    gn.chave,
                    gn.tipo,
                    COUNT(ga.id_aresta) as grau
                FROM grafo_no gn
                LEFT JOIN grafo_aresta ga ON gn.id_no = ga.id_no_origem
                GROUP BY gn.id_no
                ORDER BY grau DESC
                LIMIT :limite
            """),
                {"limite": limite},
            ).fetchall()

            return [{"chave": row[0], "tipo": row[1], "grau": row[2]} for row in result]

    def close(self):
        """Fechar conexões"""
        if hasattr(self, "db"):
            self.db.close()

    # ============================================
    # PESOS DINÂMICOS (FASE 1: FUNDAÇÃO SISTÊMICA)
    # ============================================

    def fortalecer_relacoes_usadas(
        self, relacoes: List[Tuple[str, str, str]], qualidade: float
    ) -> Dict[str, Any]:
        """
        Fortalecer pesos de relações que foram úteis em uma consulta.

        Implementa: feedback positivo → peso aumenta

        Args:
            relacoes: Lista de tuplas (origem, destino, tipo_relacao)
            qualidade: Score de qualidade da consulta (0-1)

        Returns:
            Estatísticas da operação
        """
        with self.db._get_session() as session:
            from sqlalchemy import text

            relacoes_atualizadas = 0

            for origem, destino, tipo in relacoes:
                # Obter aresta atual
                no_origem = self.obter_no(origem)
                no_destino = self.obter_no(destino)

                if not no_origem or not no_destino:
                    continue

                # Buscar aresta
                result = session.execute(
                    text("""
                    SELECT id_aresta, peso FROM grafo_aresta
                    WHERE id_no_origem = :id_origem 
                    AND id_no_destino = :id_destino 
                    AND relacao = :tipo
                """),
                    {
                        "id_origem": no_origem["id_no"],
                        "id_destino": no_destino["id_no"],
                        "tipo": tipo,
                    },
                ).fetchone()

                if not result:
                    continue

                id_aresta, peso_atual = result

                # Calcular incremento baseado em qualidade
                incremento = qualidade * 0.05  # Max 5% por consulta

                # Novo peso (limitado a 1.0)
                novo_peso = min(1.0, peso_atual + incremento)

                # Salvar peso anterior no histórico
                session.execute(
                    text("""
                    INSERT INTO historico_peso 
                    (chave_origem, chave_destino, tipo_relacao, peso_anterior, peso_novo, motivo, qualidade_interacao)
                    VALUES (:origem, :destino, :tipo, :peso_ant, :peso_novo, 'uso', :qualidade)
                """),
                    {
                        "origem": origem,
                        "destino": destino,
                        "tipo": tipo,
                        "peso_ant": peso_atual,
                        "peso_novo": novo_peso,
                        "qualidade": qualidade,
                    },
                )

                # Atualizar peso
                session.execute(
                    text("""
                    UPDATE grafo_aresta 
                    SET peso = :novo_peso, updated_at = CURRENT_TIMESTAMP
                    WHERE id_aresta = :id_aresta
                """),
                    {"novo_peso": novo_peso, "id_aresta": id_aresta},
                )

                # Atualizar metadados
                session.execute(
                    text("""
                    INSERT INTO grafo_aresta_metadados 
                    (id_aresta, ultimo_uso, contador_uso, qualidade_media, aplicada_grafo)
                    VALUES (:id_aresta, CURRENT_TIMESTAMP, 1, :qualidade, 1)
                    ON CONFLICT(id_aresta) DO UPDATE SET
                        ultimo_uso = CURRENT_TIMESTAMP,
                        contador_uso = contador_uso + 1,
                        qualidade_media = (qualidade_media * contador_uso + :qualidade) / (contador_uso + 1),
                        aplicada_grafo = 1
                """),
                    {"id_aresta": id_aresta, "qualidade": qualidade},
                )

                relacoes_atualizadas += 1

            session.commit()

            return {
                "relacoes_processadas": len(relacoes),
                "relacoes_atualizadas": relacoes_atualizadas,
                "qualidade_consulta": qualidade,
                "timestamp": datetime.now().isoformat(),
            }

    def decaimento_temporal_pesos(self, dias_inatividade: int = 30) -> Dict[str, Any]:
        """
        Aplicar decaimento exponencial em arestas não usadas.

        Implementa: auto-regularização - conhecimento não usado enfraquece

        Args:
            dias_inatividade: Dias de inatividade para aplicar decaimento

        Returns:
            Estatísticas da operação
        """
        with self.db._get_session() as session:
            from sqlalchemy import text

            hoje = datetime.now()
            data_corte = hoje - timedelta(days=dias_inatividade)

            # Buscar arestas inativas
            result = session.execute(
                text("""
                SELECT 
                    ga.id_aresta,
                    ga.peso,
                    gno.chave as origem,
                    gnd.chave as destino,
                    ga.relacao,
                    gam.ultimo_uso
                FROM grafo_aresta ga
                JOIN grafo_no gno ON ga.id_no_origem = gno.id_no
                JOIN grafo_no gnd ON ga.id_no_destino = gnd.id_no
                LEFT JOIN grafo_aresta_metadados gam ON ga.id_aresta = gam.id_aresta
                WHERE gam.ultimo_uso IS NULL 
                   OR gam.ultimo_uso < :data_corte
            """),
                {"data_corte": data_corte},
            ).fetchall()

            arestas_removidas = 0
            arestas_enfraquecidas = 0

            for row in result:
                id_aresta, peso_atual, origem, destino, tipo, ultimo_uso = row

                # Calcular fator de decaimento (exponencial)
                if ultimo_uso:
                    dias_inativos = (hoje - ultimo_uso).days
                else:
                    dias_inativos = dias_inatividade

                # Decaimento exponencial: peso_novo = peso_atual * 0.95^(dias/30)
                fator_decaimento = 0.95 ** (dias_inativos / 30)
                novo_peso = peso_atual * fator_decaimento

                if novo_peso < 0.1:
                    # Remover aresta muito fraca
                    session.execute(
                        text("""
                        DELETE FROM grafo_aresta WHERE id_aresta = :id_aresta
                    """),
                        {"id_aresta": id_aresta},
                    )

                    session.execute(
                        text("""
                        DELETE FROM grafo_aresta_metadados WHERE id_aresta = :id_aresta
                    """),
                        {"id_aresta": id_aresta},
                    )

                    arestas_removidas += 1
                else:
                    # Registrar no histórico
                    session.execute(
                        text("""
                        INSERT INTO historico_peso 
                        (chave_origem, chave_destino, tipo_relacao, peso_anterior, peso_novo, motivo)
                        VALUES (:origem, :destino, :tipo, :peso_ant, :peso_novo, 'decaimento')
                    """),
                        {
                            "origem": origem,
                            "destino": destino,
                            "tipo": tipo,
                            "peso_ant": peso_atual,
                            "peso_novo": novo_peso,
                        },
                    )

                    # Atualizar peso
                    session.execute(
                        text("""
                        UPDATE grafo_aresta 
                        SET peso = :novo_peso, updated_at = CURRENT_TIMESTAMP
                        WHERE id_aresta = :id_aresta
                    """),
                        {"novo_peso": novo_peso, "id_aresta": id_aresta},
                    )

                    arestas_enfraquecidas += 1

            session.commit()

            # Registrar evento do sistema
            session.execute(
                text("""
                INSERT INTO evento_sistema (tipo_evento, detalhes_json)
                VALUES ('decaimento_temporal', :detalhes)
            """),
                {
                    "detalhes": json.dumps(
                        {
                            "arestas_removidas": arestas_removidas,
                            "arestas_enfraquecidas": arestas_enfraquecidas,
                            "dias_inatividade": dias_inatividade,
                            "executado_em": hoje.isoformat(),
                        }
                    )
                },
            )
            session.commit()

            return {
                "arestas_removidas": arestas_removidas,
                "arestas_enfraquecidas": arestas_enfraquecidas,
                "dias_inatividade": dias_inatividade,
                "executado_em": hoje.isoformat(),
            }

    def normalizar_pesos_no(self, chave_no: str) -> Dict[str, Any]:
        """
        Normalizar pesos das arestas de saída de um nó.

        Garante que a soma dos pesos não exceda um limite razoável,
        evitando inflação de pesos.

        Args:
            chave_no: Chave do nó para normalizar

        Returns:
            Estatísticas da operação
        """
        with self.db._get_session() as session:
            from sqlalchemy import text

            no = self.obter_no(chave_no)
            if not no:
                return {"erro": "Nó não encontrado"}

            # Buscar todas as arestas de saída
            result = session.execute(
                text("""
                SELECT 
                    ga.id_aresta,
                    ga.peso,
                    gnd.chave as destino,
                    ga.relacao
                FROM grafo_aresta ga
                JOIN grafo_no gnd ON ga.id_no_destino = gnd.id_no
                WHERE ga.id_no_origem = :id_no
            """),
                {"id_no": no["id_no"]},
            ).fetchall()

            if not result:
                return {"arestas_normalizadas": 0, "mensagem": "Nenhuma aresta de saída"}

            # Calcular soma total
            soma_pesos = sum(row[1] for row in result)

            # Se soma > 2.0, normalizar proporcionalmente
            if soma_pesos > 2.0:
                fator_normalizacao = 2.0 / soma_pesos
                arestas_normalizadas = 0

                for id_aresta, peso_atual, destino, tipo in result:
                    novo_peso = peso_atual * fator_normalizacao

                    # Registrar no histórico
                    session.execute(
                        text("""
                        INSERT INTO historico_peso 
                        (chave_origem, chave_destino, tipo_relacao, peso_anterior, peso_novo, motivo)
                        VALUES (:origem, :destino, :tipo, :peso_ant, :peso_novo, 'normalizacao')
                    """),
                        {
                            "origem": chave_no,
                            "destino": destino,
                            "tipo": tipo,
                            "peso_ant": peso_atual,
                            "peso_novo": novo_peso,
                        },
                    )

                    # Atualizar peso
                    session.execute(
                        text("""
                        UPDATE grafo_aresta 
                        SET peso = :novo_peso, updated_at = CURRENT_TIMESTAMP
                        WHERE id_aresta = :id_aresta
                    """),
                        {"novo_peso": novo_peso, "id_aresta": id_aresta},
                    )

                    arestas_normalizadas += 1

                session.commit()

                return {
                    "arestas_normalizadas": arestas_normalizadas,
                    "soma_anterior": soma_pesos,
                    "soma_nova": 2.0,
                    "fator_normalizacao": fator_normalizacao,
                }
            else:
                return {
                    "arestas_normalizadas": 0,
                    "mensagem": "Pesos já normalizados",
                    "soma_atual": soma_pesos,
                }

    def obter_estatisticas_grafo(self) -> Dict[str, Any]:
        """
        Obter estatísticas completas do grafo.

        Returns:
            Estatísticas detalhadas
        """
        with self.db._get_session() as session:
            from sqlalchemy import text

            # Contar nós
            nos = session.execute(text("SELECT COUNT(*) FROM grafo_no")).fetchone()[0]

            # Contar arestas
            arestas = session.execute(text("SELECT COUNT(*) FROM grafo_aresta")).fetchone()[0]

            # Calcular densidade (para grafo direcionado: arestas / (nos * (nos-1)))
            densidade = arestas / (nos * (nos - 1)) if nos > 1 else 0

            # Peso médio
            peso_medio = (
                session.execute(
                    text("""
                SELECT AVG(peso) FROM grafo_aresta
            """)
                ).fetchone()[0]
                or 0
            )

            # Nó mais conectado
            no_top = session.execute(
                text("""
                SELECT 
                    gn.chave,
                    COUNT(ga.id_aresta) as grau
                FROM grafo_no gn
                LEFT JOIN grafo_aresta ga ON gn.id_no = ga.id_no_origem
                GROUP BY gn.id_no
                ORDER BY grau DESC
                LIMIT 1
            """)
            ).fetchone()

            # Taxa de uso recente (última semana)
            data_semana = datetime.now() - timedelta(days=7)
            arestas_ativas = session.execute(
                text("""
                SELECT COUNT(*) FROM grafo_aresta_metadados
                WHERE ultimo_uso >= :data_semana
            """),
                {"data_semana": data_semana},
            ).fetchone()[0]

            return {
                "nos_total": nos,
                "arestas_total": arestas,
                "densidade": round(densidade, 4),
                "peso_medio": round(peso_medio, 3),
                "no_mais_conectado": {
                    "chave": no_top[0] if no_top else None,
                    "grau": no_top[1] if no_top else 0,
                },
                "arestas_ativas_semana": arestas_ativas,
                "taxa_atividade": round(arestas_ativas / arestas * 100, 2) if arestas > 0 else 0,
            }
