#!/usr/bin/python3
import pickle
INPUT = "../db/pickle/map_location2code.p"
COUNTRIES = "../db/pickle/map_country2code.p"
location2code = pickle.load( open(INPUT, "rb"))
country2code = pickle.load(open(COUNTRIES, "rb"))
cant_locaciones = 0
locations_with_spaces= 0
for location in location2code:
    cant_locaciones = cant_locaciones+1
    if " " in location:
        locations_with_spaces = locations_with_spaces +1
print("cantidad de locaciones con espacios: "+str(locations_with_spaces))
print("cantidad de locaciones en total: "+str(cant_locaciones))
print("cantidad de locaciones evalidas: "+str(cant_locaciones-locations_with_spaces))

paises_contenidos_en_locations = 0
paises_no_contenidos_en_locations = 0
paises_con_espacio = 0
for country in country2code:
    if " " in country :
        paises_con_espacio = paises_con_espacio +  1
    if country in location2code:
        paises_contenidos_en_locations = paises_contenidos_en_locations +1
    else:
        paises_no_contenidos_en_locations = paises_no_contenidos_en_locations +1

print("paises contenidos en locaciones: " + str(paises_contenidos_en_locations))
print("paises no contenidos en locaciones: "+str(paises_no_contenidos_en_locations))
print("paises con espacio: "+str(paises_con_espacio))