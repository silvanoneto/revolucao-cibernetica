#!/bin/bash
set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$PROJECT_DIR/logs/server.pid"

echo -e "${BLUE}🛑 Parando Orquestrador de Conhecimento...${NC}"
echo ""

# Tentar usar arquivo PID primeiro
if [ -f "$PID_FILE" ]; then
    SERVER_PID=$(cat "$PID_FILE")
    
    if ps -p "$SERVER_PID" > /dev/null 2>&1; then
        echo -e "${BLUE}📋 PID do servidor: $SERVER_PID${NC}"
        echo -e "${BLUE}🔄 Enviando sinal TERM...${NC}"
        
        kill -TERM "$SERVER_PID"
        
        # Aguardar processo terminar (timeout de 10 segundos)
        TIMEOUT=10
        COUNT=0
        while ps -p "$SERVER_PID" > /dev/null 2>&1; do
            if [ $COUNT -ge $TIMEOUT ]; then
                echo -e "${YELLOW}⚠️  Processo não respondeu ao TERM, forçando término...${NC}"
                kill -KILL "$SERVER_PID"
                sleep 1
                break
            fi
            sleep 1
            COUNT=$((COUNT + 1))
            echo -n "."
        done
        
        echo ""
        rm -f "$PID_FILE"
        echo -e "${GREEN}✅ Servidor parado com sucesso!${NC}"
        exit 0
    else
        # PID file existe mas processo não está rodando
        echo -e "${YELLOW}⚠️  Arquivo PID existe mas processo não está rodando${NC}"
        rm -f "$PID_FILE"
    fi
fi

# Fallback: procurar processo manualmente
echo -e "${BLUE}🔍 Procurando processo do servidor...${NC}"
PID=$(ps aux | grep "python.*server/main.py" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo -e "${YELLOW}⚠️  Servidor não está rodando${NC}"
    exit 0
fi

# Parar processo encontrado
echo -e "${BLUE}📋 PID encontrado: $PID${NC}"
kill $PID

echo -e "${GREEN}✅ Servidor parado (PID: $PID)${NC}"
echo ""

