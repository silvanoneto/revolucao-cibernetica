"""
Configurações do Orquestrador de Conhecimento
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Diretório do projeto
PROJECT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Configurações da aplicação"""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # Ignorar variáveis extras do .env (Spark, Java, etc)
    )

    # Servidor
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Banco de dados
    database_url: str = f"sqlite:///{PROJECT_DIR}/data/db/orquestrador.db"

    # Embeddings
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings_dir: str = str(PROJECT_DIR / "data" / "embeddings")

    # Spark
    spark_home: Optional[str] = os.getenv("SPARK_HOME")
    spark_master: str = "local[*]"
    spark_driver_memory: str = "2g"
    spark_executor_memory: str = "2g"

    # Grafo
    graph_db_type: str = "sqlite"  # sqlite ou neo4j
    neo4j_uri: Optional[str] = None
    neo4j_user: Optional[str] = None
    neo4j_password: Optional[str] = None

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # segundos

    # Logging
    log_level: str = "INFO"
    log_dir: str = str(PROJECT_DIR / "logs")


# Instância global
settings = Settings()
