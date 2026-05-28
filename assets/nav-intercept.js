/* Forces a full navigation on internal link clicks. Framer's runtime
   used to handle these client-side; since the runtime is stripped,
   internal links would otherwise no-op when the bundle is missing.
   Captures click in the capture phase so it preempts any leftover
   Framer handler that might re-attach. External schemes and
   modifier-clicks are passed through. */
(function () {
  addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var h = a.getAttribute('href');
    if (!h || /^(https?:|mailto:|tel:|#|javascript:)/i.test(h)) return;
    if (a.target && a.target !== '' && a.target !== '_self') return;
    e.preventDefault();
    e.stopImmediatePropagation();
    location.assign(a.href);
  }, true);
})();
