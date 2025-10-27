/**
 * ============================================
 * NAVEGAÇÃO RIZOMÁTICA
 * Revolução Cibernética - Sistema de Conceitos Interligados
 * ============================================
 * 
 * Sistema inspirado no conceito de "rizoma" de Deleuze & Guattari:
 * - Não-hierárquico
 * - Multiplicidade de entradas
 * - Conexões heterogêneas
 * - Sem estrutura arbórea
 */

// Grafo de conceitos (nós do rizoma)
const conceptGraph = {
    'cibernetica': {
        name: 'Cibernética',
        description: 'Ciência do controle e comunicação',
        connections: ['feedback', 'autopoiese', 'segunda-ordem'],
        color: '#8b5cf6',
        layer: -1 // Passado
    },
    'feedback': {
        name: 'Feedback Loop',
        description: 'Ciclo de retorno que modifica o sistema',
        connections: ['cibernetica', 'autopoiese', 'temporalidade'],
        color: '#10b981',
        layer: 0 // Presente
    },
    'autopoiese': {
        name: 'Autopoiese',
        description: 'Sistemas que se auto-criam (Maturana & Varela)',
        connections: ['cibernetica', 'feedback', 'nhandereko'],
        color: '#8b5cf6',
        layer: -1
    },
    'segunda-ordem': {
        name: 'Cibernética de Segunda Ordem',
        description: 'Observador incluído no sistema observado',
        connections: ['cibernetica', 'meta-observacao', 'ontologia-executavel'],
        color: '#10b981',
        layer: 0
    },
    'rizoma': {
        name: 'Rizoma',
        description: 'Estrutura não-hierárquica (Deleuze & Guattari)',
        connections: ['multiplicidade', 'devir', 'navegacao-rizomatica'],
        color: '#8b5cf6',
        layer: -1
    },
    'multiplicidade': {
        name: 'Multiplicidade',
        description: 'Não é uno nem múltiplo - é multiplicidade',
        connections: ['rizoma', 'devir', 'ontologia-relacional'],
        color: '#8b5cf6',
        layer: -1
    },
    'capitalismo-vigilancia': {
        name: 'Capitalismo de Vigilância',
        description: 'Extração de dados comportamentais (Zuboff)',
        connections: ['mais-valia-dados', 'plataformizacao', 'resistencia'],
        color: '#ef4444',
        layer: 0
    },
    'mais-valia-dados': {
        name: 'Mais-Valia de Dados',
        description: 'Valor extraído do trabalho digital não-pago',
        connections: ['capitalismo-vigilancia', 'uberizacao', 'trabalho-imaterial'],
        color: '#ef4444',
        layer: 0
    },
    'ontologia-executavel': {
        name: 'Ontologia Executável',
        description: 'Filosofia que se performa em código',
        connections: ['segunda-ordem', 'critica-performativa', 'canvas-background'],
        color: '#10b981',
        layer: 0
    },
    'critica-performativa': {
        name: 'Crítica Performativa',
        description: 'Sistema que executa sua própria crítica',
        connections: ['ontologia-executavel', 'captcha', 'ironia-politica'],
        color: '#10b981',
        layer: 0
    },
    'captcha': {
        name: 'CAPTCHA Anti-Algorítmico',
        description: 'Humanos passam, bots falham',
        connections: ['critica-performativa', 'caos', 'resistencia'],
        color: '#10b981',
        layer: 0
    },
    'sistema-ternario': {
        name: 'Sistema Ternário (-1, 0, +1)',
        description: 'Base 3 balanceada para representar temporalidade',
        connections: ['temporalidade', 'feedback', 'backfeed'],
        color: '#10b981',
        layer: 0
    },
    'temporalidade': {
        name: 'Temporalidade Ternária',
        description: 'Presente como tensão entre passado e futuro',
        connections: ['sistema-ternario', 'feedback', 'guaiamum'],
        color: '#10b981',
        layer: 0
    },
    'nhandereko': {
        name: 'Nhandereko',
        description: 'Orquestrador de conhecimento autopoiético',
        connections: ['autopoiese', 'epistemologia-guarani', 'modo-colaborativo'],
        color: '#6366f1',
        layer: 1 // Futuro
    },
    'epistemologia-guarani': {
        name: 'Epistemologias Guarani',
        description: 'Conhecimento relacional indígena',
        connections: ['nhandereko', 'ontologia-relacional', 'decolonial'],
        color: '#8b5cf6',
        layer: -1
    },
    'navegacao-rizomatica': {
        name: 'Navegação Rizomática',
        description: 'Este sistema que você está usando agora',
        connections: ['rizoma', 'grafo-conceitos', 'modo-colaborativo'],
        color: '#6366f1',
        layer: 1
    },
    'modo-colaborativo': {
        name: 'Modo Colaborativo',
        description: 'Interação síncrona entre usuários (planejado)',
        connections: ['nhandereko', 'navegacao-rizomatica', 'websocket'],
        color: '#6366f1',
        layer: 1
    },
    'resistencia': {
        name: 'Resistência em Código',
        description: 'Técnicas práticas de contra-automação',
        connections: ['captcha', 'opacidade', 'honeypots', 'critica-performativa'],
        color: '#10b981',
        layer: 0
    },
    'devir': {
        name: 'Devir',
        description: 'Processo de tornar-se, transformação contínua sem destino fixo',
        connections: ['rizoma', 'multiplicidade', 'ontologia-relacional'],
        color: '#8b5cf6',
        layer: -1
    },
    'ontologia-relacional': {
        name: 'Ontologia Relacional',
        description: 'Ser é relação, não substância isolada',
        connections: ['autopoiese', 'devir', 'multiplicidade', 'epistemologia-guarani'],
        color: '#8b5cf6',
        layer: -1
    },
    'uberizacao': {
        name: 'Uberização',
        description: 'Precarização do trabalho via plataformas digitais',
        connections: ['mais-valia-dados', 'plataformizacao', 'trabalho-imaterial'],
        color: '#ef4444',
        layer: 0
    },
    'trabalho-imaterial': {
        name: 'Trabalho Imaterial',
        description: 'Trabalho cognitivo, afetivo e comunicacional não-pago',
        connections: ['mais-valia-dados', 'uberizacao', 'capitalismo-vigilancia'],
        color: '#ef4444',
        layer: 0
    },
    'plataformizacao': {
        name: 'Plataformização',
        description: 'Monopolização da infraestrutura digital',
        connections: ['capitalismo-vigilancia', 'uberizacao', 'resistencia'],
        color: '#ef4444',
        layer: 0
    },
    'decolonial': {
        name: 'Pensamento Decolonial',
        description: 'Crítica à colonialidade do saber e do poder',
        connections: ['epistemologia-guarani', 'ubuntu', 'cosmotecnica'],
        color: '#8b5cf6',
        layer: -1
    },
    'ubuntu': {
        name: 'Ubuntu',
        description: 'Filosofia africana: "Eu sou porque nós somos"',
        connections: ['decolonial', 'ontologia-relacional', 'modo-colaborativo'],
        color: '#8b5cf6',
        layer: -1
    },
    'cosmotecnica': {
        name: 'Cosmotécnica',
        description: 'Técnicas enraizadas em cosmologias locais (Yuk Hui)',
        connections: ['decolonial', 'epistemologia-guarani', 'ontologia-executavel'],
        color: '#8b5cf6',
        layer: -1
    },
    'guaiamum': {
        name: 'Guaiamum Lateral',
        description: 'Movimento diagonal, não-linear, caranguejo',
        connections: ['temporalidade', 'navegacao-rizomatica', 'backfeed'],
        color: '#10b981',
        layer: 0
    },
    'backfeed': {
        name: 'Backfeed',
        description: 'Retorno do futuro para o presente (antecipação)',
        connections: ['feedback', 'temporalidade', 'guaiamum', 'sistema-ternario'],
        color: '#10b981',
        layer: 0
    },
    'opacidade': {
        name: 'Opacidade Estratégica',
        description: 'Resistir via não-transparência (Édouard Glissant)',
        connections: ['resistencia', 'honeypots', 'captcha'],
        color: '#10b981',
        layer: 0
    },
    'honeypots': {
        name: 'Honeypots',
        description: 'Armadilhas para capturar bots invasores',
        connections: ['resistencia', 'opacidade', 'captcha'],
        color: '#10b981',
        layer: 0
    },
    'ironia-politica': {
        name: 'Ironia Política',
        description: 'Crítica através da performance contraditória',
        connections: ['critica-performativa', 'captcha', 'ontologia-executavel'],
        color: '#10b981',
        layer: 0
    },
    'grafo-conceitos': {
        name: 'Grafo de Conceitos',
        description: 'Estrutura de dados que representa o rizoma',
        connections: ['navegacao-rizomatica', 'rizoma', 'websocket'],
        color: '#6366f1',
        layer: 1
    },
    'websocket': {
        name: 'WebSocket',
        description: 'Comunicação bidirecional em tempo real',
        connections: ['modo-colaborativo', 'grafo-conceitos', 'nhandereko'],
        color: '#6366f1',
        layer: 1
    },
    'meta-observacao': {
        name: 'Meta-Observação',
        description: 'Observar o ato de observar (segunda ordem)',
        connections: ['segunda-ordem', 'ontologia-executavel', 'cibernetica'],
        color: '#10b981',
        layer: 0
    },
    'canvas-background': {
        name: 'Canvas Background',
        description: 'Sistema de arte generativa que performa a filosofia',
        connections: ['ontologia-executavel', 'sistema-ternario', 'caos'],
        color: '#10b981',
        layer: 0
    },
    'caos': {
        name: 'Caos Criativo',
        description: 'Desordem produtiva, não-entrópica',
        connections: ['canvas-background', 'captcha', 'sistema-ternario'],
        color: '#10b981',
        layer: 0
    }
};

