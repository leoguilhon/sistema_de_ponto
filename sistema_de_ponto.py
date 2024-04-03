import sqlite3
import re
import datetime



def inic_db():
    global conn
    global cursor
    #Estabelece a conexão com o banco de dados (se não existir, será criado)
    conn = sqlite3.connect('data.db')

    #Criando um cursor para executar comandos SQL
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS colaboradores
                (ID INTEGER PRIMARY KEY,
                NOME VARCHAR(255),
                TEL VARCHAR(20),
                EMAIL VARCHAR(50),
                ENDERECO VARCHAR(255),
                SEXO VARCHAR(20),
                PIX VARCHAR(50),
                HI VARCHAR(20),
                HO VARCHAR(20),
                STATUS INTEGER,
                FOTO VARCHAR(255),
                CPF VARCHAR(20),
                DN VARCHAR(20),
                CARTAO VARCHAR(20),
                CARGO VARCHAR(50))''')
    return

# Validações
def validar_nome():
    while True:
        nome = input("Insira o nome:")
        if nome and nome.replace(" ", "").isalpha():
            return nome
        print("Nome inválido")

def validar_telefone():
    while True:
        tel = input("Insira o telefone:")
        if tel and tel.isdigit():
            return tel
        print("Telefone inválido")

def validar_email():
    while True:
        email = input("Insira o e-mail:")
        if email and '@' in email:
            return email
        print("E-mail inválido")

def validar_cpf():
    while True:
        cpf = input("Insira o CPF:")
        if cpf and re.match(r'^\d{11}$', cpf):
            return cpf
        print("CPF inválido")

def validar_data_nascimento():
    while True:
        dn = input("Insira a data de nascimento (DD/MM/AAAA):")
        if dn and re.match(r'^\d{2}/\d{2}/\d{4}$', dn):
            return dn
        print("Data de nascimento inválida")

# Funções do Sistema de Ponto

# Registro de Colaborador
def incluirColaborador():
    #Input's e Validações
    nome = validar_nome()
    telefone = validar_telefone()
    email = validar_email()
    endereco = input("Insira o endereco:")
    sexo = input("Insira o sexo:")
    pix = input("Insira o pix:")
    hi = 0
    ho = 0
    status = 0
    foto = "C:\\Users\\leonardo.guilhon\\Desktop\\Sistema de Ponto\\fotos\\"+f"foto-{nome}.png"
    cpf = validar_cpf()
    dn = validar_data_nascimento()
    cartao = input("Insira o cartão:")
    cargo = input("Insira o cargo:")
    
    # Inserir dados
    cursor.execute("INSERT INTO colaboradores (NOME, TEL, EMAIL, ENDERECO, SEXO, PIX, HI, HO, STATUS, FOTO, CPF, DN, CARTAO, CARGO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (nome, telefone, email, endereco, sexo, pix, hi, ho, status, foto, cpf, dn, cartao, cargo))
    conn.commit()
    print(f'Colaborador {nome} registrado com sucesso no sistema.')
    return
# Excluir colaborador do banco de dados
def excluirColaborador():
    lista_de_colaboradores = list(cursor.execute("SELECT ID, NOME, CPF FROM colaboradores"))
    conn.commit()
    id_colaborador = input("Insira o ID do colaborador que deseja excluir:")
    for colaborador in lista_de_colaboradores:
        if id_colaborador in str(colaborador[0]):
            cursor.execute(f"DELETE FROM colaboradores WHERE ID = {id_colaborador};")
            conn.commit()
            print("Colaborador excluído com sucesso da base de dados.")
        else:
            print('ID não encontrado')

# Atualizar o cartão do colaborador
def atualizarColaborador():
    lista_de_colaboradores = list(cursor.execute("SELECT ID, NOME, CARTAO FROM colaboradores"))
    conn.commit()
    id_colaborador = input("Insira o ID do colaborador que deseja atualizar o cartão:")
    for colaborador in lista_de_colaboradores:
        if id_colaborador in str(colaborador[0]):
            novo_cartao = input("Insira o novo cartão:")
            cursor.execute(f"UPDATE colaboradores SET CARTAO = {novo_cartao} WHERE ID = {id_colaborador};")
            conn.commit()
            print(f"Cartão: {novo_cartao} associado com sucesso a {colaborador[1]}.")
        else:
            print('ID não encontrado')

# Listagem dos Colaboradores
def listarColaboradores():
    print("Lista de Colaboradores:")
    # Executa a consulta SQL para selecionar os registros da tabela de colaboradores
    cursor.execute("SELECT * FROM colaboradores")

    # Recupera todos os resultados da consulta
    colaboradores = cursor.fetchall()

    # Exibe os resultados
    for colaborador in colaboradores:
        print(colaborador)
    return

# Acesso do colaborador
def acessarColaborador():
    lista_de_colaboradores = list(cursor.execute("SELECT ID, NOME, HI, HO, STATUS, CARTAO FROM colaboradores"))
    conn.commit()
    card_solicitando = input("Insira o cartão para realizar o acesso:")
    for colaborador in lista_de_colaboradores:
        if card_solicitando in str(colaborador[5]):
            status = colaborador[4]
            if status == 0:
                data_hora_atual = datetime.datetime.now()
                data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
                cursor.execute("UPDATE colaboradores SET STATUS = ?, HI = ? WHERE ID = ?;", (1, data_hora_formatada, colaborador[0]))
                conn.commit()
                print(f"Acesso realizado!\nBem vindo, {colaborador[1]}!")
            elif status == 1:
                data_hora_atual = datetime.datetime.now()
                data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
                cursor.execute("UPDATE colaboradores SET STATUS = ?, HO = ? WHERE ID = ?;", (0, data_hora_formatada, colaborador[0]))
                conn.commit()
                print(f"Acesso realizado!\nAté logo, {colaborador[1]}!")
        else:
            print('Cartão não encontrado no banco de dados')
    
inic_db()
# Menu
while True:
    print("*** SISTEMA DE PONTO ***")
    print("1. Incluir")
    print("2. Listar")
    print("3. Excluir")
    print("4. Atualizar")
    print("5. Acessar")
    print("6. Sair")
    escolha = input("Escolha a opção:")
    match (escolha):
        case "1":
            incluirColaborador()
        case "2":
            listarColaboradores()
        case "3":
            excluirColaborador()
        case "4":
            atualizarColaborador()
        case "5":
            acessarColaborador()
        case "6":
            print("Saindo...")
            break
        case _:
            print("Opção inválida")


conn.close()