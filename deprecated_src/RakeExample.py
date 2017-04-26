#!/usr/bin/python3

from deprecated_src import RAKE

Rake = RAKE.Rake("../stopwords/SmartStoplist.txt");
# You can use one of the stoplists included in the repository under stoplists/
with open("../db/EneroFiltrado", 'r') as content_file:
    content = content_file.read()


output = Rake.run(content);
print(output);