// Mobile menu
const toggle = document.querySelector('.nav-toggle');
const nav = document.getElementById('site-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.textContent = 'Menu';
  }));
}

// Publication filter
const buttons = document.querySelectorAll('.filter');
const list = document.querySelector('.pubs');
const pubs = document.querySelectorAll('.pubs li');
const count = document.querySelector('.pub-count');
const more = document.querySelector('.pub-more');
const phone = window.matchMedia('(max-width: 760px)');

function applyFilter(topic) {
  let shown = 0;
  pubs.forEach(li => {
    const match = topic === 'all' || li.dataset.topic === topic;
    li.hidden = !match;
    if (match) shown++;
  });
  buttons.forEach(b => {
    const active = b.dataset.filter === topic;
    b.classList.toggle('is-active', active);
    b.setAttribute('aria-pressed', String(active));
  });

  // On phones, the full list starts collapsed to the six most recent papers.
  const collapse = topic === 'all' && phone.matches;
  if (list) list.classList.toggle('is-collapsed', collapse);
  if (more) more.hidden = !collapse;
  if (count) {
    count.textContent = collapse
      ? `Showing 6 of ${pubs.length} publications`
      : `Showing ${shown} of ${pubs.length} publications`;
  }
}

buttons.forEach(b => b.addEventListener('click', () => applyFilter(b.dataset.filter)));
if (more) {
  more.addEventListener('click', () => {
    list.classList.remove('is-collapsed');
    more.hidden = true;
    if (count) count.textContent = `Showing ${pubs.length} of ${pubs.length} publications`;
  });
}
phone.addEventListener('change', () => {
  const active = document.querySelector('.filter.is-active');
  applyFilter(active ? active.dataset.filter : 'all');
});
applyFilter('all');
