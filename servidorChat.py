import socket
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
    def abreSalaGeral(self, bufferSize=1024):

        #Criação do socket
        conexPorta = 2000
        salaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket TCP

        try:
            salaSocket.bind(('', conexPorta))
        except:
            print('Falha na ligação!')


        salaSocket.listen()
        msgOnline = "Servidor online!\nSala Geral aberta e esperando conexões na porta %d" % (conexPorta)
        print(msgOnline)


    def adicionaCliente(self, cliente):
        self.clientes.append(cliente)

    def deletaCliente(self, cliente):
        self.clientes.remove(cliente)







