// Lightbox + graceful fallback when an image file is missing.
(() => {
  const thumbs = [...document.querySelectorAll('.thumb')];
  const dlg = document.getElementById('lightbox');
  const img = document.getElementById('lb-img');
  const cap = document.getElementById('lb-cap');
  let i = 0;

  document.querySelectorAll('.thumb img').forEach(el => {
    el.addEventListener('error', () => {
      el.removeAttribute('src');
      el.closest('.thumb').style.background = 'repeating-linear-gradient(45deg,#2a1850,#2a1850 12px,#331f60 12px,#331f60 24px)';
      el.closest('.thumb').title = 'Image file not found in static/images';
    }, { once: true });
  });

  const show = n => {
    i = (n + thumbs.length) % thumbs.length;
    const t = thumbs[i];
    img.src = t.dataset.full;
    img.alt = t.querySelector('img').alt;
    cap.textContent = `${t.dataset.cap} (${i + 1} / ${thumbs.length})`;
  };
  thumbs.forEach((t, n) => t.addEventListener('click', () => { show(n); dlg.showModal(); }));
  dlg.querySelector('.close').addEventListener('click', () => dlg.close());
  dlg.querySelector('.prev').addEventListener('click', () => show(i - 1));
  dlg.querySelector('.next').addEventListener('click', () => show(i + 1));
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
  document.addEventListener('keydown', e => {
    if (!dlg.open) return;
    if (e.key === 'ArrowLeft') show(i - 1);
    if (e.key === 'ArrowRight') show(i + 1);
  });
})();
