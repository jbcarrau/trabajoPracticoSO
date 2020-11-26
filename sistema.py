import time #Libreria Tiempo
import threading #Libreria Hilos
import sys
import operator # Libreria para utilizar itemgetter (funcion sorted())
from time import sleep # funcion sleep
from operator import itemgetter, attrgetter
from optparse import OptionParser
from queue import Queue

q = Queue()

usage = "usage: %prog [options] arg"
parser = OptionParser(usage=usage)

a_choices = ["fcfs", "sfj", "prioridades", "rr","rrthread"]
parser.add_option("-a", "--algorithm",
                  action="store", type="choice", choices=a_choices, dest="name", 
                  help = "Define the scheduling method by picking an algorithm of your choice")

parser.add_option("-q", "--quantum", 
                  action="store", type="int", dest="quantum", 
                  help = "Execution Quantum time. Choose wiseley")


                  
parser.add_option("-t", "--threads", 
                  type="int", dest="thr", help='specify number of threads')

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

# Funciones de los algoritmos (Procesos) funcionan a tiempo real
def fcfs(): #El primero que entra, el primero que sale. Se ejecuta el primero en llegar y los demas a medida que llegan estan en una cola.
    print ("\n Algoritmo FCFS \n")
    lista = sorted(listaProcesos, key=attrgetter('tarribo', 'prio'))
    t = lista[0].tarribo #Tiempo actual
    #print ('Son las : ', time.strftime("%H:%M:%S"), '\n') # Las lineas comentadas seria el uso del algoritmo a tiempo real
    tTurnaroundProm = 0
    tEsperaTotalProcesos = 0
    tRespuestaProm = 0
    trabajos1000 = 0
    n = len(lista)
    for x in range (0,n):
        z = lista[x]
        #tInicio = time.time()
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        #time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion') # a las', time.strftime("%H:%M:%S"))
        #tFinal = time.time()
        if (z.tprocesador >= 1000):
            trabajos1000 += 1
        t += (z.tprocesador)
        tTurnaround = t - z.tarribo
        tEsperaCola = tTurnaround - z.tprocesador
        tTurnaroundProm += tTurnaround
        tEsperaTotal = tEsperaCola # No se utilizan I/O entonces los datos que necesitan finalizacion de I/O es hasta finalizacion de proceso => Tturnaround - tiempo CPU
        tEsperaTotalProcesos += tEsperaTotal
        tRespuesta = t - z.tarribo # finalizacion primer I/O - tiempo de arribo // => finalizacion proceso - tiempo de arribo => Es igual al turnaround
        tRespuestaProm += tRespuesta
        tTotalUsoP = z.tprocesador # El tiempo total que el proceso tomo uso del procesador
        print ('\n ---------------------------------------------------- \n')
        listaProcesosReporte.append([z.pid,tTurnaround,tEsperaCola,tEsperaTotal,tRespuesta,tTotalUsoP])
    tTurnaroundProm = tTurnaroundProm/n
    tRespuestaProm = tRespuestaProm/n
    if (trabajos1000 >= 1):
        trabajos1000 = trabajos1000/n
    listaSistema.append ([tTurnaroundProm,tEsperaTotalProcesos,tRespuestaProm,trabajos1000,0])
    generarReporteProcesos(listaProcesosReporte)
    generarReporteSistema(listaSistema)

