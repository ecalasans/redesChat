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

        except ConnectionError:
            print('Falha na conexão!')

        while True:
            # Recebe a primeira mensagem e verifica se é pra digitar o nick
            msgRecebida = self.clienteSocket.recv(self.BUFFERSIZE).decode('utf-8')

            msgContainer = Classes.desempacotaMensagem(msgRecebida)

            if msgContainer.comando.find('nick') != -1:  # Se o comando for nick
                self.executaComando(msgContainer)
            else:
                self.manipulaMensagem(msgContainer)


    #Recebe a mensagem do servidor e printa na tela
    def manipulaMensagem(self, msgContainer):
        dataHora = datetime.datetime.now().strftime('%H:%m:%S')

        self.executaComando(msgContainer)

        thAEnviar = Thread(target=self.enviaMensagem, args=(msgContainer,), daemon=True)
        thAEnviar.start()


    #Comando vindo do servidor para imprimir mensagens na tela
    def tela(self, msgContainer):

        timeMensagem = datetime.datetime.now().strftime('%H:%m:%S')

        print('{}\n'.format(msgContainer.mensagem))


    #Comando vindo do servidor para fornecer o nick
    def nick(self, msgContainer):
        print('Executando comando nick...')

        timeMensagem  = datetime.datetime.now().strftime('%H:%m:%S')

        nick = input('{}({}) - {}'.format(timeMensagem, msgContainer.nickName, msgContainer.mensagem))

        self.nickName = nick

        resposta = Mensagem(16 + len(''), msgContainer.ipDestino, msgContainer.ipOrigem, nick, 'nick()', nick)

        self.clienteSocket.send(resposta.getMensagemCompleta().encode('utf-8'))


    def enviaMensagem(self, msgContainer):
        dataHora = datetime.datetime.now().strftime('%H:%m:%S')

        msgAEnviar = input('')

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