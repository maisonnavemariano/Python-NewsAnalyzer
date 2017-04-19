#!/usr/bin/python3

#imports
import math

# INPUTs
cant_instancias_mayor_cluster = 300 #121
cant_instancias               = 1689 #1689

instancias_acumuladas = 0
nro_cluster = 0
string_suma = ""
valores = []
while instancias_acumuladas < cant_instancias:
    nro_cluster = nro_cluster + 1
    valores.append(math.ceil((cant_instancias_mayor_cluster/nro_cluster)))
    string_suma = string_suma + str(valores[-1]) + " + "
    instancias_acumuladas = instancias_acumuladas + valores[-1]

#i = 0
#sum =0
#for i in range (1,218):
#    sum = sum + valores[i]
#print("primer 20%: "+str(sum))

print(" * *  * *  * *  * *  * *  Respetando la distribucion * *  * *  * *  * *  * * ")
print("suma: "+string_suma[:-3])
print("instancias acumuladas: "+str(instancias_acumuladas))
print("cantidad de clusters necesarios: "+str(nro_cluster))

# BASADO EN EL 80-20

cant_instancias80_porciento = cant_instancias * 0.80


instancias_acumuladas = 0
nro_cluster = 0
valores = []
while(instancias_acumuladas < cant_instancias80_porciento):
    nro_cluster = nro_cluster+1
    valores.append(math.ceil((cant_instancias_mayor_cluster/nro_cluster)))
    instancias_acumuladas = instancias_acumuladas + valores[-1]

cant_total_clusters = cant_instancias - cant_instancias80_porciento +nro_cluster
print(" * *  * *  * *  * *  * *  Respetando el 80-20  * *  * *  * *  * *  * * ")
print("cantidad de clusters para cubrir el 80% de las instancias (1351): "+ str(nro_cluster))
print("cantidad de clusters total: "+str(cant_total_clusters))
print("cantidad de clusters teoricos: "+str(nro_cluster/0.2))


cant_instancias_mayor_cluster = 50
for cant_instancias_mayor_cluster in range (10,500):
    print("frec mas alta: "+str(cant_instancias_mayor_cluster))
    instancias_acumuladas = 0
    nro_cluster = 0
    while instancias_acumuladas < cant_instancias:
        nro_cluster = nro_cluster + 1
        instancias_acumuladas = instancias_acumuladas + math.ceil((cant_instancias_mayor_cluster / nro_cluster))


    instancias_acumuladas = 0
    nro_cluster_necesarios = nro_cluster
    nro_cluster = 0
    while (instancias_acumuladas < cant_instancias80_porciento):
        nro_cluster = nro_cluster + 1
        instancias_acumuladas = instancias_acumuladas + math.ceil((cant_instancias_mayor_cluster / nro_cluster))
    nro_cluster_teorico = nro_cluster/0.2
    print("clusters necesarios: "+str(nro_cluster_necesarios))
    print("clusters teoricos: "+str(nro_cluster_teorico))
