#!/bin/bash
set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Modo daemon (segundo plano)
DAEMON_MODE=false

# Parse argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--daemon)
            DAEMON_MODE=true
            shift
            ;;
        -h|--help)
            echo "Uso: $0 [opções]"
            echo ""
            echo "Opções:"
            echo "  -d, --daemon    Executar servidor em segundo plano (daemon mode)"
            echo "  -h, --help      Mostrar esta mensagem de ajuda"
            echo ""
            echo "Exemplos:"
            echo "  $0              # Executar em primeiro plano (padrão)"
            echo "  $0 -d           # Executar em segundo plano"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Argumento desconhecido: $1${NC}"
            echo "Use -h ou --help para ver as opções disponíveis"
            exit 1
            ;;
    esac
done

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}🚀 Iniciando Orquestrador de Conhecimento...${NC}"
echo ""

# Verificar se ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Ambiente virtual não encontrado!${NC}"
    echo -e "${BLUE}Execute primeiro: ./scripts/install.sh${NC}"
    exit 1
fi

# Ativar ambiente virtual
echo -e "${BLUE}📦 Ativando ambiente virtual...${NC}"
source .venv/bin/activate

# Carregar variáveis de ambiente
if [ -f ".env" ]; then
    echo -e "${BLUE}🔧 Carregando variáveis de ambiente...${NC}"
    source .env
fi

# Verificar se banco de dados existe
if [ ! -f "data/db/orquestrador.db" ]; then
    echo -e "${YELLOW}⚠️  Banco de dados não encontrado!${NC}"
    echo -e "${BLUE}Inicializando banco de dados...${NC}"
    python scripts/init-db.py
fi

# Criar diretório de logs
mkdir -p logs

# Arquivo PID para controle do processo
PID_FILE="$PROJECT_DIR/logs/server.pid"

# Verificar se servidor já está rodando
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Servidor já está rodando (PID: $OLD_PID)${NC}"
        echo -e "${BLUE}Para parar o servidor, execute: ./scripts/stop-server.sh${NC}"
        exit 1
    else
        # PID file existe mas processo não está rodando
        rm -f "$PID_FILE"
    fi
fi

# Iniciar servidor
echo -e "${GREEN}✨ Iniciando servidor...${NC}"
echo ""

cd server

if [ "$DAEMON_MODE" = true ]; then
    # Modo daemon: redirecionar para logs e executar em segundo plano
    LOG_FILE="$PROJECT_DIR/logs/server.log"
    echo -e "${BLUE}📝 Logs serão salvos em: $LOG_FILE${NC}"
    echo -e "${BLUE}🔧 Para ver os logs em tempo real: tail -f $LOG_FILE${NC}"
    echo -e "${BLUE}🛑 Para parar o servidor: ./scripts/stop-server.sh${NC}"
    echo ""
    
    # Executar em segundo plano e salvar PID
    nohup python main.py > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    echo $SERVER_PID > "$PID_FILE"
    
    echo -e "${GREEN}✅ Servidor iniciado em segundo plano (PID: $SERVER_PID)${NC}"
    echo ""
else
    # Modo normal: executar em primeiro plano
    python main.py
fi

