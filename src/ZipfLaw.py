#!/usr/bin/python3

#imports
import math

# INPUTs
cant_instancias_mayor_cluster = 121
cant_instancias               = 1689

instancias_acumuladas = 0
nro_cluster = 0
string_suma = ""
valores = []
while instancias_acumuladas < cant_instancias:
    nro_cluster = nro_cluster + 1
    valores.append(math.ceil((cant_instancias_mayor_cluster/nro_cluster)))
    string_suma = string_suma + str(valores[-1]) + " + "
    instancias_acumuladas = instancias_acumuladas + valores[-1]

i = 0
sum =0
for i in range (1,218):
    sum = sum + valores[i]
print("primer 20%: "+str(sum))

print("suma: "+string_suma[:-3])
print("instancias acumuladas: "+str(instancias_acumuladas))
print("cantidad de clusters necesarios: "+str(nro_cluster))