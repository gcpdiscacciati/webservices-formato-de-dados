# server.py
# coding: utf-8

import socket

# Configuração da conexão
serverPort = 16000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(0)

print("Servidor pronto para receber")

# Retorna o nome da turma com maior número de alunos
def largestClass(lista):
    maior = max(lista, key=lambda x: len(x.split('#')[2].split(';')))
    nomeTurma = maior.split('#')[0]
    return nomeTurma

# Retorna o ano da turma mais antiga
def oldestClass(lista):
    turma = min(lista, key=lambda x: x.split('#')[1])
    ano = turma.split('#')[1]
    return ano

# Checa o número médio de alunos das turmas
def avgNumberStudents(lista):
    soma = 0.0
    for i in lista:
        alunos = i.split('#')[2].split(';')
        alunos.remove('')
        soma += len(alunos)
    return soma/(len(lista))

# Loop que aguarda a conexão do cliente e processa a mensagem recebida
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        print("Conexão vinda de {}".format(addr))
        message = connectionSocket.recv(2048)
        print("{} ==> {}".format(addr, message.decode('utf-8')))
        decodedMessage = message.decode('utf-8')
        # Transforma a string recebida em uma lista de strings
        listaTurmas = decodedMessage.split('\n')
        listaTurmas.pop()
        # Calcula o número de turmas
        quantidadeTurmas = len(listaTurmas)
        # Checa a maior turma
        maisAlunos = largestClass(listaTurmas)
        # Checa a turma mais antiga
        maisAntiga = oldestClass(listaTurmas)
        # Checa a média de alunos das turmas
        mediaAlunos = avgNumberStudents(listaTurmas)

        # Formata os dados em uma string
        modifiedMessage = (f"Quantidade de turmas: {quantidadeTurmas}"
                        f"\nTurma com mais alunos: {maisAlunos}"
                        f"\nAno da turma mais antiga: {maisAntiga}"
                        f"\nQuantidade média de alunos: {mediaAlunos:.2f}")

        # Retorna a mensagem modificada
        connectionSocket.send(modifiedMessage.encode('utf-8'))

        # Encerra a conexão com o cliente
        connectionSocket.close()
    except ConnectionResetError:
        print(f"Conexão perdida com {addr}")
