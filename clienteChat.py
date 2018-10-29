import socket
import threading
import Classes
import datetime
from Classes import Mensagem

class ClienteChat():

    BUFFERSIZE = 1024

    def __init__(self, clienteSocket = None):
        self.clienteSocket = clienteSocket

    def solicitaConexao(self, destino, porta):
        msgContainer = None
        strMensagem = ''


        #Cria conexão
        try:
            print('Tentando conexão...')
            self.clienteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clienteSocket.connect((destino, porta))

            strMensagem = '{} solicitando conexão...'.format(Classes.getNetworkIP())
            msgContainer = Mensagem(str(16 + len(strMensagem)), Classes.getNetworkIP(), destino, ' ', ' ', strMensagem)

            self.clienteSocket.send(msgContainer.getMensagemCompleta().encode('utf-8'))
        except ConnectionError:
            print('Falha na conexão!')

        while True:
            self.recebeMensagem()


    #Recebe a mensagem do servidor e printa na tela
    def recebeMensagem(self):
        msgContainer = None
        strMensagem = ''

        #Loop infinito para ficar recebendo as mensagens
        while True:
            try:
                msgRecebida = self.clienteSocket.recv(self.BUFFERSIZE).decode('utf-8')
                self.tela(msgRecebida)

            #Caso o cliente tenha desconectado do chat
            except OSError:
                break


    def fechaConexao(self):
        self.clienteSocket.close()

    def tela(self, mensagem):
        mensTela = Classes.desempacotaMensagem(mensagem)

        timeMensagem = datetime.datetime.now().strftime('%H:%m:%S')

        return print('{}({}) - {}'.format(timeMensagem, mensTela.nickName, mensTela.mensagem))