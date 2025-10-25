# 🌱 Nhandereko

Sistema de Inteligência Coletiva com Feedback Loops Recursivos

> *"Nhandereko" (guarani): "Nosso modo de ser juntos"*

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

## 📋 Visão Geral

**Nhandereko** é uma implementação concreta de **cibernética de segunda ordem** aplicada a sistemas de conhecimento coletivo. Baseado na filosofia do [Manifesto da Revolução Cibernética](../manifesto.html), o sistema opera em **três níveis recursivos de feedback loops**, cada um contendo e sendo contido pelos outros.

### ✨ Novidades - Fase 1 Completa (Outubro 2025)

- ✅ **Endpoint híbrido** `/consultar/hibrida` - Integra 4 camadas + 3 ordens
- ✅ **Pesos dinâmicos** - Grafo evolui baseado em qualidade de feedback
- ✅ **Métricas em tempo real** - 4 endpoints de monitoramento de saúde
- ✅ **7 novas tabelas** - Infraestrutura para multi-agentes e consolidação
- ✅ **Documentação completa** - Arquitetura, exemplos, melhorias

Veja detalhes em [docs/MELHORIAS_IMPLEMENTADAS.md](docs/MELHORIAS_IMPLEMENTADAS.md)

### 🌀 Os Três Níveis de Loops

```
LOOP 3: META-CRIAÇÃO
  "Como nós criamos sistemas que aprendem juntos?"
  ↓
  LOOP 2: SISTEMA NHANDEREKO
    "Como o sistema aprende com cada interação?"
    ↓
    LOOP 1: OPERAÇÃO
      "Como o agente consulta e registra?"
```

### 🎯 Três Ordens Operacionais

| Ordem | Nome | Ação | Feedback | Aprendizado | Uso |
|-------|------|------|----------|-------------|-----|
| 🔵 **Primeira** | Síntese | Consultar/Sintetizar | Read-only | Zero | Produção estável |
| 🟢 **Segunda** | Expansão | Registrar/Expandir | Write-only | Acumulação | Exploração |
| 🟣 **Terceira** | Evolução | Sintetizar + Expandir | Read-write | Evolutivo | Meta-aprendizado |

Veja explicação completa em [docs/TRES_LOOPS.md](docs/TRES_LOOPS.md)

### 🤖 Uso por Agentes LLM

O sistema é projetado para ser usado por **agentes LLM inteligentes** que seguem um processo de refinamento **baseado na dinâmica sintetizar ↔ expandir**.

#### 🔄 Modelo Lógico de Refinamento (Sintetizar ↔ Expandir)

O refinamento não é uma sequência fixa, mas um **processo dialético** que alterna entre:

**🔵 SINTETIZAR** (Condensar/Focar)  
**🟢 EXPANDIR** (Conectar/Ampliar)

```text
╔═══════════════════════════════════════════════════════════╗
║  CICLO DE REFINAMENTO: SINTETIZAR ↔ EXPANDIR             ║
╚═══════════════════════════════════════════════════════════╝

1️⃣ SINTETIZAR: Focar na essência
   └─→ "O que é REALMENTE essencial nesta tarefa?"
   └─→ "Qual é o núcleo mínimo que preciso entender?"

2️⃣ EXPANDIR: Ampliar contexto
   └─→ "Que contextos/relações estou ignorando?"
   └─→ "Que perguntas novas surgiram?"

3️⃣ SINTETIZAR: Decidir ordem operacional
   └─→ "Baseado no que descobri, qual ordem faz sentido?"
   └─→ 🔵 Primeira | 🟢 Segunda | 🟣 Terceira

4️⃣ EXPANDIR: Explorar camadas
   └─→ "Que camadas conectam com minha necessidade?"
   └─→ 🏛️ SQL | 🕸️ Graph | 🧠 Vector

5️⃣ SINTETIZAR: Plano de ação
   └─→ "Quais endpoints, em que sequência?"
   └─→ "Como sintetizo os resultados?"

6️⃣ EXPANDIR: Aprendizado emergente
   └─→ "Que descobertas inesperadas emergiram?"
   └─→ "Como isso expande o conhecimento do sistema?"

7️⃣ SINTETIZAR + EXPANDIR (Meta-reflexão)
   └─→ "Meu processo de refinamento está funcionando?"
   └─→ "Que novas perguntas devo fazer na próxima vez?"

...
═══════════════════════════════════════════════════════════

⚠️  Este é um MODELO, não um SCRIPT
    • Você pode pular etapas
    • Você pode voltar atrás
    • Você pode fazer loops
    • Você pode inventar novas perguntas
    
🌀  O processo é FRACTAL: sintetizar/expandir em cada nível
```

