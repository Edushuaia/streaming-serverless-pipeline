document.addEventListener('DOMContentLoaded', () => {
    console.log("Página de portafolio cargada. Proyecto de Streaming listo para ser presentado.");

    // Función para resaltar la pestaña de navegación activa
    const navItems = document.querySelectorAll('.tool-nav .nav-item');
    const path = window.location.pathname.split('/').pop(); // Obtiene el nombre del archivo actual (ej: index.html)

    navItems.forEach(item => {
        const itemHref = item.getAttribute('href');
        
        // Verifica si el href coincide con el archivo actual
        if (itemHref === path || (path === '' && itemHref === 'index.html')) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
});