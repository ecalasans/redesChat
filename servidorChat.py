import socket
import threading
from Classes import Cliente, Mensagem

class ServidorChat:
    #Atributos
    clientes = {} #Sockets de clientes conectados
    enderecos = {} #Endereços dos clientes conectados(key:socket de cliente, value:endereco)

    #CONSTANTES
    HOST = ''
    BUFFERSIZE = 1024
    PORTA_SERVIDOR = 2018
    ENDERECO = (HOST, PORTA_SERVIDOR)


#Métodos
    #Construtor
    def __init__(self, clientes={}, enderecos=[]):
        self.clientes = clientes
        self.enderecos = enderecos

    #Cria conexão
    def onlineServidor(self):

        #Criação do socket
        servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket TCP

        #Tenta fazer a ligação do socket
        try:
            servSocket.bind(self.ENDERECO)
        except:
            print('Falha na ligação!')


        #Coloca o servidor em modo de escuta
        servSocket.listen(100)  #Máximo de 100 conexões
        msgOnline = "Servidor online!\nSala Geral aberta e esperando conexões na porta %d" % (self.PORTA_SERVIDOR)
        print(msgOnline)

        #Loop onde o servidor maneja as conexões dos clientes, atualizando as listas e
        #requistando o nickname
        while True:
            clienteSocket, clienteEndereco = servSocket.accept()
            print('{}:{} conectou-se!'.format(clienteEndereco))

            #Solicita o nick ao cliente
            clienteSocket.send('Digite seu nick:  '.encode('utf-8'))

            #Adiciona o endereco do cliente ao dicionário
            self.enderecos[clienteSocket] = clienteEndereco

            #thread para manipular um cliente
            threadCliente = threading.Thread(target=self.manipulaCliente, args=(clienteSocket,)).start()


    def manipulaCliente(self, cliente):
        #Recebe o nick do cliente
        nick = cliente.recv(self.BUFFERSIZE).decode('utf-8')

        #Responde ao cliente após receber o nick
        cliente.send('Bem-vindo, {}!  Digite \'sair\' para encerrar a conexão!'.format(nick).encode('utf-8'))

        #Alerta a todos sobre a conexão
        self.mensBroadcast('{} conectou-se'.format(nick).encode('utf-8'))

        #Adiciona o nick ao dicionário de clientes
        self.clientes[cliente] = nick

        #Loop para transmissão das mensagens para todos os clientes
        while True:
            msgCliente = cliente.recv(self.BUFFERSIZE)

            #Se o comando for sair, encerra a conexão e avisa a todos
            if msgCliente == 'sair':
                #Envia comando para ser tratado do lado do cliente
                cliente.send('sair'.encode('utf-8'))

                #Desconecta o cliente
                cliente.close()

                #Remove do dicionário de clientes
                del self.clientes[cliente]

                #Avisa aos demais clientes da desconexão
                self.mensBroadcast('{} desconectou-se!'.format(nick), nick)

                #Sai do loop
                break
            else:
                #Segue enviando mensagens para todos os clientes
                self.mensBroadcast(msgCliente,nick)




    def mensBroadcast(self, mensagem, nick):
        #Varre o dicionáriio de clientes e manda a mensagem para todos
        for cliente in self.clientes:
            cliente.send("{} - {}".format(nick, mensagem).encode('utf-8'))







