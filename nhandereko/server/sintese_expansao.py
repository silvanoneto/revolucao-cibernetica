"""
Módulo de Síntese e Expansão
Implementa os conceitos de:
- Primeira Ordem: Consultar/Sintetizar (processar conhecimento)
- Segunda Ordem: Registrar/Expandir (conectar conhecimento)
- Terceira Ordem: Sintetizar + Expandir (co-criar conhecimento)
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json


class SinteseManager:
    """
    Gerencia síntese de conhecimento (Primeira Ordem)

    Não retorna dados brutos - processa, condensa e sintetiza informação
    em conhecimento útil e contextualizado.
    """

    def __init__(self, db_manager, embeddings_manager, graph_manager):
        self.db = db_manager
        self.embeddings = embeddings_manager
        self.graph = graph_manager

    def sintetizar_entidade(self, chave: str) -> Dict[str, Any]:
        """
        Sintetiza informações sobre uma entidade.

        Ao invés de apenas retornar o registro do banco,
        processa e condensa em uma síntese útil.
        """
        # 1. Dados estruturais
        entidade = self.db.obter_entidade(chave)
        if not entidade:
            return None

        # 2. Contexto do grafo (relações)
        relacoes = self.graph.obter_vizinhos(chave, limite=10)

        # 3. Documentos relacionados (semânticos)
        docs_relacionados = self.embeddings.buscar_similares(
            query=entidade.get("nome", ""), top_k=5
        )

        # 4. SINTETIZAR tudo em resposta útil
        sintese = {
            "entidade": {
                "nome": entidade.get("nome"),
                "tipo": entidade.get("tipo"),
                "categoria": entidade.get("categoria"),
                "descricao": entidade.get("descricao"),
            },
            "relacoes_principais": self._processar_relacoes(relacoes),
            "contexto_semantico": self._processar_documentos(docs_relacionados),
            "metadados_sintese": {
                "timestamp": datetime.now().isoformat(),
                "fontes": ["estrutural", "grafo", "vetorial"],
                "qualidade": self._calcular_qualidade_sintese(
                    entidade, relacoes, docs_relacionados
                ),
            },
        }

        return sintese

    def sintetizar_consulta(self, query: str, top_k: int = 10) -> Dict[str, Any]:
        """
        Sintetiza resultados de uma busca semântica.

        Não apenas lista documentos - organiza, agrupa e sintetiza
        o conhecimento encontrado.
        """
        # 1. Buscar documentos
        documentos = self.embeddings.buscar_similares(query, top_k=top_k)

        # 2. Extrair entidades mencionadas
        entidades_mencionadas = self._extrair_entidades(documentos)

        # 3. Mapear relações entre entidades
        conexoes = self._mapear_conexoes(entidades_mencionadas)

        # 4. SINTETIZAR em estrutura útil
        sintese = {
            "query_original": query,
            "sintese_conhecimento": {
                "conceitos_chave": self._identificar_conceitos_chave(documentos),
                "relacoes_principais": self._sintetizar_relacoes(conexoes),
                "insights": self._gerar_insights(documentos, conexoes),
            },
            "documentos_fonte": [
                {
                    "texto": doc.get("texto", "")[:200] + "...",  # Preview
                    "relevancia": doc.get("score", 0),
                    "metadados": doc.get("metadados", {}),
                }
                for doc in documentos[:3]  # Top 3 apenas
            ],
            "metadados_sintese": {
                "timestamp": datetime.now().isoformat(),
                "documentos_analisados": len(documentos),
                "entidades_identificadas": len(entidades_mencionadas),
                "conexoes_mapeadas": len(conexoes),
                "score_sintese": self._calcular_score_sintese(documentos),
            },
        }

        return sintese

    def _processar_relacoes(self, relacoes: List[Dict]) -> List[Dict]:
        """Processa relações em formato sintético"""
        if not relacoes:
            return []

        # Agrupa por tipo e ordena por importância
        relacoes_processadas = []
        for rel in relacoes[:5]:  # Top 5 relações
            relacoes_processadas.append(
                {"destino": rel.get("destino"), "tipo": rel.get("tipo"), "peso": rel.get("peso", 0)}
            )

        return relacoes_processadas

    def _processar_documentos(self, documentos: List[Dict]) -> str:
        """Sintetiza documentos em contexto textual"""
        if not documentos:
            return "Sem contexto semântico disponível"

        # Extrai conceitos principais dos top 3 documentos
        conceitos = []
        for doc in documentos[:3]:
            texto = doc.get("texto", "")
            # Simplificado: em produção, usar NLP para extrair conceitos
            palavras_chave = texto.split()[:10]
            conceitos.extend(palavras_chave)

        return f"Contexto principal: {' '.join(set(conceitos[:20]))}"

    def _calcular_qualidade_sintese(self, entidade, relacoes, docs) -> float:
        """Calcula score de qualidade da síntese"""
        score = 0.0

        # Tem descrição?
        if entidade.get("descricao"):
            score += 0.3

        # Tem relações?
        if relacoes and len(relacoes) > 0:
            score += 0.3

        # Tem documentos relacionados?
        if docs and len(docs) > 0:
            score += 0.4

        return round(score, 2)

    def _extrair_entidades(self, documentos: List[Dict]) -> List[str]:
        """Extrai entidades mencionadas nos documentos"""
        # Simplificado: em produção, usar NER
        entidades = set()
        for doc in documentos:
            texto = doc.get("texto", "")
            # Buscar palavras capitalizadas como proxy de entidades
            palavras = texto.split()
            for palavra in palavras:
                if palavra[0].isupper() and len(palavra) > 3:
                    entidades.add(palavra.lower())

        return list(entidades)[:10]

    def _mapear_conexoes(self, entidades: List[str]) -> List[Dict]:
        """Mapeia conexões entre entidades no grafo"""
        conexoes = []
        for entidade in entidades:
            vizinhos = self.graph.obter_vizinhos(entidade, limite=3)
            if vizinhos:
                conexoes.extend(vizinhos)

        return conexoes

    def _identificar_conceitos_chave(self, documentos: List[Dict]) -> List[str]:
        """Identifica conceitos-chave nos documentos"""
        # Simplificado: análise de frequência
        todas_palavras = []
        for doc in documentos:
            texto = doc.get("texto", "")
            palavras = texto.lower().split()
            todas_palavras.extend(palavras)

        # Conta frequência (simplificado)
        from collections import Counter

        freq = Counter(todas_palavras)
        return [palavra for palavra, _ in freq.most_common(5)]

    def _sintetizar_relacoes(self, conexoes: List[Dict]) -> List[str]:
        """Sintetiza relações em frases"""
        if not conexoes:
            return []

        sinteses = []
        for conn in conexoes[:3]:
            sinteses.append(f"{conn.get('origem')} {conn.get('tipo')} {conn.get('destino')}")

        return sinteses

    def _gerar_insights(self, documentos: List[Dict], conexoes: List[Dict]) -> List[str]:
        """Gera insights baseados nos dados"""
        insights = []

        if len(documentos) > 5:
            insights.append(f"Alto volume de informação disponível ({len(documentos)} documentos)")

        if len(conexoes) > 3:
            insights.append("Entidade altamente conectada no grafo de conhecimento")

        return insights

    def _calcular_score_sintese(self, documentos: List[Dict]) -> float:
        """Calcula score de qualidade da síntese"""
        if not documentos:
            return 0.0

        # Média dos scores de relevância
        scores = [doc.get("score", 0) for doc in documentos]
        return round(sum(scores) / len(scores), 3)


class ExpansaoManager:
    """
    Gerencia expansão de conhecimento (Segunda Ordem)

    Não apenas acumula dados - cria conexões, enriquece o grafo,
    e expande organicamente a rede de conhecimento.
    """

    def __init__(self, db_manager, embeddings_manager, graph_manager):
        self.db = db_manager
        self.embeddings = embeddings_manager
        self.graph = graph_manager

    def expandir_com_documento(self, texto: str, metadados: Dict = None) -> Dict[str, Any]:
        """
        Adiciona documento E expande a rede de conhecimento.

        Não apenas insere - detecta relações, cria links, enriquece contexto.
        """
        if metadados is None:
            metadados = {}

        # 1. Adicionar documento (base)
        doc_id = self.embeddings.adicionar_documento(texto, metadados)

        # 2. Extrair entidades do texto
        entidades_novas = self._extrair_entidades_texto(texto)

        # 3. EXPANDIR: detectar conexões com conhecimento existente
        conexoes_criadas = []
        for entidade in entidades_novas:
            # Verificar se entidade já existe
            entidade_existente = self.db.obter_entidade(entidade)

            if entidade_existente:
                # Enriquecer entidade existente
                self._enriquecer_entidade(entidade, texto)

                # Criar conexões com outras entidades do texto
                for outra in entidades_novas:
                    if outra != entidade:
                        conexao = self.graph.criar_ou_fortalecer_aresta(
                            origem=entidade, destino=outra, tipo="co_ocorre", peso_incremento=0.1
                        )
                        if conexao:
                            conexoes_criadas.append(conexao)
            else:
                # Criar nova entidade
                self.db.criar_entidade(
                    {
                        "chave_negocio": entidade,
                        "nome": entidade,
                        "tipo": "auto_extraida",
                        "categoria": "conhecimento",
                        "descricao": f"Extraída do documento {doc_id}",
                        "atributos_json": json.dumps({"fonte_doc_id": doc_id}),
                    }
                )

        # 4. Calcular métricas de expansão
        metricas = self._calcular_metricas_expansao(entidades_novas, conexoes_criadas)

        return {
            "documento_id": doc_id,
            "expansao": {
                "entidades_novas": entidades_novas,
                "entidades_enriquecidas": self._contar_enriquecidas(entidades_novas),
                "conexoes_criadas": len(conexoes_criadas),
                "conexoes_detalhes": conexoes_criadas[:5],  # Top 5
            },
            "metricas": metricas,
        }

    def expandir_com_relacao(
        self, origem: str, destino: str, tipo: str, peso: float = 1.0, metadados: Dict = None
    ) -> Dict[str, Any]:
        """
        Cria relação E expande o contexto.

        Não apenas adiciona aresta - enriquece ambas as entidades,
        atualiza embeddings, fortalece conexões indiretas.
        """
        # 1. Criar/fortalecer aresta direta
        aresta = self.graph.criar_ou_fortalecer_aresta(
            origem=origem, destino=destino, tipo=tipo, peso_incremento=peso, metadados=metadados
        )

        # 2. EXPANDIR: detectar e fortalecer conexões indiretas
        expansao_indireta = self._expandir_conexoes_indiretas(origem, destino)

        # 3. Atualizar contexto semântico
        self._atualizar_contexto_semantico(origem, destino, tipo)

        return {
            "aresta_principal": aresta,
            "expansao_indireta": expansao_indireta,
            "metricas": {
                "conexoes_indiretas_fortalecidas": len(expansao_indireta),
                "grau_expansao": self._calcular_grau_expansao(origem, destino),
            },
        }

    def _extrair_entidades_texto(self, texto: str) -> List[str]:
        """Extrai entidades do texto"""
        # Simplificado: em produção, usar NER
        palavras = texto.split()
        entidades = []

        for palavra in palavras:
            if palavra[0].isupper() and len(palavra) > 3:
                entidades.append(palavra.lower())

        return list(set(entidades))[:10]

    def _enriquecer_entidade(self, chave: str, contexto: str):
        """Enriquece entidade existente com novo contexto"""
        # Atualizar embeddings com novo contexto
        self.embeddings.adicionar_documento(
            texto=f"{chave}: {contexto}", metadados={"tipo": "enriquecimento", "entidade": chave}
        )

    def _contar_enriquecidas(self, entidades: List[str]) -> int:
        """Conta quantas entidades foram enriquecidas"""
        contador = 0
        for entidade in entidades:
            if self.db.obter_entidade(entidade):
                contador += 1
        return contador

    def _calcular_metricas_expansao(
        self, entidades: List[str], conexoes: List[Dict]
    ) -> Dict[str, Any]:
        """Calcula métricas de expansão"""
        entidades_novas = len(entidades)
        conexoes_novas = len(conexoes)

        # Taxa de conectividade: conexões / entidades
        taxa_conectividade = conexoes_novas / entidades_novas if entidades_novas > 0 else 0

        return {
            "entidades_processadas": entidades_novas,
            "conexoes_criadas": conexoes_novas,
            "taxa_conectividade": round(taxa_conectividade, 2),
            "timestamp": datetime.now().isoformat(),
        }

    def _expandir_conexoes_indiretas(self, origem: str, destino: str) -> List[Dict]:
        """Expande conexões indiretas (transitivas)"""
        expansao = []

        # Vizinhos de origem
        viz_origem = self.graph.obter_vizinhos(origem, limite=5)

        # Vizinhos de destino
        viz_destino = self.graph.obter_vizinhos(destino, limite=5)

        # Fortalecer conexões entre vizinhos (triângulos)
        for v1 in viz_origem:
            for v2 in viz_destino:
                if v1.get("destino") == v2.get("origem"):
                    # Fortalecer conexão transitiva
                    aresta = self.graph.criar_ou_fortalecer_aresta(
                        origem=v1.get("destino"),
                        destino=v2.get("destino"),
                        tipo="transitiva",
                        peso_incremento=0.05,
                    )
                    if aresta:
                        expansao.append(aresta)

        return expansao

    def _atualizar_contexto_semantico(self, origem: str, destino: str, tipo: str):
        """Atualiza embeddings com nova relação"""
        contexto = f"{origem} {tipo} {destino}"
        self.embeddings.adicionar_documento(
            texto=contexto,
            metadados={
                "tipo": "relacao",
                "origem": origem,
                "destino": destino,
                "tipo_relacao": tipo,
            },
        )

    def _calcular_grau_expansao(self, origem: str, destino: str) -> float:
        """Calcula grau de expansão da rede"""
        # Número de novos caminhos criados
        viz_origem = len(self.graph.obter_vizinhos(origem, limite=100))
        viz_destino = len(self.graph.obter_vizinhos(destino, limite=100))

        # Grau médio de conexão
        grau_medio = (viz_origem + viz_destino) / 2

        return round(grau_medio / 10, 2)  # Normalizado
