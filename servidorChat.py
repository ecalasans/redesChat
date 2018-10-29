import socket
import threading
import ifaddr   #Biblioteca para obter dados dos adaptatores de rede(https://pythonhosted.org/ifaddr/)
import Classes
from Classes import Mensagem

from Classes import Cliente, Mensagem

class ServidorChat:
    #CONSTANTES
    HOST = ''
    BUFFERSIZE = 1024
    PORTA_SERVIDOR = 2018
    ENDERECO = (HOST, PORTA_SERVIDOR)
    HOST_INTERFACE_REDE = Classes.getNetworkIP()

#Métodos
    #Construtor
    def __init__(self, clientes, enderecos):
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
        servSocket.listen(10000)  #Máximo de 10000 conexões para simular infinitas conexãoes
        msgOnline = "Servidor online!\nSala Geral aberta e esperando conexões na porta %d" % (self.PORTA_SERVIDOR)
        print(msgOnline)

        #Loop onde o servidor maneja as conexões dos clientes, atualizando as listas e
        #requistando o nickname
        while True:
            clienteSocket, clienteEndereco = servSocket.accept()
            print('{}:{} conectou-se!'.format(clienteEndereco[0], clienteEndereco[1]))

            #Solicita o nick ao cliente
            solNick = Mensagem(str(len('Digite seu nick:  ')),self.HOST_INTERFACE_REDE, clienteEndereco[0],
                               'serv', 'n', 'Digite seu nick:  ')
            clienteSocket.send(solNick.getMensagemCompleta().encode('utf-8'))

            #Adiciona o endereco e porta do cliente ao dicionário
            self.enderecos[clienteSocket] = clienteEndereco

            #thread para manipular um cliente
            threadCliente = threading.Thread(target=self.manipulaCliente, args=(clienteSocket,)).start()


    def manipulaCliente(self, cliente):
        msgContainer = None
        strMensagem = ''
        #Recebe o nick do cliente
        recebidoDoCliente = cliente.recv(self.BUFFERSIZE).decode('utf-8')

        #Extrai o nick enviado
        nick = Classes.desempacotaMensagem(recebidoDoCliente).nickName

        #Responde ao cliente após receber o nick
        strMensagem = 'Bem-vindo, {}!  Digite \'q\' para sair!'.format(nick)
        msgContainer = Mensagem(str(len(strMensagem)), self.HOST_INTERFACE_REDE,
                                     self.enderecos[cliente][0], 'serv', 'p', strMensagem)
        cliente.send(msgContainer.getMensagemCompleta().encode('utf-8'))

        #Alerta a todos sobre a conexão
        strMensagem = '{} conectou-se'.format(nick)
        msgContainer = Mensagem(str(len(strMensagem)), self.HOST_INTERFACE_REDE,
                                     self.enderecos[cliente][0], 'serv', 'p', strMensagem)
        self.mensBroadcast(msgContainer)

        #Adiciona o nick ao dicionário de clientes
        self.clientes[cliente] = cliente

        #Loop para transmissão das mensagens para todos os clientes
        while True:
            msgCliente = cliente.recv(self.BUFFERSIZE).decode('utf-8')

            #Transforma string em
            msgCliente = Classes.desempacotaMensagem(msgCliente)

            #Se o comando for sair, encerra a conexão e avisa a todos
            if msgCliente.comando == 'q':
                #Envia comando para ser tratado do lado do cliente
                strMensagem = 'Servidor enviou o comando \'q\''
                msgContainer = Mensagem(str(len(strMensagem)), self.HOST_INTERFACE_REDE,
                                        self.enderecos[cliente][0], 'serv', 'q', strMensagem)
                cliente.send(msgContainer.getMensagemCompleta().encode('utf-8'))

                #Desconecta o cliente
                cliente.close()

                #Remove do dicionário de clientes
                del self.clientes[cliente]

                #Avisa aos demais clientes da desconexão
                strMensagem = '{} desconectou-se!'.format(nick)
                msgContainer = Mensagem(str(len(strMensagem)), self.HOST_INTERFACE_REDE,
                                        self.enderecos[cliente][0], 'serv', 'q', strMensagem)
                self.mensBroadcast(msgContainer)

                #Sai do loop
                break
            else:
                #Segue enviando mensagens para todos os clientes
                self.mensBroadcast(msgCliente)


    def mensBroadcast(self, mensagem):

        objMensagem = Classes.desempacotaMensagem(mensagem)

        strMensagem =  "{} - {}".format(objMensagem.nickName, objMensagem.mensagem)

        msgContainer = Mensagem(str(len(strMensagem)), self.HOST_INTERFACE_REDE,
                                        objMensagem.ipDestino, 'serv', 'p', strMensagem)

        #Varre o dicionário de clientes e manda a mensagem para todos
        for cliente in self.clientes:
            cliente.send(msgContainer.getMensagemCompleta().encode('utf-8'))







