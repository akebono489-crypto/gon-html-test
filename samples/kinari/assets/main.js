const body = document.body;
const header = document.querySelector('.site-header');
const nav = document.querySelector('[data-nav]');
const toggle = document.querySelector('[data-menu-toggle]');
const toast = document.getElementById('toast');

if (header) {
  function setHeader() {
    header.classList.toggle('is-scrolled', window.scrollY > 20);
  }
  window.addEventListener('scroll', setHeader, { passive: true });
  setHeader();
}

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.classList.toggle('is-active', open);
    toggle.setAttribute('aria-expanded', String(open));
    body.classList.toggle('menu-open', open);
  });

  nav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      nav.classList.remove('is-open');
      toggle.classList.remove('is-active');
      toggle.setAttribute('aria-expanded', 'false');
      body.classList.remove('menu-open');
    });
  });
}

document.querySelectorAll('[data-demo-reserve]').forEach(btn => {
  btn.addEventListener('click', () => {
    if (!toast) return;
    toast.classList.add('is-visible');
    setTimeout(() => toast.classList.remove('is-visible'), 2800);
  });
});