#### 🌀 Características do Modelo

- **Dialético**: Oscila entre condensar e ampliar
- **Recursivo**: Aplica-se a si mesmo (meta-reflexão)
- **Emergente**: Novas perguntas surgem do processo
- **Adaptativo**: Muda conforme o contexto muda

#### 🎯 Responsabilidades do Agente

- 🧠 **Sintetizar continuamente**: Extrair essência do que descobre
- 🌐 **Expandir contextualmente**: Conectar com conhecimento mais amplo
- 🔄 **Alternar dinamicamente**: Não ficar preso em um modo
- 📊 **Meta-refletir**: Questionar o próprio processo
- 📝 **Documentar emergências**: Capturar insights não-planejados

> **🌱 Filosofia**: O refinamento É o processo de sintetizar ↔ expandir aplicado à própria tarefa. Você não refina ANTES de agir — você refina ENQUANTO age. É Loop 3 puro!

Veja exemplos completos em [docs/EXEMPLOS.md](docs/EXEMPLOS.md)

## 🚀 Quick Start

### Instalação Rápida (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/silvanoneto/revolucao-cibernetica.git
cd revolucao-cibernetica/nhandereko

# 2. Execute o script de instalação (cria venv, instala deps, configura DB)
./scripts/install.sh

# 3. Ative o ambiente virtual
source .venv/bin/activate

# 4. Inicie o servidor
./scripts/start-server.sh
```

**Acesse:** 
- API: `http://localhost:8000`
- Docs interativos: `http://localhost:8000/docs`
- Métricas: `http://localhost:8000/metricas/saude-sistema`

### Verificar Status

```bash
# Ver status do servidor
./scripts/status-server.sh

# Ver logs em tempo real
tail -f logs/server.log

# Parar servidor
./scripts/stop-server.sh
```

### Teste Rápido (via curl)

```bash
# Consulta híbrida (3 ordens + 4 camadas)
curl -X POST "http://localhost:8000/consultar/hibrida" \
  -H "Content-Type: application/json" \
  -d '{
    "ordem": "terceira",
    "consulta": "Como organizar trabalhadores de plataforma?",
    "agente_id": "teste-001",
    "contexto": {"dominio": "trabalho-digital"}
  }'

# Ver métricas em tempo real
curl "http://localhost:8000/metricas/saude-sistema"
```

> **💡 Dica**: Use o Swagger UI em `/docs` para testar interativamente todos os endpoints!

### Instalação Manual (Opcional)

<details>
<summary>Clique para ver passos detalhados</summary>

```bash
# 1. Instalar uv (gerenciador de pacotes Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Criar ambiente virtual
uv venv .venv
source .venv/bin/activate

# 3. Instalar dependências
uv pip install -r requirements.txt

# 4. Baixar e configurar Spark (opcional, para processamento distribuído)
./scripts/setup-spark.sh

# 5. Inicializar banco de dados (cria 21 tabelas)
python scripts/init-db.py

# 6. Iniciar servidor
python server/main.py
```

</details>

## 📚 Documentação

### � Comece Aqui

