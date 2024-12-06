from flask import Flask, render_template, request, session, flash, redirect,g
import sqlite3
from Rotas import Consultas, Pacientes,Medicos

app = Flask(__name__)
app.secret_key = 'Senai'

app.register_blueprint(Consultas.bp)
app.register_blueprint(Pacientes.bp)
app.register_blueprint(Medicos.bp)

def ligar_banco():
    banco = g._database = sqlite3.connect('ClinicaMedica.db')
    cursor = banco.cursor()
    cursor.execute("PRAGMA foreign_keys  = ON;")
    return banco



# ----------------HOME----------------
@app.route('/')
def home():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        return render_template('Home.html', Titulo='Home')


#---------------- PÁGINA DE LOGIN ----------------
@app.route('/login')
def login():
    return render_template('Login.html', Titulo='Login')


#----------------ROTA INTERMEDIÁRIA (AUTENTICAR) ----------------
@app.route('/autenticar', methods=['POST'])
def autenticar():
    banco = ligar_banco()
    cursor = banco.cursor()
    usuario = request.form['usuario'] #Seleciona o usuário inserido pela pessoa
    cursor.execute('SELECT * FROM Usuarios WHERE Nome = ?', (usuario,))
    dados = cursor.fetchone()
    senha = request.form['senha']
    if senha == dados[2]:
        session['Usuario_Logado'] = usuario
        flash('Usuario logado com sucesso!')
        return redirect('/')

    else:
        flash('Usuario não encontrado. Tente novamente!')
        return redirect('/login')


#---------------- DESLOGAR ----------------
@app.route('/deslogar')
def deslogar():
    session.clear()
    return redirect('/login')


#---------------- PÁGINA DE GESTÃO ----------------
@app.route('/gestao')
def gestao_Pac():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        return render_template('Gestao.html', Titulo='Gestão QuaityCare')


#---------------- ROTA PAGINAÇÃO ----------------
@app.route('/listaMedicos/<int:pagina>')
def listaMedicos(pagina):
    por_pagina = 6  # Número de médicos por página
    banco = ligar_banco()  # Conecta ao banco de dados
    cursor = banco.cursor()
    offset = (pagina - 1) * por_pagina
    cursor.execute('SELECT * FROM Medicos LIMIT ? OFFSET ?', (por_pagina, offset))
    ListaMedicos = cursor.fetchall()

    # Calcula o número total de médicos
    cursor.execute('SELECT COUNT(*) FROM Medicos')
    total_medicos = cursor.fetchone()[0]
    total_paginas = (total_medicos + por_pagina - 1)

    # Passa as informações para o template
    return render_template('ListaMedicos.html',
                           Titulo='Lista de Médicos',
                           total_paginas=total_paginas,
                           ListaMedicos=ListaMedicos,pagina=pagina)


#---------------- PÁGINA DE CADASTRO MÉDICO ----------------
@app.route('/cadastroMedico')
def cad_Medico():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        return render_template('CadMedico.html', Titulo='Cadastro de Médico')


#---------------- PÁGINA LISTAR CONSULTA ----------------
@app.route('/listaConsultas/<int:pagina>')
def listaConsultas(pagina):
    por_pagina = 6  # Número de médicos por página
    banco = ligar_banco()  # Conecta ao banco de dados
    cursor = banco.cursor()
    offset = (pagina - 1) * por_pagina
    cursor.execute('SELECT * FROM Consultas LIMIT ? OFFSET ?', (por_pagina, offset))
    ListaConsultas = cursor.fetchall()

    # Calcula o número total de consultas
    cursor.execute('SELECT COUNT(*) FROM Consultas')
    total_consultas = cursor.fetchone()[0]
    total_paginas = (total_consultas + por_pagina - 1)

    # Calcula o número total de consultas
    cursor.execute('SELECT ID_Med,Nome FROM Medicos')
    total_medicos = cursor.fetchall()

    cursor.execute('SELECT ID_Pac,Nome,Genero FROM Pacientes')
    total_pacientes = cursor.fetchall()
    # Passa as informações para o template
    return render_template('ListaConsultas.html',
                           Titulo='Lista de Consultas',
                           total_paginas=total_paginas,
                           ListaConsultas=ListaConsultas,pagina=pagina,
                           medicos=total_medicos,pacientes=total_pacientes)


#---------------- PÁGINA CADASTRAR CONSULTA ----------------
@app.route('/consulta')
def Consulta():
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('SELECT ID_Med, Nome FROM Medicos;')
        Nome_Meds = cursor.fetchall()
        cursor.execute('SELECT ID_Pac, Nome FROM Pacientes;')
        Nome_Pacs = cursor.fetchall()
        print(Nome_Pacs)

        return render_template('CadConsulta.html', Titulo='Cadastro de Consulta', listaMedicos=Nome_Meds,
                               listaPacientes=Nome_Pacs)


if __name__ == '__main__':
    app.run()
