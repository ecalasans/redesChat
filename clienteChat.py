from socket import *
import threading
import Classes
import datetime
from Classes import Mensagem

class ClienteChat():

    BUFFERSIZE = 1024

    def __init__(self, clienteSocket = None):
        self.clienteSocket = socket(AF_INET, SOCK_STREAM)
        self.nickName = ''

    def solicitaConexao(self, destino, porta):
        msgContainer = None
        strMensagem = ''


        #Cria conexão
        try:
            print('Tentando conexão...')
            self.clienteSocket = socket(AF_INET, SOCK_STREAM)
            self.clienteSocket.connect((destino, porta))

            '''
            strMensagem = '{} solicitando conexão...'.format(Classes.getNetworkIP())
            msgContainer = Mensagem(str(16 + len(strMensagem)), Classes.getNetworkIP(), destino, ' ', ' ', strMensagem)

            self.clienteSocket.send(msgContainer.getMensagemCompleta().encode('utf-8'))
            '''
        except ConnectionError:
            print('Falha na conexão!')

        while True:
            self.recebeMensagem()


    #Recebe a mensagem do servidor e printa na tela
    def recebeMensagem(self):
        msgContainer = None
        strMensagem = ''

        dataHora = datetime.datetime.now().strftime('%H:%m:%S')

        #Loop infinito para ficar recebendo as mensagens
        while True:
            try:
                msgRecebida = self.clienteSocket.recv(self.BUFFERSIZE).decode('utf-8')
                msgContainer = Classes.desempacotaMensagem(msgRecebida)
                self.executaComando(msgContainer)

                msgAEnviar = input('({}) - '.format(dataHora))

                msgContainer = Mensagem(16 + len(msgAEnviar), Classes.getNetworkIP(), msgContainer.ipOrigem,
                                        self.nickName, 'tela()', msgAEnviar)

                self.clienteSocket.send(msgContainer.getMensagemCompleta().encode('utf-8'))

            #Caso o cliente tenha desconectado do chat
            except OSError:
                break

    #Comando vindo do servidor para imprimir mensagens na tela
    def tela(self, msgContainer):

        timeMensagem = datetime.datetime.now().strftime('%H:%m:%S')

        return print('{}({}) - {}'.format(timeMensagem, msgContainer.nickName, msgContainer.mensagem))


    #Comando vindo do servidor para fornecer o nick
    def nick(self, msgContainer):
        print('Executando comando nick...')

        timeMensagem  = datetime.datetime.now().strftime('%H:%m:%S')

        nick = input('{}({}) - {}'.format(timeMensagem, msgContainer.nickName, msgContainer.mensagem))

        self.nickName = nick

        resposta = Mensagem(16 + len(''), msgContainer.ipDestino, msgContainer.ipOrigem, nick, 'nick()', '')

        self.clienteSocket.send(resposta.getMensagemCompleta().encode('utf-8'))



    def executaComando(self, msgContainer):
        if 'nick' in msgContainer.comando:
            self.nick(msgContainer)

        if 'tela' in msgContainer.comando:
            self.tela(msgContainer)

        if 'sair' in msgContainer.comando:
            self.clienteSocket.close()