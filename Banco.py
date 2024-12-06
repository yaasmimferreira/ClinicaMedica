import sqlite3

conexao = sqlite3.connect('ClinicaMedica.db')
cursor = conexao.cursor()

# cursor.execute('CREATE TABLE IF NOT EXISTS Usuarios('
#                'ID INTEGER PRIMARY KEY,'
#                'Nome TEXT,'
#                'Senha TEXT)')

# cursor.execute('CREATE TABLE IF NOT EXISTS Medicos('
#                'ID_Med INTEGER PRIMARY KEY,'
#                'Nome TEXT,'
#                'DataNas TEXT,'
#                'Genero TEXT,'
#                'Formacao TEXT,'
#                'Especialidade TEXT)')
#
# cursor.execute('CREATE TABLE IF NOT EXISTS Pacientes('
#                'ID_Pac INTEGER PRIMARY KEY,'
#                'Nome TEXT,'
#                'DataNas TEXT,'
#                'Genero TEXT,'
#                'RG INTEGER,'
#                'Endereco TEXT,'
#                'Email TEXT,'
#                'Telefone INTEGER)')

# cursor.execute('''CREATE TABLE IF NOT EXISTS Consultas(
#                ID INTEGER PRIMARY KEY,
#                Horario TEXT,
#                DataCon TEXT,
#                ID_Med INTEGER,
#                ID_Pac INTEGER,
#                FOREIGN KEY (ID_Med) REFERENCES Medicos(ID_Med),
#                FOREIGN KEY (ID_Pac) REFERENCES Pacientes(ID_Pac)
#                );''')