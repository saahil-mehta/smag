/* S-MAG animations: parity with the original Framer motion, vanilla via Motion.
   - Scroll reveals: fade + slide-up (+ optional blur), spring (stiffness 400, damping 58).
   - Navbar: slide-down on load.
   - Marquee: seamless horizontal loop.
   - Press feedback on buttons.
   Progressive enhancement: content is visible by default; this only runs when
   Motion loaded and prefers-reduced-motion is not set. */
(function () {
  var M = window.Motion;
  var html = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Pill+arrow CTA hover/click is CSS-driven (see animations.css). We only
  // need to index each letter span so the per-letter stagger works. The
  // class .framer-m76ur6 marks every pill+arrow anchor across the site.
  document.querySelectorAll('a.framer-m76ur6 [class*="rolling-text-inner-"]').forEach(function (inner) {
    var spans = inner.children;
    for (var i = 0; i < spans.length; i++) spans[i].style.setProperty('--smag-i', i);
  });

  // Mobile drawer menu. Replaces Framer's runtime-driven mobile menu.
  // Hrefs use the same relative prefix as the existing navbar links on this
  // page (pages under blogs/, projects/, package/ need a "../" prefix), so
  // we probe an existing internal link instead of hard-coding paths.
  (function injectDrawer() {
    if (document.getElementById('smag-mm')) return;
    var probe = document.querySelector('a[href$="about-us.html"]');
    var prefix = probe ? (probe.getAttribute('href').match(/^((?:\.\.\/)*)/) || [''])[0] : '';
    var links = [
      ['index.html', 'Home'],
      ['about-us.html', 'About'],
      ['services.html', 'Services'],
      ['package.html', 'Packages'],
      ['blogs.html', 'Blogs'],
      ['contact.html', 'Contact'],
    ];
    var mm = document.createElement('div');
    mm.id = 'smag-mm';
    mm.setAttribute('role', 'dialog');
    mm.setAttribute('aria-modal', 'true');
    mm.setAttribute('aria-label', 'Menu');
    var close = document.createElement('button');
    close.id = 'smag-mm-close';
    close.setAttribute('aria-label', 'Close menu');
    close.innerHTML = '&times;';
    close.addEventListener('click', function () { mm.classList.remove('open'); });
    mm.appendChild(close);
    links.forEach(function (l) {
      var a = document.createElement('a');
      a.href = prefix + l[0];
      a.textContent = l[1];
      mm.appendChild(a);
    });
    document.body.appendChild(mm);

    document.querySelectorAll('[data-framer-name="Menu Button"]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        mm.classList.add('open');
      }, true);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mm.classList.contains('open')) mm.classList.remove('open');
    });
  })();

  // Marquee: always make the track visible; animate only when motion is allowed.
  document.querySelectorAll('[data-marquee]').forEach(function (track) {
    track.style.opacity = '1';
    track.style.transform = 'none';
    if (!M || reduce) return;
    var items = [].slice.call(track.children);
    if (!items.length) return;
    items.forEach(function (it) { track.appendChild(it.cloneNode(true)); });
    var half = track.scrollWidth / 2;
    if (half > 0) M.animate(track, { x: [0, -half] }, { duration: half / 80, ease: 'linear', repeat: Infinity });
  });

  // No motion library or reduced motion: reveal everything statically and stop.
  if (!M || reduce) { html.classList.remove('motion-ready'); return; }

  var spring = { type: 'spring', stiffness: 400, damping: 58, mass: 1 };

  function reveal(el) {
    if (el.__revealed) return;
    el.__revealed = true;
    var mode = el.getAttribute('data-reveal');
    var to = { opacity: [0, 1], y: [mode === 'nav' ? -20 : 10, 0] };
    if (mode === 'blur') to.filter = ['blur(10px)', 'blur(0px)'];
    M.animate(el, to, spring);
  }

  // Navbar reveals on load; the rest on scroll into view (one shared observer).
  var deferred = [];
  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    if (el.getAttribute('data-reveal') === 'nav') reveal(el);
    else deferred.push(el);
  });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -8% 0px' });
    deferred.forEach(function (el) { io.observe(el); });
  } else {
    deferred.forEach(reveal);
  }

  // Press feedback (parity with Framer's highlight/press states).
  if (M.press) {
    M.press('[data-highlight="true"], [data-framer-name="Menu Button"]', function (el) {
      M.animate(el, { scale: 0.94 }, { duration: 0.12 });
      return function () { M.animate(el, { scale: 1 }, { type: 'spring', stiffness: 500, damping: 30 }); };
    });
  }
})();