// Estado do rizoma
let rizomaActive = false;
let rizomaOverlay = null;
let selectedConcept = null;
let searchFilter = '';
let layerFilter = 'all'; // 'all', -1, 0, 1
let viewMode = 'grid'; // 'grid' ou 'graph'

/**
 * Inicializar sistema de navegação rizomática
 */
function initializeRizoma() {
    console.log('🌀 Inicializando navegação rizomática...');
    
    // Criar overlay
    rizomaOverlay = document.createElement('div');
    rizomaOverlay.id = 'rizoma-overlay';
    rizomaOverlay.className = 'rizoma-overlay';
    rizomaOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(10, 10, 15, 0.95);
        z-index: 9999;
        display: none;
        overflow: auto;
        padding: 2rem;
    `;
    
    document.body.appendChild(rizomaOverlay);
    
    // Adicionar botão de fechar
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✕ Fechar Rizoma';
    closeBtn.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 600;
        z-index: 10000;
        transition: all 0.3s ease;
    `;
    closeBtn.onclick = closeRizoma;
    rizomaOverlay.appendChild(closeBtn);
    
    console.log('✅ Navegação rizomática inicializada');
}

/**
 * Abrir visualização do rizoma
 * @param {string} startConcept - Conceito inicial (opcional)
 */
