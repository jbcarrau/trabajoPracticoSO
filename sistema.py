import time #Libreria Tiempo
import threading #Libreria Hilos

archivo = urllib.urlopen('https://github.com/franbenettini/TrabajoPracticoSO/blob/main/procesos.txt%27')
print (f.read())
f.close()

'''
# Intento prueba de RR // falta usar el Quantum // Faltan datos de los procesos y entrada por TXT entre otras cosas
n = int (input ("Cuantos procesos son? "))
tuso = [] #tiempo de uso
tespera = [0,0,0,0,0,0,0,0,0] # tiempo de espera
trespuesta = [0,0,0,0,0,0,0,0,0,0] #turn around time
q = int (input ("Que quantum usar para los procesos? ")) #quantum medidos en segundos

#datos entrada
for i in range (0,n):
    tuso.append(int(input(f"Tiempo de uso para el proceso {i} ->")))

# tiempo de espera
for i in range (1,n):
    tespera[i] = 0
    for j in range (0,i):
        tespera[i] += tuso[i]

#tiempo de respuesta
for i in range (0,n):
    trespuesta[i] = tuso[i] + tespera[i]

print ()
print ("El quantum es de: ", q , "segundos")
print ("\tProceso\t\tTiempo en uso\t\tTiempo de espera\t\tTurn around time")
for i in range (0,n):
    print (f"\t  P[{i}]\t\t\t {tuso[i]}\t\t\t {tespera[i]}\t\t\t\t {trespuesta[i]}")



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
'''