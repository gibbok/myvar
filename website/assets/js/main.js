document.addEventListener('click', (event) => {
  const link = event.target.closest('.book-banner a');

  if (!link || typeof window.gtag !== 'function') {
    return;
  }

  window.gtag('event', 'free_edition_banner_click', {
    link_url: link.href,
  });
});