function openRizoma(startConcept = null) {
    console.log('🌀 Abrindo rizoma...', startConcept);
    
    // Verificar se há transição ternária em andamento
    if (typeof isTransitioning !== 'undefined' && isTransitioning) {
        console.warn('⏸️ Aguarde a transição ternária concluir');
        return;
    }
    
    if (!rizomaOverlay) {
        initializeRizoma();
    }
    
    selectedConcept = startConcept;
    rizomaActive = true;
    rizomaOverlay.style.display = 'block';
    
    // Render do grafo
    renderRizomaGraph();

    // Após render, rolar suavemente até o card do conceito inicial (se houver)
    setTimeout(() => {
        if (startConcept) {
            const card = document.querySelector(`[data-concept-key="${startConcept}"]`);
            if (card) {
                // Scroll dentro do overlay para centralizar o card
                try {
                    card.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
                    // foco acessível
                    if (typeof card.focus === 'function') card.focus({ preventScroll: true });
                } catch (err) {
                    // fallback simples
                    card.scrollIntoView();
                }
            }
        }
    }, 200);
    
    // Impedir scroll do body
    document.body.style.overflow = 'hidden';
}

/**
 * Fechar visualização do rizoma
 */
function closeRizoma() {
    console.log('👻 Fechando rizoma...');
    
    // Verificar se há transição ternária em andamento
    if (typeof isTransitioning !== 'undefined' && isTransitioning) {
        console.warn('⏸️ Aguarde a transição ternária concluir');
        return;
    }
    
    rizomaActive = false;
    if (rizomaOverlay) {
        rizomaOverlay.style.display = 'none';
    }
    
    // Restaurar scroll
    document.body.style.overflow = '';
}

/**
 * Renderizar grafo de conceitos
 */
function renderRizomaGraph() {
    if (!rizomaOverlay) return;
    
    // Limpar conteúdo anterior (exceto botão de fechar)
    const closeBtn = rizomaOverlay.querySelector('button');
    rizomaOverlay.innerHTML = '';
    rizomaOverlay.appendChild(closeBtn);
    
    // Container principal
    const container = document.createElement('div');
    container.style.cssText = `
        max-width: 1400px;
        margin: 0 auto;
        padding-top: 4rem;
        position: relative;
    `;
    
    // Título
    const title = document.createElement('h2');
    title.textContent = '🌀 Navegação Rizomática';
    title.style.cssText = `
        text-align: center;
        color: #ec4899;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    `;
    container.appendChild(title);
    
    // Subtítulo
    const subtitle = document.createElement('p');
    subtitle.innerHTML = 'Conceitos interligados sem hierarquia. <strong>Clique para explorar conexões.</strong><br><small>Pressione <kbd>R</kbd> para abrir/fechar | <kbd>ESC</kbd> para fechar</small>';
    subtitle.style.cssText = `
        text-align: center;
        color: #a78bfa;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    `;
    container.appendChild(subtitle);
    
    // Barra de busca e filtros
    const searchBar = document.createElement('div');
    searchBar.style.cssText = `
        display: flex;
        gap: 1rem;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    `;
    
    // Campo de busca
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = '🔍 Buscar conceitos...';
    searchInput.value = searchFilter;
    searchInput.style.cssText = `
        background: rgba(26, 26, 46, 0.8);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #d1d5db;
        font-size: 1rem;
        width: 300px;
        outline: none;
        transition: all 0.3s ease;
    `;
    searchInput.addEventListener('focus', () => {
        searchInput.style.borderColor = '#8b5cf6';
        searchInput.style.boxShadow = '0 0 15px rgba(139, 92, 246, 0.3)';
    });
    searchInput.addEventListener('blur', () => {
        searchInput.style.borderColor = 'rgba(139, 92, 246, 0.3)';
        searchInput.style.boxShadow = 'none';
    });
    searchInput.addEventListener('input', (e) => {
        searchFilter = e.target.value.toLowerCase();
        renderRizomaGraph();
    });
    
    // Filtro de camada temporal
    const layerSelect = document.createElement('select');
    layerSelect.style.cssText = `
        background: rgba(26, 26, 46, 0.8);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #d1d5db;
        font-size: 1rem;
        cursor: pointer;
        outline: none;
        transition: all 0.3s ease;
    `;
    layerSelect.innerHTML = `
        <option value="all">📅 Todas as camadas</option>
        <option value="-1">🕰️ Passado (-1)</option>
        <option value="0">⚡ Presente (0)</option>
        <option value="1">🔮 Futuro (+1)</option>
    `;
    layerSelect.value = layerFilter;
    layerSelect.addEventListener('change', (e) => {
        layerFilter = e.target.value === 'all' ? 'all' : parseInt(e.target.value);
        renderRizomaGraph();
    });
    
    // Botão limpar filtros
    const clearBtn = document.createElement('button');
    clearBtn.textContent = '🗑️ Limpar';
    clearBtn.style.cssText = `
        background: rgba(239, 68, 68, 0.2);
        border: 2px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #ef4444;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
    `;
    clearBtn.addEventListener('click', () => {
        searchFilter = '';
        layerFilter = 'all';
        renderRizomaGraph();
    });
    clearBtn.addEventListener('mouseenter', () => {
        clearBtn.style.background = 'rgba(239, 68, 68, 0.3)';
        clearBtn.style.transform = 'scale(1.05)';
    });
    clearBtn.addEventListener('mouseleave', () => {
        clearBtn.style.background = 'rgba(239, 68, 68, 0.2)';
        clearBtn.style.transform = 'scale(1)';
    });
    
    searchBar.appendChild(searchInput);
    searchBar.appendChild(layerSelect);
    searchBar.appendChild(clearBtn);
    
    // Botão de alternar visualização
    const toggleViewBtn = document.createElement('button');
    toggleViewBtn.textContent = viewMode === 'grid' ? '🕸️ Grafo' : '🔲 Grade';
    toggleViewBtn.style.cssText = `
        background: rgba(99, 102, 241, 0.2);
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #6366f1;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
    `;
    toggleViewBtn.addEventListener('click', () => {
        viewMode = viewMode === 'grid' ? 'graph' : 'grid';
        renderRizomaGraph();
    });
    toggleViewBtn.addEventListener('mouseenter', () => {
        toggleViewBtn.style.background = 'rgba(99, 102, 241, 0.3)';
        toggleViewBtn.style.transform = 'scale(1.05)';
    });
    toggleViewBtn.addEventListener('mouseleave', () => {
        toggleViewBtn.style.background = 'rgba(99, 102, 241, 0.2)';
        toggleViewBtn.style.transform = 'scale(1)';
    });
    
    searchBar.appendChild(toggleViewBtn);
    container.appendChild(searchBar);
    
    // Estatísticas do rizoma
    const stats = document.createElement('div');
    const allConcepts = Object.entries(conceptGraph);
    
    // Aplicar filtros
    const filteredConcepts = allConcepts.filter(([key, concept]) => {
        // Filtro de busca
        const matchesSearch = !searchFilter || 
            concept.name.toLowerCase().includes(searchFilter) ||
            concept.description.toLowerCase().includes(searchFilter) ||
            key.toLowerCase().includes(searchFilter);
        
        // Filtro de camada
        const matchesLayer = layerFilter === 'all' || concept.layer === layerFilter;
        
        return matchesSearch && matchesLayer;
    });
    
    const totalConcepts = Object.keys(conceptGraph).length;
    const visibleConcepts = filteredConcepts.length;
    const totalConnections = Object.values(conceptGraph).reduce((sum, c) => sum + c.connections.length, 0);
    
    stats.innerHTML = `
        <div style="text-align: center; margin-bottom: 2rem; color: #9ca3af;">
            📊 <strong>${visibleConcepts}</strong> conceitos ${visibleConcepts < totalConcepts ? `(${totalConcepts} total)` : ''} • 
            🔗 <strong>${totalConnections}</strong> conexões • 
            🌊 <strong>Estrutura rizomática</strong>
        </div>
    `;
    container.appendChild(stats);
    
    // SVG para linhas de conexão (posicionado atrás do grid)
    const svgContainer = document.createElement('div');
    svgContainer.id = 'connection-svg-container';
    svgContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    `;
    
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');
    svg.style.position = 'absolute';
    svg.style.top = '0';
    svg.style.left = '0';
    svgContainer.appendChild(svg);
    container.appendChild(svgContainer);
    
    // Renderizar baseado no modo de visualização
    if (viewMode === 'graph') {
        renderGraphView(container, filteredConcepts);
    } else {
        renderGridView(container, filteredConcepts);
    }
    
    rizomaOverlay.appendChild(container);
    
    // Desenhar conexões e garantir que o card selecionado esteja visível (modo grid)
    if (selectedConcept && viewMode === 'grid') {
        setTimeout(() => {
            const selectedCard = document.querySelector(`[data-concept-key="${selectedConcept}"]`);
            if (selectedCard) {
                try {
                    selectedCard.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
                    if (typeof selectedCard.focus === 'function') selectedCard.focus({ preventScroll: true });
                } catch (err) {
                    selectedCard.scrollIntoView();
                }
            }
            drawConnections();
        }, 200);
    }
}

/**
 * Renderizar visualização em grade
 */
function renderGridView(container, filteredConcepts) {
    // Grid de conceitos
    const grid = document.createElement('div');
    grid.id = 'concepts-grid';
    grid.style.cssText = `
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
        position: relative;
        z-index: 1;
    `;
    
    // Renderizar apenas conceitos filtrados
    filteredConcepts.forEach(([key, concept]) => {
        const card = createConceptCard(key, concept);
        card.dataset.conceptKey = key;
        grid.appendChild(card);
    });
    
    // Mensagem se não houver resultados
    if (filteredConcepts.length === 0) {
        const noResults = document.createElement('div');
        noResults.style.cssText = `
            grid-column: 1 / -1;
            text-align: center;
            padding: 3rem;
            color: #9ca3af;
            font-size: 1.2rem;
        `;
        noResults.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <strong>Nenhum conceito encontrado</strong>
            <p style="margin-top: 0.5rem; font-size: 1rem;">Tente ajustar os filtros de busca</p>
        `;
        grid.appendChild(noResults);
    }
    
    container.appendChild(grid);
    
    // Legenda de camadas
    const legend = createLegend();
    container.appendChild(legend);
}

