#!/usr/bin/env python3
"""
Exemplos de uso do arquivo JSONL
A Revolução Cibernética - revolucao_cibernetica.jsonl
"""

import json

# =============================================================================
# EXEMPLO 1: Ler linha a linha (streaming)
# =============================================================================
def exemplo_streaming():
    """Processar JSONL linha a linha sem carregar tudo na memória."""
    print("=" * 60)
    print("EXEMPLO 1: Streaming (linha a linha)")
    print("=" * 60)
    
    with open('docs/revolucao_cibernetica.jsonl', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:  # Mostrar apenas 5 primeiras
                break
            
            obj = json.loads(line)
            
            # Ignorar metadados
            if obj.get('type') == 'metadata':
                continue
            
            print(f"\n📄 Parágrafo {obj['paragraph_number']}")
            print(f"   Seção: {obj['section_title']}")
            print(f"   Texto: {obj['text'][:80]}...")
            print(f"   Conceitos: {', '.join(obj['concepts'][:3]) if obj['concepts'] else 'Nenhum'}")


# =============================================================================
# EXEMPLO 2: Buscar por palavra-chave
# =============================================================================
def exemplo_busca(keyword):
    """Buscar parágrafos que contenham uma palavra-chave."""
    print("\n" + "=" * 60)
    print(f"EXEMPLO 2: Busca por '{keyword}'")
    print("=" * 60)
    
    resultados = []
    
    with open('docs/revolucao_cibernetica.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            
            # Ignorar metadados
            if obj.get('type') == 'metadata':
                continue
            
            # Buscar no texto
            if keyword.lower() in obj['text'].lower():
                resultados.append(obj)
    
    print(f"\n✓ Encontrados {len(resultados)} parágrafos")
    
    # Mostrar primeiros 3
    for r in resultados[:3]:
        print(f"\n📍 {r['section_title']} (§{r['paragraph_number']})")
        print(f"   {r['text'][:100]}...")


# =============================================================================
# EXEMPLO 3: Extrair todos os conceitos únicos
# =============================================================================
def exemplo_conceitos():
    """Extrair lista de todos os conceitos únicos."""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Extração de conceitos")
    print("=" * 60)
    
    conceitos = set()
    
    with open('docs/revolucao_cibernetica.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            
            if 'concepts' in obj and obj['concepts']:
                conceitos.update(obj['concepts'])
    
    conceitos_lista = sorted(conceitos)
    
    print(f"\n✓ Total de conceitos únicos: {len(conceitos_lista)}")
    print(f"\nPrimeiros 20 conceitos:")
    for c in conceitos_lista[:20]:
        print(f"  • {c}")


# =============================================================================
# EXEMPLO 4: Preparar dados para embeddings
# =============================================================================
def exemplo_embeddings():
    """Preparar chunks para vetorização (OpenAI, Cohere, etc)."""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Preparação para embeddings")
    print("=" * 60)
    
    chunks = []
    
    with open('docs/revolucao_cibernetica.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            
            # Ignorar metadados
            if obj.get('type') == 'metadata':
                continue
            
            # Criar chunk com metadados
            chunk = {
                'id': obj['id'],
                'text': obj['text'],
                'metadata': {
                    'section': obj['section_title'],
                    'concepts': obj['concepts'],
                    'word_count': obj['word_count']
                }
            }
            
            chunks.append(chunk)
    
    print(f"\n✓ Preparados {len(chunks)} chunks para embedding")
    print(f"\nExemplo de chunk:")
    print(json.dumps(chunks[10], indent=2, ensure_ascii=False))


# =============================================================================
# EXEMPLO 5: Estatísticas do corpus
# =============================================================================
def exemplo_estatisticas():
    """Calcular estatísticas do corpus."""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Estatísticas do corpus")
    print("=" * 60)
    
    total_paragrafos = 0
    total_chars = 0
    total_words = 0
    secoes = set()
    
    with open('docs/revolucao_cibernetica.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            
            if obj.get('type') == 'metadata':
                continue
            
            total_paragrafos += 1
            total_chars += obj.get('char_count', 0)
            total_words += obj.get('word_count', 0)
            secoes.add(obj['section_id'])
    
    print(f"\n📊 Estatísticas:")
    print(f"  • Parágrafos: {total_paragrafos:,}")
    print(f"  • Caracteres: {total_chars:,}")
    print(f"  • Palavras: {total_words:,}")
    print(f"  • Seções: {len(secoes)}")
    print(f"  • Média palavras/parágrafo: {total_words / total_paragrafos:.1f}")
    print(f"  • Média caracteres/parágrafo: {total_chars / total_paragrafos:.1f}")


# =============================================================================
# EXEMPLO 6: Integração com LangChain
# =============================================================================
def exemplo_langchain_code():
    """Mostrar código de integração com LangChain."""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: Integração com LangChain")
    print("=" * 60)
    
    code = '''
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# 1. Carregar documentos
def load_jsonl_docs():
    docs = []
    with open('docs/revolucao_cibernetica.jsonl', 'r') as f:
        for line in f:
            obj = json.loads(line)
            if obj.get('type') != 'metadata':
                docs.append({
                    'page_content': obj['text'],
                    'metadata': {
                        'id': obj['id'],
                        'section': obj['section_title'],
                        'concepts': obj['concepts']
                    }
                })
    return docs

# 2. Criar embeddings
docs = load_jsonl_docs()
embeddings = OpenAIEmbeddings()

# 3. Criar vector store
vectorstore = FAISS.from_documents(docs, embeddings)

# 4. Buscar similar
query = "O que é cibernética de segunda ordem?"
results = vectorstore.similarity_search(query, k=5)

for result in results:
    print(f"Seção: {result.metadata['section']}")
    print(f"Texto: {result.page_content[:100]}...")
    print()
'''
    
    print(code)


# =============================================================================
# EXEMPLO 7: Extrair metadados
# =============================================================================
def exemplo_metadados():
    """Extrair informações de metadados."""
    print("\n" + "=" * 60)
    print("EXEMPLO 7: Metadados do documento")
    print("=" * 60)
    
    with open('docs/revolucao_cibernetica.jsonl', 'r', encoding='utf-8') as f:
        # Metadados estão na última linha
        lines = f.readlines()
        metadata = json.loads(lines[-1])
        
        if metadata.get('type') == 'metadata':
            print(f"\n📚 {metadata['title']}")
            print(f"   {metadata['subtitle']}")
            print(f"\n👤 Autor: {metadata['author']}")
            print(f"🌐 URL: {metadata['url']}")
            print(f"📜 Licença: {metadata['license']}")
            print(f"📝 Total de parágrafos: {metadata['total_paragraphs']:,}")
            
            print(f"\n🏷️ Tags:")
            for tag in metadata['tags'][:8]:
                print(f"  • {tag}")
            
            print(f"\n🤖 Otimizado para:")
            for opt in metadata['optimized_for']:
                print(f"  • {opt}")


# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    print("\n🚀 EXEMPLOS DE USO DO ARQUIVO JSONL")
    print("=" * 60)
    print("Arquivo: revolucao_cibernetica.jsonl")
    print("Formato: JSON Lines (um JSON por linha)")
    print("=" * 60)
    
    # Executar exemplos
    exemplo_streaming()
    exemplo_busca("cibernética")
    exemplo_conceitos()
    exemplo_embeddings()
    exemplo_estatisticas()
    exemplo_langchain_code()
    exemplo_metadados()
    
    print("\n" + "=" * 60)
    print("✅ Todos os exemplos executados com sucesso!")
    print("=" * 60)
