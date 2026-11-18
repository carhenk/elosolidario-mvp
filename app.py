from datetime import timedelta, date
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elosolidario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ItemEstoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_item = db.Column(db.String(100), nullable=False)
    quantidade_atual = db.Column(db.Integer, default=0)
    quantidade_minima = db.Column(db.Integer, default=5)
    data_validade = db.Column(db.Date, nullable=True)

    @property
    def estoque_critico(self):
        return self.quantidade_atual <= self.quantidade_minima

    @property
    def validade_proxima(self):
        return self.data_validade and (self.data_validade - date.today()).days <= 7

class Familia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    bloqueada_30d = db.Column(db.Boolean, default=False)

CSS = """
body{font-family:system-ui,sans-serif;background:#f4f6f9;color:#222;margin:0}
nav{background:#198754;color:#fff;padding:14px 24px;display:flex;
justify-content:space-between;align-items:center}
.btn{padding:6px 12px;border:0;border-radius:6px;font-weight:700;cursor:pointer}
.btn-y{background:#ffc107;color:#000}.btn-w{background:#fff;color:#198754}
.wrap{max-width:1050px;margin:20px auto;padding:0 16px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:20px}
.grid2{display:grid;grid-template-columns:1.4fr 1fr;gap:16px}
.card{background:#fff;border-radius:10px;padding:16px;box-shadow:0 2px 6px #0001}
.num{font-size:2rem;font-weight:800;margin:4px 0 0}
table{width:100%;border-collapse:collapse;margin-top:10px}
th,td{padding:10px;border-bottom:1px solid #eee;text-align:left}
.bg{padding:4px 8px;border-radius:12px;font-size:.8rem;font-weight:700;color:#fff}
.r{background:#dc3545}.y{background:#ffc107;color:#000}.g{background:#198754}.s{background:#6c757d}
body.hc{background:#000;color:#FFD700}
body.hc .card{background:#111;color:#FFD700;border:2px solid #FFD700}
body.hc th,body.hc td{border-color:#444}
body.lg{font-size:1.22rem}
"""

HTML = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>EloSolidário — Gestão Comunitária (ODS 2)</title>
<style>""" + CSS + """</style></head><body>
<nav><strong>🤝 EloSolidário | ODS 2 — Fome Zero</strong>
<div><button class="btn btn-y" onclick="document.body.classList.toggle('hc')">
🌓 Alto Contraste</button>
<button class="btn btn-w" onclick="document.body.classList.toggle('lg')">
🔠 A+ Fonte</button></div></nav>
<div class="wrap"><div class="grid3">
<div class="card"><small>Famílias Atendidas</small>
<p class="num" style="color:#198754">{{ familias|length }}</p></div>
<div class="card"><small>Itens em Estoque Crítico</small>
<p class="num" style="color:#dc3545">{{ urgentes|length }}</p></div>
<div class="card"><small>Cestas Entregues (Mês)</small>
<p class="num" style="color:#0d6efd">14</p></div></div>
<div class="grid2"><div class="card">
<strong>📦 Controle de Estoque (Operador: Ana - Coord.)</strong>
<table><tr><th>Alimento</th><th>Saldo</th><th>Validade</th><th>Status</th></tr>
{% for i in itens %}<tr><td>{{ i.nome_item }}</td><td>{{ i.quantidade_atual }} un.</td>
<td>{{ i.data_validade.strftime('%d/%m/%Y') if i.data_validade else '—' }}</td><td>
{% if i.estoque_critico %}<span class="bg r">Estoque Crítico</span>
{% elif i.validade_proxima %}<span class="bg y">Vence em breve</span>
{% else %}<span class="bg g">Normal</span>{% endif %}</td></tr>{% endfor %}
</table></div><div><div class="card" style="margin-bottom:16px;border-left:5px solid #ffc107">
<strong>📢 Lista de Urgências (WhatsApp)</strong><ul>{% for u in urgentes %}
<li><b>{{ u.nome_item }}</b> (restam {{ u.quantidade_atual }} un.)</li>{% endfor %}
</ul></div><div class="card"><strong>👨‍👩‍👧‍👦 Famílias e Trava 30 Dias</strong><ul>
{% for f in familias %}<li>{{ f.nome }} ({{ f.bairro }}) —
{% if f.bloqueada_30d %}<span class="bg s">Bloqueio 30d</span>
{% else %}<span class="bg g">Liberada</span>{% endif %}</li>{% endfor %}
</ul></div></div></div></div></body></html>"""

@app.route('/')
def index():
    itens = ItemEstoque.query.all()
    urgentes = [i for i in itens if i.estoque_critico]
    familias = Familia.query.all()
    return render_template_string(HTML, itens=itens, urgentes=urgentes, familias=familias)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=False)

with app.app_context():
    db.create_all()
    if ItemEstoque.query.count() == 0:
        db.session.add_all([
            ItemEstoque(nome_item="Arroz Tipo 1 (5kg)", quantidade_atual=3, quantidade_minima=8, data_validade=date.today()+timedelta(days=90)),
            ItemEstoque(nome_item="Feijão Carioca (1kg)", quantidade_atual=4, quantidade_minima=10, data_validade=date.today()+timedelta(days=60)),
            ItemEstoque(nome_item="Leite Integral (1L)", quantidade_atual=18, quantidade_minima=6, data_validade=date.today()+timedelta(days=4)),
            ItemEstoque(nome_item="Óleo de Soja (900ml)", quantidade_atual=22, quantidade_minima=8, data_validade=date.today()+timedelta(days=120)),
            Familia(nome="Maria Oliveira Santos", bairro="Jardim Esperança", bloqueada_30d=True),
            Familia(nome="José Carlos Pereira", bairro="Vila Nova", bloqueada_30d=False)
        ])
        db.session.commit()