def sfj(): #Tiene prioridad el de ciclo de CPU mas corto
    print ("\n Algoritmo SFJ \n")
    lista = sorted(listaProcesos, key=attrgetter('tarribo', 'tprocesador'))
    t = lista[0].tarribo
    #print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
    tTurnaroundProm = 0
    tEsperaTotalProcesos = 0
    tRespuestaProm = 0
    trabajos1000 = 0
    n = len(lista)
    while len(lista) != 0:
        z = lista.pop(0)
        #tInicio = time.time()
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        #time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion')# a las', time.strftime("%H:%M:%S"))
        if (z.tprocesador >= 1000):
            trabajos1000 += 1
        #tFinal = time.time()
        t += (z.tprocesador)
        tTurnaround = t - z.tarribo
        tEsperaCola = tTurnaround - z.tprocesador
        tTurnaroundProm += tTurnaround
        tEsperaTotal = tEsperaCola
        tEsperaTotalProcesos += tEsperaTotal
        tRespuesta = t - z.tarribo 
        tRespuestaProm += tRespuesta
        tTotalUsoP = z.tprocesador
        print ('\n ---------------------------------------------------- \n')
        listaProcesosReporte.append([z.pid,tTurnaround,tEsperaCola,tEsperaTotal,tRespuesta,tTotalUsoP])
        lista = sorted(lista, key=lambda m:m.tprocesador)
        while (len(lista) != 0 and z.tarribo >= t ):
            x = z
            z = lista.pop(0)
            lista.append(x)
    tTurnaroundProm = tTurnaroundProm/n
    tRespuestaProm = tRespuestaProm/n
    if (trabajos1000 >= 1):
        trabajos1000 = trabajos1000/n
    listaSistema.append ([tTurnaroundProm,tEsperaTotalProcesos,tRespuestaProm,trabajos1000,0])
    generarReporteProcesos(listaProcesosReporte)
    generarReporteSistema(listaSistema)


def prioridades(): # Se ordena por prioridad del proceso
    print ("\n Algoritmo Prioridades : \n")
    lista = sorted(listaProcesos, key=attrgetter('tarribo', 'prio'))
    t = lista[0].tarribo
    #print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
    tTurnaroundProm = 0
    tEsperaTotalProcesos = 0
    tRespuestaProm = 0
    trabajos1000 = 0
    n = len(lista)
    while len(lista) != 0:
        z = lista.pop(0)
        tInicio = time.time()
        tEsperaCola = t - z.tarribo
        print ('El proceso ',z.pid ,'se esta ejecutando ...')
        print ()
        #time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, 'termino su ejecucion')# a las', time.strftime("%H:%M:%S"))
        #tFinal = time.time()
        if (z.tprocesador >= 1000):
            trabajos1000 += 1
        t += (z.tprocesador)
        tTurnaround = t - z.tarribo
        tEsperaCola = tTurnaround - z.tprocesador
        tTurnaroundProm += tTurnaround
        tEsperaTotal = tEsperaCola
        tEsperaTotalProcesos += tEsperaTotal
        tRespuesta = t - z.tarribo 
        tRespuestaProm += tRespuesta
        tTotalUsoP = z.tprocesador
        print ('\n ---------------------------------------------------- \n')
        listaProcesosReporte.append([z.pid,tTurnaround,tEsperaCola,tEsperaTotal,tRespuesta,tTotalUsoP])
        lista = sorted(lista, key=lambda m:m.prio)
        while (len(lista) != 0 and z.tarribo >= t ):
            x = z
            z = lista.pop(0)
            lista.append(x)
    tTurnaroundProm = tTurnaroundProm/n
    tRespuestaProm = tRespuestaProm/n
    if (trabajos1000 >= 1):
        trabajos1000 = trabajos1000/n
    listaSistema.append ([tTurnaroundProm,tEsperaTotalProcesos,tRespuestaProm,trabajos1000,0])
    generarReporteProcesos(listaProcesosReporte)
    generarReporteSistema(listaSistema)

