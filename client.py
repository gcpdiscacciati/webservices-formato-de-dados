# client.py
# coding: utf-8

import socket

# Função que cadastra um aluno em uma turma.
def cadastrarAluno():
    aluno = input("Nome do aluno (vazio para encerrar): ")
    if(len(aluno)!=0):
        aluno += ';'
    return aluno

# Função que cadastra uma turma. Ao menos uma turma deve ser cadastrada.
# Para encerrar o cadastro, informe um nome de turma vazio.
# O formato da string cadastrada será: nome_da_turma#ano_da_turma#aluno1;aluno2;aluno3;
def cadastrarTurma():
    alunos = ''
    print("Para encerrar o cadastro, informe um nome de turma vazio (ENTER)")
    turma = input("Nome da turma: ")
    if (len(turma)==0):
        return None
    turma += '#'
    # Valida o ano informado
    while True:
        ano = input("Ano da turma: ")
        if(ano.isnumeric()):
            if(int(ano)>=1900 and int(ano)<=2050):
                break
        print("Ano inválido. O ano deve ser um valor numérico entre 1900 e 2050")
    turma += ano + '#'
    # Faz uma chamada à função de cadastro de alunos. Ao menos 1 aluno deve ser cadastrado.
    while True:
        aluno = cadastrarAluno()
        alunos += aluno
        if(len(aluno)==0):
            if(len(alunos)==0):
                print("Cadastre ao menos 1 aluno")
            else:
                break
        
    turma += alunos
    print()
    return turma

#IP do servidor, deve ser alterado caso cliente e servidor não estejam na mesma máquina
serverName = '127.0.0.1'
serverPort = 16000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((serverName, serverPort))

    turmas = ''
    print("Cadastro de Turmas")

    try:
        # Recebe os dados do cliente    
        while True:
            turma = cadastrarTurma()
            if (turma is not None):
                turmas += turma + '\n'
            elif(len(turmas)==0):
                    print("Insira ao menos 1 turma")
            else:
                break

        # Envia os dados para o servidor
        clientSocket.send(turmas.encode('utf-8'))

        # Recebe e imprime a mensagem processada
        modifiedMessage = clientSocket.recv(1024)
        print("\n--Relatório--")
        print(modifiedMessage.decode('utf-8'))

        clientSocket.close()
    except Exception as e:
        print("Conexão perdida. Erro ao enviar dados.")

except ConnectionRefusedError:
    print("Falha na conexão! Servidor offline!")