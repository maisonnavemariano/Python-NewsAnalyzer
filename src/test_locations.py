#!/usr/bin/python3
import pickle
INPUT = "../db/pickle/map_location2code.p"

location2code = pickle.load( open(INPUT, "rb"))
cant_locaciones = 0
locations_with_spaces= 0
for location in location2code:
    cant_locaciones = cant_locaciones+1
    if " " in location:
        locations_with_spaces = locations_with_spaces +1
print("cantidad de locaciones con espacios: "+str(locations_with_spaces))
print("cantidad de locaciones en total: "+str(cant_locaciones))
print("cantidad de locaciones evalidas: "+str(cant_locaciones-locations_with_spaces))