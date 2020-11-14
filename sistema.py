import time #Libreria Tiempo
import threading #Libreria Hilos
import sys
import operator # Libreria para utilizar itemgetter (funcion sorted())
from time import sleep # funcion sleep


# Crea Clase Proceso
class Proceso:
    pid = 0
    tarribo = 0
    prio = 0
    tprocesador = 0
    linea = ''
    arrSplit=[]

    def __init__(self, linea):
        self.arrSplit = linea.split('-')
        self.pid = int(self.arrSplit[0])
        self.tarribo = int(self.arrSplit[1])
        self.prio = int(self.arrSplit[2])
        self.tprocesador = int(self.arrSplit[3])


def fcfs():
    print ("Algoritmo FCFS \n")
    lista = sorted(listaProcesos, key=lambda m:m.tarribo)

    # FCFS?
    for x in range (0,len(lista)):
        z = lista[x]
        print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion a las', time.strftime("%H:%M:%S"))
        print ('\n ---------------------------------------------------- \n')

def sfj():
    print ("Algoritmo SFJ \n")
    lista = sorted(listaProcesos, key=lambda m:m.tprocesador)

    for x in range (0,len(lista)):
        z = lista[x]
        print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion a las', time.strftime("%H:%M:%S"))
        print ('\n ---------------------------------------------------- \n')


def prioridades():
    print ("Algoritmo Prioridades : \n")
    lista = sorted(listaProcesos, key=lambda m:m.prio)

    for x in range (0,len(lista)):
        z = lista[x]
        print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion a las', time.strftime("%H:%M:%S"))
        print ('\n ---------------------------------------------------- \n')



def rr():
    print ("Algoritmo RR \n")
    lista = sorted(listaProcesos, key=lambda m:m.tarribo)

    ## ORDENACION POR TIEMPO DE ARRIBO
    listatarribo = sorted(listaProcesos, key=lambda m:m.tarribo)

    print("Orden de procesos por tarribo (segunda columna): ")
    for x in range (0,len(listatarribo)):
        z =listatarribo[x]
        print(z.pid, z.tarribo, z.prio, z.tprocesador)

    print("--deberia ser 3 1 6 7 9--")

    q = int(input("Elige un Quantum: "))
    # FCFS?
    while len(lista) != 0:
        z = lista.pop(0)
        print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
        print ('El proceso ',z.pid ,'se esta ejecutando ... Tiene un tiempo de ',z.tprocesador, ' segundos')
        if q >= z.tprocesador:
            time.sleep (z.tprocesador)
            print ('El proceso ',z.pid, ' termino su ejecucion ... a las ', time.strftime("%H:%M:%S") )
        else:
            time.sleep (q)
            z.tprocesador -=  q
            lista.append(z)
            print ('El proceso ', z.pid , 'Le queda ',z.tprocesador, ' segundos') 
        print ('\n ---------------------------------------------------- \n')


        

def pedirNumeroEntero():
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Elige una opcion: "))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')
    return num

# MENU DEL PROGRAMA

def menu():
    salir = False
    while not salir:
        print ("1. FCFS")
        print ("2. SFJ S/ Desalojo")
        print ("3. Prioridad S/ Desalojo")
        print ("4. RR")
        print ("5. Salir")
    
        opcion = pedirNumeroEntero()
    
        if opcion == 1:
            fcfs()
        elif opcion == 2:
            sfj()
        elif opcion == 3:
            prioridades()
        elif opcion == 4:
            rr()
        elif opcion == 5:
            salir = True
        else:
            print ("Introduce un numero entre 1 y 5")

# CARGA EL TXT
def cargaProcesos():
    
    # Asigna valor al n
    f = open ("procesos.txt" , 'r')
    n = (len(f.readlines()))
    f.close()

    # Llena la clase proceso con valores del TXT

    f = open ("procesos.txt" , 'r')
    linea = f.readline()
    for i in range (0,n):
        listaProcesos.append(Proceso(linea))
        linea = f.readline()
    f.close()


# MAIN

listaProcesos = []
listaPid = []
listatarribo = []
listaprio = []
listatprocesador = []


cargaProcesos()
menu ()

'''
# MUESTRA
# Lista completa sin orden
for x in range (0,len(listaProcesos)):
    z = listaProcesos[x]
    print(z.pid,z.tarribo,z.prio,z.tprocesador)

## ORDENACION POR PID
listaPid = sorted(listaProcesos, key=lambda m:m.pid)

print("Orden de procesos por pid(primera columna): ")
for x in range (0,len(listaPid)):
    z =listaPid[x]
    print(z.pid, z.tarribo, z.prio, z.tprocesador)

print("--deberia ser 1 3 6--------------")

print()
print("----------------")

## ORDENACION POR TIEMPO DE ARRIBO
listatarribo = sorted(listaProcesos, key=lambda m:m.tarribo)

print("Orden de procesos por tarribo (segunda columna): ")
for x in range (0,len(listatarribo)):
    z =listatarribo[x]
    print(z.pid, z.tarribo, z.prio, z.tprocesador)

print("--deberia ser 3 1 6--------------")

print()
print("----------------")

## ORDENACION POR PRIORIDAD
listaprio = sorted(listaProcesos, key=lambda m:m.prio)

print("Orden de procesos por prio (tercera columna): ")
for x in range (0,len(listaprio)):
    z =listaprio[x]
    print(z.pid, z.tarribo, z.prio, z.tprocesador)

print("--deberia ser 6 3 1--------------")

print()
print("----------------")

## ORDENACION POR TIEMPO DE PROCESADOR
listatprocesador = sorted(listaProcesos, key=lambda m:m.tprocesador)

print("Orden de procesos por tprocesador (cuarta columna): ")
for x in range (0,len(listatprocesador)):

    print(listatprocesador[x].pid, listatprocesador[x].tarribo, listatprocesador[x].prio, listatprocesador[x].tprocesador)

print("--deberia ser 1 6 3--------------")  '''



 






















# //////////////////////////////////////////////////////////////////
#                   Comentarios / Consignas para el tp


# Requisitos Generales

# - No se desarrollarán interfaces de usuario, el programa se ejecuta desde la terminal
# - La configuración del sistema operativo a simular se indica a través de flags o parámetros del sistema.
# - Los resultados de la simulación deben imprimirse por pantalla y además guardarse en un archivo.
# - Aquellas cuestiones no especificadas explícitamente, quedan a consideración del alumno.

# Requisitos Simulacion

# - Todos los tiempos se miden en segundos. // quantum
# - La memoria es infinita.
# - Ante cualquier conflicto entre procesos (por ejemplo, dos con igual prioridad) se debe dar prioridad según FCFS.
# - La prioridad 1 es la mayor y la N es la menor.
# - No se realizan llamadas al sistema por I/O de un proceso.
# - Se desconoce (no se requiere) la propiedad usuario de los procesos.
# - Los procesos del sistema operativo a simular se identifican por un código y cuentan con una serie de atributos.
# Estos valores se ingresan al sistema por medio de un archivo de extensión txt cuyo nombre se debe solicitar al inicio 
# de la ejecución delsimulador.
# - Si se están utilizando threads, los mismos podrán acceder al archivo de procesos o imprimir la terminal de a uno.

# Usar funcion time ejemplo

# print ('Hoy es -', time.ctime(), time.time())