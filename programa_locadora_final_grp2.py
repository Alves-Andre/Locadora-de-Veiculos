from tkinter import messagebox as msg
from tkinter import filedialog as dlg
from datetime import datetime
from tkinter import ttk
from tkinter import *
import schedule
import sqlite3
import zipfile
import shutil
import time
import os

app = Tk()
def comandos(*funcs):
   def combinedFunc(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
   return combinedFunc

class Conecta():
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except:
            print('Erro ao se conectar com o banco de dados')

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            pass
        self.conn.close()

class Janela(Frame):

    def __init__(self, master):
        self.font=('times', 13)
        self.master = master
        self.programa = app
        self.programa.resizable(True, True)
        self.home()

        self.db = Conecta('login.db')
        self.db1 = Conecta('locadora.db')

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS administradores (
            username VARCHAR(10) NOT NULL PRIMARY KEY,
            senha VARCHAR(18) NOT NULL);
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            rg VARCHAR(12) NOT NULL,
            cnhValida VARCHAR(11) NOT NULL);
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS manutencoes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            modelo TEXT,
            custo FLOAT,
            data DATE);
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modelo TEXT,
            descricao TEXT, 
            cor TEXT, 
            placa TEXT UNIQUE, 
            ano BIGINT(4), 
            combustivel TEXT);
            """)

        self.db1.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contratos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            precoDaDiaria FLOAT NOT NULL,
            valorSeguro FLOAT NOT NULL,
            idClienteFK INTEGER NOT NULL,
            idVeiculoFK INTEGER NOT NULL,
            FOREIGN KEY (idClienteFK) REFERENCES clientes(id)
            FOREIGN KEY (idVeiculoFK) REFERENCES veiculos(id));
            """)

        self.db.commit_db()

    def home(self):
        self.programa.title("Login")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack(anchor=S, expand=True, pady=100, padx=10)

        self.nome = Label(self.cont1, width=13, text="Nome: ", font=self.font)
        self.nome.pack(side=LEFT)

        self.nomeEntrada = Entry(self.cont1)
        self.nomeEntrada.pack(side=RIGHT)

        self.senha = Label(self.cont2, width=13, text="Senha: ", font=self.font)
        self.senha.pack(side=LEFT)

        self.senhaEntrada = Entry(self.cont2, show="*")
        self.senhaEntrada.pack(side=RIGHT)

        self.button1 = Button(self.cont3, text="Login", width=13, command=self.realizarLoginAdmin, font=self.font)
        self.button1.pack(side=RIGHT)

        self.lb_cadastro = Label(self.cont4, text='Não é cadastrado?', font=self.font, width=13)
        self.lb_cadastro.pack(side=LEFT)

        self.button2 = Button(self.cont4, text="Cadastrar", width=13,
                              command=lambda: comandos(self.delete(4), self.cadastroAdmin()), font=self.font)
        self.button2.pack(side=RIGHT)

    def realizarLoginAdmin(self):
        while True:
            username = self.nomeEntrada.get()

            self.db.cursor.execute("""
                SELECT * from administradores WHERE username = ?;
                """, (username,))

            nickname = self.db.cursor.fetchall()
            if nickname:
                break
            else:
                msg.showwarning(message='Username inexistente. Por favor, tente novamente ou cadastre-se.')
                break

        while True:
            senha = self.senhaEntrada.get()

            self.db.cursor.execute("""
                SELECT senha FROM administradores WHERE username = ?;
                """, (username,))

            password = self.db.cursor.fetchall()
            if senha == password[0][0]:
                self.pagIni()
                break
            else:
                msg.showwarning(message='Senha inválida. Por favor, tente novamente.')
                break

    def pagIni(self):
        self.delete(4)

        self.programa.title("Página inicial")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack(anchor=S, expand=True, pady=5, padx=10)

        self.button = Button(self.cont1, text = "Iniciar backup", width = 13, command = lambda: comandos(self.delete(4), self.mainBackup()),font = self.font)
        self.button.pack()

        self.button1 = Button(self.cont2, text = "Operações", width = 13, command = self.funcAdmin, font = self.font)
        self.button1.pack()

        self.button2 = Button(self.cont4, text = "Voltar", width = 13, command = lambda: comandos(self.delete(4), self.home()), font = self.font)
        self.button2.pack()

    def funcAdmin(self):
        self.delete(4)

        self.programa.title("Página do Administrador")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack(anchor=S, expand=True, pady=5, padx=10)

        self.button1 = Button(self.cont1, text = "Cadastrar veículo", width = 18, command = self.cadastrarVeiculo, font = self.font)
        self.button1.pack()

        self.button2 = Button(self.cont2, text = "Cadastrar cliente", width = 18, command = self.realizarCadastro, font = self.font)
        self.button2.pack()

        self.button3 = Button(self.cont3, text = "Adicionar manutenção", width = 18, command = self.manutencoes, font = self.font)
        self.button3.pack()

        self.button4 = Button(self.cont4, text = "Realizar contrato", width = 18, command = self.realizarContrato, font = self.font)
        self.button4.pack()

        self.button5 = Button(self.cont5, text = "Realizar consultas", width = 18, command = self.consultas, font = self.font)
        self.button5.pack()

        self.button6 = Button(self.cont6, text = "Voltar", width = 13, command = lambda: comandos(self.delete(6), self.pagIni()), font = self.font)
        self.button6.pack()

    def realizarCadastro(self):
        self.delete(6)

        self.programa.title("Cadastro do Cliente")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack()

        self.nome = Label(self.cont1, width = 13, text = "Nome: ", font = self.font)
        self.nome.pack(side = LEFT)

        self.nomeEntrada = Entry(self.cont1)
        self.nomeEntrada.pack(side = RIGHT)

        self.endereco = Label(self.cont2, width = 13, text = "Endereço: ", font = self.font)
        self.endereco.pack(side = LEFT)

        self.enderecoEntrada = Entry(self.cont2)
        self.enderecoEntrada.pack(side = RIGHT)

        self.cpf = Label(self.cont3, width = 13, text = "Cpf: ", font = self.font)
        self.cpf.pack(side = LEFT)

        self.cpfEntrada = Entry(self.cont3)
        self.cpfEntrada.pack(side = RIGHT)
        self.cpfEntrada.bind("<KeyRelease>", self.formato_cpf)

        self.rg = Label(self.cont4, width = 13, text = "Rg: ", font = self.font)
        self.rg.pack(side = LEFT)

        self.rgEntrada = Entry(self.cont4)
        self.rgEntrada.pack(side = RIGHT)

        self.cnh = Label(self.cont5, width = 13, text = "Cnh: ", font = self.font)
        self.cnh.pack(side = LEFT)

        self.cnhEntrada = Entry(self.cont5)
        self.cnhEntrada.pack(side = RIGHT)

        self.button = Button(self.cont6, text = "Cadastrar", width = 13, command = self.cadastro, font = self.font)
        self.button.pack(side = LEFT)

        self.button1 = Button(self.cont6, text = "Voltar", width = 13, command = lambda: comandos(self.delete(6), self.funcAdmin()), font = self.font)
        self.button1.pack(side = RIGHT)

    def cadastro(self):
        numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        p_nome = self.nomeEntrada.get()
        p_endereco = self.enderecoEntrada.get()
        p_cpf = self.cpfEntrada.get()
        p_rg = self.rgEntrada.get()
        p_cnhValida = self.cnhEntrada.get()
        acumula=0
        if p_nome and p_endereco and p_cpf and p_rg and p_cnhValida != '':
            while True:
                if len(p_cpf)==14:
                    self.db1.cursor.execute("""
                       SELECT * from clientes WHERE cpf = ?;
                       """, (p_cpf,))
                    rows = self.db1.cursor.fetchall()
                    if rows:
                        msg.showwarning(message='O cpf inserido já está cadastrado.')
                        break
                    else:
                        acumula+=1
                        break
                else:
                    msg.showwarning(message='CPF inválido.')
                    break

            while True:
                cont_1 = 0
                cont_2 = 0

                if p_rg != '':
                    for x in p_rg:
                        cont_1 += 1
                        if x in numeros:
                            cont_2 += 1
                    if cont_1 == cont_2:
                        self.db1.cursor.execute("""
                           SELECT * from clientes WHERE rg = ?;
                           """, (p_rg,))

                        rows = self.db1.cursor.fetchall()
                        if rows:
                            msg.showwarning(message='O Rg inserido já está cadastrado.')
                            break
                        else:
                            acumula += 1
                            break
                    else:
                        msg.showwarning(message='Rg inválido. Lembre-se de digitar apenas os caracteres numéricos.')
                        break

            while True:
                cont_1 = 0
                cont_2 = 0

                for x in p_cnhValida:
                    cont_1 += 1
                    if x in numeros:
                        cont_2 += 1
                if cont_1 == cont_2:
                    self.db1.cursor.execute("""
                       SELECT * from clientes WHERE cnhValida = ?;
                       """, (p_cnhValida,))

                    rows = self.db1.cursor.fetchall()
                    if rows:
                        msg.showwarning(message='A CNH inserido já está cadastrado.')
                        break
                    else:
                        acumula += 1
                        break
                else:
                    msg.showwarning(message='CNH inválida. Lembre-se de digitar apenas os caracteres numéricos.')
                    break

            if acumula==3:
                self.db1.cursor.execute("""
                    INSERT INTO clientes(nome, endereco, cpf, rg, cnhValida)
                    VALUES (?,?,?,?,?);
                    """, (p_nome, p_endereco, p_cpf, p_rg, p_cnhValida))
                self.db1.commit_db()
                schedule.run_pending()
                msg.showinfo(message='Cadastro realizado com sucesso.')
                self.nomeEntrada.delete(0, END)
                self.enderecoEntrada.delete(0, END)
                self.cpfEntrada.delete(0, END)
                self.rgEntrada.delete(0, END)
                self.cnhEntrada.delete(0, END)
        else:
            msg.showwarning(message='Por favor, preencha todos os campos.')

    def realizarContrato(self):
        self.delete(6)

        self.programa.title("Página de Contrato")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack()

        self.cont7 = Frame(self.master)
        self.cont7.pack()

        self.cont7 = Frame(self.master)
        self.cont7.pack()

        self.dataIni = Label(self.cont1, width = 20, text = "Data:\n(aaaa-mm-dd) ", font = self.font)
        self.dataIni.pack(side = LEFT)

        self.dataIniEntrada = Entry(self.cont1)
        self.dataIniEntrada.pack(side = RIGHT)

        self.dataIniEntrada.bind("<KeyRelease>", self.formato_data)

        self.diaria = Label(self.cont2, width = 20, text = "Preço da diária: ", font = self.font)
        self.diaria.pack(side = LEFT)

        self.diariaEntrada = Entry(self.cont2)
        self.diariaEntrada.pack(side = RIGHT)

        self.seguro = Label(self.cont3, width = 20, text = "Valor do seguro: ", font = self.font)
        self.seguro.pack(side = LEFT)

        self.seguroEntrada = Entry(self.cont3)
        self.seguroEntrada.pack(side = RIGHT)

        self.idCliente = Label(self.cont4, width = 20, text = "Id cliente: ", font = self.font)
        self.idCliente.pack(side = LEFT)

        self.idClienteEntrada = Entry(self.cont4)
        self.idClienteEntrada.pack(side = RIGHT)

        self.idVeiculo = Label(self.cont5, width = 20, text = "Id veículo: ", font = self.font)
        self.idVeiculo.pack(side = LEFT)

        self.idVeiculoEntrada = Entry(self.cont5)
        self.idVeiculoEntrada.pack(side = RIGHT)

        self.button = Button(self.cont7, text = "Cadastrar", width = 13, command = self.contrato, font = self.font)
        self.button.pack(side = LEFT)

        self.button1 = Button(self.cont7, text = "Voltar", width = 13, command = lambda: comandos(self.delete(7), self.funcAdmin()), font = self.font)
        self.button1.pack(side = RIGHT)

    def contrato(self):
        p_data = self.dataIniEntrada.get()
        p_precoDaDiaria = self.diariaEntrada.get()
        p_valorSeguro = self.seguroEntrada.get()
        p_idCliente = self.idClienteEntrada.get()
        p_idVeiculo = self.idVeiculoEntrada.get()

        if p_data and p_precoDaDiaria and p_valorSeguro and p_idCliente and p_idVeiculo != "":
            cont_acumula = 0
            try:
                int(p_precoDaDiaria), int(p_valorSeguro), int(p_idCliente), int(p_idVeiculo)
            except:
                msg.showwarning(message='Por favor, digite apenas valores numéricos nos campos.')
            else:
                while True:

                   data = p_data.split('-')
                   if len(data) == 3 and len(data[0]) == 4 and len(data[1]) == 2 and len(data[2]) == 2 and (int(data[0]) >= 2000 and int(data[0]) <= 2021):
                       cont_acumula+=1
                       break
                   else:
                       msg.showwarning(message='Data inválida. Por favor, siga o modelo aaaa-mm-dd.')
                       break

                while True:
                    if int(p_precoDaDiaria) > 0:
                        cont_acumula += 1
                        break
                    else:
                        msg.showwarning(message='Por favor, digite um valor numérico maior que 0 para diária.')
                        break

                while True:
                    if int(p_valorSeguro) > 0:
                        cont_acumula += 1
                        break
                    else:
                        msg.showwarning(message='Por favor, digite um valor numérico maior que 0.')
                        break

                while True:
                    self.db1.cursor.execute("""
                    SELECT * from clientes WHERE id = ?;
                    """, (p_idCliente,))

                    rows = self.db1.cursor.fetchall()

                    if rows:
                        cont_acumula += 1
                        break
                    else:
                        msg.showwarning(message='O cliente informado não está cadastrado no banco de dados.')
                        break

                while True:
                    self.db1.cursor.execute("""
                    SELECT * FROM veiculos WHERE id = ?;
                    """, (p_idVeiculo,))

                    rows = self.db1.cursor.fetchall()

                    if rows:
                        self.db1.cursor.execute("""
                        SELECT * FROM contratos where idVeiculoFK = ?;
                        """, (p_idVeiculo,))

                        rows = self.db1.cursor.fetchall()
                        if rows:
                            msg.showwarning(message='O veículo inserido já tem um contrato.')
                            break
                        else:
                            cont_acumula += 1
                            break
                    else:
                        msg.showwarning(message='O veículo inserido não está cadastrado no banco de dados.')
                        break

                self.db1.cursor.execute("""
                SELECT custo FROM manutencoes WHERE modelo = (SELECT modelo FROM veiculos WHERE id = ?);
                """, (p_idVeiculo,))

                custo_man = self.db1.cursor.fetchall()
                try:

                    custo_man = float(custo_man[0][0])

                    if custo_man:
                        cont_acumula += 1
                        p_precoDaDiaria = int(p_precoDaDiaria) + custo_man * 0.1

                except:
                    msg.showwarning(message= 'Esse veículo não possui valor de manutenção fornecido.')

                else:
                    if cont_acumula == 6:
                        self.db1.cursor.execute("""
                            INSERT INTO contratos(data, precoDaDiaria, valorSeguro, idClienteFK, idVeiculoFK)
                            VALUES (?,?,?,?,?);
                            """, (p_data, str(p_precoDaDiaria), p_valorSeguro, p_idCliente, p_idVeiculo))
                        self.db1.commit_db()
                        schedule.run_pending()
                        msg.showinfo(message='Cadastro realizado com sucesso.')
                        self.dataIniEntrada.delete(0, END)
                        self.diariaEntrada.delete(0, END)
                        self.seguroEntrada.delete(0, END)
                        self.idClienteEntrada.delete(0, END)
                        self.idVeiculoEntrada.delete(0, END)
        else:
            msg.showwarning(message='Por favor, preencha todos os campos.')

    def formato_data(self, event=None):
        text = self.dataIniEntrada.get().replace("-", "").replace("/", "")[:8]
        new_text = ""
        for index in range(len(text)):
            if not text[index] in "0123456789": continue
            if index in [3, 5]:
                new_text += text[index] + "-"
            else:
                new_text += text[index]
        self.dataIniEntrada.delete(0, "end")
        self.dataIniEntrada.insert(0, new_text)

    def formato_cpf(self, event=None):
        text = self.cpfEntrada.get().replace(".", "").replace("-", "")[:11]
        new_text = ""
        if event.keysym.lower() == "backspace": return
        for index in range(len(text)):

            if not text[index] in "0123456789": continue
            if index in [2, 5]:
                new_text += text[index] + "."
            elif index == 8:
                new_text += text[index] + "-"
            else:
                new_text += text[index]

        self.cpfEntrada.delete(0, "end")
        self.cpfEntrada.insert(0, new_text)

    def cadastrarVeiculo(self):
        self.delete(6)

        self.programa.title("Cadastro do Veículo")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack()

        self.cont7 = Frame(self.master)
        self.cont7.pack()

        self.cont8 = Frame(self.master)
        self.cont8.pack()

        self.marca = Label(self.cont1, width = 13, text = "Marca: ", font = self.font)
        self.marca.pack(side = LEFT)

        self.marcaEntrada = Entry(self.cont1)
        self.marcaEntrada.pack(side = RIGHT)

        self.modelo = Label(self.cont2, width = 13, text = "Modelo: ", font = self.font)
        self.modelo.pack(side = LEFT)

        self.modeloEntrada = Entry(self.cont2)
        self.modeloEntrada.pack(side = RIGHT)

        self.descricao = Label(self.cont3, width = 13, text = "Descrição: ", font = self.font)
        self.descricao.pack(side = LEFT)

        self.descricaoEntrada = Entry(self.cont3)
        self.descricaoEntrada.pack(side = RIGHT)

        self.cor = Label(self.cont4, width = 13, text = "Cor: ", font = self.font)
        self.cor.pack(side = LEFT)

        self.corEntrada = Entry(self.cont4)
        self.corEntrada.pack(side = RIGHT)

        self.placa = Label(self.cont5, width = 13, text = "Placa: ", font = self.font)
        self.placa.pack(side = LEFT)

        self.placaEntrada = Entry(self.cont5)
        self.placaEntrada.pack(side = RIGHT)

        self.ano = Label(self.cont6, width = 13, text = "Ano: ", font = self.font)
        self.ano.pack(side = LEFT)

        self.anoEntrada = Entry(self.cont6)
        self.anoEntrada.pack(side = RIGHT)

        self.combustivel = Label(self.cont7, width = 13, text = "Combustível: ", font = self.font)
        self.combustivel.pack(side = LEFT)

        self.combustivelEntrada = Entry(self.cont7)
        self.combustivelEntrada.pack(side = RIGHT)

        self.button = Button(self.cont8, text = "Cadastrar", width = 13, command = self.veiculo, font = self.font)
        self.button.pack(side = LEFT)

        self.button1 = Button(self.cont8, text = "Voltar", width = 13, command = lambda: comandos(self.delete(8), self.funcAdmin()), font = self.font)
        self.button1.pack(side = RIGHT)

    def veiculo(self):
        p_marca = self.marcaEntrada.get()
        p_modelo  = self.modeloEntrada.get()
        p_descricao = self.descricaoEntrada.get()
        p_cor = self.corEntrada.get()
        p_placa = self.placaEntrada.get()
        p_ano = self.anoEntrada.get()
        p_combustivel = self.combustivelEntrada.get()

        cont_acumula = 0
        if p_marca and p_modelo and p_descricao and p_cor and p_placa and p_ano and p_combustivel != '':
            try:
                int(p_ano)
            except:
                msg.showwarning(message='Por favor, digite um valor numérico para ano.')
            else:
                while True:
                    self.db1.cursor.execute("""
                    SELECT * FROM veiculos WHERE placa = ?;
                    """, (p_placa,))

                    rows = self.db1.cursor.fetchall()
                    if rows:
                        msg.showwarning(message='A placa digitada já foi inserida. Por favor, tente novamente.')
                        break
                    else:
                        n = 0
                        placa = []
                        for x in p_placa:
                            n += 1
                            placa.append(x)
                        if n != 7:
                            msg.showwarning(message='Placa inválida.')
                            break
                        else:
                            cont_acumula += 1
                            break
                while True:
                    if p_ano!='':
                        if int(p_ano) < 1900 or int(p_ano) > 2021 :
                            msg.showwarning(message= 'Ano inválido.')
                            break
                        else:
                            cont_acumula+=1
                            break
                    else:
                        msg.showwarning(message='Ano inválido.')
                        break
                if cont_acumula == 2:

                    self.db1.cursor.execute("""
                        INSERT INTO veiculos(marca, modelo, descricao, cor, placa, ano, combustivel)
                        VALUES (?,?,?,?,?,?,?);
                        """, (p_marca, p_modelo, p_descricao, p_cor, p_placa, p_ano, p_combustivel))
                    self.db1.commit_db()
                    schedule.run_pending()
                    msg.showinfo(message='Cadastro realizado com sucesso.')
                    self.marcaEntrada.delete(0, END)
                    self.modeloEntrada.delete(0, END)
                    self.descricaoEntrada.delete(0, END)
                    self.corEntrada.delete(0, END)
                    self.placaEntrada.delete(0, END)
                    self.anoEntrada.delete(0, END)
                    self.combustivelEntrada.delete(0, END)
        else:
            msg.showwarning(message='Por favor, preencha todos os campos.')

    def manutencoes(self):
        self.delete(6)

        self.programa.title("Adicionar Manutenção")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.modelo = Label(self.cont1, width = 20, text = "Modelo: ", font = self.font)
        self.modelo.pack(side = LEFT)

        self.modeloEntrada = Entry(self.cont1)
        self.modeloEntrada.pack(side = RIGHT)

        self.custo = Label(self.cont2, width = 20, text = "Custo médio \nde manutenção: ", font = self.font)
        self.custo.pack(side = LEFT)

        self.custoEntrada = Entry(self.cont2)
        self.custoEntrada.pack(side = RIGHT)

        self.button = Button(self.cont3, text = "Inserir", width = 13, command = self.inserirManutencao, font = self.font)
        self.button.pack(side = LEFT)

        self.button1 = Button(self.cont3, text = "Voltar", width = 13, command = lambda: comandos(self.delete(3), self.funcAdmin()), font = self.font)
        self.button1.pack(side = RIGHT)

    def inserirManutencao(self):
        p_modelo = self.modeloEntrada.get()
        if p_modelo != '':
            while True:
                p_data = datetime.today().strftime('%Y-%m-%d')
                cont_acumula1 = 0

                self.db1.cursor.execute("""
                    SELECT * FROM manutencoes WHERE modelo = ?;
                """, (p_modelo,))

                rows = self.db1.cursor.fetchall()
                if rows:
                    msg.showwarning(message= 'Já há um valor de manutenção definido para este modelo.')
                    break
                else:
                    self.db1.cursor.execute("""
                        SELECT * FROM veiculos WHERE modelo = ?;
                    """, (p_modelo,))
                    rows1 = self.db1.cursor.fetchall()
                    if rows1:
                        cont_acumula1 +=1
                        break
                    else:
                        msg.showwarning(message='Esse modelo não foi cadastrado.')
                        break
            while True:
                try:
                    p_custo = float(self.custoEntrada.get())
                except:
                    msg.showwarning(message= 'Por favor, digite um valor numérico para custo.')
                    break
                else:
                    if p_custo <= 0:
                        msg.showwarning(message= 'Por favor, digite um valor de manutenção maior que 0.')
                        break
                    else:
                        cont_acumula1 +=1
                        break

            if cont_acumula1 == 2:
                msg.showinfo(message= 'Manutenção inserida com sucesso!')
                self.modeloEntrada.delete(0, END)
                self.custoEntrada.delete(0, END)

                self.db1.cursor.execute("""
                    INSERT INTO manutencoes(modelo, custo, data)
                    VALUES (?,?,?);
                    """, (p_modelo, p_custo, p_data))
                self.db1.commit_db()
                schedule.run_pending()
        else:
            msg.showwarning(message='Por favor, preencha todos os campos.')

    def consultas(self):
        self.delete(6)

        self.programa.title("Consultas")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack()

        self.cont5 = Frame(self.master)
        self.cont5.pack()

        self.cont6 = Frame(self.master)
        self.cont6.pack(anchor=S, expand=True, pady=5, padx=10)

        self.label = Label(self.cont1, width = 15, text = "Realizar consulta", font = self.font)
        self.label.pack(side = "top")

        self.button1 = Button(self.cont2, text = "Veículos", width = 13, command = lambda: comandos(self.delete(6), self.consultarVeiculos()), font = self.font)
        self.button1.pack()

        self.button2 = Button(self.cont3, text = "Manutenções", width = 13, command = lambda: comandos(self.delete(6), self.consultarManutencoes()), font = self.font)
        self.button2.pack()

        self.button3 = Button(self.cont4, text = "Clientes", width = 13, command = lambda: comandos(self.delete(6), self.consultarClientes()), font = self.font)
        self.button3.pack()

        self.button4 = Button(self.cont5, text = "Contratos", width = 13, command = lambda: comandos(self.delete(6), self.consultarContratos()), font = self.font)
        self.button4.pack()

        self.button5 = Button(self.cont6, text = "Voltar", width = 13, command = lambda: comandos(self.delete(6), self.funcAdmin()), font = self.font)
        self.button5.pack()

    def consultarVeiculos(self):
        self.programa.title("Consultar Veículos")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='Marca')
        self.listaVei.heading("#3", text='Modelo')
        self.listaVei.heading("#4", text='Descrição')
        self.listaVei.heading("#5", text='Cor')
        self.listaVei.heading("#6", text='Placa')
        self.listaVei.heading("#7", text='Ano')
        self.listaVei.heading("#8", text='Combustível')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.column('#5', anchor=CENTER, width=80)
        self.listaVei.column('#6', anchor=CENTER, width=80)
        self.listaVei.column('#7', anchor=CENTER, width=80)
        self.listaVei.column('#8', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)

        self.db1.cursor.execute("""
                SELECT * FROM veiculos;
                """)
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1("veiculos")

    def consultarManutencoes(self):
        self.programa.title("Consultar Manutenções")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='Modelo')
        self.listaVei.heading("#3", text='Custo')
        self.listaVei.heading("#4", text='Data')

        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)

        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)

        self.db1.cursor.execute("""
            SELECT * FROM manutencoes;
            """)
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1("manutencoes")

    def consultarClientes(self):
        self.programa.title("Consultar Clientes")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='Nome')
        self.listaVei.heading("#3", text='Endereço')
        self.listaVei.heading("#4", text='CPF')
        self.listaVei.heading("#5", text='RG')
        self.listaVei.heading("#6", text='CNH')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.column('#5', anchor=CENTER, width=80)
        self.listaVei.column('#6', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)

        self.db1.cursor.execute("""
                SELECT * FROM clientes;
                """)
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1("clientes")

    def consultarContratos(self):
        self.programa.title("Consultar Contratos")
        self.programa.geometry('700x500')
        self.frames()
        self.listaVei = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaVei.heading("#0", text="")
        self.listaVei.heading("#1", text='Id')
        self.listaVei.heading("#2", text='Data')
        self.listaVei.heading("#3", text='Preço Diaria')
        self.listaVei.heading("#4", text='Valor Seguro')
        self.listaVei.heading("#5", text='Id Cliente')
        self.listaVei.heading("#6", text='Id Veículo')
        self.listaVei.column('#0', width=0, stretch=NO)
        self.listaVei.column('#1', anchor=CENTER, width=80)
        self.listaVei.column('#2', anchor=CENTER, width=80)
        self.listaVei.column('#3', anchor=CENTER, width=80)
        self.listaVei.column('#4', anchor=CENTER, width=80)
        self.listaVei.column('#5', anchor=CENTER, width=80)
        self.listaVei.column('#6', anchor=CENTER, width=80)
        self.listaVei.place(relx=0.008, rely=0.1, relwidth=0.98, relheight=0.85)

        self.db1.cursor.execute("""
                SELECT * FROM contratos;
                """)
        for registro in self.db1.cursor.fetchall():
            if registro:
                self.listaVei.insert("", END, values=(registro))
        self.opcoesFrame_1("contratos")

    def opcoesFrame_1(self, tabela):
        if tabela == 'veiculos':
            tabela_consulta = 'self.consultarVeiculos()'
        if tabela == 'manutencoes':
            tabela_consulta = 'self.consultarManutencoes()'
        if tabela == 'clientes':
            tabela_consulta = 'self.consultarClientes()'
        if tabela == 'contratos':
            tabela_consulta = 'self.consultarContratos()'

        self.id = Label(self.frame_1, text = 'Id: ', font = self.font, bg='gray83')
        self.id.place(relx=0.48, rely=0.05)

        self.idEntrada = Entry(self.frame_1)
        self.idEntrada.place(relx=0.46, rely=0.15, relwidth=0.08)

        self.bt_deletar = Button(self.frame_1, text="Deletar", font = self.font, command= lambda: comandos(self.excluir(tabela), self.listaVei.destroy(), self.frame_1.destroy(), self.frame_2.destroy(), exec(tabela_consulta), schedule.run_pending()), width = 13)
        self.bt_deletar.place(relx=0.45, rely=0.35, relwidth=0.1, relheight=0.15)

        self.bt_voltar = Button(self.frame_1, text="Voltar", width = 13, command=lambda: comandos(self.listaVei.destroy(), self.frame_1.destroy(), self.frame_2.destroy(), self.programa.geometry('550x350'), self.consultas()), font=self.font)
        self.bt_voltar.pack(anchor=S, expand=True, pady=5, padx=10)

    def excluir(self, tabela):
        idExcluir = self.idEntrada.get()
        try:
            int(idExcluir)
        except:
            msg.showwarning(message="Digite apenas números.")
        else:
            res = msg.askyesno(title = "Alerta", message = "Tem certeza que deseja excluir?")
            if res == True:
                if tabela == 'veiculos':

                    self.db1.cursor.execute("""
                        DELETE FROM veiculos
                        WHERE id = (?);
                        """, (idExcluir))

                if tabela == 'manutencoes':

                    self.db1.cursor.execute("""
                        DELETE FROM manutencoes
                        WHERE id = (?);
                        """, (idExcluir))

                if tabela == 'clientes':

                    self.db1.cursor.execute("""
                        DELETE FROM clientes
                        WHERE id = (?);
                        """, (idExcluir,))

                if tabela == 'contratos':
                    self.db1.cursor.execute("""
                        DELETE FROM contratos
                        WHERE id = (?);
                        """, (idExcluir,))

                self.db1.commit_db()
                msg.showinfo(message="Exclusão realizada com sucesso.")
                self.idEntrada.delete(0,END)

    def frames(self):
        self.frame_1 = Frame(self.programa, bd=4, bg='gray83', highlightbackground='gray45', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.programa, bd=4, bg='gray83', highlightbackground='gray45', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def cadastroAdmin(self):
        self.delete(4)
        self.programa.title("Cadastrar Administrador")

        self.cont1 = Frame(self.master)
        self.cont1.pack()

        self.cont2 = Frame(self.master)
        self.cont2.pack()

        self.cont3 = Frame(self.master)
        self.cont3.pack()

        self.cont4 = Frame(self.master)
        self.cont4.pack(anchor=S, expand=True, pady=5, padx=10)

        self.nome = Label(self.cont1, width = 13, text = "Nome: ", font = self.font)
        self.nome.pack(side = LEFT)

        self.nomeEntrada = Entry(self.cont1)
        self.nomeEntrada.pack(side = RIGHT)

        self.senha = Label(self.cont2, width = 13, text = "Senha: ", font = self.font)
        self.senha.pack(side = LEFT)

        self.senhaEntrada = Entry(self.cont2, show = "*")
        self.senhaEntrada.pack(side = RIGHT)

        self.button = Button(self.cont3, text = "Cadastrar", width = 13, command = self.cadastrarAdmin, font = self.font)
        self.button.pack()

        self.button1 = Button(self.cont4, text = "Voltar", width = 13, command = lambda: comandos(self.delete(4), self.home()), font = self.font)
        self.button1.pack()

    def cadastrarAdmin(self):
        cont_acumula2 = 0
        while True:
            p_username = self.nomeEntrada.get()
            check = self.verificarUsername(p_username, 'administradores')
            if check == True:
                msg.showwarning(message='Nome de usuário já existente. Por favor, escolha outro.')
                break
            else:
                cont_acumula2 += 1
                break

        while True:
            p_senha = self.senhaEntrada.get()
            check = self.verificarSenha(p_senha)
            if check == True:
                cont_acumula2 += 1
                break
            else:
                msg.showwarning(message='Por favor, digite uma senha válida (com ao menos 8 caracteres totais, 1 letra maiúscula, 1 minúscula, 1 número e 1 caractere especial.)')
                break

        if cont_acumula2 == 2:

            self.db.cursor.execute("""
                INSERT INTO administradores(username, senha)
                VALUES (?,?);
                """, (p_username, p_senha))

            self.db.commit_db()
            schedule.run_pending()
            msg.showinfo(message= 'Cadastro de administrador realizado com sucesso!')
            self.nomeEntrada.delete(0, END)
            self.senhaEntrada.delete(0, END)

    def verificarUsername(self, username, tabela):
        self.db.cursor.execute("""
            SELECT * from """+tabela+""" WHERE username = ?;
        """, (username,))

        rows = self.db.cursor.fetchall()
        if rows:
            return True
        else:
            return False

    def verificarSenha(self, senha):
        cont = 0
        if any(n.isupper() for n in senha):
            cont += 1
        if any(n.islower() for n in senha):
            cont += 1
        if any(n.isdigit() for n in senha):
            cont += 1
        if any(n in ('?#!$%&*()_^~@/') for n in senha):
            cont += 1
        if cont >= 4 and len(senha) >= 8:
            return True

    def backupLocadora(self):
        # Definindo o horário
        data_atual = datetime.now()
        data_e_hora = data_atual.strftime('%d%m%Y%H%M%S')

        # Formatando o nome do arquivo .db
        shutil.copyfile(self.origem_locadora, os.path.join(self.path_locadora, f'backup_locadora_{data_e_hora}.db'))

        # Definindo o nome do arquivo zip
        zipFile = f'backup_locadora_{data_e_hora}.zip'

        # Definindo caminho do zip
        pathZip = f'{self.path_locadora}\\{zipFile}'

        # Compactando o arquivo
        arq_zip = zipfile.ZipFile(pathZip, mode='w', compression=zipfile.ZIP_DEFLATED)
        arq_zip.write(f'backup_locadora_{data_e_hora}.db')
        arq_zip.close()

        # Copiando para o destino
        shutil.copyfile(pathZip, os.path.join(self.destinoNuvem, zipFile))
        shutil.copyfile(pathZip, os.path.join(self.destinoFisico, zipFile))
        print(f'Backups de \'locadora\' realizados em {data_atual}')

        # Excluindo arquivos '.db' já em backup
        self.excluirArq(self.path_locadora)

    def backupLogin(self):
        data_atual = datetime.now()
        data_e_hora = data_atual.strftime('%d%m%Y%H%M%S')

        shutil.copyfile(self.origem_login, os.path.join(self.path_login, f'backup_login_{data_e_hora}.db'))
        zipFile = f'backup_login_{data_e_hora}.zip'
        pathZip = f'{self.path_login}\\{zipFile}'

        arq_zip = zipfile.ZipFile(pathZip, mode='w', compression=zipfile.ZIP_DEFLATED)
        arq_zip.write(f'backup_login_{data_e_hora}.db')
        arq_zip.close()

        shutil.copyfile(pathZip, os.path.join(self.destinoFisico, zipFile))
        shutil.copyfile(pathZip, os.path.join(self.destinoNuvem, zipFile))
        print(f'Backups de \'login\' realizados em {data_atual}')
        self.excluirArq(self.path_login)

    def excluirArq(self, path):
        for file in os.listdir(path):
            if file.startswith("backup_") and (file.endswith('.db') or file.endswith('.zip')):
                os.remove(os.path.join(path, file))

    def mainBackup(self):
        # Definindo o caminho de origem de 'locadora.db'
        try:
            self.origem_locadora = os.path.abspath('locadora.db')
            self.path_locadora = self.origem_locadora.split('\\')
            self.path_locadora.remove('locadora.db')
            self.path_locadora = '\\'.join(self.path_locadora)
        except:
            msg.showwarning(message='Erro ao encontar \'locadora.db\'. Por favor, verifique seus arquivos.')
        else:
            try:
                # Definindo o caminho de origem de 'login.db'
                self.origem_login = os.path.abspath('login.db')
                self.path_login = self.origem_login.split('\\')
                self.path_login.remove('login.db')
                self.path_login = '\\'.join(self.path_login)
            except:
                msg.showwarning('Erro ao encontar \'login.db\'. Por favor, verifique seus arquivos.')
            else:
                self.cont1 = Frame(self.master)
                self.cont1.pack()

                self.cont2 = Frame(self.master)
                self.cont2.pack()

                self.cont3 = Frame(self.master)
                self.cont3.pack(anchor=S, expand=True, pady=5, padx=10)

                self.lb_destRemoto = Label(self.cont1, text='Destino Remoto:', font=self.font, width=18)
                self.lb_destRemoto.pack(side=LEFT)
                self.entry_destRemoto = Entry(self.cont1)
                self.entry_destRemoto.pack(side=LEFT)
                self.button_destRemoto = Button(self.cont1, text='...', command=self.escolherDestinoNuvem)
                self.button_destRemoto.pack(side=RIGHT)

                self.lb_destRFisico = Label(self.cont2, text='Destino Físico:', font=self.font, width=18)
                self.lb_destRFisico.pack(side=LEFT)
                self.entry_destFisico = Entry(self.cont2)
                self.entry_destFisico.pack(side=LEFT)
                self.button_destFisico = Button(self.cont2, text='...', command=self.escolherDestinoFisico)
                self.button_destFisico.pack(side=RIGHT)

                self.buttonBack = Button(self.cont3, text="Iniciar backup", width=13, font=self.font,
                                         command=self.loopBackup)
                self.buttonBack.pack(side=LEFT)

                self.button1 = Button(self.cont3, text="Voltar", width=13,
                                      command=lambda: comandos(self.delete(3), self.pagIni()), font=self.font)
                self.button1.pack(side=RIGHT)

    def loopBackup(self):
        self.destinoNuvem = self.entry_destRemoto.get()
        self.destinoFisico = self.entry_destFisico.get()
        if self.destinoNuvem != '' and self.destinoFisico != '':
            self.entry_destFisico.delete(0, END)
            self.entry_destRemoto.delete(0, END)
            msg.showinfo(message='Backup iniciado!')
            schedule.every(1).seconds.do(self.backupLocadora)
            schedule.every(1).seconds.do(self.backupLogin)

            schedule.run_pending()
            time.sleep(1)
        else:
            msg.showwarning(message='Escolha os destinos do backup.')

    def escolherDestinoNuvem(self):
        text = dlg.askdirectory(title="Escolha um dispositivo remoto para exportar o backup. (Nuvem computacional)")
        self.entry_destRemoto.delete(0, "end")
        self.entry_destRemoto.insert(0, text)

    def escolherDestinoFisico(self):
        text = dlg.askdirectory(title="Escolha um dispositivo físico para exportar o backup. (Exemplo: HD externo)")
        self.entry_destFisico.delete(0, "end")
        self.entry_destFisico.insert(0, text)

    def delete(self, num):
        for c in range(num):
            exec(f"self.cont{c+1}.destroy()")

app.geometry('550x350')
Janela(app)
app.mainloop()