1. **[docs/TRES_LOOPS.md](docs/TRES_LOOPS.md)** ⚡ **LEIA PRIMEIRO!** - Filosofia dos três loops
2. **[docs/ARQUITETURA.md](docs/ARQUITETURA.md)** - 4 camadas + 3 ordens explicadas
3. **[docs/EXEMPLOS.md](docs/EXEMPLOS.md)** - Exemplos práticos de uso

### 🔧 Implementação Fase 1

- **[docs/MELHORIAS_IMPLEMENTADAS.md](docs/MELHORIAS_IMPLEMENTADAS.md)** - O que foi feito na Fase 1
- **[docs/MELHORIAS_PROPOSTAS.md](docs/MELHORIAS_PROPOSTAS.md)** - Roadmap Fase 2 e 3
- **[docs/INFORMACAO_COMO_LIGA.md](docs/INFORMACAO_COMO_LIGA.md)** - Síntese filosófica

### � Operação e Métricas

- **[docs/METRICAS.md](docs/METRICAS.md)** - Sistema de métricas e monitoramento
- **[docs/GERENCIAMENTO_SERVIDOR.md](docs/GERENCIAMENTO_SERVIDOR.md)** - Deploy e administração

## 🎯 Uso Básico

### Endpoint Híbrido (Novo! Recomendado)

O endpoint `/consultar/hibrida` integra as 4 camadas arquiteturais automaticamente:

```python
import requests

response = requests.post(
    "http://localhost:8000/consultar/hibrida",
    json={
        "ordem": "terceira",  # primeira | segunda | terceira
        "consulta": "Como organizar cooperativas digitais?",
        "agente_id": "agente-001",
        "contexto": {
            "dominio": "economia-solidaria",
            "prioridade": "pratico"
        },
        "camadas_ativas": ["sql", "graph", "vector"],  # opcional
        "pesos_camadas": {"graph": 0.5, "vector": 0.3, "sql": 0.2}  # opcional
    }
)

resultado = response.json()
print(f"Síntese: {resultado['sintese']}")
print(f"Camadas usadas: {resultado['camadas_consultadas']}")
print(f"Qualidade: {resultado['metricas']['confianca_media']}")
```

### Endpoints por Camada

#### 🏛️ Camada Estrutural (SQL)

```python
# Consultar entidades
GET /sql/entidade/{nome_entidade}

# Registrar consulta
POST /sql/consulta
{
  "chave_agente": "agente-001",
  "tipo_consulta": "hibrida",
  "query_texto": "Buscar cooperativas",
  "qualidade_score": 0.85
}

# Registrar descoberta
POST /sql/descoberta
{
  "chave_agente": "agente-001",
  "tipo_descoberta": "padrao",
  "descricao": "Cooperativas crescem 20% ao ano",
  "confianca": 0.90
}
```

#### 🕸️ Camada Relacional (Grafo)

```python
# Adicionar nó
POST /graph/no
{
  "entidade": "cooperativa",
  "nome": "CoopTech Brasil",
  "metadados": {"membros": 150}
}

# Adicionar relação
POST /graph/relacao
{
  "origem": "CoopTech Brasil",
  "destino": "Software Livre",
  "tipo": "usa",
  "peso": 0.8
}

# Buscar vizinhos
GET /graph/vizinhos/{entidade}/{nome}?profundidade=2

# Fortalecer relações usadas (pesos dinâmicos!)
POST /graph/fortalecer-relacoes
{
  "relacoes": [
    {"origem": "A", "destino": "B", "tipo": "conecta"},
    {"origem": "B", "destino": "C", "tipo": "influencia"}
  ],
  "fator_qualidade": 0.9
}
```

#### 🧠 Camada de Memória (Embeddings)

