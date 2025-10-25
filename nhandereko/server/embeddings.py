"""
Gerenciador de Embeddings
Camada de Memória (Vector Database)
"""

import os
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer


class EmbeddingsManager:
    """Gerencia embeddings e busca vetorial"""

    def __init__(self, model_name: str, persist_dir: str = None):
        """
        Inicializar gerenciador de embeddings

        Args:
            model_name: Nome do modelo de embeddings
            persist_dir: Diretório para persistir os dados
        """
        self.model_name = model_name

        # Configurar diretório de persistência
        if persist_dir is None:
            project_dir = Path(__file__).parent.parent
            persist_dir = project_dir / "data" / "embeddings"

        persist_dir = Path(persist_dir)
        persist_dir.mkdir(parents=True, exist_ok=True)

        # Inicializar modelo de embeddings
        print(f"📥 Carregando modelo de embeddings: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("✅ Modelo carregado")

        # Inicializar ChromaDB
        print("📦 Inicializando ChromaDB...")
        self.client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False, allow_reset=True),
        )

        # Obter ou criar coleção
        self.collection = self.client.get_or_create_collection(
            name="documentos",
            metadata={"description": "Documentos do Orquestrador de Conhecimento"},
        )
        print("✅ ChromaDB inicializado")

    def adicionar_documento(
        self, texto: str, metadados: Optional[Dict[str, Any]] = None, doc_id: Optional[str] = None
    ) -> str:
        """
        Adicionar documento à base vetorial

        Args:
            texto: Texto do documento
            metadados: Metadados opcionais
            doc_id: ID opcional do documento

        Returns:
            ID do documento adicionado
        """
        if doc_id is None:
            doc_id = str(uuid.uuid4())

        # Gerar embedding
        embedding = self.model.encode(texto).tolist()

        # Preparar metadados
        if metadados is None:
            metadados = {}

        # Adicionar à coleção
        self.collection.add(
            ids=[doc_id], embeddings=[embedding], documents=[texto], metadatas=[metadados]
        )

        return doc_id

    def adicionar_documentos_lote(
        self,
        textos: List[str],
        metadados: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Adicionar múltiplos documentos em lote

        Args:
            textos: Lista de textos
            metadados: Lista de metadados (opcional)
            ids: Lista de IDs (opcional)

        Returns:
            Lista de IDs dos documentos adicionados
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in textos]

        if metadados is None:
            metadados = [{} for _ in textos]

        # Gerar embeddings em lote
        embeddings = self.model.encode(textos).tolist()

        # Adicionar à coleção
        self.collection.add(ids=ids, embeddings=embeddings, documents=textos, metadatas=metadados)

        return ids

    def buscar(
        self, query: str, top_k: int = 5, filtros: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Buscar documentos por similaridade semântica

        Args:
            query: Texto da busca
            top_k: Número de resultados
            filtros: Filtros de metadados (opcional)

        Returns:
            Lista de documentos encontrados
        """
        # Gerar embedding da query
        query_embedding = self.model.encode(query).tolist()

        # Buscar na coleção
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k, where=filtros
        )

        # Formatar resultados
        documentos = []
        for i in range(len(results["ids"][0])):
            documentos.append(
                {
                    "id": results["ids"][0][i],
                    "texto": results["documents"][0][i],
                    "metadados": results["metadatas"][0][i],
                    "distancia": results["distances"][0][i] if "distances" in results else None,
                    "score": 1 - results["distances"][0][i] if "distances" in results else None,
                }
            )

        return documentos

    def obter_documento(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Obter documento por ID

        Args:
            doc_id: ID do documento

        Returns:
            Documento ou None se não encontrado
        """
        try:
            result = self.collection.get(ids=[doc_id])

            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "texto": result["documents"][0],
                    "metadados": result["metadatas"][0],
                }
            return None
        except Exception:
            return None

    def atualizar_documento(
        self, doc_id: str, texto: Optional[str] = None, metadados: Optional[Dict[str, Any]] = None
    ):
        """
        Atualizar documento existente

        Args:
            doc_id: ID do documento
            texto: Novo texto (opcional)
            metadados: Novos metadados (opcional)
        """
        update_data = {"ids": [doc_id]}

        if texto is not None:
            embedding = self.model.encode(texto).tolist()
            update_data["embeddings"] = [embedding]
            update_data["documents"] = [texto]

        if metadados is not None:
            update_data["metadatas"] = [metadados]

        self.collection.update(**update_data)

    def remover_documento(self, doc_id: str):
        """
        Remover documento

        Args:
            doc_id: ID do documento
        """
        self.collection.delete(ids=[doc_id])

    def contar_documentos(self) -> int:
        """
        Contar total de documentos

        Returns:
            Número de documentos
        """
        return self.collection.count()

    def limpar_colecao(self):
        """Limpar todos os documentos da coleção"""
        self.client.delete_collection("documentos")
        self.collection = self.client.create_collection(
            name="documentos",
            metadata={"description": "Documentos do Orquestrador de Conhecimento"},
        )

    def close(self):
        """Fechar conexões"""
        # ChromaDB persiste automaticamente
        pass
