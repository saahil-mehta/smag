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

  // Framer also bakes a `transform: scale(<1)` appear rest state on some
  // component containers, meant to grow to scale(1) on load. Without the runtime
  // these freeze shrunk (e.g. the services cards rendered at half size). Reset
  // the baked scale so they render full size. Runs once at load, before any
  // interaction, so it only clears static rest states (press/tilt set their own
  // transforms later and are unaffected).
  document.querySelectorAll('[style*="transform:scale"], [style*="transform: scale"]').forEach(function (el) {
    if (el.closest('nav[name="Navbar"], [data-framer-name="Nav menu"], #smag-mm, [data-marquee]')) return;
    el.style.transform = 'none';
  });

  // Hero photo fade-in: the hero area is tinted with the photo's average colour
  // (animations.css), and the photo fades in over it instead of flashing white
  // then popping. Only hide-then-fade photos that have not loaded yet; cached
  // ones stay visible. Skipped under reduced motion (instant, tint then photo).
  if (!reduce) {
    ['.framer-176qp25 img', '.framer-5fqrd0 img', '.framer-1v7v30q img'].forEach(function (sel) {
      var img = document.querySelector(sel);
      if (!img || (img.complete && img.naturalWidth > 0)) return;
      img.classList.add('smag-imgfade');
      var show = function () { img.classList.add('smag-imgfade-in'); };
      img.addEventListener('load', show, { once: true });
      img.addEventListener('error', show, { once: true });
    });
  }

  // Service-card icons: inject a line-art icon per service. They morph and
  // recolour on card hover and play a confirm (check + ring) on click, all
  // CSS-driven (see animations.css). Works on the home and services pages
  // (both use #services .framer-12rgd66). Matched to each card by its title.
  var SVC_ICONS = {
    magnet: '<svg class="smag-ic" viewBox="0 0 24 24"><path d="M6 20v-8a6 6 0 0 1 12 0v8"/><path d="M4 20h4M16 20h4"/><path class="smag-ic-draw" d="M8 21.4q4 2.4 8 0"/></svg>',
    layers: '<svg class="smag-ic" viewBox="0 0 24 24"><path class="smag-lyr-top" d="M12 3l8.5 4.7-8.5 4.7L3.5 7.7 12 3z"/><path d="M3.5 12.2l8.5 4.7 8.5-4.7"/><path d="M3.5 16.7l8.5 4.7 8.5-4.7"/></svg>',
    gauge: '<svg class="smag-ic" viewBox="0 0 24 24"><path d="M5 18a7 7 0 1 1 14 0"/><path class="smag-needle" d="M12 18l4.4-4.2"/><circle cx="12" cy="18" r="1.45" fill="currentColor" stroke="none"/></svg>',
    gear: '<svg class="smag-ic" viewBox="0 0 24 24"><g class="smag-gear"><circle cx="12" cy="12" r="6.4"/><circle cx="12" cy="12" r="2.5"/><path d="M12 5.6V2.6M12 18.4v2.8M18.4 12h2.8M5.6 12H2.8M16.5 7.5l2.2-2.2M7.5 16.5l-2.2 2.2M16.5 16.5l2.2 2.2M7.5 7.5L5.3 5.3"/></g></svg>',
    check: '<svg class="smag-ic" viewBox="0 0 24 24"><path d="M12 3l7 2.5v5.6c0 4.2-3 7.4-7 8.6-4-1.2-7-4.4-7-8.6V5.5L12 3z"/><path class="smag-ic-redraw" d="M8.5 12l2.5 2.5L15.6 9.4"/></svg>',
    truck: '<svg class="smag-ic" viewBox="0 0 24 24"><g class="smag-truck"><path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h3.8l3.2 3.2v2.8h-7z"/></g><circle cx="6.6" cy="17.4" r="1.6"/><circle cx="16.6" cy="17.4" r="1.6"/></svg>'
  };
  var SVC_CONFIRM = '<svg class="smag-ic-confirm" viewBox="0 0 24 24" aria-hidden="true"><path class="smag-confirm-check" d="M5 12.5l4.5 4.5L19 7"/></svg>';
  var SVC_MAP = [
    { re: /custom|magnet design/i, k: 'magnet' },
    { re: /standard|product range/i, k: 'layers' },
    { re: /duty|match|select/i, k: 'gauge' },
    { re: /in.?house|manufactur/i, k: 'gear' },
    { re: /test|quality/i, k: 'check' },
    { re: /supply|after.?sales|deliver/i, k: 'truck' }
  ];
  document.querySelectorAll('#services .framer-12rgd66').forEach(function (card) {
    if (card.querySelector('.smag-svc-icon')) return;
    var wrap = card.querySelector('.framer-ljkzq1') || card;
    var titleEl = card.querySelector('h1,h2,h3,h4,h5,h6');
    var title = ((titleEl && titleEl.textContent) || '').trim();
    var match = SVC_MAP.filter(function (m) { return m.re.test(title); })[0];
    var key = match ? match.k : 'layers';
    var span = document.createElement('span');
    span.className = 'smag-svc-icon';
    span.setAttribute('data-svc-icon', key);
    span.setAttribute('role', 'img');
    span.setAttribute('aria-label', title || 'Service');
    span.innerHTML = SVC_ICONS[key] + SVC_CONFIRM;
    wrap.insertBefore(span, wrap.firstChild);
    span.addEventListener('click', function (e) {
      e.stopPropagation();
      span.classList.remove('smag-confirm');
      void span.offsetWidth;            // restart the animation
      span.classList.add('smag-confirm');
      setTimeout(function () { span.classList.remove('smag-confirm'); }, 850);
    });
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

  // Sticky navbar: give it a background + lift once the page is scrolled so it
  // stays readable over content, and keep it above everything (z-index).
  (function () {
    var bar = document.querySelector('[data-framer-name="Navbar"]');
    if (!bar) return;
    var onScroll = function () {
      bar.classList.toggle('smag-nav-scrolled', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  })();

  // Product-family cards: each individual card links to its catalogue section,
  // reacts to the cursor with a 3D tilt, and shows a "View products" affordance.
  (function () {
    var sec = document.getElementById('benifit-1');
    if (!sec) return;
    var map = {
      'Magnetic Separators': 'separators',
      'Magnetic Lifters': 'lifters',
      'Magnetic Chucks': 'chucks',
      'Grills and Filters': 'grills'
    };
    var probe = document.querySelector('a[href$="products.html"]');
    var prefix = probe ? (probe.getAttribute('href').match(/^((?:\.\.\/)*)/) || [''])[0] : '';
    [].forEach.call(sec.querySelectorAll('.framer-1faa9ry, .framer-19cvw77, .framer-3h7pth, .framer-ib9i7h'), function (card) {
      var titleEl = card.querySelector('h3, h4, h5');
      var title = titleEl ? titleEl.textContent.trim() : '';
      var anchor = map[title];
      if (!anchor) return;
      var href = prefix + 'products.html#' + anchor;
      card.classList.add('smag-tilt');
      card.style.cursor = 'pointer';
      card.setAttribute('role', 'link');
      card.setAttribute('tabindex', '0');
      card.setAttribute('aria-label', title + ' products');
      card.style.setProperty('transform', 'none', 'important');

      var cta = document.createElement('span');
      cta.className = 'smag-fam-cta';
      cta.innerHTML = 'View products <span aria-hidden="true">&rarr;</span>';
      card.appendChild(cta);

      var go = function () { location.href = href; };
      card.addEventListener('click', go);
      card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
      });
      if (!reduce) {
        card.addEventListener('mousemove', function (e) {
          var r = card.getBoundingClientRect();
          var rx = ((e.clientY - r.top) / r.height - 0.5) * -10;
          var ry = ((e.clientX - r.left) / r.width - 0.5) * 10;
          card.style.setProperty('transform', 'perspective(760px) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg) scale(1.03)', 'important');
        });
        card.addEventListener('mouseleave', function () {
          card.style.setProperty('transform', 'none', 'important');
        });
      }
    });

    // Prominent CTA to the full catalogue below the family cards.
    if (!sec.querySelector('.smag-fam-bottomcta')) {
      var bcta = document.createElement('a');
      bcta.className = 'smag-fam-bottomcta';
      bcta.href = prefix + 'products.html';
      bcta.innerHTML = 'View the full product catalogue <span aria-hidden="true">&rarr;</span>';
      sec.appendChild(bcta);
    }
  })();

  // Contact info cards render each value twice (legacy two-slot layout); show
  // each detail once by hiding exact-duplicate links within a card.
  document.querySelectorAll('[data-framer-name="Icon Image"]').forEach(function (icon) {
    var card = icon.parentElement;
    while (card && card.querySelectorAll('a').length < 2) card = card.parentElement;
    if (!card) return;
    var seen = {};
    card.querySelectorAll('a').forEach(function (a) {
      var t = (a.textContent || '').trim().toLowerCase();
      if (!t) return;
      if (seen[t]) a.style.display = 'none'; else seen[t] = 1;
    });
  });

  // Marquee: always make the track visible; animate only when motion is allowed.
  document.querySelectorAll('[data-marquee]').forEach(function (track) {
    track.style.opacity = '1';
    track.style.transform = 'none';
    if (!M || reduce) return;
    var items = [].slice.call(track.children);
    if (!items.length) return;
    items.forEach(function (it) { track.appendChild(it.cloneNode(true)); });
    var half = track.scrollWidth / 2;
    if (half > 0) M.animate(track, { x: [0, -half] }, { duration: half / 40, ease: 'linear', repeat: Infinity });
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

  // The navbar is persistent chrome: mark it revealed so it stays visible
  // without re-running an entrance animation on every navigation. The rest
  // reveal on scroll into view (one shared observer).
  var deferred = [];
  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    if (el.getAttribute('data-reveal') === 'nav') el.__revealed = true;
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