def rr():
    lista = sorted(listaProcesos, key=attrgetter('tarribo', 'prio'))
    q = options.quantum
    aux = []
    #print ('Son las : ', time.strftime("%H:%M:%S"), '\n')
    t = lista[0].tarribo
    tTurnaroundProm = 0
    tEsperaTotalProcesos = 0
    tRespuestaProm = 0
    trabajos1000 = 0
    n = len(lista)
    for x in range (0,len(lista)):
        z = lista.pop(0)
        if (z.tprocesador >= 1000):
            trabajos1000 += 1
        aux.append([z.pid,z.tprocesador])
        lista.append(z)
    while len(lista) != 0:
        z = lista.pop(0)
        print ('El proceso ',z.pid ,'se esta ejecutando ... Tiene un tiempo de ',z.tprocesador, ' segundos')
        if q >= z.tprocesador:
            t += z.tprocesador
            #time.sleep (z.tprocesador)
            print ('El proceso ',z.pid, ' termino su ejecucion ')#... a las ', time.strftime("%H:%M:%S") )
            tTurnaround = t - z.tarribo
            tTurnaroundProm += tTurnaround
            tRespuesta = t - z.tarribo 
            tRespuestaProm += tRespuesta
            tEsperaCola =  tTurnaround - z.tprocesador
            tEsperaTotal = tEsperaCola
            tEsperaTotalProcesos += tEsperaTotal
            z.tprocesador = 0
            for i in range (0,len(aux)):
                if(aux[i][0] == z.pid):
                    tTotalUsoP = aux[i][1]
            listaProcesosReporte.append([z.pid,tTurnaround,tEsperaCola,tEsperaTotal,tRespuesta,tTotalUsoP])
        else:
            #time.sleep (q)
            z.tprocesador -=  q
            t += q
            lista.append(z)
            print ('El proceso ', z.pid , 'Le queda ',z.tprocesador, ' segundos') 
        print ('\n ---------------------------------------------------- \n')
    tTurnaroundProm = tTurnaroundProm/n
    tRespuestaProm = tRespuestaProm/n
    if (trabajos1000 >= 1):
        trabajos1000 = trabajos1000/n
    listaSistema.append ([tTurnaroundProm,tEsperaTotalProcesos,tRespuestaProm,trabajos1000,0])
    generarReporteProcesos(listaProcesosReporte)
    generarReporteSistema(listaSistema)
    
# Funcion Hilos (RR)
def threadScan(thr):
    global tiempoRRHilos
    global trabajos1000hilos
    for p in range(thr):
        t = threading.Thread(target=threader, daemon=True).start()
   #Pongo en la queue los procesos que serian los jobs que van a ejecutar los threads
    lista = sorted(listaProcesos, key=attrgetter('tarribo', 'prio'))
    for x in range (0,len(lista)):
        y = lista.pop(0)
        if (y.tprocesador >= 1000):
            trabajos1000hilos += 1
        aux.append([y.pid,y.tprocesador])
        lista.append(y)
    tiempoRRHilos = lista[0].tarribo
    for x in range(0,len(lista)):
        q.put(lista[x])
    q.join()

def threader():
    while True:
        z = q.get()
        rrThread(z)
        q.task_done()

