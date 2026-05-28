/* Runs synchronously from <head> before body paints so the
   .motion-ready class can hide [data-reveal] elements before they
   first appear, preventing a flash of revealed content. Removes
   itself after 2s if Motion never loads, so content stays visible. */
(function () {
  var h = document.documentElement;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  h.classList.add('motion-ready');
  setTimeout(function () { if (!window.Motion) h.classList.remove('motion-ready'); }, 2000);
})();
