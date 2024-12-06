from flask import Blueprint, render_template, session, redirect, g, request, send_file
import sqlite3

bp = Blueprint('Consultas', __name__)

def ligar_banco():
    banco = g._database = sqlite3.connect('ClinicaMedica.db')
    cursor = banco.cursor()
    cursor.execute("PRAGMA foreign_keys  = ON;")
    return banco


@bp.route('/consulta2/<pagina>')
def consulta2(pagina):
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        banco = ligar_banco()
        cursor = banco.cursor()
        pagina = int(pagina)
        por_pagina= 3
        offset = (pagina-1)*por_pagina
        cursor.execute('SELECT * FROM Consultas LIMIT ? OFFSET?;',(por_pagina, offset))
        Consultas = cursor.fetchall()
        cursor.execute('SELECT COUNT(*) FROM Consultas;')
        total_consultas = cursor.fetchone()[0]
        total_paginas = (total_consultas + por_pagina - 1)
        return render_template('ListaConsultas.html', Titulo="Cadastro de Médicos", ListaConsultas=Consultas,
                            pagina=pagina, total_paginas=total_paginas)


#---------------- PÁGINA CADASTRO DE CONSULTA ----------------
@bp.route('/cadastroConsulta')
def cad_Consulta():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('SELECT ID_Med, Nome FROM Medicos;')
        Nome_Meds = cursor.fetchall()
        cursor.execute('SELECT ID_Pac, Nome FROM Pacientes;')
        Nome_Pacs = cursor.fetchall()

        return render_template('CadConsulta.html', Titulo='Cadastro de Consulta', listaMedicos=Nome_Meds,
                               listaPacientes=Nome_Pacs)


#----------------ROTA INTERMEDIÁRIA (CRIAR CONSULTA) ----------------
@bp.route('/criarConsulta', methods=['POST', 'GET'])
def criar_Consulta():
    banco = ligar_banco()
    cursor = banco.cursor()

    nomeMed = request.form['nomeMed']
    nomePac = request.form['nomePac']
    horario = request.form['hora']
    dataCons = request.form['dataCons']
    cursor.execute('INSERT INTO Consultas (Horario,DataCon,ID_Med,ID_Pac) '
                       'VALUES (?,?,?,?);',
                       (horario, dataCons, nomeMed, nomePac))
    banco.commit()
    return redirect('/listaConsultas/1')

#----------------ROTA INTERMEDIÁRIA (ALTERAR) ----------------
@bp.route('/alterarConsulta/<pag>', methods=['POST'])
def alterar(pag):
    banco = ligar_banco()
    cursor = banco.cursor()
    # --> Passo 1: Armazenar as novas informações do form em uma variável.

    ID = request.form['idcon']
    nomePac = request.form['nomePac']
    nomeMed = request.form['nomeMed']
    hora = request.form['hora']
    dataCons = request.form['dataCons']

    # --> Passo 2: Conectar-se ao banco de dados.
    banco = ligar_banco()
    cursor = banco.cursor()

    # --> Passo 3: Tenta atualizar as informações do banco de dados.

    cursor.execute('UPDATE Consultas SET ID_Pac=?, ID_Med=?, Horario=?, DataCon=? WHERE ID=?;',
                       (nomePac, nomeMed, hora, dataCons, ID))
    banco.commit()
    return redirect('/listaConsultas/1')




@bp.route('/excluirConsulta/<ID>/<pag>', methods=['GET','DELETE'])
def deletar(ID,pag):
        banco = ligar_banco()
        cursor = banco.cursor()#execulta comando
        try:
            cursor.execute('DELETE FROM Consultas WHERE ID =?;', (ID,))
            banco.commit()#atualizar as intormaçoes, salvar
        except:
            banco.rollback()#deleta comandos que nao funcionarem
        return redirect(f'/listaConsultas/{pag}')


@bp.route('/editar/<ID>/<pag>', methods=['GET'])
def editar(ID, pag):

        banco = ligar_banco()
        cursor = banco.cursor()

        cursor.execute('SELECT ID_Med,Nome FROM Medicos')
        total_medicos = cursor.fetchall()

        cursor.execute('SELECT ID_Pac,Nome,Genero FROM Pacientes')
        total_pacientes = cursor.fetchall()
        print(total_pacientes)

        cursor.execute('SELECT * FROM Consultas WHERE ID =?',(ID,))
        encontrado = cursor.fetchone()#somente uma tupla
        print(encontrado)
        return render_template('EditarConsulta.html', Consulta=encontrado,
                                   Titulo="Editar Consulta", pagina=pag, medicos=total_medicos, pacientes=total_pacientes)