from datetime import datetime, timedelta, date
from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-dev-elosolidario')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///elosolidario.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default='voluntario')
    ativo = db.Column(db.Boolean, default=True)

class ItemEstoque(db.Model):
    __tablename__ = 'itens_estoque'
    id = db.Column(db.Integer, primary_key=True)
    nome_item = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    quantidade_atual = db.Column(db.Integer, nullable=False, default=0)
    quantidade_minima = db.Column(db.Integer, nullable=False, default=5)
    data_validade = db.Column(db.Date, nullable=True)

    @property
    def estoque_critico(self):
        return self.quantidade_atual <= self.quantidade_minima

    @property
    def validade_proxima(self):
        if not self.data_validade:
            return False
        return (self.data_validade - date.today()).days <= 7

class Familia(db.Model):
    __tablename__ = 'familias'
    id = db.Column(db.Integer, primary_key=True)
    nome_responsavel = db.Column(db.String(120), nullable=False)
    documento_cpf = db.Column(db.String(14), unique=True, nullable=False)
    bairro_endereco = db.Column(db.String(150), nullable=False)
    qtd_dependentes = db.Column(db.Integer, nullable=False, default=1)

class Entrega(db.Model):
    __tablename__ = 'entregas'
    id = db.Column(db.Integer, primary_key=True)
    familia_id = db.Column(db.Integer, db.ForeignKey('familias.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_entrega = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    itens_resumo = db.Column(db.Text, nullable=False)

def pode_receber_cesta(familia_id):
    limite = datetime.utcnow() - timedelta(days=30)
    ultima = Entrega.query.filter(
        Entrega.familia_id == familia_id,
        Entrega.data_entrega >= limite
    ).first()
    return ultima is None

@app.route('/')
def index():
    itens = ItemEstoque.query.all()
    urgentes = [i for i in itens if i.estoque_critico]
    return {"status": "online", "projeto": "EloSolidario", "itens_urgentes": len(urgentes)}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
