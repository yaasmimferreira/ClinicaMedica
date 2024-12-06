from flask import Blueprint, session,redirect,render_template, g, request,send_file
import sqlite3
import io
from datetime import datetime

bp = Blueprint('Medicos', __name__) ##arquivo que esta aberto, criando um objeto bp


def ligar_banco():
    banco = g._database = sqlite3.connect('ClinicaMedica.db')
    cursor = banco.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return banco


@bp.route('/medico2/<pagina>')
def medico2(pagina):
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        banco = ligar_banco()
        cursor = banco.cursor()
        pagina = int(pagina)
        por_pagina= 3
        offset = (pagina-1)*por_pagina
        cursor.execute('SELECT * FROM Medicos LIMIT ? OFFSET?;',(por_pagina, offset))
        Medicos = cursor.fetchall()
        cursor.execute('SELECT COUNT(*) FROM Medicos;')
        total_medicos = cursor.fetchone()[0]
        total_paginas = (total_medicos + por_pagina - 1)
        return render_template('ListaMedicos.html', Titulo="Cadastro de Médicos", ListaMedicos=Medicos,
                            pagina=pagina, total_paginas=total_paginas)


@bp.route('/criarMedico', methods=['POST', 'GET'])
def criar():
    banco = ligar_banco()
    cursor = banco.cursor()

    nomeMed = request.form['nomeMed']
    dataNas_Med = request.form['dataNas_Med']
    formacao = request.form['formacao']
    especialidade = request.form['especialidade']
    genero = request.form['genero']
    cursor.execute('INSERT INTO Medicos'
                       '(Nome, DataNas, Formacao, Especialidade, Genero)'
                       ' VALUES (?,?,?,?,?);',
                        (nomeMed, dataNas_Med, formacao, especialidade, genero))
    banco.commit()

    return redirect('/')


@bp.route('/alterar/<pag>', methods=['PUT', 'POST'])
def alterar(pag):  # Adicione 'pag' nos parâmetros

    id_med = request.form['idmed']
    nome_Med = request.form['nomeMed']  # Nome correto do campo
    dataNas_Med = request.form['dataNas_Med']  # Corrigido de 'dataNas_Med' para 'datanas'
    formacao = request.form['formacao']
    especialidade = request.form['especialidade']
    genero = request.form['genero']

    banco = ligar_banco()
    cursor = banco.cursor()
    try:
        cursor.execute('UPDATE Medicos SET Nome=?, DataNas=?, Formacao=?, Especialidade=?, Genero=? WHERE ID_Med=?;',
                       (nome_Med, dataNas_Med, formacao, especialidade, genero, id_med))  # Corrigida a query SQL
        banco.commit()
        return redirect(f'/listaMedicos/{pag}')

    except Exception as e:
        banco.rollback()  # Reverter alterações em caso de erro
        print(f"Erro ao alterar médico: {e}")  # Logar o erro para facilitar o diagnóstico
        return redirect(f'/listaMedicos/{pag}')


@bp.route('/excluirMedicos/<ID_Med>/<pag>', methods=['GET','DELETE'])
def deletar(ID_Med,pag):
        banco = ligar_banco()
        cursor = banco.cursor()#execulta comando
        try:
            cursor.execute('DELETE FROM Medicos WHERE ID_Med =?;', (ID_Med,))
            banco.commit()#atualizar as intormaçoes, salvar
        except:
            banco.rollback()#deleta comandos que nao funcionarem
        return redirect(f'/listaMedicos/{pag}')


@bp.route('/editarMed/<ID_Med>/<pag>', methods=['GET'])
def editar(ID_Med, pag):
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM Medicos WHERE ID_Med =?',(ID_Med,))
        encontrado = cursor.fetchone()#somente uma tupla
        return render_template('EditarMedico.html', Medico=encontrado,
                                   Titulo="Editar Médico", pagina=pag)