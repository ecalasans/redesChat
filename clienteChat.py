import socket
import threading

class ClienteChat():
    ip = ''
    nick = ''
    porta = 0

    clienteSocket = None

    BUFFERSIZE = 1024

    def __init__(self, ip='', nick='', porta=0):
        self.ip = ip
        self.nick = nick
        self.porta = porta

    def abreConexao(self, destino, porta):
        #Cria conexão
        try:
            self.clienteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clienteSocket.connect((destino, porta))
        except ConnectionError:
            print('Falha na conexão!')

        while True:
            self.recebeMensagem()

    def recebeMensagem(self):
        #Loop infinito para ficar recebendo as mensagens
        while True:
            try:
                msgRecebida = self.clienteSocket.recv(self.BUFFERSIZE).decode('utf-8')
                print('{}:{} - {}'.format(msgRecebida))
            #Caso o cliente tenha desconectado do chat
            except OSError:
                break


    def fechaConexao(self):
        self.clienteSocket.close()