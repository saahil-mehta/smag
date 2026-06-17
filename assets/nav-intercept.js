/* Forces full navigation on internal link clicks, with a short exit fade.
   Framer's runtime used to handle these client-side; since the runtime is
   stripped, internal links would otherwise no-op when the bundle is missing.
   Captures click in the capture phase so it preempts any leftover Framer
   handler that might re-attach. External schemes and modifier-clicks pass
   through. */
(function () {
  function pageName(pathname) {
    return (pathname.split('/').pop() || 'index.html').toLowerCase();
  }

  function isHomePath(pathname) {
    var page = pageName(pathname);
    return page === '' || page === 'index.html';
  }

  function sameDocument(url) {
    return url.origin === location.origin &&
      url.pathname === location.pathname &&
      url.search === location.search;
  }

  function go(url) {
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.documentElement.classList.add('smag-page-leaving');
    setTimeout(function () { location.assign(url.href); }, reduce ? 0 : 180);
  }

  addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var h = a.getAttribute('href');
    if (!h || /^(mailto:|tel:|#|javascript:)/i.test(h)) return;
    if (a.target && a.target !== '' && a.target !== '_self') return;

    var url;
    try { url = new URL(h, location.href); } catch (_) { return; }
    if (url.origin !== location.origin) return;
    if (sameDocument(url) && url.hash) return;

    e.preventDefault();
    e.stopImmediatePropagation();
    if (url.hash === '#services' && isHomePath(url.pathname)) {
      try { sessionStorage.setItem('smagScrollTarget', 'services'); } catch (_) {}
      url.hash = '';
    }
    go(url);
  }, true);
})();
