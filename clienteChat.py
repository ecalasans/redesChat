from socket import *
from threading import Thread
import Classes
import datetime
from Classes import Mensagem
import time

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

            dataHora = datetime.datetime.now().strftime('%H:%m:%S')

            self.nickName = input('{} - Digite seu nick:'.format(dataHora))

        except ConnectionError:
            print('Falha na conexão!')


        thOuvir = Thread(target=self.ouveMensagem, daemon=True)
        thOuvir.start()

        while True:
            dataHora = datetime.datetime.now().strftime('%H:%m:%S')

            msgAEnviar = input('{} - '.format(dataHora))

            msgContainer = Mensagem(16 + len(msgAEnviar), Classes.getNetworkIP(), destino,
                                    self.nickName, 'tela()', msgAEnviar)

            self.clienteSocket.send(msgContainer.getMensagemCompleta().encode('utf-8'))

    #Recebe a mensagem do servidor e printa na tela
    def ouveMensagem(self):
        while True:
            # Recebe a primeira mensagem e verifica se é pra digitar o nick
            msgRecebida = self.clienteSocket.recv(self.BUFFERSIZE).decode('utf-8')

            msgContainer = Classes.desempacotaMensagem(msgRecebida)

            self.executaComando(msgContainer)


    #Comando vindo do servidor para imprimir mensagens na tela
    def tela(self, msgContainer):

        timeMensagem = datetime.datetime.now().strftime('%H:%m:%S')

        print('{} escreveu {}\n'.format(msgContainer.nickName, msgContainer.mensagem))


    #Comando vindo do servidor para fornecer o nick
    def nick(self, msgContainer):
        print('Executando comando nick...')

        timeMensagem  = datetime.datetime.now().strftime('%H:%m:%S')

        resposta = Mensagem(16 + len(''), msgContainer.ipDestino, msgContainer.ipOrigem, self.nickName, 'nick()',
                            self.nickName)

        self.clienteSocket.send(resposta.getMensagemCompleta().encode('utf-8'))


    def enviaMensagem(self, msgContainer):
        dataHora = datetime.datetime.now().strftime('%H:%m:%S')

        msgAEnviar = input('{} - '.format(dataHora))

        msgContainer = Mensagem(16 + len(msgAEnviar), Classes.getNetworkIP(), msgContainer.ipOrigem,
                                self.nickName, 'tela()', msgAEnviar)

        self.clienteSocket.send(msgContainer.getMensagemCompleta().encode('utf-8'))

    def executaComando(self, msgContainer):
        if 'nick' in msgContainer.comando:
            self.nick(msgContainer)

        if 'tela' in msgContainer.comando:
            self.tela(msgContainer)

        if 'sair' in msgContainer.comando:
            self.clienteSocket.close()
