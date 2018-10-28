import ifaddr


'''
Classe Cliente
'''

class Cliente:
    def __init__(self, nick, ip, porta):
        self.nickName = nick
        self.ip = ip
        self.porta = porta

    def getCliente(self):
        return '{}\0{}\0{}\0'.format(self.ip, self.porta, self.nickName)

'''
Class Mensagem
'''
class Mensagem:
    def __init__(self, tam=0, origem='', destino='', nick='', comando='', mensagem=''):
        self.tamahoMensagem = tam
        self.ipOrigem = origem
        self.ipDestino = destino
        self.nickName = nick
        self.comando = comando
        self.mensagem = mensagem

    def getMensagemCompleta(self):
        return '{}\0{}\0{}\0{}\0{}\0{}\0'.format(
            self.tamahoMensagem,
            self.ipOrigem,
            self.ipDestino,
            self.nickName,
            self.comando,
            self.mensagem
        )



#Obtém ip da interface de rede usada
def getNetworkIP():
    ip = ''
    #Coleta dados sobre os adaptadores de rede
    adapters = ifaddr.get_adapters()

    #lista que irá conter os ips dos adaptadores de rede do dispositivo
    lista = []

    for adapt in adapters:
        for objIP in adapt.ips:

            #Adiciona os ips à lista de ips
            lista.append(objIP.ip)

    #Busca o ip da interface de rede usada para conexão eliminando o localhost
    for itemIP in lista:
        if isinstance(itemIP, tuple):
            continue
        else:
            if itemIP.find('127'):
                ip = itemIP
                break

    #Retorna o ip da interface de rede
    return ip

# Cria objeto do tipo Mensagem com a string recebida
def desempacotaMensagem(mensagem):
# Cria lista com a mensagem , separando pelo caractere nulo
    itens = mensagem.split(b'\0')

    # Cria objeto do tipo Mensagem e popula com itens da lista
    objMsg = Mensagem()
    objMsg.tamahoMensagem = itens[0]
    objMsg.ipOrigem = itens[1]
    objMsg.ipDestino = itens[2]
    objMsg.nickName = itens[3]
    objMsg.comando = itens[4]
    objMsg.mensagem = itens[5]

    return objMsg