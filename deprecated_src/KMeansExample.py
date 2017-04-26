#!/usr/bin/python3

from scipy.cluster.vq import kmeans2
import numpy as np



INPUT_CSV = "../db/observations_kmeans/obs.csv"
def long_archivo(fname):
    i = 0
    with open(fname) as f:
        for line in f:
            if len(line)>1:
                i = i +1
    return i



instanceNro = -1
cant_instancias = long_archivo(INPUT_CSV) - 1

with open(INPUT_CSV) as f:
    for line in f:
        if len(line)>1:
            if instanceNro == -1:
                cant_dimensiones = len(line[:-1].split(","))
                observations = np.zeros(shape=(cant_instancias, cant_dimensiones))
                instanceNro = 0
            else:
                attribute_nro = 0
                for attrib in line[:-1].split(","):
                    observations[instanceNro][attribute_nro] = float(attrib)
                    attribute_nro = attribute_nro + 1
                instanceNro = instanceNro + 1

for row in observations:
    line = ""
    for element in row:
        line = line + str(element) + " "
    print(line)

resultado = kmeans2(observations,2)
print(resultado[1])
