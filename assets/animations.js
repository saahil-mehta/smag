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

  // Framer baked scroll-reveal rest states (opacity:0, plus a translate
  // offset) into the exported HTML, expecting its runtime to animate them in.
  // That runtime was removed, so any reveal container we don't manage below
  // stays invisible (e.g. the CTA image bands, the "what sets us apart"
  // cards). Neutralise these orphaned rest states up front so all content is
  // visible by default; the managed reveals further down re-apply their own
  // clean start state when Motion is available. The Framer mobile menu keeps
  // its opacity:0 (it is a real hidden state, replaced by #smag-mm).
  document.querySelectorAll('[style*="opacity:0"], [style*="opacity: 0"]').forEach(function (el) {
    if (el.closest('nav[name="Navbar"], [data-framer-name="Nav menu"], #smag-mm')) return;
    el.style.opacity = '1';
    if (/translate|matrix/.test(el.style.transform)) el.style.transform = 'none';
  });

  // Pill+arrow CTA hover/click is CSS-driven (see animations.css). We only
  // need to index each letter span so the per-letter stagger works. The
  // class .framer-m76ur6 marks every pill+arrow anchor across the site.
  document.querySelectorAll('a.framer-m76ur6 [class*="rolling-text-inner-"]').forEach(function (inner) {
    var spans = inner.children;
    for (var i = 0; i < spans.length; i++) spans[i].style.setProperty('--smag-i', i);
  });

  function alignProductFamilyCards() {
    var section = document.getElementById('benifit-1');
    if (!section) return;
    ['framer-1faa9ry', 'framer-19cvw77', 'framer-3h7pth', 'framer-ib9i7h'].forEach(function (className) {
      section.querySelectorAll('.' + className).forEach(function (card) {
        card.style.setProperty('transform', 'none', 'important');
      });
    });
  }

  alignProductFamilyCards();
  requestAnimationFrame(alignProductFamilyCards);
  window.addEventListener('load', alignProductFamilyCards);
  setTimeout(alignProductFamilyCards, 500);

  // Mark the navbar / footer link matching the current page so Framer's
  // [data-framer-page-link-current] CSS rules apply. The partials strip
  // this attribute (it would otherwise be frozen to the page each partial
  // was extracted from), so we re-set it here per page.
  var here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  document.querySelectorAll('nav[name="Navbar"] a[href], .framer-plv1rs-container a[href]').forEach(function (a) {
    var basename = (a.getAttribute('href').split('/').pop() || '').toLowerCase();
    if (basename === here) a.setAttribute('data-framer-page-link-current', 'true');
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
      ['products.html', 'Products'],
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
  // Premium section reveal: slow ease-out-expo, larger offset. Used for
  // content blocks tagged by the section scanner below.
  var sectionEase = { duration: 0.9, ease: [0.16, 1, 0.3, 1] };

  function reveal(el) {
    if (el.__revealed) return;
    el.__revealed = true;
    var mode = el.getAttribute('data-reveal');
    if (mode === 'section') {
      M.animate(el, { opacity: [0, 1], y: [32, 0] }, sectionEase);
      return;
    }
    var to = { opacity: [0, 1], y: [mode === 'nav' ? -20 : 10, 0] };
    if (mode === 'blur') to.filter = ['blur(10px)', 'blur(0px)'];
    M.animate(el, to, spring);
  }

  // Tag Framer content containers for premium scroll-in. Skip anything
  // already revealed (per-letter blur, navbars), the navbar itself, the
  // footer, and the marquee track. The hero stays at rest (already on
  // screen at load); below-the-fold blocks animate as the user scrolls.
  var sectionSelectors = [
    '[data-framer-name="Heading+subtitle+button"]',
    '[data-framer-name="Heading+subtitle+Button"]',
    '[data-framer-name="Heading+button"]',
    '[data-framer-name="Heading+Button"]',
    '[data-framer-name="Heading+subtitle"]',
    '[data-framer-name="Subtitle+button"]',
    '[data-framer-name="Tag+heading+Button"]',
    '[data-framer-name="Tag+heading+button"]',
    '[data-framer-name="Tag+heading"]',
    '[data-framer-name="Heading + Text"]',
    '[data-framer-name="Variant 1"]',
  ];
  var sectionSelectorList = sectionSelectors.join(',');
  document.querySelectorAll(sectionSelectorList).forEach(function (el) {
    if (el.hasAttribute('data-reveal')) return;
    if (el.closest('nav[name="Navbar"], .framer-plv1rs-container, [data-marquee]')) return;
    // Skip the hero: it already animates its subtitle letter-by-letter
    // via the existing "blur" reveal, and a section-level slide on top
    // would fight that. Detect by descendant data-reveal.
    if (el.querySelector('[data-reveal]')) return;
    // Don't double-animate nested content blocks (e.g. a Heading+Text
    // inside a card that's already a Variant 1).
    if (el.parentElement && el.parentElement.closest(sectionSelectorList)) return;
    el.setAttribute('data-reveal', 'section');
    // Framer sets inline opacity:1 on these blocks which beats the
    // .motion-ready [data-reveal] CSS rule. Force the rest state inline
    // so Motion has a clean starting point.
    el.style.opacity = '0';
    el.style.transform = 'translateY(32px)';
  });

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
