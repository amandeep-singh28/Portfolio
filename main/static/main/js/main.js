// ─── LOADER ───
const loader = document.getElementById('loader');
window.addEventListener('load', () => {
  setTimeout(() => loader && loader.classList.add('hidden'), 1200);
});

// ─── NAV ───
const nav = document.getElementById('nav');
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 40);
  highlightNav();
  updateProgress();
  updateBackToTop();
  handleParallax();
});

navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
navLinks.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', e => {
    navLinks.classList.remove('open');
  });
});

const navIndicator = document.getElementById('navIndicator');

function highlightNav() {
  const sections = document.querySelectorAll('section[id], header[id]');
  const links = navLinks.querySelectorAll('a');
  let currentActive = null;

  sections.forEach(s => {
    const top = s.offsetTop - 100;
    if (window.scrollY >= top) {
      links.forEach(a => {
        a.classList.remove('active');
        if (a.getAttribute('href') === '#' + s.id) {
          a.classList.add('active');
          currentActive = a;
        }
      });
    }
  });

  if (navIndicator && currentActive) {
    navIndicator.style.width = `${currentActive.offsetWidth}px`;
    navIndicator.style.left = `${currentActive.offsetLeft}px`;
    navIndicator.style.opacity = '1';
  } else if (navIndicator) {
    navIndicator.style.opacity = '0';
  }
}

// ─── HERO PARALLAX ───
const heroBg = document.querySelector('.hero-bg');
const heroGrid = document.querySelector('.hero-grid');
const orbs = document.querySelectorAll('.orb');
const heroCanvas = document.getElementById('particles');

function handleParallax() {
  const scrolled = window.scrollY;
  if (scrolled > window.innerHeight) return;

  if (heroBg) heroBg.style.transform = `translateY(${scrolled * 0.4}px)`;
  if (heroGrid) heroGrid.style.transform = `translateY(${scrolled * 0.2}px)`;
  if (heroCanvas) heroCanvas.style.transform = `translateY(${scrolled * 0.3}px)`;
  orbs.forEach((orb, i) => {
    orb.style.transform = `translateY(${scrolled * (0.15 * (i + 1))}px)`;
  });
}


// ─── SCROLL PROGRESS BAR ───
const progressBar = document.getElementById('progressBar');
function updateProgress() {
  if (!progressBar) return;
  const total = document.documentElement.scrollHeight - window.innerHeight;
  const pct = (window.scrollY / total) * 100;
  progressBar.style.width = pct + '%';
}

// ─── BACK TO TOP ───
const backToTop = document.getElementById('backToTop');
function updateBackToTop() {
  if (!backToTop) return;
  backToTop.classList.toggle('visible', window.scrollY > 300);
}
backToTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// ─── CUSTOM CURSOR ───
const cursor = document.getElementById('cursor');
const cursorRing = document.getElementById('cursorRing');

if (cursor && cursorRing && window.matchMedia('(pointer: fine)').matches) {
  let ringX = 0, ringY = 0, mouseX = 0, mouseY = 0;

  document.addEventListener('mousemove', e => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    cursor.style.left = mouseX + 'px';
    cursor.style.top = mouseY + 'px';
  });

  function animateRing() {
    ringX += (mouseX - ringX) * 0.12;
    ringY += (mouseY - ringY) * 0.12;
    cursorRing.style.left = ringX + 'px';
    cursorRing.style.top = ringY + 'px';
    requestAnimationFrame(animateRing);
  }
  animateRing();

  document.addEventListener('mousedown', () => {
    cursor.classList.add('clicking');
    cursorRing.classList.add('clicking');
  });
  document.addEventListener('mouseup', () => {
    cursor.classList.remove('clicking');
    cursorRing.classList.remove('clicking');
  });
}

