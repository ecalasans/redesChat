import time
import threading

def contador():
    for i in range(0, 1000):
        print(i)
        time.sleep(0.5)


thTeste = threading.Thread(target=contador, daemon=True)
thTeste.start()

while True:
    frase = input('Digite algo:  ')
    print(frase)