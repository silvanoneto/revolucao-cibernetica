#!/bin/bash
set -e

echo "⚡ Configurando Apache Spark..."

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Diretórios
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPARK_DIR="$PROJECT_DIR/spark"
DOWNLOAD_DIR="/tmp"

# Detectar versão do PySpark instalado no .venv
echo -e "${BLUE}� Detectando versão do PySpark...${NC}"
if [ -f "$PROJECT_DIR/.venv/bin/python" ]; then
    PYSPARK_VERSION=$("$PROJECT_DIR/.venv/bin/python" -c "import pyspark; print(pyspark.__version__)" 2>/dev/null || echo "")
    if [ -z "$PYSPARK_VERSION" ]; then
        echo -e "${RED}❌ PySpark não encontrado no ambiente virtual${NC}"
        echo -e "${YELLOW}Execute 'uv pip install -r requirements.txt' primeiro${NC}"
        exit 1
    fi
    SPARK_VERSION=$PYSPARK_VERSION
    echo -e "${GREEN}✅ PySpark ${PYSPARK_VERSION} detectado${NC}"
else
    echo -e "${RED}❌ Ambiente virtual não encontrado${NC}"
    echo -e "${YELLOW}Execute './scripts/install.sh' primeiro${NC}"
    exit 1
fi

# Detectar versões de Hadoop e Scala baseado na versão do Spark
if [[ "$SPARK_VERSION" == 4.* ]]; then
    HADOOP_VERSION="3"
    SCALA_VERSION="2.13"
elif [[ "$SPARK_VERSION" == 3.5.* ]]; then
    HADOOP_VERSION="3"
    SCALA_VERSION="2.12"
else
    HADOOP_VERSION="3"
    SCALA_VERSION="2.12"
fi

echo -e "${BLUE}📦 Configuração:${NC}"
echo -e "${BLUE}   Spark: $SPARK_VERSION${NC}"
echo -e "${BLUE}   Hadoop: $HADOOP_VERSION${NC}"
echo -e "${BLUE}   Scala: $SCALA_VERSION${NC}"
echo ""

# Verificar se Spark já está instalado
if [ -d "$SPARK_DIR" ]; then
    INSTALLED_VERSION=$(cat "$SPARK_DIR/RELEASE" 2>/dev/null | grep 'Spark' | sed -n 's/.*Spark \([0-9.]*\).*/\1/p' || echo "unknown")
    if [ "$INSTALLED_VERSION" == "$SPARK_VERSION" ]; then
        echo -e "${GREEN}✅ Spark $SPARK_VERSION já instalado${NC}"
        exit 0
    fi
    if [ "$INSTALLED_VERSION" != "unknown" ]; then
        echo -e "${YELLOW}⚠️  Versão diferente instalada ($INSTALLED_VERSION)${NC}"
    else
        echo -e "${YELLOW}⚠️  Versão instalada desconhecida${NC}"
    fi
    echo -e "${YELLOW}Removendo para instalar versão $SPARK_VERSION...${NC}"
    rm -rf "$SPARK_DIR"
fi

# Verificar se Java está instalado
echo -e "${BLUE}☕ Verificando Java...${NC}"
if ! command -v java &> /dev/null; then
    echo -e "${YELLOW}⚠️  Java não encontrado.${NC}"
    echo -e "${YELLOW}Por favor, instale Java 11 ou superior:${NC}"
    echo -e "${YELLOW}  macOS: brew install openjdk@11${NC}"
    echo -e "${YELLOW}  Linux: sudo apt-get install openjdk-11-jdk${NC}"
    exit 1
else
    JAVA_VERSION=$(java -version 2>&1 | head -n 1)
    echo -e "${GREEN}✅ Java encontrado: $JAVA_VERSION${NC}"
fi
echo ""

# Baixar Spark
SPARK_PACKAGE="spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}"
SPARK_URL="https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz"
SPARK_MIRROR_URL="https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz"

echo -e "${BLUE}📥 Baixando Spark ${SPARK_VERSION}...${NC}"

cd "$DOWNLOAD_DIR"
DOWNLOAD_FILE="${SPARK_PACKAGE}.tgz"

if [ -f "$DOWNLOAD_FILE" ]; then
    echo -e "${YELLOW}⚠️  Arquivo já existe em cache${NC}"
    echo -e "${BLUE}Verificando integridade...${NC}"
    # Se o arquivo for muito pequeno (< 100MB), está corrompido
    FILE_SIZE=$(stat -f%z "$DOWNLOAD_FILE" 2>/dev/null || stat -c%s "$DOWNLOAD_FILE" 2>/dev/null)
    if [ "$FILE_SIZE" -lt 104857600 ]; then
        echo -e "${YELLOW}⚠️  Arquivo corrompido, removendo...${NC}"
        rm -f "$DOWNLOAD_FILE"
    else
        echo -e "${GREEN}✅ Usando arquivo em cache${NC}"
    fi
fi

if [ ! -f "$DOWNLOAD_FILE" ]; then
    echo -e "${BLUE}URL primária: $SPARK_URL${NC}"
    if curl -L --fail --progress-bar "$SPARK_URL" -o "$DOWNLOAD_FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ Download concluído${NC}"
    else
        echo -e "${YELLOW}⚠️  Falha no download, tentando mirror...${NC}"
        echo -e "${BLUE}URL mirror: $SPARK_MIRROR_URL${NC}"
        if curl -L --fail --progress-bar "$SPARK_MIRROR_URL" -o "$DOWNLOAD_FILE" 2>/dev/null; then
            echo -e "${GREEN}✅ Download concluído via mirror${NC}"
        else
            echo -e "${RED}❌ Falha no download do Spark${NC}"
            echo -e "${YELLOW}Por favor, baixe manualmente de:${NC}"
            echo -e "${YELLOW}  $SPARK_URL${NC}"
            echo -e "${YELLOW}e coloque em: $DOWNLOAD_DIR/${DOWNLOAD_FILE}${NC}"
            exit 1
        fi
    fi
