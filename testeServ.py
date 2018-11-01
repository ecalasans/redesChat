import ifaddr
import ipaddress
from servidorChat import ServidorChat


clientes = {}
enderecos = {}

servidor = ServidorChat(clientes, enderecos)

servidor.onlineServidor()


