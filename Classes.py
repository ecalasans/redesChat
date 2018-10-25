'''
Classe Cliente
'''

class Cliente:
    def __init__(self, nick, ip, porta):
        self.nickName = nick
        self.ip = ip
        self.porta = porta

    def getCliente(self):
        return (self.ip, self.nickName, self.porta)

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
        return (self.tamahoMensagem, self.ipOrigem, self.ipDestino, self.nickName, self.comando, self.mensagem)