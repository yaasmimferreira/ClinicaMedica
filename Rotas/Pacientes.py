from flask import Blueprint, render_template, session, redirect, g, request, send_file
import sqlite3

bp = Blueprint('Pacientes', __name__)

def ligar_banco():
    banco = g._database = sqlite3.connect('ClinicaMedica.db')
    cursor = banco.cursor()
    cursor.execute("PRAGMA foreign_keys  = ON;")
    return banco

#---------------- PÁGINA CADASTRO DE PACIENTES ----------------
@bp.route('/cadastroPaciente')
def cad_Pac():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        return render_template('CadPaciente.html', Titulo='Cadastro de Paciente')


#----------------ROTA INTERMEDIÁRIA (CRIAR PACIENTES) ----------------
@bp.route('/criarPaciente', methods=['POST', 'GET'])
def criar_Pac():
    banco = ligar_banco()
    cursor = banco.cursor()
    try:
        nome = request.form['nomeComp']
        dataNas = request.form['datanas']
        genero = request.form['genero']
        rg = request.form['rg']
        endereco = request.form['endereco']
        email = request.form['email']
        telefone = request.form['telefone']
        cursor.execute('INSERT INTO Pacientes (Nome,DataNas,Genero,RG,Endereco,Email,Telefone) '
                       'VALUES (?,?,?,?,?,?,?);',
                       (nome, dataNas, genero, rg, endereco, email, telefone))
        banco.commit()
    except:
        banco.rollback()
    return redirect('/')


#---------------- PÁGINA EXIBIR PACIENTES GERAL ----------------
@bp.route('/exibirPaciente')
def exibir_Pac():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM Pacientes;')
        pacientes = cursor.fetchall()
        return render_template('ListaPacientesC.html', Titulo='Exibir Paciente', ListaPac=pacientes)


#---------------- Editar Pacientes  ----------------
@bp.route('/alterarPAC', methods=['PUT', 'POST'])
def alterar():
    # Coleta as informações do formulário
    banco = ligar_banco()
    cursor = banco.cursor()

    nome = request.form['nomeComp']
    datanas = request.form['datanas']
    genero = request.form['genero']
    rg = request.form['rg']
    endereco = request.form['endereco']
    email = request.form['email']
    telefone = request.form['telefone']
    ID_Pac = request.form['idpac']

    cursor.execute('UPDATE Pacientes SET Nome=?,DataNas=?,Genero=?,'
                   'RG=?,Endereco=?,Email=?,Telefone=? WHERE ID_Pac=?;',
                       (nome,datanas,genero,rg,endereco,email,telefone,ID_Pac))
    banco.commit()


    return redirect('/exibirPaciente')



@bp.route('/excluirPacientes/<ID_Pac>', methods=['GET','DELETE'])
def deletar(ID_Pac):
        banco = ligar_banco()
        cursor = banco.cursor()#execulta comando
        try:
            cursor.execute('DELETE FROM Pacientes WHERE ID_Pac =?;', (ID_Pac,))
            banco.commit()#atualizar as intormaçoes, salvar
        except:
            banco.rollback()#deleta comandos que nao funcionarem
        return redirect(f'/exibirPaciente')


@bp.route('/editar/<ID_Pac>', methods=['GET'])
def editar(ID_Pac):
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM Pacientes WHERE ID_Pac =?',(ID_Pac,))
        encontrado = cursor.fetchone()#somente uma tupla
        return render_template('EditarPac.html', paciente=encontrado,
                                   Titulo="Editar Pacientes")
