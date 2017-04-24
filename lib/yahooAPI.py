#Consumer_Key    = "    dj0yJmk9M0dweTdFRnRvUEZNJmQ9WVdrOVRqTXlibFJLTjJjbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1kNg--"
#Consumer_Secret = "7e559bd574335333f51185ca519e8fea987f39b3"

import httplib2
import json

#{"query":{"count":0,"created":"2013-01-11T18:39:21Z","lang":"en-US","results":null}}


def validPlace(place):
    url = "http://query.yahooapis.com/v1/public/yql?q=select%20%2a%20from%20geo.places%20where%20text='"+place+"'&format=json"
    resp, content = httplib2.Http().request(url)
    print(str(content)[2:-1])
    wjdata = json.loads(str(content)[2:-1])
    if wjdata["query"]["results"]==None:
        return False
    else:
        return True

