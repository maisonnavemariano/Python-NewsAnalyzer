#!/usr/bin/python3

import pickle

CONFIG = "../etc/var.config"

IGNORE_LOCATION_WITH_SPACES = "IGNORE_LOCATION_WITH_SPACES = "

def initVar():
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(IGNORE_LOCATION_WITH_SPACES):
                ignore_location_with_spaces = line[len(IGNORE_LOCATION_WITH_SPACES):-1] == "True"
    return ignore_location_with_spaces

country2code = {}
location2code = {}

LOCATIONS = "../db/paises/allCountries.txt"
COUNTRY_INFO = "../db/paises/countryInfo.txt"

MAPEO_PAISES = "../db/pickle/map_country2code.p"
MAPEO_LOCACIONES = "../db/pickle/map_location2code.p"

print("Generando mapeos.")
ignoreLocationsWithSpaces = initVar()
countries_count = 0
todos_los_codigos = set()
with open(COUNTRY_INFO) as f:
    for line in f:
        if not line.startswith("#"):
            countries_count = countries_count +1
            parts = line[:-1].split("\t")
            codigo = parts[0]
            pais = parts[4].lower()
            todos_los_codigos.add(codigo)

            country2code[pais] = codigo

with open(LOCATIONS) as f:
    for line in f:
        parts = line[:-1].split("\t")
        code = parts[8]

        name = parts[1].lower()
        if code in todos_los_codigos and (not(" "in name and ignoreLocationsWithSpaces)):
            location2code[name] = code

pickle.dump(country2code, open(MAPEO_PAISES, "wb"))
pickle.dump(location2code, open(MAPEO_LOCACIONES, "wb"))
print("mapeo locacion a codigo pais, tamanio: "+str(len(location2code))+" almacenado en: "+MAPEO_LOCACIONES)
print("mapeo pais a codigo pais, tamanio: "+str(len(country2code))+" almacenado en: "+MAPEO_PAISES)

# The main 'geoname' table has the following fields :
# ---------------------------------------------------
# geonameid         : integer id of record in geonames database
# name              : name of geographical point (utf8) varchar(200)
# asciiname         : name of geographical point in plain ascii characters, varchar(200)
# alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
# latitude          : latitude in decimal degrees (wgs84)
# longitude         : longitude in decimal degrees (wgs84)
# feature class     : see http://www.geonames.org/export/codes.html, char(1)
# feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
# country code      : ISO-3166 2-letter country code, 2 characters
# cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
# admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
# admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
# admin3 code       : code for third level administrative division, varchar(20)
# admin4 code       : code for fourth level administrative division, varchar(20)
# population        : bigint (8 byte int)
# elevation         : in meters, integer
# dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
# timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
# modification date : date of last modification in yyyy-MM-dd format