fi
echo ""

# Extrair Spark
echo -e "${BLUE}📂 Extraindo Spark...${NC}"
tar -xzf "${SPARK_PACKAGE}.tgz"
mv "${SPARK_PACKAGE}" "$SPARK_DIR"
echo -e "${GREEN}✅ Spark extraído para $SPARK_DIR${NC}"
echo ""

# Configurar variáveis de ambiente
echo -e "${BLUE}🔧 Configurando variáveis de ambiente...${NC}"

# Detectar JAVA_HOME
if [ -n "$JAVA_HOME" ]; then
    DETECTED_JAVA_HOME="$JAVA_HOME"
elif command -v java &> /dev/null; then
    # No macOS com Homebrew
    if [ -d "/opt/homebrew/opt/openjdk@11" ]; then
        DETECTED_JAVA_HOME="/opt/homebrew/opt/openjdk@11"
    elif [ -d "/usr/local/opt/openjdk@11" ]; then
        DETECTED_JAVA_HOME="/usr/local/opt/openjdk@11"
    else
        # Tentar detectar pelo comando java
        JAVA_PATH=$(which java)
        DETECTED_JAVA_HOME=$(readlink -f "$JAVA_PATH" 2>/dev/null | sed 's:/bin/java::' || echo "/usr/lib/jvm/java-11-openjdk-amd64")
    fi
else
    DETECTED_JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
fi

ENV_FILE="$PROJECT_DIR/.env"
cat > "$ENV_FILE" << EOF
# Spark Configuration
export SPARK_HOME=$SPARK_DIR
export PATH=\$SPARK_HOME/bin:\$PATH
export PYSPARK_PYTHON=python3
export PYSPARK_DRIVER_PYTHON=python3

# Java Configuration
export JAVA_HOME=$DETECTED_JAVA_HOME

# Project Configuration
export PYTHONPATH=$PROJECT_DIR:\$PYTHONPATH
EOF

echo -e "${GREEN}✅ Arquivo .env criado${NC}"
echo ""

# Criar script de ativação
ACTIVATE_SCRIPT="$PROJECT_DIR/.venv/bin/activate-spark"
cat > "$ACTIVATE_SCRIPT" << 'EOF'
#!/bin/bash
# Ativar ambiente Spark
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$PROJECT_DIR/.env"
echo "⚡ Spark ativado: $SPARK_HOME"
EOF

chmod +x "$ACTIVATE_SCRIPT"
echo -e "${GREEN}✅ Script de ativação criado${NC}"
echo ""

# Criar configuração do Spark
SPARK_CONF_DIR="$SPARK_DIR/conf"
echo -e "${BLUE}⚙️  Criando configuração do Spark...${NC}"

cat > "$SPARK_CONF_DIR/spark-defaults.conf" << EOF
# Spark Configuration for Orquestrador de Conhecimento
spark.master                     local[*]
spark.driver.memory              2g
spark.executor.memory            2g
spark.sql.warehouse.dir          $PROJECT_DIR/data/spark-warehouse
spark.eventLog.enabled           true
spark.eventLog.dir               $PROJECT_DIR/logs/spark-events
spark.history.fs.logDirectory    $PROJECT_DIR/logs/spark-events

# Performance
spark.sql.adaptive.enabled       true
spark.sql.adaptive.coalescePartitions.enabled  true

# Logging
spark.driver.extraJavaOptions    -Dlog4j.configuration=file:$SPARK_CONF_DIR/log4j.properties
spark.executor.extraJavaOptions  -Dlog4j.configuration=file:$SPARK_CONF_DIR/log4j.properties
EOF

echo -e "${GREEN}✅ Configuração do Spark criada${NC}"
echo ""

# Configurar logging
cat > "$SPARK_CONF_DIR/log4j.properties" << EOF
# Set everything to WARN
log4j.rootCategory=WARN, console

# Console appender
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=System.err
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n

# Settings to quiet third party logs
log4j.logger.org.apache.spark=WARN
log4j.logger.org.spark_project.jetty=WARN
log4j.logger.org.apache.hadoop=WARN
log4j.logger.io.netty=WARN
log4j.logger.org.apache.zookeeper=WARN
EOF

echo -e "${GREEN}✅ Logging configurado${NC}"
echo ""

# Criar diretórios necessários
mkdir -p "$PROJECT_DIR/data/spark-warehouse"
mkdir -p "$PROJECT_DIR/logs/spark-events"

# Testar instalação
echo -e "${BLUE}🧪 Testando instalação do Spark...${NC}"
source "$ENV_FILE"

"$SPARK_DIR/bin/spark-submit" --version 2>&1 | head -n 1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Spark instalado e funcionando corretamente!${NC}"
else
    echo -e "${YELLOW}⚠️  Erro ao testar Spark${NC}"
    exit 1
fi
echo ""

# Limpar arquivos temporários
echo -e "${BLUE}🧹 Limpando arquivos temporários...${NC}"
rm -f "$DOWNLOAD_DIR/${SPARK_PACKAGE}.tgz"
echo -e "${GREEN}✅ Limpeza concluída${NC}"
echo ""

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}⚡ Spark configurado com sucesso! ⚡${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Para usar o Spark, ative o ambiente:${NC}"
echo -e "${YELLOW}source .env${NC}"
echo ""

