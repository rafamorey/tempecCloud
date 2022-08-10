'''
def mi(c,v,*some): # * = tupla ** = diccionario
    print(c * v)
    for ca in some:
        print(ca * v)
mi('Wanda ',5)

def summ(num1,num2):
    return num1 + num2
r = summ(5,0.5)
print(r)

#Multiprocesos

from multiprocessing import Process
import os
import winsound

def funcion(numero):
    x = 0
    print(os.getpid())
    for n in range(10):
        valor = n * n + n
        print(valor, "------>", numero)
        #Proceso Caulquiera
        winsound.Beep(2500,100)
        for n in range(1024):
            x = 0
            for n in range(1024):
                x = x + 1

procesos = []
cores = os.cpu_count()
print("Tienes ", cores, "nucleos")

print("------> Iniciar")
for n in range(cores):
    proceso = Process(target=funcion, args=(n,))
    procesos.append(proceso)

print("----> Ejecutar")
for p in procesos:
    p.start()

for pr in procesos:
    pr.join()

print("------Regteso a la ejecucion Inicial")
'''