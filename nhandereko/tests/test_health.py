"""
Testes básicos de saúde do sistema
"""

import pytest
from pathlib import Path
import sys

# Adicionar diretório do projeto ao path
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))


def test_project_structure():
    """Testar se a estrutura do projeto está correta"""
    assert (project_dir / "server").exists()
    assert (project_dir / "scripts").exists()
    assert (project_dir / "docs").exists()
    assert (project_dir / "data").exists()


def test_database_exists():
    """Testar se o banco de dados foi criado"""
    db_path = project_dir / "data" / "db" / "orquestrador.db"
    assert db_path.exists(), "Banco de dados não encontrado"


def test_import_modules():
    """Testar se os módulos podem ser importados"""
    try:
        from server import config
        from server import database
        from server import embeddings
        from server import graph

        assert True
    except ImportError as e:
        pytest.fail(f"Erro ao importar módulos: {e}")


def test_config_settings():
    """Testar se as configurações estão corretas"""
    from server.config import settings

    assert settings.host is not None
    assert settings.port > 0
    assert settings.database_url is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
