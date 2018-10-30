import socket
import threading
import datetime
import Classes



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
        self.clientes = {}
        self.enderecos = {}


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
        try:
            servSocket.listen(10000)  #Máximo de 10000 conexões para simular infinitas conexãoes
            msgOnline = "Servidor online e esperando conexões na porta %d" % (self.PORTA_SERVIDOR)
        except:
            msgOnline = "Servidor offline!"

        print(msgOnline)

        #Loop onde o servidor maneja as conexões dos clientes, atualizando as listas e
        #requistando o nickname
        while True:
            clienteSocket, clienteEndereco = servSocket.accept()
            print('{}:{} conectou-se!'.format(clienteEndereco[0], clienteEndereco[1]))

            #Solicita o nick ao cliente
            solNick = Mensagem(str(16 + len('Digite seu nick:  ')), self.HOST_INTERFACE_REDE, clienteEndereco[0],
                               'serv', 'nick()', 'Digite seu nick:  ')
            clienteSocket.send(solNick.getMensagemCompleta().encode('utf-8'))

            #Adiciona o endereco e porta do cliente ao dicionário
            self.enderecos[clienteSocket] = clienteEndereco

            #thread para manipular um cliente
            threadCliente = threading.Thread(target=self.manipulaCliente, args=(clienteSocket,)).start()


    def manipulaCliente(self, clienteSocket):
        print('Executando manipulaCliente...')
        msgContainer = None
        strMensagem = ''

        #Recebe o nick do cliente
        recebidoDoCliente = clienteSocket.recv(self.BUFFERSIZE).decode('utf-8')

        #Extrai o nick enviado
        nick = Classes.desempacotaMensagem(recebidoDoCliente).nickName

        #Responde ao cliente após receber o nick
        strMensagem = 'Bem-vindo, {}!  Digite \'sair()\' para sair!'.format(nick)
        msgContainer = Mensagem(str(16 + len(strMensagem)), self.HOST_INTERFACE_REDE,
                                     self.enderecos[clienteSocket][0], 'serv', 'tela()', strMensagem)
        clienteSocket.send(msgContainer.getMensagemCompleta().encode('utf-8'))

        #Alerta a todos sobre a conexão
        strMensagem = '{} conectou-se'.format(nick)
        msgContainer = Mensagem(str(16 + len(strMensagem)), self.HOST_INTERFACE_REDE,
                                     self.enderecos[clienteSocket][0], 'serv', 'tela()', strMensagem)

        # Adiciona o nick ao dicionário de clientes
        self.clientes[clienteSocket] = nick

        self.mensBroadcast(msgContainer)


        #Loop para transmissão das mensagens para todos os clientes
        while True:
            msgCliente = clienteSocket.recv(self.BUFFERSIZE).decode('utf-8')

            objMensagem = Classes.desempacotaMensagem(msgCliente)

            '''
            #Se o comando for sair, encerra a conexão e avisa a todos
            if msgCliente.comando == 'q':
                #Envia comando para ser tratado do lado do cliente
                strMensagem = 'Servidor enviou o comando \'sair()\''
                msgContainer = Mensagem(str(16 + len(strMensagem)), self.HOST_INTERFACE_REDE,
                                        self.enderecos[clienteSocket][0], 'serv', 'sair()', strMensagem)
                clienteSocket.send(msgContainer.getMensagemCompleta().encode('utf-8'))

                #Desconecta o cliente
                clienteSocket.close()

                #Remove do dicionário de clientes
                del self.clientes[clienteSocket]

                #Avisa aos demais clientes da desconexão
                strMensagem = '{} desconectou-se!'.format(nick)
                msgContainer = Mensagem(str(16 + len(strMensagem)), self.HOST_INTERFACE_REDE,
                                        self.enderecos[clienteSocket][0], 'serv', 'sair()', strMensagem)
                self.mensBroadcast(msgContainer)

                #Sai do loop
                break
            else:
                #Segue enviando mensagens para todos os clientes
                self.mensBroadcast(msgCliente)

                self.tela(msgCliente)
            '''

    def mensBroadcast(self, mensagem):

        #objMensagem = Classes.desempacotaMensagem(mensagem)

        strMensagem = "{} - {}".format(mensagem.nickName, mensagem.mensagem)

        msgContainer = Mensagem(str(16 + len(strMensagem)), self.HOST_INTERFACE_REDE,
                                        mensagem.ipDestino, 'serv', 'tela()', strMensagem)

        #Varre o dicionário de clientes e manda a mensagem para todos
        for cliente in self.clientes:
            cliente.send(msgContainer.getMensagemCompleta().encode('utf-8'))
#TODO: PEGAR A KEY DE CLIENTES

    def lista(self, nick):
        strClientes = ''

        destino = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for key, value in self.clientes.items():
            if value == nick:
                destino = key

        for cliente in self.clientes.values():
            strClientes = strClientes + '{}_'.format(cliente)

        strMensagem = strClientes

        destinoIP = self.enderecos[destino][0]

        msgContainer = Mensagem(str(16 + len(strMensagem)), self.HOST_INTERFACE_REDE,
                                destinoIP, 'serv', 'lista()', strMensagem)

        destino.send(msgContainer.getMensagemCompleta().encode('utf-8'))

    def nick(self, nick, ipCliente):
        #Varre os enderecos procurando o socket do cliente
        for socCliente, enderecoCliente in self.enderecos.items():

            #Se o ip fornecido for encontrado troca o nick para o referido socket
            if ipCliente == enderecoCliente[0]:
                velhoNick = self.clientes[socCliente]
                self.clientes[socCliente] = nick

                strMensagem = "{} agora é conhecido como {}".format(velhoNick, self.clientes[socCliente])

                msgContainer = Mensagem(str(16 + len(strMensagem)), self.HOST_INTERFACE_REDE,
                                    enderecoCliente[0], 'serv', 'tela()', strMensagem)

                self.mensBroadcast(msgContainer.getMensagemCompleta())

            else:
                continue

    def tela(self, mensagem):
        mensTela = Classes.desempacotaMensagem(mensagem)

        timeMensagem = datetime.datetime.now().strftime('%H:%m:%S')

        return print('{}({}) - {}'.format(timeMensagem, mensTela.nickName, mensTela.mensagem))


    #Encerra a conexão de todos os clientes
    def sair(self):

        strMensagem = 'Servidor encerrado!  Você foi desconectado'

        for cliente in self.enderecos.items():
            msgContainer = Mensagem(str(16 + len(strMensagem)), self.HOST_INTERFACE_REDE,
                                    cliente[0], 'serv', 'tela()', strMensagem)
            cliente[0].close()



    #Seleciona e executa os comandos vindos do cliente
    def executaComandos(self, mensagem):

        msgContainer = Classes.desempacotaMensagem(mensagem)

        if 'tela' in msgContainer.comando:
            self.tela(mensagem)

        if msgContainer.mensagem.find('nick') != -1:
            self.nick(msgContainer.nickName, msgContainer.ipOrigem)

        if msgContainer.mensagem.find('lista') != -1:
            self.lista(msgContainer.nickName)





