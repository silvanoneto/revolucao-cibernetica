
// ====== TEMA ======
function toggleTheme() {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
}

// Restaurar tema salvo
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    document.documentElement.classList.remove('dark');
}

// ====== TAMANHO DO TEXTO ======
function toggleFontSize() {
    const html = document.documentElement;
    const currentSize = localStorage.getItem('fontSize') || 'medium';
    
    let newSize;
    if (currentSize === 'small') {
        newSize = 'medium';
    } else if (currentSize === 'medium') {
        newSize = 'large';
    } else {
        newSize = 'small';
    }
    
    // Remover classes antigas
    html.classList.remove('font-small', 'font-medium', 'font-large');
    
    // Adicionar nova classe
    html.classList.add('font-' + newSize);
    
    // Salvar preferência
    localStorage.setItem('fontSize', newSize);
}

// Restaurar tamanho de fonte salvo
const savedFontSize = localStorage.getItem('fontSize') || 'medium';
document.documentElement.classList.add('font-' + savedFontSize);

// ====== MENU MOBILE ======
function toggleMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.mobile-overlay, .sidebar-overlay');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (!sidebar || !overlay) return;
    
    const isOpen = sidebar.classList.contains('mobile-open');
    
    if (isOpen) {
        closeMobileMenu();
    } else {
        sidebar.classList.add('mobile-open');
        overlay.classList.add('active');
        if (menuBtn) menuBtn.classList.add('menu-open');
        document.body.style.overflow = 'hidden';
    }
}

// Alias para compatibilidade
function toggleMenu() {
    toggleMobileMenu();
}

function closeMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.mobile-overlay, .sidebar-overlay');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (!sidebar || !overlay) return;
    
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('active');
    if (menuBtn) menuBtn.classList.remove('menu-open');
    document.body.style.overflow = '';
}

function handleOverlayKey(event) {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        closeMobileMenu();
    }
}

// Fechar menu ao pressionar ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeMobileMenu();
    }
});

// ====== BARRA DE PROGRESSO ======
window.addEventListener('scroll', () => {
    const progressBar = document.getElementById('reading-progress');
    if (!progressBar) return;
    
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    progressBar.style.width = scrolled + '%';
});

// ====== BOTÃO VOLTAR AO TOPO ======
const backToTopBtn = document.getElementById('back-to-top');

if (backToTopBtn) {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ====== NAVEGAÇÃO ATIVA ======
function updateActiveNav() {
    const sections = document.querySelectorAll('section[id], .chapter');
    const navLinks = document.querySelectorAll('.sidebar-nav a, .nav-chapter a');

    let current = '';
    const scrollPosition = window.scrollY + 100;
    
    for (const section of sections) {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    }

    for (const link of navLinks) {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href === '#' + current || href === `#${current}`) {
            link.classList.add('active');
        }
    }
}

// Atualizar navegação em scroll e load
window.addEventListener('scroll', updateActiveNav);
window.addEventListener('load', updateActiveNav);

// Modal de imagem em tela cheia
document.addEventListener('DOMContentLoaded', function () {
    // Criar modal
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <span class="image-modal-close">&times;</span>
        <img src="" alt="Diagrama em tela cheia">
    `;
    document.body.appendChild(modal);

    const modalImg = modal.querySelector('img');
    const closeBtn = modal.querySelector('.image-modal-close');

    // Adicionar classe e evento de clique a todas as imagens de diagrama
    const diagramImages = document.querySelectorAll('div[style*="rgba(139, 92, 246, 0.05)"] img');
    for (const img of diagramImages) {
        img.classList.add('clickable-diagram');
        img.setAttribute('role', 'button');
        img.setAttribute('tabindex', '0');
        img.setAttribute('aria-label', 'Clique para ampliar esta imagem');

        const openModal = function () {
            modal.classList.add('active');
            modalImg.src = img.src;
            modalImg.alt = img.alt;
            document.body.style.overflow = 'hidden';
        };

        img.addEventListener('click', openModal);
        img.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openModal();
            }
        });
    }

    // Adicionar evento de clique a todas as imagens com classe clickable-image
    const clickableImages = document.querySelectorAll('.clickable-image');
    for (const img of clickableImages) {
        img.style.cursor = 'zoom-in';
        img.setAttribute('role', 'button');
        img.setAttribute('tabindex', '0');
        img.setAttribute('aria-label', 'Clique para ampliar esta imagem');

        const openModal = function () {
            modal.classList.add('active');
            modalImg.src = img.src;
            modalImg.alt = img.alt || 'Imagem em tela cheia';
            document.body.style.overflow = 'hidden';
        };

        img.addEventListener('click', openModal);
        img.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openModal();
            }
        });
    }

    // Fechar modal
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) {
        if (e.target === modal || e.target === closeBtn) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // Calcular tempo de leitura
    calculateReadingTime();
});

// Calcular e exibir tempo de leitura para cada capítulo
function calculateReadingTime() {
    const wordsPerMinute = 200;
    const chapters = document.querySelectorAll('.chapter');

    for (const chapter of chapters) {
        const text = chapter.textContent || '';
        const words = text.trim().split(/\s+/).length;
        const minutes = Math.ceil(words / wordsPerMinute);

        const heading = chapter.querySelector('h1');
        if (heading && !heading.querySelector('.reading-time')) {
            const readingTimeEl = document.createElement('div');
            readingTimeEl.className = 'reading-time';
            readingTimeEl.setAttribute('aria-label', `Tempo estimado de leitura: ${minutes} minutos`);
            readingTimeEl.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                </svg>
                <span>${minutes} min de leitura</span>
            `;
            heading.appendChild(readingTimeEl);
        }
    }
}
