/* Elektro Paul Neumann – site interactions (no dependencies) */
(() => {
  document.documentElement.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* mobile menu */
  const btn = $('.menu-btn'), menu = $('#mobile-menu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      menu.hidden = !open;
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }

  /* services mega menu: click toggles on touch, Escape closes */
  $$('.has-mega').forEach((m) => {
    const link = $('.nav-link', m);
    link.addEventListener('click', (ev) => {
      if (matchMedia('(hover: none)').matches && !m.classList.contains('open')) { ev.preventDefault(); m.classList.add('open'); }
    });
    document.addEventListener('click', (ev) => { if (!m.contains(ev.target)) m.classList.remove('open'); });
    m.addEventListener('keydown', (ev) => { if (ev.key === 'Escape') { m.classList.remove('open'); link.focus(); m.blur(); } });
  });

  /* reveal on scroll */
  const io = 'IntersectionObserver' in window && !reduce ? new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }) : null;
  $$('.reveal').forEach((el, i) => {
    if (!io) { el.classList.add('in'); return; }
    el.style.transitionDelay = `${(i % 4) * 70}ms`;
    io.observe(el);
  });

  /* background videos: play only while visible */
  const vids = $$('video[data-autoplay]');
  if (vids.length && 'IntersectionObserver' in window && !reduce) {
    const vio = new IntersectionObserver((entries) => entries.forEach((en) => {
      const v = en.target;
      if (en.isIntersecting) { v.play().catch(() => {}); } else { v.pause(); }
    }), { threshold: 0.25 });
    vids.forEach((v) => vio.observe(v));
  }

  /* project rail arrows */
  const rail = $('.rail');
  $$('[data-rail]').forEach((b) => b.addEventListener('click', () => {
    rail.scrollBy({ left: Number(b.dataset.rail) * rail.clientWidth * 0.8, behavior: reduce ? 'auto' : 'smooth' });
  }));

  /* project filter */
  $$('.filter').forEach((f) => f.addEventListener('click', () => {
    $$('.filter').forEach((x) => x.classList.toggle('is-on', x === f));
    $$('.pcard').forEach((c) => c.classList.toggle('is-hidden', f.dataset.filter !== 'all' && c.dataset.cat !== f.dataset.filter));
  }));

  /* YouTube: load only after consent (privacy-enhanced mode) */
  const loadYT = (box, autoplay) => {
    const id = box.dataset.yt;
    box.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${id}?rel=0${autoplay ? '&autoplay=1' : ''}" title="YouTube video" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
  };
  let ytOk = false;
  try { ytOk = sessionStorage.getItem('yt-consent') === '1'; } catch (e) { /* storage blocked */ }
  $$('.yt').forEach((box) => {
    if (ytOk) { loadYT(box, false); return; }
    $('.yt-btn', box).addEventListener('click', () => {
      try { sessionStorage.setItem('yt-consent', '1'); } catch (e) { /* ignore */ }
      $$('.yt').forEach((b) => loadYT(b, b === box));
    });
  });

  /* lightbox */
  const lb = $('.lightbox');
  if (lb) {
    const im = $('img', lb), cap = $('figcaption', lb);
    let group = [], idx = 0, lastFocus = null;
    const show = (i) => {
      idx = (i + group.length) % group.length;
      const a = group[idx];
      im.src = a.getAttribute('href');
      im.alt = $('img', a)?.alt || '';
      cap.textContent = `${a.dataset.caption || ''}${group.length > 1 ? `  ·  ${idx + 1} / ${group.length}` : ''}`;
      const multi = group.length > 1;
      $('.lb-prev', lb).hidden = !multi; $('.lb-next', lb).hidden = !multi;
      // preload neighbour
      if (multi) { const n = new Image(); n.src = group[(idx + 1) % group.length].getAttribute('href'); }
    };
    const open = (a) => {
      group = $$(`[data-lightbox="${a.dataset.lightbox}"]`);
      lastFocus = document.activeElement;
      lb.hidden = false; document.body.style.overflow = 'hidden';
      show(group.indexOf(a)); $('.lb-close', lb).focus();
    };
    const close = () => { lb.hidden = true; im.src = ''; document.body.style.overflow = ''; lastFocus?.focus(); };
    document.addEventListener('click', (ev) => {
      const a = ev.target.closest('[data-lightbox]');
      if (a) { ev.preventDefault(); open(a); }
    });
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', () => show(idx - 1));
    $('.lb-next', lb).addEventListener('click', () => show(idx + 1));
    lb.addEventListener('click', (ev) => { if (ev.target === lb) close(); });
    document.addEventListener('keydown', (ev) => {
      if (lb.hidden) return;
      if (ev.key === 'Escape') close();
      if (ev.key === 'ArrowLeft') show(idx - 1);
      if (ev.key === 'ArrowRight') show(idx + 1);
      if (ev.key === 'Tab') { ev.preventDefault(); $('.lb-close', lb).focus(); }
    });
    let x0 = null;
    lb.addEventListener('touchstart', (ev) => { x0 = ev.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (ev) => {
      if (x0 === null) return;
      const dx = ev.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }
})();
