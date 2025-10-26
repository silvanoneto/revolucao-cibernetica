#!/usr/bin/env python3
"""
Exemplos de uso do arquivo revolucao_cibernetica.xml
para processamento por agentes de IA e sistemas de RAG.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict

def load_xml(filepath: str = 'docs/revolucao_cibernetica.xml'):
    """Carrega o arquivo XML."""
    tree = ET.parse(filepath)
    return tree.getroot()

def get_metadata(root):
    """Extrai metadados do documento."""
    metadata = root.find('metadata')
    
    return {
        'title': metadata.find('title').text,
        'subtitle': metadata.find('subtitle').text,
        'author': metadata.find('author').text,
        'language': metadata.find('language').text,
        'license': metadata.find('license').text,
        'url': metadata.find('url').text,
        'description': metadata.find('description').text,
        'tags': [tag.text for tag in metadata.findall('.//tag')]
    }

def get_all_paragraphs(root) -> List[Dict]:
    """
    Extrai todos os parágrafos para indexação vetorial.
    Ideal para criar embeddings.
    """
    paragraphs = []
    
    for document in root.findall('document'):
        doc_type = document.get('type')
        
        for section in document.findall('section'):
            section_id = section.get('id')
            section_title = section.find('title').text
            
            for para in section.findall('.//paragraph'):
                paragraphs.append({
                    'id': f"{section_id}_p{para.get('index')}",
                    'section_id': section_id,
                    'section_title': section_title,
                    'document_type': doc_type,
                    'text': para.text,
                    'index': int(para.get('index'))
                })
    
    return paragraphs

def get_sections_by_keyword(root, keyword: str) -> List[Dict]:
    """
    Busca seções que contêm uma palavra-chave específica.
    Útil para busca semântica inicial.
    """
    keyword_lower = keyword.lower()
    matching_sections = []
    
    for section in root.findall('.//section'):
        section_id = section.get('id')
        title = section.find('title').text
        
        # Verificar título
        if keyword_lower in title.lower():
            matching_sections.append({
                'section_id': section_id,
                'title': title,
                'match_type': 'title'
            })
            continue
        
        # Verificar parágrafos
        for para in section.findall('.//paragraph'):
            if para.text and keyword_lower in para.text.lower():
                matching_sections.append({
                    'section_id': section_id,
                    'title': title,
                    'match_type': 'content'
                })
                break
    
    return matching_sections

def get_section_full_context(root, section_id: str) -> Dict:
    """
    Recupera contexto completo de uma seção.
    Ideal para RAG (Retrieval-Augmented Generation).
    """
    section = root.find(f".//section[@id='{section_id}']")
    
    if not section:
        return None
    
    context = {
        'id': section_id,
        'title': section.find('title').text,
        'level': int(section.get('level')),
        'paragraphs': [],
        'quotes': [],
        'lists': [],
        'concepts': [],
        'images': []
    }
    
    # Parágrafos
    for para in section.findall('.//paragraph'):
        context['paragraphs'].append(para.text)
    
    # Citações
    for quote in section.findall('.//quotes/quote'):
        context['quotes'].append(quote.text)
    
    # Listas
    for lst in section.findall('.//lists/list'):
        list_items = [item.text for item in lst.findall('item')]
        context['lists'].append({
            'type': lst.get('type'),
            'items': list_items
        })
    
    # Conceitos-chave
    for concept in section.findall('.//key_concepts/concept'):
        if concept.text:
            context['concepts'].append(concept.text)
    
    # Imagens
    for img in section.findall('.//images/image'):
        context['images'].append({
            'src': img.get('src'),
            'alt': img.get('alt', '')
        })
    
    return context

def get_glossary(root) -> Dict[str, str]:
    """Extrai glossário de conceitos fundamentais."""
    glossary = {}
    
    for entry in root.findall('.//glossary/entry'):
        term = entry.find('term').text
        definition = entry.find('definition').text
        glossary[term] = definition
    
    return glossary

def get_ai_hints(root) -> List[str]:
    """Extrai instruções para processamento por IA."""
    hints = []
    
    for hint in root.findall('.//ai_processing_hints/hint'):
        hints.append(hint.text)
    
    return hints

def get_themes(root) -> List[Dict]:
    """Extrai temas principais com keywords."""
    themes = []
    
    for theme in root.findall('.//main_themes/theme'):
        themes.append({
            'name': theme.find('name').text,
            'description': theme.find('description').text,
            'keywords': [kw.text for kw in theme.findall('.//keyword')]
        })
    
    return themes

def get_key_concepts(root) -> Dict[str, List[str]]:
    """
    Mapeia conceitos-chave por seção.
    Útil para construir grafo de conhecimento.
    """
    concepts_map = {}
    
    for section in root.findall('.//section'):
        section_id = section.get('id')
        concepts = [c.text for c in section.findall('.//key_concepts/concept') if c.text]
        
        if concepts:
            concepts_map[section_id] = concepts
    
    return concepts_map

def build_concept_cooccurrence_matrix(root) -> Dict[tuple, int]:
    """
    Constrói matriz de co-ocorrência de conceitos.
    Conceitos que aparecem juntos na mesma seção.
    """
    cooccurrence = {}
    
    for section in root.findall('.//section'):
        concepts = [c.text for c in section.findall('.//key_concepts/concept') if c.text]
        
        # Pares de conceitos na mesma seção
        for i, c1 in enumerate(concepts):
            for c2 in concepts[i+1:]:
                pair = tuple(sorted([c1, c2]))
                cooccurrence[pair] = cooccurrence.get(pair, 0) + 1
    
    return cooccurrence


# ============================================================
# EXEMPLO DE USO
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Exemplos de Uso - revolucao_cibernetica.xml")
    print("=" * 60)
    print()
    
    # Carregar XML
    root = load_xml()
    
    # 1. Metadados
    print("1. METADADOS")
    print("-" * 60)
    metadata = get_metadata(root)
    print(f"Título: {metadata['title']}")
    print(f"Autor: {metadata['author']}")
    print(f"Tags: {', '.join(metadata['tags'][:5])}...")
    print()
    
    # 2. Extrair parágrafos para embeddings
    print("2. PARÁGRAFOS PARA EMBEDDINGS")
    print("-" * 60)
    paragraphs = get_all_paragraphs(root)
    print(f"Total de parágrafos: {len(paragraphs)}")
    print(f"Exemplo (primeiro parágrafo):")
    print(f"  ID: {paragraphs[0]['id']}")
    print(f"  Seção: {paragraphs[0]['section_title']}")
    print(f"  Texto: {paragraphs[0]['text'][:150]}...")
    print()
    
    # 3. Busca por palavra-chave
    print("3. BUSCA POR PALAVRA-CHAVE")
    print("-" * 60)
    results = get_sections_by_keyword(root, 'cibernética')
    print(f"Seções com 'cibernética': {len(results)}")
    for i, result in enumerate(results[:3]):
        print(f"  {i+1}. {result['title']} ({result['match_type']})")
    print()
    
    # 4. Contexto completo de seção (para RAG)
    print("4. CONTEXTO COMPLETO (RAG)")
    print("-" * 60)
    context = get_section_full_context(root, 'teoria_2')
    print(f"Seção: {context['title']}")
    print(f"Parágrafos: {len(context['paragraphs'])}")
    print(f"Conceitos-chave: {context['concepts'][:5]}")
    print()
    
    # 5. Glossário
    print("5. GLOSSÁRIO")
    print("-" * 60)
    glossary = get_glossary(root)
    print(f"Conceitos no glossário: {len(glossary)}")
    for term in list(glossary.keys())[:3]:
        print(f"  • {term}")
    print()
    
    # 6. Hints para IA
    print("6. INSTRUÇÕES PARA IA")
    print("-" * 60)
    hints = get_ai_hints(root)
    print(f"Total de hints: {len(hints)}")
    print(f"Primeiro hint: {hints[0]}")
    print()
    
    # 7. Temas principais
    print("7. TEMAS PRINCIPAIS")
    print("-" * 60)
    themes = get_themes(root)
    for theme in themes:
        print(f"  • {theme['name']}")
        print(f"    Keywords: {', '.join(theme['keywords'][:3])}...")
    print()
    
    # 8. Co-ocorrência de conceitos
    print("8. CO-OCORRÊNCIA DE CONCEITOS")
    print("-" * 60)
    cooccurrence = build_concept_cooccurrence_matrix(root)
    top_pairs = sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 pares de conceitos que aparecem juntos:")
    for (c1, c2), count in top_pairs:
        print(f"  • '{c1}' + '{c2}': {count} seções")
    print()
    
    print("=" * 60)
    print("✅ Exemplos executados com sucesso!")
    print("=" * 60)
