#!/usr/bin/python3
import json
import requests
import sys
from time import sleep
OUTPUT = "../db/noticias/"
INSTANCE_NRO = "instanceNro: "
TITLE = "webTitle: "
SECTION = "sectionName: "
HEADLINE = "headline: "
TRAILTEXT = "trailText: "
DATE = "webPublicationDate: "
BODY = "bodytext: "

month = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
starts_dates = ["2013-01-01","2013-02-01","2013-03-01","2013-04-01","2013-05-01","2013-06-01","2013-07-01","2013-08-01","2013-09-01","2013-10-01","2013-11-01","2013-12-01"]
end_date = ["2013-01-31","2013-02-28","2013-03-31","2013-04-30","2013-05-31","2013-06-30","2013-07-31","2013-08-31","2013-09-30","2013-10-31","2013-11-30","2013-12-31"]
page_size = 50
current_page = 1
api_key = "5c622da5-f682-49f4-aaa5-a3d5e014b416"


URL = 'http://content.guardianapis.com/search?from-date={0}&to-date={1}&show-fields=all&page-size={2}&page={3}&api-key={4}'

for current_month in range(4,12):
    nro_instancia = 0
    current_page = 1
    print("mes actual: "+str(month[current_month]))
    writer = open(OUTPUT+month[current_month], "w")
    url  = URL.format(starts_dates[current_month], end_date[current_month], page_size, current_page,api_key)
    response = requests.get(url)
    print(response)
    json_response = response.json()
    CANT_PAG = int(json_response['response']['pages'])
    print("cantidad de paginas: "+str(CANT_PAG))
    for current_page in range(1,CANT_PAG+1):
        print("Pagina actual: "+str(current_page)+"/"+str(CANT_PAG))
        sys.stdout.write("\033[F")
        url = URL.format(starts_dates[current_month], end_date[current_month], page_size, current_page, api_key)
        print("URL consultada: "+url)
        sys.stdout.write("\033[F")
        response = requests.get(url)
        json_response = response.json()
        for noticia in json_response['response']['results']:
            sectionName = noticia['sectionName']
            date = noticia['webPublicationDate']
            webTitle = noticia['webTitle']
            headline = noticia["fields"]["headline"]
            trailText = noticia["fields"]["trailText"]
            bodyText = noticia["fields"]["body"]
            writer.write(INSTANCE_NRO+str(nro_instancia)+"\n")
            writer.write(TITLE+webTitle+"\n")
            writer.write(SECTION+sectionName+"\n")
            writer.write(HEADLINE+headline+"\n")
            writer.write(TRAILTEXT+trailText+"\n")
            writer.write(DATE+date+"\n")
            writer.write(BODY+bodyText+"\n")
            nro_instancia = nro_instancia + 1
        sleep(0.01)  # Time in seconds.
    writer.close()