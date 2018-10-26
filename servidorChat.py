import socket
import threading
from Classes import Cliente, Mensagem

class ServidorChat:
#Atributos
    host = socket.gethostbyname(socket.gethostname())

#Métodos
    #Construtor
    def __init__(self, clientes=[], salas=[]):
        self.clientes = clientes
        self.salas = salas

    #Cria conexão
    def abreSala(self, bufferSize=1024):

        #Criação do socket
        conexPorta = 2000
        salaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket TCP

        #Tenta fazer a ligação do socket
        try:
            salaSocket.bind(('', conexPorta))
        except:
            print('Falha na ligação!')


        salaSocket.listen()
        msgOnline = "Servidor online!\nSala Geral aberta e esperando conexões na porta %d" % (conexPorta)
        print(msgOnline)

        #Retorna o socket de conexão à sala
        return salaSocket

    def manipulaMsg(self, msg=Mensagem()):
        componentes = msg.getMensagemCompleta().split(b'\0')

        msg = componentes[:-1]
        resto = componentes[-1]

        return (msg, resto)

    def recebeMsgs(self, dados=bytes()):
        '''
        Função para enviar uma mensagem a um cliente
        :param mensagem: Objeto do tipo Mensagem
        :return:
        '''



    def adicionaCliente(self, cliente):
        self.clientes.append(cliente)

    def deletaCliente(self, cliente):
        self.clientes.remove(cliente)