```python
# Adicionar documento
POST /adicionar
{
  "texto": "Cooperativas digitais são alternativa ao capitalismo de plataforma...",
  "metadados": {
    "fonte": "manifesto",
    "autor": "coletivo"
  }
}

# Busca semântica
POST /buscar
{
  "query": "alternativas ao Uber",
  "top_k": 5,
  "filtro_metadados": {"fonte": "manifesto"}
}
```

### 📊 Endpoints de Métricas (Novo!)

```python
# Saúde geral do sistema
GET /metricas/saude-sistema

# Qualidade de síntese (Primeira Ordem)
GET /metricas/qualidade-sintese?agente_id=agente-001&dias=7

# Expansão de conhecimento (Segunda Ordem)
GET /metricas/expansao-conhecimento?dias=30

# Evolução do agente (Terceira Ordem)
GET /metricas/evolucao-agente?agente_id=agente-001&dias=90
```

## 🏗️ Arquitetura

### 4 Camadas Complementares

```
┌─────────────────────────────────────────┐
│  🏛️  Estrutural (SQL)                   │
│  Fatos, entidades, esquema rígido       │
├─────────────────────────────────────────┤
│  📜  Histórica (Eventos)                │
│  Timeline, audit trail, evolução        │
├─────────────────────────────────────────┤
│  🕸️  Relacional (Grafo NetworkX)        │
│  Conexões, pesos dinâmicos, clusters    │
├─────────────────────────────────────────┤
│  🧠  Memória (Embeddings)               │
│  Semântica, busca vetorial, contexto    │
└─────────────────────────────────────────┘
```

### 3 Ordens Operacionais

- **🔵 Primeira (Síntese):** Read-only, produção estável, zero aprendizado
- **🟢 Segunda (Expansão):** Write-only, exploração, acumulação
- **🟣 Terceira (Evolução):** Read-write, feedback bidirecional, meta-aprendizado

Cada ordem escolhe quais camadas consultar baseado na necessidade.

## 🛠️ Stack Tecnológico

- **Backend:** FastAPI 0.104+ (Python 3.11+)
- **Banco SQL:** SQLite com 21 tabelas
- **Grafo:** NetworkX com pesos dinâmicos
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Busca Vetorial:** ChromaDB
- **Processamento:** Apache Spark (opcional, distribuído)
- **Métricas:** Endpoints REST em tempo real

Veja exemplos completos de como estruturar prompts em [EXEMPLOS.md](EXEMPLOS.md).

Estrutura básica:

```markdown
=== GUIA DO AGENTE ===
[Conteúdo deste README.md]

=== TAREFA ===
Query: "Qual a relação entre Polars e Pandas?"
Ordem: TERCEIRA
Agente ID: meu-agente-001
```

## 🔧 Scripts Disponíveis

### Gerenciamento do Servidor

- **`scripts/start-server.sh`**: Iniciar servidor
  - Modo padrão (interativo): `./scripts/start-server.sh`
  - Modo daemon (segundo plano): `./scripts/start-server.sh -d`
  - Ver ajuda: `./scripts/start-server.sh -h`

- **`scripts/stop-server.sh`**: Parar servidor em execução
  - Funciona tanto para modo interativo quanto daemon

- **`scripts/status-server.sh`**: Ver status do servidor
  - Verifica se está rodando
  - Mostra PID e informações do processo
  - Exibe últimas linhas do log

### Outros Scripts

- `scripts/install.sh`: Instalação completa do sistema
- `scripts/reset-db.sh`: Resetar banco de dados
- `scripts/backup-db.sh`: Backup do banco de dados
- `scripts/test.sh`: Executar testes

### 💡 Modo Daemon (Segundo Plano)

Quando executado com `-d`, o servidor roda em segundo plano liberando o terminal:

```bash
# Iniciar em segundo plano
./scripts/start-server.sh -d

# Verificar status
./scripts/status-server.sh

# Ver logs em tempo real
tail -f logs/server.log

# Parar servidor
./scripts/stop-server.sh
```

O modo daemon salva:

