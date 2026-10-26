// Скрипт подключён с defer: элементы страницы уже созданы.
const backToTop = document.querySelector('.back-to-top');

if (backToTop) {
  backToTop.hidden = false;
  backToTop.addEventListener('click', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduceMotion ? 'instant' : 'smooth' });
  });
}
