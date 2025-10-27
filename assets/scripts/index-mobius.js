/**
 * 🌀 INDEX MÖBIUS - Fita Navegável para o Livro Completo
 * 
 * Integra Teoria (33 capítulos) + Manifesto + Sistema Nhandereko
 * em um loop infinito de Möbius.
 * 
 * Estrutura RGB Ternária (35 pontos):
 * - CAMADA PASSADO (Vermelho/Tese): Caps 0-10 — Fundamentos Marxismo + Cibernética
 * - CAMADA PRESENTE (Verde/Antítese): Caps 11-21 — Síntese + Análise crítica atual
 * - CAMADA FUTURO (Azul/Síntese): Caps 22-32 + Manifesto + Sistema — Construção
 */

class IndexMobius {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error('❌ Canvas não encontrado:', canvasId);
            return;
        }
        
        this.ctx = this.canvas.getContext('2d');
        this.options = {
            width: options.width || Math.min(window.innerWidth - 40, 1200),
            height: options.height || 600,
            segments: options.segments || 120,
            radius: options.radius || 180,
            stripWidth: options.stripWidth || 60,
            rotationSpeed: options.rotationSpeed || 0.002,
            showLabels: options.showLabels !== false,
            interactive: options.interactive !== false,
            ...options
        };
        
        // Estado
        this.rotation = 0;
        this.autoRotate = true;
        this.hoveredPoint = null;
        this.selectedLayer = null;
        this.mouseX = 0;
        this.mouseY = 0;
        
        // Cores das camadas temporais (RGB TERNÁRIO)
        this.layerColors = {
            passado: { 
                primary: '#dc2626',    // Vermelho (Tese)
                secondary: '#ef4444',  // Vermelho claro
                name: 'PASSADO (Tese)' 
            },
            presente: { 
                primary: '#059669',    // Verde (Antítese)
                secondary: '#10b981',  // Verde claro
                name: 'PRESENTE (Antítese)' 
            },
            futuro: { 
                primary: '#2563eb',    // Azul (Síntese)
                secondary: '#3b82f6',  // Azul claro
                name: 'FUTURO (Síntese)' 
            }
        };
        
        // Pontos de navegação mapeados
        this.navigationPoints = this.createNavigationPoints();
        
        this.init();
    }
    
    createNavigationPoints() {
        const points = [];
        const totalPoints = 35; // 33 caps (0-32) + manifesto + sistema
        
        // CAMADA PASSADO (Vermelho): Caps 0-10 (Fundamentos + Marxismo + Cibernética)
        const passadoCaps = [
            { id: 'cap-0', label: 'Cap 0: Como Usar Este Livro', short: 'Início' },
            { id: 'cap-1', label: 'Cap 1: Introdução ao Marxismo', short: 'Marxismo' },
            { id: 'cap-2', label: 'Cap 2: Introdução à Cibernética', short: 'Cibernética' },
            { id: 'cap-3', label: 'Cap 3: Capitalismo Digital', short: 'Cap. Digital' },
            { id: 'cap-4', label: 'Cap 4: Economia Política', short: 'Econ. Política' },
            { id: 'cap-5', label: 'Cap 5: Marx e Crítica', short: 'Marx' },
            { id: 'cap-6', label: 'Cap 6: Cibernética e Sociedade', short: 'Cib. Social' },
            { id: 'cap-7', label: 'Cap 7: Marxismo e Tecnologia', short: 'Marx Tech' },
            { id: 'cap-8', label: 'Cap 8: Trabalho Imaterial', short: 'Trab. Imaterial' },
            { id: 'cap-9', label: 'Cap 9: Pós-Operaísmo', short: 'Pós-Op' },
            { id: 'cap-10', label: 'Cap 10: Crítica do Valor', short: 'Wertkritik' }
        ];
        
        // CAMADA PRESENTE (Verde): Caps 11-21 (Síntese + Crítica Atual)
        const presenteCaps = [
            { id: 'cap-11', label: 'Cap 11: Síntese Informacional', short: 'Síntese' },
            { id: 'cap-12', label: 'Cap 12: Ciberfeminismo', short: 'Ciberfem' },
            { id: 'cap-13', label: 'Cap 13: Plataformas', short: 'Plataformas' },
            { id: 'cap-14', label: 'Cap 14: Vigilância', short: 'Vigilância' },
            { id: 'cap-15', label: 'Cap 15: Algoritmos', short: 'Algoritmos' },
            { id: 'cap-16', label: 'Cap 16: Uberização', short: 'Uberização' },
            { id: 'cap-17', label: 'Cap 17: IA e Trabalho', short: 'IA' },
            { id: 'cap-18', label: 'Cap 18: Criptomoedas', short: 'Crypto' },
            { id: 'cap-19', label: 'Cap 19: NFTs', short: 'NFT' },
            { id: 'cap-20', label: 'Cap 20: Geopolítica', short: 'Geopolítica' },
            { id: 'cap-21', label: 'Cap 21: Brasil Subordinado', short: 'Brasil' }
        ];
        
        // CAMADA FUTURO (Azul): Caps 22-32 + Manifesto + Sistema (Construção)
        const futuroCaps = [
            { id: 'cap-22', label: 'Cap 22: Necropolítica Digital', short: 'Necropolítica' },
            { id: 'cap-23', label: 'Cap 23: Resistências', short: 'Resistências' },
            { id: 'cap-24', label: 'Cap 24: Cybersyn', short: 'Cybersyn' },
            { id: 'cap-25', label: 'Cap 25: Commons', short: 'Commons' },
            { id: 'cap-26', label: 'Cap 26: Cooperativas', short: 'Cooperativas' },
            { id: 'cap-27', label: 'Cap 27: Software Livre', short: 'FOSS' },
            { id: 'cap-28', label: 'Cap 28: Democracia Digital', short: 'Democracia' },
            { id: 'cap-29', label: 'Cap 29: Comunicação e Informação', short: 'Comunicação' },
            { id: 'cap-30', label: 'Cap 30: Salto Dialético', short: 'Salto' },
            { id: 'cap-31', label: 'Cap 31: Fim do Ultrarracionalismo', short: 'Ultrarrac.' },
            { id: 'cap-32', label: 'Cap 32: Projeto Urgente', short: 'Projeto' },
            { id: 'manifesto', label: 'Manifesto: Eu Coletivo', short: 'Manifesto' },
            { id: 'nhandereko', label: 'Sistema Nhandereko', short: 'Sistema' }
        ];
        
        // Distribuir no círculo
        let index = 0;
        
        passadoCaps.forEach((cap, i) => {
            const angle = (index / totalPoints) * Math.PI * 2;
            points.push({
                ...cap,
                layer: 'passado',
                angle: angle,
                index: index
            });
            index++;
        });
        
        presenteCaps.forEach((cap, i) => {
            const angle = (index / totalPoints) * Math.PI * 2;
            points.push({
                ...cap,
                layer: 'presente',
                angle: angle,
                index: index
            });
            index++;
        });
        
        futuroCaps.forEach((cap, i) => {
            const angle = (index / totalPoints) * Math.PI * 2;
            points.push({
                ...cap,
                layer: 'futuro',
                angle: angle,
                index: index
            });
            index++;
        });
        
        return points;
    }
    
    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        if (this.options.interactive) {
            this.setupEventListeners();
        }
        
        this.animate();
        console.log('🌀 Index Möbius inicializado com', this.navigationPoints.length, 'pontos');
    }
    
    resize() {
        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = this.options.width * dpr;
        this.canvas.height = this.options.height * dpr;
        this.canvas.style.width = this.options.width + 'px';
        this.canvas.style.height = this.options.height + 'px';
        this.ctx.scale(dpr, dpr);
    }
    
    setupEventListeners() {
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouseX = e.clientX - rect.left;
            this.mouseY = e.clientY - rect.top;
            
            this.hoveredPoint = this.getPointAtMouse(this.mouseX, this.mouseY);
            this.canvas.style.cursor = this.hoveredPoint ? 'pointer' : 'default';
        });
        
        this.canvas.addEventListener('click', (e) => {
            if (this.hoveredPoint) {
                this.navigateToSection(this.hoveredPoint.id);
            }
        });
        
        this.canvas.addEventListener('mouseenter', () => {
            this.autoRotate = false;
        });
        
        this.canvas.addEventListener('mouseleave', () => {
            this.autoRotate = true;
            this.hoveredPoint = null;
        });
        
        // Touch support
        let touchStartX = 0;
        this.canvas.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
            this.autoRotate = false;
        });
        
        this.canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            const touchX = e.touches[0].clientX;
            const delta = touchX - touchStartX;
            this.rotation += delta * 0.01;
            touchStartX = touchX;
        }, { passive: false });
        
        this.canvas.addEventListener('touchend', () => {
            setTimeout(() => {
                this.autoRotate = true;
            }, 2000);
        });
    }
    
    getPointAtMouse(mx, my) {
        const centerX = this.options.width / 2;
        const centerY = this.options.height / 2;
        
        for (const point of this.navigationPoints) {
            const angle = point.angle + this.rotation;
            const x = centerX + Math.cos(angle) * this.options.radius;
            const y = centerY + Math.sin(angle) * this.options.radius;
            
            const distance = Math.sqrt((mx - x) ** 2 + (my - y) ** 2);
            if (distance < 20) {
                return point;
            }
        }
        
        return null;
    }
    
    navigateToSection(sectionId) {
        // Verifica se é link externo
        if (sectionId === 'manifesto') {
            window.location.href = 'manifesto.html';
            return;
        }
        
        if (sectionId === 'nhandereko') {
            window.open('https://github.com/silvanoneto/revolucao-cibernetica/tree/master/nhandereko', '_blank');
            return;
        }
        
        const element = document.getElementById(sectionId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // Highlight animation
            element.style.transition = 'all 0.3s ease';
            element.style.transform = 'scale(1.01)';
            element.style.boxShadow = '0 0 30px rgba(139, 92, 246, 0.5)';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
                element.style.boxShadow = 'none';
            }, 300);
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.options.width, this.options.height);
        
        if (this.autoRotate) {
            this.rotation += this.options.rotationSpeed;
        }
        
        this.drawMobius();
        this.drawNavigationPoints();
        this.drawLayerLabels();
        this.drawCenterInfo();
        
        if (this.hoveredPoint) {
            this.drawHoverTooltip();
        }
        
        requestAnimationFrame(() => this.animate());
    }
    
    drawMobius() {
        const centerX = this.options.width / 2;
        const centerY = this.options.height / 2;
        const { segments, radius, stripWidth } = this.options;
        
        for (let i = 0; i < segments; i++) {
            const t = (i / segments) * Math.PI * 2;
            const normalizedT = ((t + this.rotation) % (Math.PI * 2) + Math.PI * 2) % (Math.PI * 2);
            
            // Determinar layer
            let layer;
            if (normalizedT < (9 / 27) * Math.PI * 2) {
                layer = 'passado';
            } else if (normalizedT < (17 / 27) * Math.PI * 2) {
                layer = 'presente';
            } else {
                layer = 'futuro';
            }
            
            const colors = this.layerColors[layer];
            
            // Calcular geometria da fita
            const x = centerX + Math.cos(t + this.rotation) * radius;
            const y = centerY + Math.sin(t + this.rotation) * radius;
            
            const twist = t / 2; // Möbius twist
            const perpX = -Math.sin(t + this.rotation);
            const perpY = Math.cos(t + this.rotation);
            
            const width = stripWidth * Math.cos(twist);
            const x1 = x + perpX * width;
            const y1 = y + perpY * width;
            const x2 = x - perpX * width;
            const y2 = y - perpY * width;
            
            // Gradient
            const gradient = this.ctx.createLinearGradient(x1, y1, x2, y2);
            gradient.addColorStop(0, colors.primary);
            gradient.addColorStop(1, colors.secondary);
            
            this.ctx.strokeStyle = gradient;
            this.ctx.lineWidth = 4;
            this.ctx.globalAlpha = 0.5 + 0.5 * Math.abs(Math.cos(twist));
            
            this.ctx.beginPath();
            this.ctx.moveTo(x1, y1);
            this.ctx.lineTo(x2, y2);
            this.ctx.stroke();
        }
        
        this.ctx.globalAlpha = 1;
    }
    
    drawNavigationPoints() {
        const centerX = this.options.width / 2;
        const centerY = this.options.height / 2;
        
        for (const point of this.navigationPoints) {
            const angle = point.angle + this.rotation;
            const x = centerX + Math.cos(angle) * this.options.radius;
            const y = centerY + Math.sin(angle) * this.options.radius;
            
            const colors = this.layerColors[point.layer];
            const isHovered = this.hoveredPoint === point;
            const pointSize = isHovered ? 12 : 6;
            
            // Glow
            if (isHovered) {
                this.ctx.shadowBlur = 25;
                this.ctx.shadowColor = colors.primary;
            }
            
            // Ponto
            this.ctx.fillStyle = colors.primary;
            this.ctx.beginPath();
            this.ctx.arc(x, y, pointSize, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Label curto
            if (this.options.showLabels && !isHovered) {
                this.ctx.shadowBlur = 0;
                this.ctx.font = 'bold 10px Inter, sans-serif';
                this.ctx.fillStyle = colors.primary;
                this.ctx.globalAlpha = 0.7;
                this.ctx.textAlign = 'center';
                this.ctx.fillText(point.short, x, y - 15);
            }
            
            this.ctx.shadowBlur = 0;
            this.ctx.globalAlpha = 1;
        }
    }
    
    drawLayerLabels() {
        if (!this.options.showLabels) return;
        
        const centerX = this.options.width / 2;
        const centerY = this.options.height / 2;
        const labelRadius = this.options.radius + 100;
        
        const layers = [
            { name: 'PASSADO', subtitle: '(Tese: Fundamentos)', angle: (4.5 / 27) * Math.PI * 2, color: '#3b82f6' },
            { name: 'PRESENTE', subtitle: '(Antítese: Crítica)', angle: (13 / 27) * Math.PI * 2, color: '#ec4899' },
            { name: 'FUTURO', subtitle: '(Síntese: Construção)', angle: (21.5 / 27) * Math.PI * 2, color: '#8b5cf6' }
        ];
        
        this.ctx.textAlign = 'center';
        
        for (const layer of layers) {
            const angle = layer.angle + this.rotation;
            const x = centerX + Math.cos(angle) * labelRadius;
            const y = centerY + Math.sin(angle) * labelRadius;
            
            this.ctx.font = 'bold 14px Inter, sans-serif';
            this.ctx.fillStyle = layer.color;
            this.ctx.globalAlpha = 0.9;
            this.ctx.fillText(layer.name, x, y);
            
            this.ctx.font = '11px Inter, sans-serif';
            this.ctx.globalAlpha = 0.6;
            this.ctx.fillText(layer.subtitle, x, y + 16);
        }
        
        this.ctx.globalAlpha = 1;
    }
    
    drawCenterInfo() {
        const centerX = this.options.width / 2;
        const centerY = this.options.height / 2;
        
        this.ctx.textAlign = 'center';
        
        // Título
        this.ctx.font = 'bold 18px Inter, sans-serif';
        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillText('REVOLUÇÃO', centerX, centerY - 20);
        this.ctx.fillText('CIBERNÉTICA', centerX, centerY + 5);
        
        // Subtítulo
        this.ctx.font = '12px Inter, sans-serif';
        this.ctx.globalAlpha = 0.7;
        this.ctx.fillText('Loop Infinito', centerX, centerY + 25);
        
        this.ctx.globalAlpha = 1;
    }
    
    drawHoverTooltip() {
        if (!this.hoveredPoint) return;
        
        const padding = 12;
        const text = this.hoveredPoint.label;
        
        this.ctx.font = '13px Inter, sans-serif';
        const metrics = this.ctx.measureText(text);
        const boxWidth = metrics.width + padding * 2;
        const boxHeight = 35;
        
        const x = this.mouseX + 20;
        const y = this.mouseY - 20;
        
        const colors = this.layerColors[this.hoveredPoint.layer];
        
        // Box
        this.ctx.fillStyle = 'rgba(10, 10, 15, 0.95)';
        this.ctx.strokeStyle = colors.primary;
        this.ctx.lineWidth = 2;
        
        this.ctx.beginPath();
        this.ctx.roundRect(x, y - boxHeight, boxWidth, boxHeight, 8);
        this.ctx.fill();
        this.ctx.stroke();
        
        // Text
        this.ctx.fillStyle = '#ffffff';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(text, x + padding, y - boxHeight / 2 + 4);
        
        // Layer indicator
        this.ctx.font = '10px Inter, sans-serif';
        this.ctx.fillStyle = colors.primary;
        this.ctx.fillText(this.layerColors[this.hoveredPoint.layer].name, x + padding, y - 8);
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('index-mobius-canvas');
    if (canvas) {
        window.indexMobius = new IndexMobius('index-mobius-canvas', {
            width: Math.min(window.innerWidth - 40, 1200),
            height: 600,
            showLabels: true,
            interactive: true
        });
    }
});
