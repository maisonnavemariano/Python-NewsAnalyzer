#!/usr/bin/python3
import pickle
import countryAnalysis
INPUT = "../db/pickle/map_location2code.p"
COUNTRIES = "../db/pickle/map_country2code.p"
location2code = pickle.load( open(INPUT, "rb"))
country2code = pickle.load(open(COUNTRIES, "rb"))

lista = countryAnalysis.sortByRelevance()
for elem in lista:
    print(elem[0].title)