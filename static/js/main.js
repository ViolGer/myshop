// ===== utils =====
const getParams = () => new URLSearchParams(location.search);
const fromCSV = s => (s ? s.split(',').map(x=>x.trim()).filter(Boolean) : []);
const toCSV = xs => Array.from(xs).filter(Boolean).join(',');
const goTo = p => {
  ['q','categories','sort','page'].forEach(k => { if (p.get(k)==='' || p.get(k)==null) p.delete(k); });
  const qs = p.toString();
  location.assign(qs ? `${location.pathname}?${qs}` : location.pathname);
};
const setActiveSort = sort => {
  const c = document.querySelector('.sort-options'); if (!c) return;
  c.querySelectorAll('.sort-button').forEach(b => {
    const on = (b.dataset.sort||'') === (sort||'');
    b.classList.toggle('active-sort', on);
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
};

// ===== products list page =====
function initProductsListPage() {
  const root = document.querySelector('.main-content-grid');
  if (!root) return;

  const params       = getParams();
  const q            = params.get('q') || '';
  const sort         = params.get('sort') || '';
  const catsSet      = new Set(fromCSV(params.get('categories')));

  const searchForm   = document.getElementById('product-search-form');
  const searchInput  = document.querySelector('.search-input');
  const sortBar      = document.querySelector('.sort-options');
  const filterBtn    = document.getElementById('filter-button');
  const keywordsList = document.querySelector('.keywords-list');
  const checkboxes   = document.querySelectorAll('.checkbox-group input[type="checkbox"]');

  // fill UI from URL
  if (searchInput) searchInput.value = q;
  setActiveSort(sort);
  checkboxes.forEach(cb => {
    const kw = cb.dataset.keyword;
    cb.checked = catsSet.has(kw);
    if (cb.checked && keywordsList && !keywordsList.querySelector(`[data-keyword="${kw}"]`)) {
      const tag = document.createElement('span');
      tag.className = 'keyword-tag';
      tag.dataset.keyword = kw;
      tag.innerHTML = `${kw} <i class="fa-solid fa-xmark remove-keyword-icon" aria-label="Remove"></i>`;
      keywordsList.appendChild(tag);
    }
  });

  // search submit (preserve filters)
  if (searchForm) {
    searchForm.addEventListener('submit', e => {
      e.preventDefault();
      const p = getParams();
      p.set('q', (searchInput && searchInput.value) || '');
      p.delete('page');
      goTo(p);
    });
  }

  // sort click
  if (sortBar) {
    sortBar.addEventListener('click', e => {
      const btn = e.target.closest('.sort-button'); if (!btn) return;
      const p = getParams();
      p.set('sort', btn.dataset.sort || '');
      p.delete('page');
      goTo(p);
    });
  }

  // checkbox <-> tag sync (UI)
  if (keywordsList && checkboxes.length) {
    const ensureTag = kw => {
      if (!keywordsList.querySelector(`[data-keyword="${kw}"]`)) {
        const tag = document.createElement('span');
        tag.className = 'keyword-tag';
        tag.dataset.keyword = kw;
        tag.innerHTML = `${kw} <i class="fa-solid fa-xmark remove-keyword-icon" aria-label="Remove"></i>`;
        keywordsList.appendChild(tag);
      }
    };
    const removeTag = kw => keywordsList.querySelector(`[data-keyword="${kw}"]`)?.remove();

    checkboxes.forEach(cb => cb.addEventListener('change', function () {
      this.checked ? ensureTag(this.dataset.keyword) : removeTag(this.dataset.keyword);
    }));

    keywordsList.addEventListener('click', e => {
      const icon = e.target.closest('.remove-keyword-icon'); if (!icon) return;
      const tag = icon.closest('.keyword-tag'); const kw = tag?.dataset.keyword; if (!kw) return;
      document.querySelector(`.checkbox-container input[data-keyword="${kw}"]`)?.click();
    });
  }

  // apply filters
  if (filterBtn) {
    filterBtn.addEventListener('click', () => {
      const selected = new Set();
      checkboxes.forEach(cb => cb.checked && selected.add(cb.dataset.keyword));
      const p = getParams();
      const csv = toCSV(selected);
      csv ? p.set('categories', csv) : p.delete('categories');
      p.delete('page');
      goTo(p);
    });
  }

  console.log('[products] init ok');
}

// ===== safe boot =====
(function bootSafe(){
  const boot = () => initProductsListPage();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