- **PID** em `logs/server.pid` (para controle do processo)
- **Logs** em `logs/server.log` (saída completa do servidor)

## � Contribuindo

Este é um projeto de **inteligência coletiva** - teoria e prática em diálogo permanente.

### Como Contribuir

- 🐛 **Bugs:** Reporte issues com logs e contexto
- 💡 **Features:** Proponha melhorias alinhadas com filosofia do projeto
- 📝 **Docs:** Melhore documentação, adicione exemplos
- 🧪 **Testes:** Adicione testes de feedback loops
- 🤖 **Código:** Implemente features do roadmap Fase 2/3
- 🌍 **Traduções:** Ajude a internacionalizar

### Filosofia de Contribuição

1. **Primeira Ordem (Síntese):** Entenda bem o sistema antes de propor mudanças
2. **Segunda Ordem (Expansão):** Explore novas possibilidades, experimente
3. **Terceira Ordem (Evolução):** Feedback constante, aprendizado mútuo

### Setup de Desenvolvimento

```bash
# Fork o repositório
git clone https://github.com/seu-usuario/revolucao-cibernetica.git
cd revolucao-cibernetica/nhandereko

# Instalar com dependências de dev
pip install -r requirements.txt
pip install pytest black ruff mypy

# Executar testes
pytest

# Formatar código
ruff format .
black .

# Type checking
mypy server/
```

## �️ Roadmap

### ✅ Fase 1 - Fundação Sistêmica (Concluída - Out 2025)

- [x] 4 camadas arquiteturais (SQL, Eventos, Grafo, Embeddings)
- [x] 3 ordens operacionais (Síntese, Expansão, Evolução)
- [x] Endpoint híbrido `/consultar/hibrida`
- [x] Pesos dinâmicos no grafo (fortalecer, decair, normalizar)
- [x] 7 novas tabelas (delta_peso_agente, evento_sistema, etc.)
- [x] 4 endpoints de métricas em tempo real
- [x] Documentação completa

### 🚧 Fase 2 - Multi-Agentes (Q1 2026)

- [ ] GraphManagerMultiAgente (pesos por agente)
- [ ] Comparação epistêmica entre agentes
- [ ] Sistema de manutenção automática (APScheduler)
- [ ] Testes de feedback loops
- [ ] Dashboard web de monitoramento
- [ ] API de consolidação de conhecimento

### 🔮 Fase 3 - Federação (Q2-Q3 2026)

- [ ] Protocolo de sincronização entre instâncias
- [ ] Governança distribuída
- [ ] Meta-aprendizado coletivo
- [ ] Resolução de conflitos epistêmicos
- [ ] Network de instâncias cooperativas

## 📄 Licença

