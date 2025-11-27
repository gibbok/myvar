let searchUI;

window.addEventListener('DOMContentLoaded', (event) => {
  const modal = document.getElementById('search-modal');
  const closeBtn = document.querySelector('.search-modal__close');
  const backdrop = document.querySelector('.search-modal__backdrop');
  const searchLink = document.querySelector('a[href="#"]');
  
  // Initialize Pagefind UI
  searchUI = new PagefindUI({ 
    element: "#search", 
    showSubResults: true,
    resetStyles: false,
    showEmptyFilters: false
  });
  
  // Open modal
  if (searchLink) {
    searchLink.addEventListener('click', (e) => {
      e.preventDefault();
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      
      // Focus search input immediately
      const searchInput = document.querySelector('#search input');
      if (searchInput) {
        searchInput.focus();
      }
    });
  }
  
  // Close modal
  function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
  
  closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', closeModal);
  
  // Close modal when clicking search results
  document.addEventListener('click', (e) => {
    if (e.target.closest('.pagefind-ui__result-link') && modal.style.display === 'flex') {
      closeModal();
    }
  });
  
  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display === 'flex') {
      closeModal();
    }
  });
});