/**
 * Renderizar visualização em grafo (force-directed)
 */
function renderGraphView(container, filteredConcepts) {
    const graphContainer = document.createElement('div');
    graphContainer.id = 'graph-view';
    graphContainer.style.cssText = `
        position: relative;
        width: 100%;
        height: 600px;
        background: rgba(10, 10, 15, 0.5);
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        margin-bottom: 2rem;
        overflow: hidden;
    `;
    
    const canvas = document.createElement('canvas');
    canvas.width = 1400;
    canvas.height = 600;
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    graphContainer.appendChild(canvas);
    
    container.appendChild(graphContainer);
    
    // Inicializar simulação de força
    initForceDirectedGraph(canvas, filteredConcepts);
    
    // Legenda
    const legend = createLegend();
    container.appendChild(legend);
}

/**
 * Criar legenda de camadas temporais
 */
function createLegend() {
    const legend = document.createElement('div');
    legend.style.cssText = `
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        padding: 2rem;
        background: rgba(139, 92, 246, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.3);
    `;
    
    legend.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #8b5cf6; border-radius: 4px;"></div>
            <span style="color: #a78bfa;">Passado (-1)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #10b981; border-radius: 4px;"></div>
            <span style="color: #10b981;">Presente (0)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #6366f1; border-radius: 4px;"></div>
            <span style="color: #a78bfa;">Futuro (+1)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #ef4444; border-radius: 4px;"></div>
            <span style="color: #ef4444;">Crítica</span>
        </div>
    `;
    
    return legend;
}

/**
 * Inicializar grafo com force-directed layout
 */
function initForceDirectedGraph(canvas, filteredConcepts) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Criar nós com posições iniciais
    const nodes = filteredConcepts.map(([key, concept]) => ({
        key,
        concept,
        x: Math.random() * width,
        y: Math.random() * height,
        vx: 0,
        vy: 0,
        radius: 25
    }));
    
    // Criar mapa de índices
    const nodeMap = {};
    nodes.forEach((node, i) => {
        nodeMap[node.key] = i;
    });
    
    // Criar arestas
    const edges = [];
    filteredConcepts.forEach(([key, concept]) => {
        concept.connections.forEach(connKey => {
            if (nodeMap[connKey] !== undefined && nodeMap[key] !== undefined) {
                edges.push({
                    source: nodeMap[key],
                    target: nodeMap[connKey]
                });
            }
        });
    });
    
    // Parâmetros da simulação
    const params = {
        repulsion: 5000,
        attraction: 0.001,
        damping: 0.85,
        centerForce: 0.02,
        minDistance: 100
    };
    
    let animationId;
    let isDragging = false;
    let draggedNode = null;
    
    // Função de atualização
    function update() {
        // Força de repulsão entre todos os nós
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const dx = nodes[j].x - nodes[i].x;
                const dy = nodes[j].y - nodes[i].y;
                const dist = Math.sqrt(dx * dx + dy * dy) || 1;
                
                if (dist < params.minDistance) {
                    const force = params.repulsion / (dist * dist);
                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;
                    
                    nodes[i].vx -= fx;
                    nodes[i].vy -= fy;
                    nodes[j].vx += fx;
                    nodes[j].vy += fy;
                }
            }
        }
        
        // Força de atração pelas arestas
        edges.forEach(edge => {
            const source = nodes[edge.source];
            const target = nodes[edge.target];
            const dx = target.x - source.x;
            const dy = target.y - source.y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;
            
            const force = dist * params.attraction;
            const fx = (dx / dist) * force;
            const fy = (dy / dist) * force;
            
            source.vx += fx;
            source.vy += fy;
            target.vx -= fx;
            target.vy -= fy;
        });
        
        // Força para o centro
        const centerX = width / 2;
        const centerY = height / 2;
        
        nodes.forEach(node => {
            const dx = centerX - node.x;
            const dy = centerY - node.y;
            node.vx += dx * params.centerForce;
            node.vy += dy * params.centerForce;
        });
        
        // Atualizar posições
        nodes.forEach(node => {
            if (node !== draggedNode) {
                node.vx *= params.damping;
                node.vy *= params.damping;
                node.x += node.vx;
                node.y += node.vy;
                
                // Manter dentro dos limites
                node.x = Math.max(node.radius, Math.min(width - node.radius, node.x));
                node.y = Math.max(node.radius, Math.min(height - node.radius, node.y));
            }
        });
    }
    
    // Função de renderização
    function render() {
        ctx.clearRect(0, 0, width, height);
        
        // Desenhar arestas
        ctx.strokeStyle = 'rgba(139, 92, 246, 0.2)';
        ctx.lineWidth = 1;
        edges.forEach(edge => {
            const source = nodes[edge.source];
            const target = nodes[edge.target];
            ctx.beginPath();
            ctx.moveTo(source.x, source.y);
            ctx.lineTo(target.x, target.y);
            ctx.stroke();
        });
        
        // Desenhar nós
        nodes.forEach(node => {
            const isSelected = node.key === selectedConcept;
            
            // Círculo externo (brilho se selecionado)
            if (isSelected) {
                ctx.fillStyle = node.concept.color + '40';
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.radius + 10, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Círculo principal
            ctx.fillStyle = node.concept.color;
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
            ctx.fill();
            
            // Borda
            ctx.strokeStyle = isSelected ? '#ffffff' : 'rgba(255, 255, 255, 0.3)';
            ctx.lineWidth = isSelected ? 3 : 1;
            ctx.stroke();
            
            // Texto
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 12px sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            
            // Dividir texto em linhas se necessário
            const words = node.concept.name.split(' ');
            if (words.length > 2) {
                ctx.fillText(words.slice(0, 2).join(' '), node.x, node.y - 5);
                ctx.fillText(words.slice(2).join(' '), node.x, node.y + 8);
            } else {
                ctx.fillText(node.concept.name, node.x, node.y);
            }
        });
    }
    
    // Loop de animação
    function animate() {
        update();
        render();
        animationId = requestAnimationFrame(animate);
    }
    
    // Interação com mouse
    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const mouseX = (e.clientX - rect.left) * scaleX;
        const mouseY = (e.clientY - rect.top) * scaleY;
        
        // Verificar se clicou em algum nó
        for (let node of nodes) {
            const dx = mouseX - node.x;
            const dy = mouseY - node.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist < node.radius) {
                isDragging = true;
                draggedNode = node;
                selectConcept(node.key);
                break;
            }
        }
    });
    
    canvas.addEventListener('mousemove', (e) => {
        if (isDragging && draggedNode) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            draggedNode.x = (e.clientX - rect.left) * scaleX;
            draggedNode.y = (e.clientY - rect.top) * scaleY;
            draggedNode.vx = 0;
            draggedNode.vy = 0;
        }
        
        // Mudar cursor se estiver sobre um nó
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const mouseX = (e.clientX - rect.left) * scaleX;
        const mouseY = (e.clientY - rect.top) * scaleY;
        
        let overNode = false;
        for (let node of nodes) {
            const dx = mouseX - node.x;
            const dy = mouseY - node.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist < node.radius) {
                overNode = true;
                break;
            }
        }
        
        canvas.style.cursor = overNode ? 'pointer' : 'default';
    });
    
    canvas.addEventListener('mouseup', () => {
        isDragging = false;
        draggedNode = null;
    });
    
    canvas.addEventListener('mouseleave', () => {
        isDragging = false;
        draggedNode = null;
    });
    
    // Iniciar animação
    animate();
    
    // Limpar ao fechar
    const originalClose = closeRizoma;
    window.closeRizoma = function() {
        if (animationId) {
            cancelAnimationFrame(animationId);
        }
        originalClose();
        window.closeRizoma = originalClose;
    };
}

/**
 * Desenhar linhas de conexão entre conceitos (modo grid)
 */
function drawConnections() {
    if (!selectedConcept) return;
    
    const svg = document.querySelector('#connection-svg-container svg');
    if (!svg) return;
    
    // Limpar conexões anteriores
    svg.innerHTML = '';
    
    // Obter posição do card selecionado
    const selectedCard = document.querySelector(`[data-concept-key="${selectedConcept}"]`);
    if (!selectedCard) return;
    
    const selectedRect = selectedCard.getBoundingClientRect();
    const containerRect = document.getElementById('concepts-grid').getBoundingClientRect();
    
    const selectedCenterX = selectedRect.left + selectedRect.width / 2 - containerRect.left;
    const selectedCenterY = selectedRect.top + selectedRect.height / 2 - containerRect.top;
    
    // Desenhar linha para cada conexão
    const concept = conceptGraph[selectedConcept];
    concept.connections.forEach(connKey => {
        const connCard = document.querySelector(`[data-concept-key="${connKey}"]`);
        if (!connCard) return;
        
        const connRect = connCard.getBoundingClientRect();
        const connCenterX = connRect.left + connRect.width / 2 - containerRect.left;
        const connCenterY = connRect.top + connRect.height / 2 - containerRect.top;
        
        // Criar linha SVG
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', selectedCenterX);
        line.setAttribute('y1', selectedCenterY);
        line.setAttribute('x2', connCenterX);
        line.setAttribute('y2', connCenterY);
        line.setAttribute('stroke', concept.color);
        line.setAttribute('stroke-width', '2');
        line.setAttribute('stroke-opacity', '0.5');
        line.setAttribute('stroke-dasharray', '5,5');
        
        // Animação de "formiga marchando"
        const animate = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        animate.setAttribute('attributeName', 'stroke-dashoffset');
        animate.setAttribute('from', '0');
        animate.setAttribute('to', '10');
        animate.setAttribute('dur', '0.5s');
        animate.setAttribute('repeatCount', 'indefinite');
        
        line.appendChild(animate);
        svg.appendChild(line);
    });
}


/**
 * Criar card de conceito
 */
function createConceptCard(key, concept) {
    const card = document.createElement('div');
    card.className = 'concept-card';
    card.dataset.concept = key;
    card.dataset.conceptKey = key;
    
    const isSelected = selectedConcept === key;
    const isConnected = selectedConcept && conceptGraph[selectedConcept]?.connections.includes(key);
    
    card.style.cssText = `
        background: ${isSelected ? 'rgba(139, 92, 246, 0.2)' : isConnected ? 'rgba(99, 102, 241, 0.15)' : 'rgba(26, 26, 46, 0.8)'};
        border: 2px solid ${isSelected ? concept.color : isConnected ? conceptGraph[selectedConcept].color : 'rgba(' + hexToRgb(concept.color) + ', 0.3)'};
        border-radius: 12px;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        ${isSelected ? 'transform: scale(1.05); box-shadow: 0 0 30px ' + concept.color + ';' : ''}
        ${isConnected ? 'box-shadow: 0 0 20px ' + conceptGraph[selectedConcept].color + '40;' : ''}
    `;
    
    // Badge de camada temporal
    const layerBadge = {
        '-1': '🕰️ Passado',
        '0': '⚡ Presente',
        '1': '🔮 Futuro'
    }[concept.layer] || '❓';
    
    card.innerHTML = `
        <div style="position: absolute; top: 0.5rem; right: 0.5rem; font-size: 0.7rem; opacity: 0.7;">
            ${layerBadge}
        </div>
        <h3 style="color: ${concept.color}; margin-bottom: 0.5rem; font-size: 1.2rem;">${concept.name}</h3>
        <p style="color: #d1d5db; font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.5;">${concept.description}</p>
        <div style="margin-top: 1rem;">
            <strong style="color: #a78bfa; font-size: 0.85rem;">Conectado a (${concept.connections.length}):</strong>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">
                ${concept.connections.map(conn => {
                    const connConcept = conceptGraph[conn];
                    if (!connConcept) return '';
                    return `<span style="background: ${connConcept.color}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem;">${connConcept.name}</span>`;
                }).join('')}
            </div>
        </div>
    `;
    
    card.addEventListener('click', () => selectConcept(key));
    
    card.addEventListener('mouseenter', () => {
        if (key !== selectedConcept) {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = `0 10px 30px ${concept.color}40`;
        }
    });
    
    card.addEventListener('mouseleave', () => {
        if (key !== selectedConcept) {
            card.style.transform = '';
            card.style.boxShadow = isConnected ? `0 0 20px ${conceptGraph[selectedConcept].color}40` : '';
        }
    });
    
    return card;
}

/**
 * Selecionar conceito
 */
function selectConcept(key) {
    console.log('🎯 Conceito selecionado:', key);
    selectedConcept = selectedConcept === key ? null : key;
    renderRizomaGraph();
    
    // Mostrar painel de detalhes se houver conceito selecionado
    if (selectedConcept) {
        showConceptDetails(selectedConcept);
    } else {
        hideConceptDetails();
    }
}

/**
 * Mostrar painel de detalhes do conceito
 */
function showConceptDetails(key) {
    const concept = conceptGraph[key];
    if (!concept) return;
    
    // Remover painel existente
    hideConceptDetails();
    
    // Criar painel
    const panel = document.createElement('div');
    panel.id = 'concept-details-panel';
    panel.style.cssText = `
        position: fixed;
        right: 2rem;
        top: 6rem;
        width: 400px;
        max-height: calc(100vh - 8rem);
        background: rgba(26, 26, 46, 0.95);
        border: 2px solid ${concept.color};
        border-radius: 12px;
        padding: 2rem;
        z-index: 10001;
        overflow-y: auto;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        animation: slideInRight 0.3s ease;
    `;
    
    // Adicionar animação CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        #concept-details-panel::-webkit-scrollbar {
            width: 8px;
        }
        #concept-details-panel::-webkit-scrollbar-track {
            background: rgba(139, 92, 246, 0.1);
            border-radius: 4px;
        }
        #concept-details-panel::-webkit-scrollbar-thumb {
            background: ${concept.color};
            border-radius: 4px;
        }
    `;
    document.head.appendChild(style);
    
    // Badge de camada
    const layerBadge = {
        '-1': '🕰️ Passado',
        '0': '⚡ Presente',
        '1': '🔮 Futuro'
    }[concept.layer] || '❓';
    
    // Conteúdo do painel
    panel.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <h3 style="color: ${concept.color}; margin: 0; font-size: 1.5rem;">${concept.name}</h3>
            <button onclick="hideConceptDetails()" style="
                background: rgba(239, 68, 68, 0.2);
                border: 1px solid rgba(239, 68, 68, 0.3);
                color: #ef4444;
                border-radius: 6px;
                padding: 0.5rem 0.75rem;
                cursor: pointer;
                font-size: 0.9rem;
                transition: all 0.3s ease;
            ">✕</button>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <span style="
                display: inline-block;
                background: ${concept.color}40;
                color: ${concept.color};
                padding: 0.5rem 1rem;
                border-radius: 6px;
                font-size: 0.9rem;
                font-weight: 600;
            ">${layerBadge}</span>
        </div>
        
        <p style="color: #d1d5db; line-height: 1.6; margin-bottom: 2rem;">
            ${concept.description}
        </p>
        
        <div style="margin-bottom: 2rem;">
            <h4 style="color: #a78bfa; font-size: 1.1rem; margin-bottom: 1rem;">
                🔗 Conexões (${concept.connections.length})
            </h4>
            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                ${concept.connections.map(connKey => {
                    const connConcept = conceptGraph[connKey];
                    if (!connConcept) return '';
                    return `
                        <div onclick="selectConcept('${connKey}')" style="
                            background: rgba(${hexToRgb(connConcept.color)}, 0.1);
                            border: 1px solid rgba(${hexToRgb(connConcept.color)}, 0.3);
                            border-radius: 8px;
                            padding: 0.75rem;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        " onmouseenter="this.style.borderColor='${connConcept.color}'; this.style.transform='translateX(5px)';"
                           onmouseleave="this.style.borderColor='rgba(${hexToRgb(connConcept.color)}, 0.3)'; this.style.transform='translateX(0)';">
                            <div style="display: flex; align-items: center; gap: 0.75rem;">
                                <div style="
                                    width: 12px;
                                    height: 12px;
                                    background: ${connConcept.color};
                                    border-radius: 50%;
                                    flex-shrink: 0;
                                "></div>
                                <div style="flex: 1;">
                                    <div style="color: ${connConcept.color}; font-weight: 600; margin-bottom: 0.25rem;">
                                        ${connConcept.name}
                                    </div>
                                    <div style="color: #9ca3af; font-size: 0.85rem;">
                                        ${connConcept.description}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
        
        <div style="
            border-top: 1px solid rgba(139, 92, 246, 0.3);
            padding-top: 1rem;
            color: #9ca3af;
            font-size: 0.85rem;
        ">
            💡 <strong>Dica:</strong> Clique em uma conexão para explorar outro conceito
        </div>
    `;
    
    rizomaOverlay.appendChild(panel);
    
    // Expor função globalmente
    window.hideConceptDetails = hideConceptDetails;
}

/**
 * Esconder painel de detalhes
 */
function hideConceptDetails() {
    const panel = document.getElementById('concept-details-panel');
    if (panel) {
        panel.remove();
    }
}

/**
 * Helper: converter hex para rgb
 */
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? 
        `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : 
        '139, 92, 246';
}

/**
 * Adicionar tags de conceitos ao conteúdo existente
 */
function tagConceptsInContent() {
    console.log('🏷️ Adicionando tags de conceitos...');
    
    // Função auxiliar para processar nó de texto
    function processTextNode(textNode) {
        const text = textNode.textContent;

        // Build alternation of concept names (longest first to prefer longer matches)
        const concepts = Object.entries(conceptGraph).map(([key, concept]) => ({ key, name: concept.name, color: concept.color }));
        concepts.sort((a, b) => b.name.length - a.name.length);
        const alternation = concepts.map(c => escapeRegExp(c.name)).join('|');

        if (!alternation) return;

        // Build combined regex (try unicode-aware, fallback to latin-range capture)
        let combinedRegex;
        let usesPrefix = false;
        try {
            combinedRegex = new RegExp('(?<!\\p{L})(' + alternation + ')(?!\\p{L})', 'giu');
        } catch (err) {
            // Fallback for older engines: capture prefix char (or start)
            combinedRegex = new RegExp('(^|[^A-Za-zÀ-ÖØ-öø-ÿ])(' + alternation + ')(?=$|[^A-Za-zÀ-ÖØ-öø-ÿ])', 'gi');
            usesPrefix = true;
        }

        const fragment = document.createDocumentFragment();
        let lastIndex = 0;
        let match;

        while ((match = combinedRegex.exec(text)) !== null) {
            const fullIndex = match.index;
            if (usesPrefix) {
                // match[1] = prefix, match[2] = word
                const prefix = match[1] || '';
                const word = match[2];
                const start = fullIndex + prefix.length;
                const end = start + word.length;

                if (start > lastIndex) {
                    fragment.appendChild(document.createTextNode(text.slice(lastIndex, start)));
                }

                // find corresponding concept key (case-insensitive)
                const found = concepts.find(c => c.name.toLowerCase() === word.toLowerCase());
                const span = document.createElement('span');
                span.className = 'concept-tag';
                span.dataset.concept = found ? found.key : word.toLowerCase();
                span.style.color = found ? found.color : '#8b5cf6';
                span.style.textDecoration = 'underline dotted';
                span.style.cursor = 'pointer';
                span.style.fontWeight = '500';
                span.style.transition = 'all 0.3s ease';
                span.textContent = word;
                span.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); if (found) window.openRizoma(found.key); });
                span.title = `🌀 Clique para explorar '${word}' no rizoma`;
                // hover effects
                span.addEventListener('mouseenter', () => {
                    span.style.textDecoration = 'underline solid';
                    if (found) span.style.textShadow = `0 0 8px rgba(${hexToRgb(found.color)}, 0.25)`;
                });
                span.addEventListener('mouseleave', () => {
                    span.style.textDecoration = 'underline dotted';
                    span.style.textShadow = 'none';
                });

                fragment.appendChild(span);
                lastIndex = end;
            } else {
                // match[1] is the word
                const word = match[1];
                const start = match.index;
                const end = start + word.length;

                if (start > lastIndex) {
                    fragment.appendChild(document.createTextNode(text.slice(lastIndex, start)));
                }

                const found = concepts.find(c => c.name.toLowerCase() === word.toLowerCase());
                const span = document.createElement('span');
                span.className = 'concept-tag';
                span.dataset.concept = found ? found.key : word.toLowerCase();
                span.style.color = found ? found.color : '#8b5cf6';
                span.style.textDecoration = 'underline dotted';
                span.style.cursor = 'pointer';
                span.style.fontWeight = '500';
                span.style.transition = 'all 0.3s ease';
                span.textContent = word;
                span.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); if (found) window.openRizoma(found.key); });
                span.title = `🌀 Clique para explorar '${word}' no rizoma`;
                // hover effects
                span.addEventListener('mouseenter', () => {
                    span.style.textDecoration = 'underline solid';
                    if (found) span.style.textShadow = `0 0 8px rgba(${hexToRgb(found.color)}, 0.25)`;
                });
                span.addEventListener('mouseleave', () => {
                    span.style.textDecoration = 'underline dotted';
                    span.style.textShadow = 'none';
                });

                fragment.appendChild(span);
                lastIndex = end;
            }
        }

        if (lastIndex < text.length) {
            fragment.appendChild(document.createTextNode(text.slice(lastIndex)));
        }

        // If no matches, do nothing
        if (!fragment.childNodes.length) return;

        const parent = textNode.parentNode;
        parent.insertBefore(fragment, textNode);
        parent.removeChild(textNode);
    }
    
    // Procurar em parágrafos e listas, mas apenas nos nós de texto
    const selectors = 'p, li, h1, h2, h3, h4, blockquote, td';
    document.querySelectorAll(selectors).forEach(element => {
        // Pular se já foi processado ou se contém elementos interativos
        if (element.querySelector('.concept-tag') || 
            element.querySelector('a') || 
            element.querySelector('button') ||
            element.closest('.sidebar') ||
            element.closest('#rizoma-overlay')) {
            return;
        }
        
        // Processar apenas nós de texto diretos
        Array.from(element.childNodes).forEach(node => {
            if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                processTextNode(node);
            }
        });
    });
    
    console.log('✅ Conceitos tagueados no conteúdo');
}

// Escapa caracteres especiais para construir safe regex a partir de strings
function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Build a regex to match a concept name as a whole word.
 * Tries to use Unicode-aware lookarounds; if not supported, returns a fallback
 * regex that captures a non-letter prefix so we can preserve it during replacement.
 */
function buildConceptRegex(escapedName) {
    try {
        // Prefer lookaround with Unicode property escapes
        const regex = new RegExp('(?<!\\p{L})(' + escapedName + ')(?!\\p{L})', 'giu');
        return { regex, usesPrefixGroup: false };
    } catch (err) {
        // Fallback: capture a non-letter prefix (or start of string) and the word
        // Note: range A-Za-zÀ-ÖØ-öø-ÿ covers many Latin-1 accented chars
        const fallback = new RegExp('(^|[^A-Za-zÀ-ÖØ-öø-ÿ])(' + escapedName + ')(?=$|[^A-Za-zÀ-ÖØ-öø-ÿ])', 'gi');
        return { regex: fallback, usesPrefixGroup: true };
    }
}

// Inicializar ao carregar página
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌀 Módulo de navegação rizomática carregado');
    
    // Inicializar overlay imediatamente
    initializeRizoma();
    
    // Expor funções globalmente ANTES de taguear
    window.openRizoma = openRizoma;
    window.closeRizoma = closeRizoma;
    window.selectConcept = selectConcept;
    window.hideConceptDetails = hideConceptDetails;
    
    // Esperar conteúdo carregar antes de taguear
    setTimeout(() => {
        tagConceptsInContent();
        console.log('✅ Sistema rizomático pronto!');
    }, 2000);
});

// Atalho de teclado: R para abrir rizoma, ESC para fechar
document.addEventListener('keydown', (e) => {
    // R para toggle
    if ((e.key === 'r' || e.key === 'R') && !e.ctrlKey && !e.metaKey && !e.altKey) {
        // Verificar se não está digitando em um input
        if (document.activeElement.tagName !== 'INPUT' && 
            document.activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (!rizomaActive) {
                openRizoma();
            } else {
                closeRizoma();
            }
        }
    }
    
    // ESC para fechar
    if (e.key === 'Escape' && rizomaActive) {
        e.preventDefault();
        closeRizoma();
    }
});
