#!/usr/bin/python3
import pickle
import countryAnalysis
import re
import datetime
now = datetime.datetime.now()

CONFIG = "../etc/var.config"

def initVar():
    selected_country_const = "SELECTED_COUNTRY = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(selected_country_const):
                selected_country = line[len(selected_country_const):-1]
    return selected_country


OUTPUT = "../db/resultados/rel_pais_{0}_date_{1}.txt"
fecha = re.sub(r'\.[0-9]*', "", str(now))
pais = initVar()

OUTPUT = OUTPUT.format(pais,fecha)


INPUT = "../db/pickle/map_location2code.p"
COUNTRIES = "../db/pickle/map_country2code.p"
location2code = pickle.load( open(INPUT, "rb"))
country2code = pickle.load(open(COUNTRIES, "rb"))

print("cantidad de paises en la lista: "+str(len(country2code)))


writer =  open(OUTPUT, "w")
lista = countryAnalysis.sortByRelevance()
for elem in lista:
    writer.write(elem[0].title+", "+str(elem[1])+"\n")

writer.close()