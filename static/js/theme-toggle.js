/**
 * Универсальный скрипт для управления темной темой
 * Автоматически применяется ко всем страницам сайта
 */

// Функция для переключения темы
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Обновляем иконку кнопки
    updateThemeIcon(newTheme);
    
    // Отправляем событие для других скриптов, если нужно
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: newTheme } }));
}

// Функция для обновления иконки кнопки переключения темы
function updateThemeIcon(theme) {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
        const icon = themeToggleBtn.querySelector('i');
        const text = document.getElementById('theme-toggle-text');
        if (icon) {
            if (theme === 'dark') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
                if (text) text.textContent = 'Светлая тема';
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
                if (text) text.textContent = 'Темная тема';
            }
        }
    }
    
    // Обновляем все кнопки переключения темы на странице
    document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
        const icon = btn.querySelector('i');
        const text = btn.querySelector('[data-theme-text]');
        if (icon) {
            if (theme === 'dark') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        }
        if (text) {
            text.textContent = theme === 'dark' ? 'Светлая тема' : 'Темная тема';
        }
    });
}

// Обработчик клика для кнопки переключения темы
function handleThemeToggle(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    toggleTheme();
}

// Инициализация темы при загрузке страницы
function initTheme() {
    // Получаем сохраненную тему или используем системную
    let savedTheme = localStorage.getItem('theme');
    
    // Если тема не сохранена, проверяем системные настройки
    if (!savedTheme) {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            savedTheme = 'dark';
        } else {
            savedTheme = 'light';
        }
    }
    
    const html = document.documentElement;
    
    // Устанавливаем тему до загрузки контента для предотвращения мерцания
    html.setAttribute('data-theme', savedTheme);
    
    // Обновляем иконки кнопок
    updateThemeIcon(savedTheme);
    
    // Добавляем обработчики событий для всех кнопок переключения темы
    const themeToggleBtns = document.querySelectorAll('#theme-toggle-btn, [data-theme-toggle]');
    themeToggleBtns.forEach(btn => {
        btn.removeEventListener('click', handleThemeToggle);
        btn.addEventListener('click', handleThemeToggle);
    });
    
    // Слушаем изменения системной темы
    if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', (e) => {
            // Обновляем только если пользователь не выбрал тему вручную
            if (!localStorage.getItem('theme')) {
                const newTheme = e.matches ? 'dark' : 'light';
                html.setAttribute('data-theme', newTheme);
                updateThemeIcon(newTheme);
            }
        });
    }
}

// Устанавливаем тему синхронно до загрузки DOM для предотвращения мерцания
(function() {
    const savedTheme = localStorage.getItem('theme') || 
        (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', savedTheme);
})();

// Запускаем инициализацию при загрузке DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
} else {
    // DOM уже загружен
    initTheme();
}

// Также пробуем инициализировать через небольшой таймаут на случай, если скрипт загрузился раньше
setTimeout(initTheme, 100);

