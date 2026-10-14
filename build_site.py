# -*- coding: utf-8 -*-
"""Build docs/index.html: embed effects.json, render each effect live in an iframe with copy buttons."""
import json, pathlib

root = pathlib.Path(__file__).parent
data = json.loads((root / "effects.json").read_text(encoding="utf-8"))
docs = root / "docs"
docs.mkdir(exist_ok=True)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pure CSS Effects - 纯 CSS 特效库</title>
<meta name="description" content="纯 CSS 实现的按钮、加载动画、卡片悬停、文字特效、背景装饰，实时预览，一键复制代码">
<style>
  :root {
    --bg: #f7f6fb; --card: #ffffff; --text: #1f2328; --muted: #656d76;
    --accent: #db2777; --accent-soft: #fce8f3; --border: #e8e4ee; --radius: 16px;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
         background: var(--bg); color: var(--text); line-height: 1.6; }
  .wrap { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
  header.hero { text-align: center; padding: 60px 20px 36px; }
  header.hero h1 { font-size: 2.3rem; }
  header.hero p.sub { color: var(--muted); margin-top: 12px; font-size: 1.05rem; }
  .stats { margin-top: 16px; display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
  .stat { background: var(--card); border: 1px solid var(--border); border-radius: 999px;
          padding: 6px 18px; font-size: 0.88rem; color: var(--muted); }
  .stat b { color: var(--accent); }
  .toolbar { position: sticky; top: 0; z-index: 10; background: rgba(247,246,251,0.92);
             backdrop-filter: blur(8px); padding: 14px 0 12px; border-bottom: 1px solid var(--border); }
  .chips { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
  .chip { padding: 6px 16px; border-radius: 999px; border: 1px solid var(--border);
          background: var(--card); cursor: pointer; font-size: 0.88rem; color: var(--muted);
          transition: all .15s; user-select: none; }
  .chip:hover { border-color: var(--accent); color: var(--accent); }
  .chip.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  main { padding: 28px 0 60px; }
  .cat-title { display: flex; align-items: baseline; gap: 10px; margin: 28px 0 14px; }
  .cat-title h2 { font-size: 1.2rem; }
  .cat-title span { color: var(--muted); font-size: 0.85rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 18px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
          overflow: hidden; transition: transform .15s, box-shadow .15s; }
  .card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(31,35,40,0.09); }
  .stage { height: 190px; background: repeating-conic-gradient(#fafafa 0 25%, #f0f0f3 0 50%) 0 0/24px 24px; }
  .stage iframe { width: 100%; height: 100%; border: none; }
  .info { padding: 14px 18px 16px; display: flex; align-items: center; justify-content: space-between; gap: 10px; }
  .info h3 { font-size: 0.98rem; }
  .info p { color: var(--muted); font-size: 0.8rem; margin-top: 2px; }
  .copy { flex-shrink: 0; padding: 8px 14px; border-radius: 8px; border: 1px solid var(--border);
          background: var(--card); color: var(--accent); font-size: 0.8rem; cursor: pointer;
          transition: all .15s; }
  .copy:hover { border-color: var(--accent); }
  dialog { border: none; border-radius: 18px; max-width: 760px; width: calc(100% - 40px); padding: 0;
           box-shadow: 0 20px 60px rgba(0,0,0,0.25); }
  dialog::backdrop { background: rgba(31,35,40,0.45); }
  .modal-body { padding: 24px 28px 28px; }
  .modal-body h3 { margin-bottom: 14px; }
  .modal-body h4 { margin: 14px 0 6px; font-size: 0.9rem; color: var(--muted); }
  pre { background: #1f2328; color: #e6edf3; border-radius: 10px; padding: 14px 18px;
        overflow-x: auto; font-size: 0.82rem; line-height: 1.6; max-height: 30vh; overflow-y: auto; }
  .modal-actions { display: flex; gap: 10px; margin-top: 16px; }
  .btn { flex: 1; padding: 11px; border-radius: 10px; border: 1px solid var(--border);
         background: var(--card); cursor: pointer; font-size: 0.92rem; }
  .btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
  footer { text-align: center; padding: 36px 20px 48px; color: var(--muted); font-size: 0.88rem; }
  footer a { color: var(--accent); text-decoration: none; }
  .toast { position: fixed; left: 50%; bottom: 32px; transform: translateX(-50%);
           background: #1f2328; color: #fff; padding: 10px 22px; border-radius: 999px;
           font-size: 0.9rem; opacity: 0; transition: opacity .25s; pointer-events: none; z-index: 99; }
  .toast.show { opacity: 1; }
</style>
</head>
<body>
<header class="hero">
  <h1>✨ Pure CSS Effects</h1>
  <p class="sub">纯 CSS 特效库 · 实时预览 · 一键复制代码 · 零依赖</p>
  <div class="stats">
    <div class="stat"><b id="statEffects">0</b> 个特效</div>
    <div class="stat">0 JavaScript 依赖*</div>
    <div class="stat">MIT · 随意商用</div>
  </div>
</header>

<div class="toolbar">
  <div class="wrap"><div class="chips" id="chips"></div></div>
</div>

<main class="wrap" id="main"></main>

<dialog id="modal">
  <div class="modal-body">
    <h3 id="mTitle"></h3>
    <h4>HTML</h4><pre id="mHtml"></pre>
    <h4>CSS</h4><pre id="mCss"></pre>
    <div class="modal-actions">
      <button class="btn primary" id="copyAll">📋 复制全部代码</button>
      <button class="btn" id="closeBtn">关闭</button>
    </div>
  </div>
</dialog>

<div class="toast" id="toast">已复制到剪贴板 ✅</div>

<footer>
  <p>用 ❤️ 维护 · <a href="https://github.com/AnonymousLeeJJ/pure-css-effects" target="_blank" rel="noopener">GitHub 仓库</a> · 欢迎 Star ⭐ 与投稿<br>
  <span style="font-size:0.78rem">* 个别效果（如聚光灯跟随）需要几行可选的 JS，已在代码中注明</span></p>
</footer>

<script id="effects-data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('effects-data').textContent);
const { categories, effects } = DATA;
const state = { cat: 'all' };
document.getElementById('statEffects').textContent = effects.length;

const chipsEl = document.getElementById('chips');
const mainEl = document.getElementById('main');
const modal = document.getElementById('modal');
const toast = document.getElementById('toast');
let current = null;

function srcdoc(e) {
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    body{margin:0;display:flex;align-items:center;justify-content:center;min-height:100vh;background:transparent}
    </style></head><body>${e.html.replace(/<\\/script>/g, '<\\/script>')}<style>${e.css}</style></body></html>`;
}

function renderChips() {
  const all = [{ id: 'all', name: '全部', icon: '✨' }, ...categories];
  chipsEl.innerHTML = all.map(c =>
    `<span class="chip ${state.cat === c.id ? 'active' : ''}" data-id="${c.id}">${c.icon} ${c.name}</span>`).join('');
  chipsEl.querySelectorAll('.chip').forEach(el =>
    el.addEventListener('click', () => { state.cat = el.dataset.id; renderChips(); renderList(); }));
}

function renderList() {
  const groups = categories
    .map(c => ({ cat: c, items: effects.map((e, i) => ({...e, idx: i})).filter(e => e.category === c.id) }))
    .filter(g => state.cat === 'all' || g.cat.id === state.cat);
  mainEl.innerHTML = groups.map(g => `
    <div class="cat-title"><h2>${g.cat.icon} ${g.cat.name}</h2><span>${g.items.length} 个</span></div>
    <div class="grid">${g.items.map(e => `
      <div class="card">
        <div class="stage"><iframe loading="lazy" srcdoc="${srcdoc(e).replace(/&/g,'&amp;').replace(/"/g,'&quot;')}"></iframe></div>
        <div class="info">
          <div><h3>${e.name}</h3><p>${e.description}</p></div>
          <button class="copy" data-idx="${e.idx}">📋 复制代码</button>
        </div>
      </div>`).join('')}
    </div>`).join('');
  mainEl.querySelectorAll('.copy').forEach(el =>
    el.addEventListener('click', () => openModal(+el.dataset.idx)));
}

function openModal(idx) {
  current = effects[idx];
  document.getElementById('mTitle').textContent = current.name + ' · ' + current.description;
  document.getElementById('mHtml').textContent = current.html;
  document.getElementById('mCss').textContent = current.css;
  modal.showModal();
}

function copyText(t) {
  if (navigator.clipboard) navigator.clipboard.writeText(t).catch(() => {});
  else { const ta = document.createElement('textarea'); ta.value = t;
    document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); }
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 1500);
}

document.getElementById('copyAll').addEventListener('click', () =>
  copyText('<!-- HTML -->\\n' + current.html + '\\n\\n<!-- CSS -->\\n<style>\\n' + current.css + '\\n</style>'));
document.getElementById('closeBtn').addEventListener('click', () => modal.close());
modal.addEventListener('click', e => { if (e.target === modal) modal.close(); });

renderChips();
renderList();
</script>
</body>
</html>
"""

html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))
(docs / "index.html").write_text(html, encoding="utf-8")
print("OK ->", docs / "index.html", f"({len(data['effects'])} effects)")