def rrThread(z):
    print_lock = threading.Lock()
    quantum = options.quantum
    lista = sorted(listaProcesos, key=attrgetter('tarribo', 'prio'))
    # while q.full():
        # z = q.get()
    tTurnaroundProm = 0
    tEsperaTotalProcesos = 0
    tRespuestaProm = 0
    n = len(lista)
    global tiempoRRHilos
    global trabajos1000hilos
    print ('El proceso ',z.pid ,'se esta ejecutando ... Tiene un tiempo de ',z.tprocesador, ' segundos')
    if quantum >= z.tprocesador:
        tiempoRRHilos += z.tprocesador
        #time.sleep (z.tprocesador)
        print ('El proceso ',z.pid, ' termino su ejecucion ')#... a las ', time.strftime("%H:%M:%S") )
        tTurnaround = tiempoRRHilos - z.tarribo
        tTurnaroundProm += tTurnaround
        tRespuesta = tiempoRRHilos - z.tarribo 
        tRespuestaProm += tRespuesta
        tEsperaCola =  tTurnaround - z.tprocesador
        tEsperaTotal = tEsperaCola
        tEsperaTotalProcesos += tEsperaTotal
        z.tprocesador = 0
        for i in range (0,len(aux)):
            if(aux[i][0] == z.pid):
                tTotalUsoP = aux[i][1]
        listaProcesosReporte.append([z.pid,tTurnaround,tEsperaCola,tEsperaTotal,tRespuesta,tTotalUsoP])
    else:
        #time.sleep (quantum)
        z.tprocesador -=  quantum
        tiempoRRHilos += quantum
        q.put(z)
        print ('El proceso ', z.pid , 'Le queda ',z.tprocesador, ' segundos') 
    print ('\n ---------------------------------------------------- \n')
    if (q.empty()):
        tTurnaroundProm = tTurnaroundProm/n
        tRespuestaProm = tRespuestaProm/n
        if (trabajos1000hilos >= 1):
            trabajos1000hilos = trabajos1000hilos/n
        listaSistema.append ([tTurnaroundProm,tEsperaTotalProcesos,tRespuestaProm,trabajos1000hilos,thr])
        generarReporteProcesos(listaProcesosReporte)
        generarReporteSistema(listaSistema)

# Funciones de los reportes

def generarReporteProcesos(listar):
    if (len(listar) != 0):
        file = open("../TrabajoPracticoSO/reporteProcesos.txt", "w")
        file.write(" PID Proceso ||| Tiempo de Turnaround ||| Tiempo de espera en cola de listos ||| Tiempo de espera Total de cada proceso ||| Tiempo de Respuesta ||| Tiempo Total de uso de procesador \n")
        print (" PID Proceso |||", "Tiempo de Turnaround |||", "Tiempo de espera en cola de listos |||", "Tiempo de espera Total de cada proceso |||", "Tiempo de Respuesta |||", "Tiempo Total de uso de procesador")
        for x in range (0,len(listar)):
            print ("  ", listar[x][0],"\t\t\t", listar[x][1],"\t\t\t\t", listar[x][2],"\t\t\t\t\t", listar[x][3],"\t\t\t\t  ", listar[x][4],"\t\t\t\t", listar[x][5],"\n")
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

def generarReporteSistema(listar):
    if (len(listar) != 0):
        file = open("../TrabajoPracticoSO/reporteSistema.txt", "w")
        file.write("Tiempo de Turnaround Promedio ||| Tiempo de espera Total de los procesos ||| Tiempo de Respuesta Promedio ||| Cantidad Promedio trabajos realizados cada 1000 seg ||| Cantidad thread utilizados\n")
        for x in range (0,len(listar)):
            file.write ("\t")
            file.write(str(listar[x][0]))
            file.write ("\t\t\t\t\t")
            file.write(str(listar[x][1]))
            file.write ("\t\t\t\t\t")
            file.write(str(listar[x][2]))
            file.write ("\t\t\t\t\t")
            file.write(str(listar[x][3]))
            file.write ("\t\t\t\t\t\t")
            file.write(str(listar[x][4]))
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
listaSistema = []
aux = []

cargaProcesos()
global tiempoRRHilos
global trabajos1000hilos
trabajos1000hilos = 0
thr = options.thr

if options.name == "fcfs":
    fcfs()
elif options.name == "sfj":
    sfj()
elif options.name == "prioridades":
    prioridades()
elif options.name == "rr":
    print ("Algoritmo RR \n")
    if options.quantum is None:
        options.quantum = 2
    print ("QUANTUM : ",options.quantum, "\n")
    rr()
elif options.name == "rrthread":
    if options.quantum is None:
        options.quantum = 2
    if options.thr is None:
        thr = 5
    else:
        thr = options.thr
    print ("Algoritmo RR con hilos\n")
    print ("QUANTUM : ",options.quantum, "\n")
    print ("Se utilizan ",thr , " Hilo/s \n")
    threadScan(thr)
    