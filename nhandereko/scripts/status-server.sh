#!/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$PROJECT_DIR/logs/server.pid"
LOG_FILE="$PROJECT_DIR/logs/server.log"

echo -e "${BLUE}📊 Status do Orquestrador de Conhecimento${NC}"
echo ""

# Verificar status do servidor
if [ -f "$PID_FILE" ]; then
    SERVER_PID=$(cat "$PID_FILE")
    
    if ps -p "$SERVER_PID" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Servidor está rodando${NC}"
        echo -e "${BLUE}📋 PID: $SERVER_PID${NC}"
        
        # Informações do processo
        echo -e "${BLUE}🔧 Informações do processo:${NC}"
        ps -p "$SERVER_PID" -o pid,ppid,%cpu,%mem,etime,command | tail -n 1
        echo ""
        
        # Verificar se log existe
        if [ -f "$LOG_FILE" ]; then
            echo -e "${BLUE}📝 Últimas linhas do log:${NC}"
            echo -e "${YELLOW}────────────────────────────────────────${NC}"
            tail -n 10 "$LOG_FILE"
            echo -e "${YELLOW}────────────────────────────────────────${NC}"
            echo ""
            echo -e "${BLUE}💡 Para ver logs em tempo real: tail -f $LOG_FILE${NC}"
        else
            echo -e "${YELLOW}⚠️  Arquivo de log não encontrado${NC}"
        fi
    else
        echo -e "${RED}❌ Servidor não está rodando${NC}"
        echo -e "${YELLOW}(Arquivo PID existe mas processo não está ativo)${NC}"
        echo ""
        echo -e "${BLUE}🔧 Para iniciar o servidor:${NC}"
        echo -e "  ./scripts/start-server.sh          # Modo interativo"
        echo -e "  ./scripts/start-server.sh -d       # Modo daemon (segundo plano)"
    fi
else
    echo -e "${RED}❌ Servidor não está rodando${NC}"
    echo ""
    echo -e "${BLUE}🔧 Para iniciar o servidor:${NC}"
    echo -e "  ./scripts/start-server.sh          # Modo interativo"
    echo -e "  ./scripts/start-server.sh -d       # Modo daemon (segundo plano)"
fi

echo ""