// ─── PARTICLES CANVAS ───
const canvas = document.getElementById('particles');
if (canvas) {
  const ctx = canvas.getContext('2d');
  let W, H, stars = [];

  function resize() {
    const hero = canvas.parentElement;
    W = canvas.width = hero.offsetWidth;
    H = canvas.height = hero.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  const STAR_COUNT = 90;
  for (let i = 0; i < STAR_COUNT; i++) {
    stars.push({
      x: Math.random() * (window.innerWidth || 1200),
      y: Math.random() * (window.innerHeight || 700),
      r: Math.random() * 1.5 + 0.3,
      vx: (Math.random() - 0.5) * 0.25,
      vy: (Math.random() - 0.5) * 0.25,
      alpha: Math.random() * 0.6 + 0.2
    });
  }

  function drawParticles() {
    ctx.clearRect(0, 0, W, H);
    stars.forEach(s => {
      s.x += s.vx; s.y += s.vy;
      if (s.x < 0) s.x = W;
      if (s.x > W) s.x = 0;
      if (s.y < 0) s.y = H;
      if (s.y > H) s.y = 0;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0, 200, 255, ${s.alpha})`;
      ctx.fill();
    });
    // Draw connecting lines between nearby stars
    for (let i = 0; i < stars.length; i++) {
      for (let j = i + 1; j < stars.length; j++) {
        const dx = stars[i].x - stars[j].x;
        const dy = stars[i].y - stars[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 110) {
          ctx.beginPath();
          ctx.moveTo(stars[i].x, stars[i].y);
          ctx.lineTo(stars[j].x, stars[j].y);
          ctx.strokeStyle = `rgba(0, 200, 255, ${0.08 * (1 - dist / 110)})`;
          ctx.lineWidth = 0.6;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(drawParticles);
  }
  drawParticles();
}

// ─── TYPING EFFECT ───
const roles = [
  'Aspiring Data Scientist',
  'Machine Learning Enthusiast',
  'Python Developer',
  'Data Analysis & Visualization',
  'Power BI Developer',
  'CSE Student @ LPU'
];
let ri = 0, ci = 0, deleting = false;
const roleEl = document.getElementById('heroRole');

function type() {
  if (!roleEl) return;
  const current = roles[ri];
  const cursor2 = '<span class="cursor"></span>';
  if (!deleting) {
    ci++;
    roleEl.innerHTML = current.slice(0, ci) + cursor2;
    if (ci === current.length) { deleting = true; setTimeout(type, 2000); return; }
    setTimeout(type, 65);
  } else {
    ci--;
    roleEl.innerHTML = current.slice(0, ci) + cursor2;
    if (ci === 0) { deleting = false; ri = (ri + 1) % roles.length; }
    setTimeout(type, 35);
  }
}
setTimeout(type, 1400);

// ─── ANIMATED STAT COUNTERS ───
function animateCounter(el) {
  const raw = el.textContent.trim();
  const suffix = raw.replace(/[\d.]/g, '');
  const target = parseFloat(raw);
  if (isNaN(target)) return;
  const duration = 3200;
  const start = performance.now();
  function step(now) {
    const t = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    const val = target * ease;
    el.textContent = (Number.isInteger(target) ? Math.floor(val) : val.toFixed(2)) + suffix;
    if (t < 1) requestAnimationFrame(step);
    else el.textContent = raw;
  }
  requestAnimationFrame(step);
}

const statsObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('.stat-num').forEach(animateCounter);
      statsObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll('.hero-stats').forEach(s => statsObserver.observe(s));

// ─── SCROLL REVEAL ───
const reveals = document.querySelectorAll('.reveal');
const ro = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 80);
    }
  });
}, { threshold: 0.08 });
reveals.forEach(r => ro.observe(r));

// ─── CAROUSELS ───
document.querySelectorAll('.carousel').forEach(carousel => {
  const slides = carousel.querySelectorAll('.carousel-slide');
  const dots = carousel.querySelectorAll('.carousel-dot');
  const prev = carousel.querySelector('.carousel-prev');
  const next = carousel.querySelector('.carousel-next');
  let current = 0, timer = null;

  if (slides.length <= 1) return;

  function goTo(index) {
    slides[current].classList.remove('active');
    dots[current]?.classList.remove('active');
    current = (index + slides.length) % slides.length;
    slides[current].classList.add('active');
    dots[current]?.classList.add('active');
  }

  function startAuto() { timer = setInterval(() => goTo(current + 1), 3500); }
  function resetAuto() { clearInterval(timer); startAuto(); }

  dots.forEach((d, i) => d.addEventListener('click', () => { goTo(i); resetAuto(); }));
  prev?.addEventListener('click', () => { goTo(current - 1); resetAuto(); });
  next?.addEventListener('click', () => { goTo(current + 1); resetAuto(); });

  startAuto();
});

// ─── 3D CARD TILT ───
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = (e.clientX - cx) / (rect.width / 2);
    const dy = (e.clientY - cy) / (rect.height / 2);
    card.style.transform = `translateY(-8px) rotateX(${-dy * 6}deg) rotateY(${dx * 6}deg)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
  });
});

