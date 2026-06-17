/* Runs synchronously from <head> before body paints so the shared
   page-loading and motion-ready classes are present before the first frame.
   animations.js releases them after it has normalised Framer's static export
   states. Timeout fallback keeps content visible if a script fails. */
(function () {
  var h = document.documentElement;
  h.classList.add('smag-page-loading');
  if (!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    h.classList.add('motion-ready');
  }
  // When this page is entered via a cross-document view transition (a same-site
  // link click, with @view-transition in animations.css), the browser is already
  // crossfading the old page into the new one. The page-load gate fading the body
  // up from blank on top of that overlay stacks two entrances and strobes (worst
  // on Safari). pagereveal fires on the incoming page before first paint with
  // event.viewTransition set, so release the gate now and let the transition own
  // the entrance. Cold loads (address bar, refresh) have no viewTransition and
  // keep the gate as normal.
  if ('onpagereveal' in window) {
    window.addEventListener('pagereveal', function (e) {
      if (!e.viewTransition) return;
      h.classList.add('smag-vt-entrance');
      h.classList.remove('smag-page-loading');
      h.classList.add('smag-page-ready');
    });
  }
  setTimeout(function () {
    h.classList.remove('smag-page-loading');
    h.classList.add('smag-page-ready');
    if (!window.Motion) h.classList.remove('motion-ready');
  }, 1600);
})();
