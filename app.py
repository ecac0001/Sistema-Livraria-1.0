from flask import render_template, redirect, url_for, request, session, flash
from config import app, db
from models import Cliente, Livro
from datetime import datetime

# Simulação de dados de login (usuário e senha)
USERS = {
    'admin': '123'  # Substitua por uma senha real
}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        data_nascimento = request.form['data_nascimento']
        identidade = request.form['identidade']
        cidade = request.form['cidade']
        profissao = request.form['profissao']
        escolaridade = request.form['escolaridade']

        novo_cliente = Cliente(
            nome_completo=nome_completo, 
            data_nascimento=data_nascimento, 
            identidade=identidade, 
            cidade=cidade, 
            profissao=profissao, 
            escolaridade=escolaridade
        )

        try:
            db.session.add(novo_cliente)
            db.session.commit()
            flash('Cliente cadastrado com sucesso!')
            return redirect(url_for('clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar cliente: {str(e)}')
            return redirect(url_for('clientes'))

    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

# Rota para editar um cliente
@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        cliente.nome_completo = request.form['nome_completo']
        cliente.data_nascimento = request.form['data_nascimento']
        cliente.identidade = request.form['identidade']
        cliente.cidade = request.form['cidade']
        cliente.profissao = request.form['profissao']
        cliente.escolaridade = request.form['escolaridade']
        # Atualize a data de cadastro, se necessário
        cliente.data_cadastro = datetime.now().date()

        try:
            db.session.commit()
            flash('Cliente atualizado com sucesso!')
            return redirect(url_for('clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar cliente: {str(e)}')
            return redirect(url_for('clientes'))

    return render_template('editar_cliente.html', cliente=cliente)


# Rota para excluir um cliente
@app.route('/deletar_cliente/<int:id>', methods=['POST'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente excluído com sucesso!')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir cliente: {str(e)}')
    return redirect(url_for('clientes'))

@app.route('/livros', methods=['GET', 'POST'])
def livros():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        data_publicacao = request.form['data_publicacao']
        genero = request.form['genero']
        isbn = request.form['isbn']

        novo_livro = Livro(
            titulo=titulo,
            autor=autor,
            data_publicacao=datetime.strptime(data_publicacao, '%Y-%m-%d').date(),  # Converte string para data
            genero=genero,
            isbn=isbn
        )

        try:
            db.session.add(novo_livro)
            db.session.commit()
            flash('Livro cadastrado com sucesso!')
            return redirect(url_for('livros'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar livro: {str(e)}')
            return redirect(url_for('livros'))

    livros = Livro.query.all()
    return render_template('livros.html', livros=livros)

@app.route('/editar_livro/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    livro = Livro.query.get_or_404(id)
    
    if request.method == 'POST':
        print(request.form)
        # Atualiza os atributos do livro
        livro.titulo = request.form['titulo']
        livro.autor = request.form['autor']
        livro.genero = request.form['genero']
        livro.isbn = request.form['isbn']

        try:
            livro.data_publicacao = datetime.strptime(request.form['data_publicacao'], '%Y-%m-%d').date()
            db.session.commit()  # Tenta salvar as alterações
            flash('Livro atualizado com sucesso!')
            return redirect(url_for('livros'))  # Redireciona para a lista de livros
        except Exception as e:
            db.session.rollback()  # Reverte as alterações em caso de erro
            flash(f'Erro ao atualizar livro: {str(e)}')
            print(f'Erro ao atualizar: {e}') 

    return render_template('editar_livro.html', livro=livro)  # Retorna o template de edição

@app.route('/deletar_livro/<int:id>', methods=['POST'])
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)  # Obtém o livro pelo ID ou retorna 404 se não encontrado
    try:
        db.session.delete(livro)  # Remove o livro da sessão
        db.session.commit()  # Confirma as mudanças
        flash('Livro excluído com sucesso!')
    except Exception as e:
        db.session.rollback()  # Reverte as alterações em caso de erro
        flash(f'Erro ao excluir livro: {str(e)}')

    return redirect(url_for('livros'))  # Redireciona para a lista de livros


@app.route('/configuracao')
def configuracao():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('configuracao.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