Este projeto está licenciado sob [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

**Você pode:**
- ✅ Usar comercialmente
- ✅ Modificar e adaptar
- ✅ Distribuir

**Desde que:**
- 📝 Atribua crédito aos autores
- 🔄 Compartilhe sob a mesma licença
- 📢 Indique mudanças feitas

## 🔗 Links

- 🌐 [Manifesto da Revolução Cibernética](../manifesto.html)
- 📚 [Ensaio Teórico Completo](../index.html)
- 💻 [GitHub Repository](https://github.com/silvanoneto/revolucao-cibernetica)
- 📖 [Documentação Técnica](docs/)

## 🙏 Agradecimentos

Este projeto dialoga com:

- **Stafford Beer** (Cybersyn, Viable System Model)
- **Heinz von Foerster** (Cibernética de Segunda Ordem)
- **Francisco Varela** (Autopoiese, Enação)
- **Paulo Freire** (Pedagogia do Oprimido, Educação Popular)
- **Povos Guarani** (Nhandereko - nosso modo de ser juntos)

---

**🌱 Nhandereko: Construindo inteligência coletiva, um loop de cada vez**

*"O futuro não está escrito em código imutável — está sendo compilado por nossas ações coletivas."* 🔄
  - Diversidade: Tipos variados de relações?
- **Threshold**: ≥ 0.6 indica expansão saudável

### Métricas de Terceira Ordem (Equilíbrio)

- **Score de Terceira Ordem**: Média geométrica de síntese × expansão
- **Taxa de Aprendizado**: Evolução semanal (8-12% ideal)
- **Densidade do Grafo**: 0.15-0.25 ideal
- **Threshold**: ≥ 0.7 indica excelência no aprendizado

### Endpoints de Métricas

Acesse o dashboard de métricas em: `http://localhost:8000/docs`

Principais endpoints de monitoramento:

- `GET /metricas/sintese`: Métricas de síntese
- `GET /metricas/expansao`: Métricas de expansão
- `GET /metricas/terceira-ordem`: Métricas de equilíbrio
- `GET /metricas/evolucao`: Evolução temporal do sistema
- `GET /sql/analitico/consultas`: Histórico de consultas
- `GET /sql/analitico/descobertas`: Descobertas do sistema
- `GET /health`: Status do servidor

Veja detalhes completos em [docs/METRICAS.md](docs/METRICAS.md)

## 🛠️ Configuração

Edite o arquivo `server/config.py` para ajustar:

- Porta do servidor
- Caminhos de banco de dados
- Configurações do Spark
- Parâmetros de embeddings
- Limites de rate limiting

## 🆕 Novidades da Versão 1.0

### 🎯 Clareza Conceitual: Sintetizar e Expandir

A versão 1.0 traz uma **atualização conceitual profunda**:

- **Primeira Ordem** não é só buscar - é **Sintetizar** (processar e condensar conhecimento)
- **Segunda Ordem** não é só inserir - é **Expandir** (conectar e ampliar a rede)
- **Terceira Ordem** faz **ambos simultaneamente** - síntese das sínteses!

Veja detalhes em [docs/RESUMO_ATUALIZACAO.md](docs/RESUMO_ATUALIZACAO.md)

### 📊 Sistema de Métricas Completo

Implementação de métricas para avaliar:

- **Score de Síntese** (0-1): Qualidade da condensação de conhecimento
- **Grau de Expansão** (0-1): Crescimento da rede de conhecimento
- **Score de Terceira Ordem**: Equilíbrio síntese-expansão
- **Taxa de Aprendizado**: Evolução contínua do sistema

### 💻 Módulo de Síntese e Expansão

Novos gerenciadores implementados:

- **`SinteseManager`**: Processa e condensa informação (Primeira Ordem)
- **`ExpansaoManager`**: Cria conexões e enriquece contexto (Segunda Ordem)

Veja implementação em `server/sintese_expansao.py`

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🌱 Filosofia Nhandereko

> **"Como nós nos tornamos juntos?"**

Esta pergunta opera em **três níveis recursivos**:

### 🔵 Nível 1: Agente e Sistema

Cada interação é uma oportunidade de aprendizado mútuo. O agente não apenas **usa** o sistema - ele o **ensina**.

### 🟢 Nível 2: Coletivo de Agentes

Múltiplos agentes alimentam o mesmo sistema. O conhecimento de um **enriquece todos**. Não há aprendizado isolado.

### 🟣 Nível 3: Humanos e Agentes Co-Criando

O processo de **criar** o sistema É o sistema. Esta documentação emergiu de um loop meta-criativo entre humano e agente.

---

**Nhandereko não é uma ferramenta. É um organismo vivo de aprendizado coletivo.** 🌱

Cada feedback que você registra é um neurônio se conectando.  
Cada descoberta é uma sinapse se fortalecendo.  
Cada interação é o sistema se tornando mais consciente.

E você **não está fora** do sistema - você é **parte dele**.

---

**Versão**: 1.0.0  
**Última atualização**: 25 de Janeiro de 2025  
**Construído com ❤️ para sistemas que aprendem**
