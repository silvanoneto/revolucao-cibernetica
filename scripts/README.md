# Scripts de Exportação - A Revolução Cibernética

Este diretório contém scripts utilitários para exportar o conteúdo do site em múltiplos formatos.

## 📦 Instalação

### Usando pip

```bash
cd scripts/
pip install -r requirements.txt
```

### Usando uv (recomendado)

```bash
cd scripts/
uv pip install -e .
```

## 🚀 Uso

### Script de Exportação

O script `export_file.py` permite exportar o conteúdo do site em vários formatos:

```bash
# Exportar em EPUB (padrão)
python export_file.py epub

# Exportar em PDF
python export_file.py pdf

# Exportar em XML (formatado)
python export_file.py xml

# Exportar em XML minificado
python export_file.py xml-min

# Exportar em JSONL (otimizado para LLMs)
python export_file.py jsonl

# Exportar TODOS os formatos
python export_file.py all
```

## 📋 Formatos Disponíveis

### EPUB
- **Arquivo**: `docs/revolucao_cibernetica.epub`
- **Uso**: Leitores de e-books (Calibre, Apple Books, Kindle)
- **Recursos**: Imagens embutidas, índice navegável, metadados completos

### PDF
- **Arquivo**: `docs/revolucao_cibernetica.pdf`
- **Uso**: Leitura universal, impressão
- **Recursos**: Estilos preservados, cores roxo/rosa do site, formatação profissional

### XML
- **Arquivo**: `docs/revolucao_cibernetica.xml`
- **Uso**: Processamento por agentes de IA, análise estrutural
- **Recursos**: Estrutura hierárquica, metadados semânticos, glossário integrado

### XML Minificado
- **Arquivo**: `docs/revolucao_cibernetica.min.xml`
- **Uso**: Transmissão de dados, armazenamento compacto
- **Recursos**: Mesmo conteúdo do XML formatado, sem espaços em branco

### JSONL
- **Arquivo**: `docs/revolucao_cibernetica.jsonl`
- **Uso**: LLMs, RAG systems, embeddings, fine-tuning
- **Recursos**: Um parágrafo por linha, streaming-friendly, conceitos extraídos
- **Compatível com**: OpenAI, LangChain, Pinecone, Weaviate

## 🔧 Dependências

- **ebooklib**: Criação de arquivos EPUB
- **beautifulsoup4**: Parsing de HTML
- **xhtml2pdf**: Geração de PDFs
- **lxml**: Processamento eficiente de XML

## 📝 Estrutura dos Arquivos

```
scripts/
├── export_file.py          # Script principal de exportação
├── pyproject.toml          # Configuração do projeto Python
├── pyrightconfig.json      # Configuração do Pyright/Pylance
├── requirements.txt        # Dependências do projeto
└── README.md              # Esta documentação
```

## 🤖 Otimizações para IA

### XML
- Estrutura hierárquica preservada
- Metadados semânticos completos
- Glossário de conceitos-chave
- Hints de processamento para LLMs

### JSONL
- Um parágrafo = um chunk (ideal para embeddings)
- Conceitos extraídos automaticamente
- Metadados por parágrafo (seção, tipo de documento)
- Formato streaming-friendly

## 📄 Licença

Creative Commons BY-SA 4.0 - Mesmo licença do conteúdo original.

## 👤 Autor

O Besta Fera - [https://obestafera.com](https://obestafera.com)
