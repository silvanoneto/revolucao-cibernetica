#!/bin/bash
set -e

echo "🚀 Instalando Orquestrador de Conhecimento..."
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}📁 Diretório do projeto: $PROJECT_DIR${NC}"
echo ""

# 1. Verificar se uv está instalado
echo -e "${BLUE}1️⃣ Verificando uv package manager...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  uv não encontrado. Instalando...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo -e "${GREEN}✅ uv instalado com sucesso${NC}"
else
    echo -e "${GREEN}✅ uv já instalado${NC}"
fi
echo ""

# 2. Criar ambiente virtual
echo -e "${BLUE}2️⃣ Criando ambiente virtual Python...${NC}"
if [ -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Ambiente virtual já existe. Removendo...${NC}"
    rm -rf .venv
fi
uv venv .venv
echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
echo ""

# 3. Ativar ambiente virtual
echo -e "${BLUE}3️⃣ Ativando ambiente virtual...${NC}"
source .venv/bin/activate
echo -e "${GREEN}✅ Ambiente virtual ativado${NC}"
echo ""

# 4. Instalar dependências Python
echo -e "${BLUE}4️⃣ Instalando dependências Python...${NC}"
uv pip install -r requirements.txt
echo -e "${GREEN}✅ Dependências instaladas${NC}"
echo ""

# 5. Baixar e configurar Spark
echo -e "${BLUE}5️⃣ Configurando Apache Spark...${NC}"
./scripts/setup-spark.sh
echo -e "${GREEN}✅ Spark configurado${NC}"
echo ""

# 6. Criar diretórios necessários
echo -e "${BLUE}6️⃣ Criando estrutura de diretórios...${NC}"
mkdir -p data/db-data/embeddings-data/backups-logs
echo -e "${GREEN}✅ Diretórios criados${NC}"
echo ""

# 7. Inicializar banco de dados
echo -e "${BLUE}7️⃣ Inicializando banco de dados...${NC}"
python scripts/init-db.py
echo -e "${GREEN}✅ Banco de dados inicializado${NC}"
echo ""

# 8. Executar testes básicos
echo -e "${BLUE}8️⃣ Executando testes básicos...${NC}"
pytest tests/test_health.py -v
echo -e "${GREEN}✅ Testes básicos passaram${NC}"
echo ""

# Mensagem final
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Instalação concluída com sucesso! ✨${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📋 Próximos passos:${NC}"
echo ""
echo -e "  1. Ativar o ambiente virtual:"
echo -e "     ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo -e "  2. Iniciar o servidor:"
echo -e "     ${YELLOW}./scripts/start-server.sh${NC}"
echo ""
echo -e "  3. Acessar a documentação da API:"
echo -e "     ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
echo -e "  4. Ler o guia do agente:"
echo -e "     ${YELLOW}cat README.md${NC}"
echo ""
echo -e "${BLUE}🌱 Nhandereko - Nosso modo de ser juntos${NC}"
echo ""

