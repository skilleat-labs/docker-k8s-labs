from flask import Flask, jsonify, request, render_template_string
import sqlite3
import os
import socket

app = Flask(__name__)
DB_PATH = '/tmp/cafe.db'


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        emoji TEXT NOT NULL,
        category TEXT NOT NULL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total INTEGER NOT NULL,
        created_at DATETIME DEFAULT (datetime('now', 'localtime'))
    )''')
    if conn.execute('SELECT COUNT(*) FROM products').fetchone()[0] == 0:
        conn.executemany('INSERT INTO products VALUES (?,?,?,?,?)', [
            (1, '아메리카노',  4500, '☕', '음료'),
            (2, '카페라떼',   5500, '🥛', '음료'),
            (3, '바닐라라떼', 5800, '🍦', '음료'),
            (4, '치즈케이크', 6500, '🍰', '디저트'),
            (5, '크로와상',   3500, '🥐', '베이커리'),
            (6, '머핀',       3000, '🧁', '베이커리'),
        ])
    conn.commit()
    conn.close()


HTML = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mono Cafe</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --primary:#6366f1;--primary-dark:#4f46e5;--primary-light:#e0e7ff;
  --bg:#f1f5f9;--card:#fff;--text:#1e293b;--muted:#94a3b8;
  --border:#e2e8f0;--green:#10b981;--amber:#f59e0b;--navy:#1e1b4b;
}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}

/* Navbar */
.navbar{background:var(--navy);color:#fff;padding:0 2rem;height:64px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;box-shadow:0 2px 12px rgba(0,0,0,.25)}
.brand{font-size:1.25rem;font-weight:800;display:flex;align-items:center;gap:.6rem;letter-spacing:-.01em}
.brand-badge{background:var(--amber);color:#1e293b;font-size:.6rem;padding:3px 9px;border-radius:999px;font-weight:800;text-transform:uppercase;letter-spacing:.06em}
.server-chip{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);border-radius:999px;padding:5px 14px;font-size:.8rem;color:#a5b4fc;display:flex;align-items:center;gap:.5rem}
.dot{width:7px;height:7px;background:var(--green);border-radius:50%;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}

/* Layout */
.page{max-width:1240px;margin:0 auto;padding:1.75rem 2rem}
.layout{display:grid;grid-template-columns:1fr 320px;gap:1.5rem;align-items:start}

/* Section label */
.label{font-size:.7rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.875rem}

/* Product grid */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.card{background:var(--card);border-radius:14px;padding:1.25rem;border:1.5px solid var(--border);cursor:pointer;transition:transform .15s,box-shadow .15s,border-color .15s}
.card:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(99,102,241,.13);border-color:#a5b4fc}
.card:active{transform:translateY(0)}
.emoji{font-size:2.75rem;display:block;margin-bottom:.75rem}
.cat{font-size:.65rem;font-weight:700;color:var(--primary);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.2rem}
.name{font-size:.975rem;font-weight:700;margin-bottom:.375rem}
.price{font-size:1.05rem;font-weight:800;color:var(--primary);margin-bottom:.875rem}
.btn{width:100%;background:var(--primary);color:#fff;border:none;border-radius:8px;padding:.5rem;font-size:.85rem;font-weight:700;cursor:pointer;transition:background .15s}
.btn:hover{background:var(--primary-dark)}

/* Orders panel */
.panel{background:var(--card);border-radius:14px;border:1.5px solid var(--border);overflow:hidden;position:sticky;top:80px}
.panel-head{padding:1rem 1.25rem;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
.panel-head h3{font-size:.9rem;font-weight:700}
.count{background:var(--primary);color:#fff;border-radius:999px;padding:2px 9px;font-size:.72rem;font-weight:700}
.orders{max-height:420px;overflow-y:auto}
.order{padding:.875rem 1.25rem;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;animation:in .25s ease}
@keyframes in{from{opacity:0;transform:translateX(8px)}to{opacity:1;transform:none}}
.order:last-child{border-bottom:none}
.oname{font-size:.85rem;font-weight:600}
.otime{font-size:.72rem;color:var(--muted);margin-top:2px}
.oprice{font-size:.9rem;font-weight:800;color:var(--primary)}
.empty{padding:2.5rem;text-align:center;color:var(--muted);font-size:.85rem}

/* Arch panel */
.arch{background:#fffbeb;border:1.5px solid #fcd34d;border-radius:14px;padding:1.5rem;margin-top:1.5rem}
.arch-title{font-weight:800;font-size:.95rem;color:#92400e;display:flex;align-items:center;gap:.5rem;margin-bottom:1.1rem}
.arch-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.875rem;margin-bottom:1rem}
.aitem{background:#fff;border:1px solid #fde68a;border-radius:10px;padding:.75rem 1rem}
.alabel{font-size:.65rem;font-weight:700;color:#b45309;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.3rem}
.aval{font-size:.85rem;font-weight:700;font-family:monospace;word-break:break-all}
.modules{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center;margin-bottom:.75rem}
.modules-label{font-size:.72rem;font-weight:700;color:#b45309;margin-right:.2rem}
.tag{background:#ede9fe;color:#5b21b6;border-radius:6px;padding:3px 10px;font-size:.72rem;font-weight:700}
.arch-warn{font-size:.8rem;color:#b45309;display:flex;align-items:flex-start;gap:.4rem;line-height:1.5}

/* Toast */
.toast{position:fixed;bottom:1.5rem;right:1.5rem;background:var(--navy);color:#fff;padding:.75rem 1.25rem;border-radius:10px;font-size:.85rem;font-weight:500;opacity:0;transform:translateY(8px);transition:all .25s;z-index:999;pointer-events:none}
.toast.on{opacity:1;transform:none}
</style>
</head>
<body>

<nav class="navbar">
  <div class="brand">
    ☕ Mono Cafe
    <span class="brand-badge">Monolith</span>
  </div>
  <div class="server-chip">
    <span class="dot"></span>
    <span id="nav-host">연결 중...</span>
    &nbsp;·&nbsp;
    <span id="nav-pid">PID –</span>
  </div>
</nav>

<div class="page">
  <div class="layout">

    <div>
      <div class="label">☕ 메뉴판</div>
      <div class="grid" id="products">
        <div style="grid-column:1/-1;padding:2rem;text-align:center;color:var(--muted)">로딩 중…</div>
      </div>
    </div>

    <div>
      <div class="label">📋 주문 내역</div>
      <div class="panel">
        <div class="panel-head">
          <h3>오늘의 주문</h3>
          <span class="count" id="ocount">0</span>
        </div>
        <div class="orders" id="olist">
          <div class="empty">아직 주문이 없습니다</div>
        </div>
      </div>
    </div>

  </div>

  <!-- Architecture Info Panel -->
  <div class="arch">
    <div class="arch-title">⚠️ 모놀리식 아키텍처 정보</div>
    <div class="arch-grid">
      <div class="aitem">
        <div class="alabel">Container Hostname</div>
        <div class="aval" id="a-host">–</div>
      </div>
      <div class="aitem">
        <div class="alabel">Process (PID)</div>
        <div class="aval" id="a-pid">–</div>
      </div>
      <div class="aitem">
        <div class="alabel">Database</div>
        <div class="aval">SQLite<br><span style="font-size:.7rem;color:#b45309">(컨테이너 내장)</span></div>
      </div>
      <div class="aitem">
        <div class="alabel">서빙 포트</div>
        <div class="aval">5000</div>
      </div>
    </div>
    <div class="modules">
      <span class="modules-label">이 프로세스 안에서 실행 중 →</span>
      <span class="tag">🛍️ 상품 모듈</span>
      <span class="tag">📦 주문 모듈</span>
      <span class="tag">🌐 웹 서버</span>
      <span class="tag">💾 SQLite DB</span>
    </div>
    <div class="arch-warn">
      ⚡ 위 모든 기능이 컨테이너 <strong id="a-host2">–</strong> 의 PID <strong id="a-pid2">–</strong> 단일 프로세스에서 실행됩니다.
      하나에 문제가 생기면 전체 서비스가 중단됩니다.
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const $=id=>document.getElementById(id);
const toast=msg=>{const t=$('toast');t.textContent=msg;t.classList.add('on');setTimeout(()=>t.classList.remove('on'),2500)};

async function loadStatus(){
  const d=await fetch('/api/status').then(r=>r.json());
  $('nav-host').textContent=d.hostname;
  $('nav-pid').textContent='PID '+d.pid;
  $('a-host').textContent=d.hostname;
  $('a-pid').textContent=d.pid;
  $('a-host2').textContent=d.hostname;
  $('a-pid2').textContent=d.pid;
}

async function loadProducts(){
  const ps=await fetch('/api/products').then(r=>r.json());
  $('products').innerHTML=ps.map(p=>`
    <div class="card" onclick="placeOrder(${p.id},'${p.name}',${p.price})">
      <span class="emoji">${p.emoji}</span>
      <div class="cat">${p.category}</div>
      <div class="name">${p.name}</div>
      <div class="price">${p.price.toLocaleString()}원</div>
      <button class="btn">주문하기</button>
    </div>`).join('');
}

async function loadOrders(){
  const os=await fetch('/api/orders').then(r=>r.json());
  $('ocount').textContent=os.length;
  if(!os.length){$('olist').innerHTML='<div class="empty">아직 주문이 없습니다</div>';return;}
  $('olist').innerHTML=os.map(o=>`
    <div class="order">
      <div>
        <div class="oname">${o.product_name} × ${o.quantity}</div>
        <div class="otime">${o.created_at}</div>
      </div>
      <div class="oprice">${o.total.toLocaleString()}원</div>
    </div>`).join('');
}

async function placeOrder(id,name,price){
  await fetch('/api/orders',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({product_id:id,product_name:name,quantity:1,total:price})});
  toast('✅ '+name+' 주문 완료!');
  loadOrders();
}

loadStatus();loadProducts();loadOrders();
setInterval(loadOrders,5000);
</script>
</body>
</html>'''


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/api/products')
def get_products():
    conn = get_db()
    rows = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/orders', methods=['GET'])
def get_orders():
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM orders ORDER BY id DESC LIMIT 30'
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    conn = get_db()
    conn.execute(
        'INSERT INTO orders (product_name, quantity, total) VALUES (?,?,?)',
        (data['product_name'], data['quantity'], data['total'])
    )
    conn.commit()
    conn.close()
    return jsonify({'ok': True})


@app.route('/api/status')
def status():
    return jsonify({
        'hostname': socket.gethostname(),
        'pid': os.getpid(),
    })


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
