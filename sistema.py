import time #Libreria Tiempo
import threading #Libreria Hilos
import sys
import operator # Libreria para utilizar itemgetter (funcion sorted())

def fcfs():
    print ("Hola estas en el algoritmo fcfs")

def sfj():
    print ("Hola estas en el algoritmo sfj")

def prioridades():
    print ("Hola estas en el algoritmo de prioridades")

def rr():
    print ("Hola estas en el algoritmo Round Robin")

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

# LEE EL TXT Y CARGA LA LISTA CON LOS DATOS DE LOS PROCESOS 
 
def cargaLista(lista):
    f = open ("procesos.txt" , 'r')
    n = (len(f.readlines()))
    f.close()
    f = open ("procesos.txt" , 'r')
    linea = f.readline()
    for i in range (0,n):
        pid = linea.split('-')[0]
        tarribo = int(linea.split('-')[1])
        prio = int(linea.split('-')[2])
        tprocesador = int(linea.split('-')[3].strip())
        listaProcesos.append([pid,tarribo,prio,tprocesador])
        linea = f.readline()
    f.close()


# MAIN

listaProcesos = []
cargaLista(listaProcesos)
print (listaProcesos)
print ("Lista ordenada")
lista = sorted(listaProcesos, reverse = False, key = operator.itemgetter(2)) #ordena pero tiene error con numeros >2 cifras (Pasar lista a enteros?)
print (lista)


 






















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