// ─── CONTACT FORM (🔥 FIXED) ───
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const form = document.getElementById('contactForm');
const formStatus = document.getElementById('formStatus');

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = form.querySelector('button[type=submit]');
    const orig = btn.textContent;
    btn.textContent = 'Sending...';
    btn.disabled = true;

    try {
      const csrftoken = getCookie('csrftoken');
      const res = await fetch('/contact/', {
        method: 'POST',
        body: new FormData(form),
        headers: {
          'X-CSRFToken': csrftoken
        }
      });

      const json = await res.json();

      if (json.status === 'success') {
        formStatus.textContent = '✅ Message sent! I\'ll get back to you soon.';
        formStatus.className = 'form-status success';
        form.reset();
      } else {
        // 🔥 SHOW REAL ERROR
        formStatus.textContent = `❌ ${json.message}`;
        formStatus.className = 'form-status error';
      }

    } catch (err) {
      // 🔥 NETWORK ERROR
      formStatus.textContent = `❌ Network error: ${err.message}`;
      formStatus.className = 'form-status error';
    } finally {
      btn.textContent = orig;
      btn.disabled = false;
    }
  });
}

// ─── SMOOTH ANCHOR SCROLL ───
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

// ─── LIGHTBOX MODAL ───
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const lightboxClose = document.querySelector('.lightbox-close');

if (lightbox && lightboxImg && lightboxClose) {
  document.querySelectorAll('.carousel-slide img').forEach(img => {
    img.addEventListener('click', () => {
      lightbox.classList.add('show');
      lightboxImg.src = img.src;
      document.body.style.overflow = 'hidden';
    });
  });

  const closeLightbox = () => {
    lightbox.classList.remove('show');
    setTimeout(() => { lightboxImg.src = ''; }, 300);
    document.body.style.overflow = '';
  };

  lightboxClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', e => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && lightbox.classList.contains('show')) closeLightbox();
  });
}

// ─── MAGNETIC BUTTONS ───
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('mouseenter', () => {
    btn.style.transition = 'transform 0.15s ease';
  });
  btn.addEventListener('mousemove', e => {
    const rect = btn.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = (e.clientX - cx) * 0.28;
    const dy = (e.clientY - cy) * 0.28;
    btn.style.transform = `translate(${dx}px, ${dy}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transition = 'transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
    btn.style.transform = 'translate(0, 0)';
  });
});

// ─── TEXT SCRAMBLE (SECTION TITLES) ───
const SCRAMBLE_CHARS = 'アイウエオカキクケコABCDEFGHIJKLMNOP0123456789@#$%&*';

function scramble(el) {
  const original = el.getAttribute('data-original') || el.textContent.trim();
  el.setAttribute('data-original', original);
  el.classList.add('scrambling');

  let frame = 0;
  const totalFrames = 28;
  const revealAt = (i) => Math.floor((i / original.length) * (totalFrames * 0.7));

  const interval = setInterval(() => {
    el.textContent = original.split('').map((char, i) => {
      if (char === ' ') return ' ';
      if (frame >= revealAt(i)) return char;
      return SCRAMBLE_CHARS[Math.floor(Math.random() * SCRAMBLE_CHARS.length)];
    }).join('');

    if (frame >= totalFrames) {
      el.textContent = original;
      el.classList.remove('scrambling');
      el.classList.add('unscrambled');
      clearInterval(interval);
    }
    frame++;
  }, 45);
}

const scrambleObserver = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      scramble(e.target);
      scrambleObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.section-title').forEach(el => scrambleObserver.observe(el));