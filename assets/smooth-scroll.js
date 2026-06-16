/* Subtle smooth scrolling via Lenis (assets/vendor/lenis.min.js).
   Eases native wheel scrolling so the page glides and settles instead of
   jumping, which is what the stripped Framer runtime used to provide.
   Touch devices keep their native momentum (Lenis does not smooth touch by
   default). Disabled entirely under prefers-reduced-motion. Progressive
   enhancement: if Lenis failed to load, scrolling stays fully native. */
(function () {
  if (!window.Lenis) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var lenis = new Lenis({
    lerp: 0.1,            // easing factor: lower glides longer, higher snaps
    wheelMultiplier: 0.9, // trim wheel distance a touch so it is not too fast
    smoothWheel: true
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);
})();
