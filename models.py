from config import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

# Modelo Cliente
class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    identidade = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    profissao = db.Column(db.String(50), nullable=False)
    escolaridade = db.Column(db.String(50), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    # Relacionamento com Emprestimos
    emprestimos = relationship('Emprestimo', back_populates='cliente')

class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    data_publicacao = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)

    # Relacionamento com Emprestimos
    emprestimos = relationship('Emprestimo', back_populates='livros')


    def __repr__(self):
        return f'<Livro {self.titulo}>'


# Modelo Emprestimo
class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, ForeignKey('cliente.id'), nullable=False)
    livro_id = db.Column(db.Integer, ForeignKey('livros.id'), nullable=False)
    data_emprestimo = db.Column(db.Date, nullable=False)

    # Relacionamento com Cliente e Livro
    cliente = db.relationship('Cliente', back_populates='emprestimos')
    livros = db.relationship('Livro', back_populates='emprestimos')

    def __repr__(self):
        return f'<Emprestimo {self.id} - Cliente: {self.cliente.nome_completo}, Livro: {self.livro.titulo}>'
