import ifaddr
import ipaddress
from servidorChat import ServidorChat

'''
adapters = ifaddr.get_adapters()
lista = []

for adapt in adapters:
    for objIP in adapt.ips:
        lista.append(objIP.ip)

for itemIP in lista:
    if isinstance(itemIP, tuple):
        continue
    else:
        if itemIP.find('127'):
            print(itemIP)

clientes = {}
enderecos = {}

servidor = ServidorChat(clientes, enderecos)

servidor.onlineServidor()

'''

clientes = {}
enderecos = {}

servidor = ServidorChat(clientes, enderecos)

servidor.onlineServidor()


