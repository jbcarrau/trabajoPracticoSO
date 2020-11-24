import time #Libreria Tiempo
import threading #Libreria Hilos
import sys
import operator # Libreria para utilizar itemgetter (funcion sorted())
from time import sleep # funcion sleep
from operator import itemgetter, attrgetter
from optparse import OptionParser

usage = "usage: %prog [options] arg"
parser = OptionParser(usage=usage)

a_choices = ["fcfs", "sfj", "prioridades", "rr"]
parser.add_option("-a", "--algorithm",
                  action="store", type="choice", choices=a_choices, dest="name", 
                  help = "Define the scheduling method by picking an algorithm of your choice")

parser.add_option("-q", "--quantum", 
                  action="store", type="int", dest="quantum", 
                  help = "Execution Quantum time. Choose wiseley")


                  
# parser.add_option("-t", "--threads", 
#                   action="store", type="int", dest="")

(options, args) = parser.parse_args()
if len(args) != 0:
        parser.error("incorrect number of arguments")


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

# Funciones de los algoritmos (Procesos)
def fcfs(): #El primero que entra, el primero que sale. Se ejecuta el primero en llegar y los demas a medida que llegan estan en una cola.
    print ("Algoritmo FCFS \n")
    lista = sorted(listaProcesos, key=lambda m:m.tarribo)
    t = lista[0].tarribo
    procesador_ocupado = 0
    print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
    for x in range (0,len(lista)):
        z = lista[x]
        tInicio = time.time()
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion a las', time.strftime("%H:%M:%S"))
        tFinal = time.time()
        tTurnaround = (int)(tFinal - tInicio)
        if procesador_ocupado == 0:
            tEsperaCola = 0
        else:
            tEsperaCola = t - z.tarribo
        t += (tTurnaround)
        tEsperaTotal = tEsperaCola # No se utilizan I/O entonces los datos que necesitan finalizacion de I/O es hasta finalizacion de proceso
        tRespuesta = t - z.tarribo # finalizacion primer I/O - tiempo de arribo // => finalizacion proceso - tiempo de arribo
        tTotalUsoP = z.tprocesador # El tiempo total que el proceso tomo uso del procesador
        procesador_ocupado = 1
        print ('\n ---------------------------------------------------- \n')
        listaProcesosReporte.append([z.pid,tTurnaround,tEsperaCola,tEsperaTotal,tRespuesta,tTotalUsoP])
    generarReporteProcesos(listaProcesosReporte)

def sfj(): #Tiene prioridad el de ciclo de CPU mas corto
    print ("Algoritmo SFJ \n")
    lista = sorted(listaProcesos, key=attrgetter('tarribo', 'tprocesador'))
    t = lista[0].tarribo
    procesador_ocupado = 0
    print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
    
    while len(lista) != 0:
        z = lista.pop(0)
        tInicio = time.time()
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion a las', time.strftime("%H:%M:%S"))
        tFinal = time.time()
        tTurnaround = (int)(tFinal - tInicio)
        if procesador_ocupado == 0:
            tEsperaCola = 0
        else:
            tEsperaCola = t - z.tarribo
        t += (tTurnaround)
        tEsperaTotal = tEsperaCola
        tRespuesta = t - z.tarribo 
        tTotalUsoP = z.tprocesador
        procesador_ocupado = 1
        print ('\n ---------------------------------------------------- \n')
        listaProcesosReporte.append([z.pid,tTurnaround,tEsperaCola,tEsperaTotal,tRespuesta,tTotalUsoP])
        lista = sorted(lista, key=lambda m:m.tprocesador)
        while (z.tarribo > t): # si TODOS los tiempos de arribo son mayores, va a ciclar infinito
            x = z
            z = lista.pop(0)
            lista.append(x)
    generarReporteProcesos(listaProcesosReporte)


def prioridades(): # Se ordena por prioridad del proceso
    print ("Algoritmo Prioridades : \n")
    lista = sorted(listaProcesos, key=attrgetter('prio', 'tarribo'))
    t = lista[0].tarribo
    procesador_ocupado = 0
    print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
    for x in range (0,len(lista)):
        z = lista[x]
        tInicio = time.time()
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion a las', time.strftime("%H:%M:%S"))
        tFinal = time.time()
        tTurnaround = (int)(tFinal - tInicio)
        if procesador_ocupado == 0:
            tEsperaCola = 0
        else:
            tEsperaCola = t - z.tarribo
        t += (tTurnaround)
        tEsperaTotal = tEsperaCola
        tRespuesta = t - z.tarribo 
        tTotalUsoP = z.tprocesador
        procesador_ocupado = 1
        print ('\n ---------------------------------------------------- \n')
        listaProcesosReporte.append([z.pid,tTurnaround,tEsperaCola,tEsperaTotal,tRespuesta,tTotalUsoP])
    generarReporteProcesos(listaProcesosReporte)



def rr():
    print ("Algoritmo RR \n")
    lista = sorted(listaProcesos, key=lambda m:m.tarribo)

    q = options.quantum
    print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
    while len(lista) != 0:
        z = lista.pop(0)
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
    #generarReporteProcesos(listaProcesosReporte)
    
# Funcion Hilos (RR)



# Funciones de los reportes

def generarReporteProcesos(listar):
    if (len(listar) != 0):
        file = open("../TrabajoPracticoSO/reporteProcesos.txt", "w")
        file.write(" PID Proceso ||| Tiempo de Turnaround ||| Tiempo de espera en cola de listos ||| Tiempo de espera Total de cada proceso ||| Tiempo de Respuesta ||| Tiempo Total de uso de procesador \n")
        for x in range (0,len(listar)):
            file.write ("\t")
            file.write(str(listar[x][0]))
            file.write ("\t\t\t")
            file.write(str(listar[x][1]))
            file.write ("\t\t\t\t")
            file.write(str(listar[x][2]))
            file.write ("\t\t\t\t\t")
            file.write(str(listar[x][3]))
            file.write ("\t\t\t\t")
            file.write(str(listar[x][4]))
            file.write ("\t\t\t\t")
            file.write(str(listar[x][5]))
            file.write ("\n")
        file.close()
    else:
        print ("No hay datos")

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
listaProcesosReporte = []

cargaProcesos()

if options.name == "fcfs":
    fcfs()
elif options.name == "sfj":
    sfj()
elif options.name == "prioridades":
    prioridades()
elif options.name == "rr":
    rr()