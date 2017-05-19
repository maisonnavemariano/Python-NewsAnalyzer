#!/usr/bin/python3
# leemos archivo nombres nltk:

    # >>> names = nltk.corpus.names
    #>>> names.fileids()
    #['female.txt', 'male.txt']
    # >>> male_names = names.words('male.txt')
    # >>> female_names = names.words('female.txt')
    # >>> [w for w in male_names if w in female_names]
    # ['Abbey', 'Abbie', 'Abby', 'Addie', 'Adrian', 'Adrien', 'Ajay', 'Alex', 'Alexis',
    # 'Alfie', 'Ali', 'Alix', 'Allie', 'Allyn', 'Andie', 'Andrea', 'Andy', 'Angel',
    # 'Angie', 'Ariel', 'Ashley', 'Aubrey', 'Augustine', 'Austin', 'Averil', ...]

# armarmos bigramas, si primer elemento del bigrama es noombre, y es un bigrama frecuente. Es nombre de persona?

# HTML CLEANER
#
# >> > url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
# >> > html = request.urlopen(url).read().decode('utf8')
# >> > html[:60]
# '<!doctype html public "-//W3C//DTD HTML 4.0 Transitional//EN'
#
# >>> from bs4 import BeautifulSoup
# >>> raw = BeautifulSoup(html).get_text()
# >>> tokens = word_tokenize(raw)
# >>> tokens
# ['BBC', 'NEWS', '|', 'Health', '|', 'Blondes', "'to", 'die', 'out', ...]


# Processing RSS Feeds
#
# The blogosphere is an important source of text, in both formal and informal registers. With the help of a Python library called the
# Universal Feed Parser, available from https://pypi.python.org/pypi/feedparser, we can access the content of a blog, as shown below:

# >> > import feedparser
# >> > llog = feedparser.parse("http://languagelog.ldc.upenn.edu/nll/?feed=atom")
# >> > llog['feed']['title']
# 'Language Log'
# >> > len(llog.entries)
# 15
# >> > post = llog.entries[2]
# >> > post.title
# "He's My BF"
# >> > content = post.content[0].value
# >> > content[:70]
# '<p>Today I was chatting with three of our visiting graduate students f'
# >> > raw = BeautifulSoup(content).get_text()
# >> > word_tokenize(raw)
# ['Today', 'I', 'was', 'chatting', 'with', 'three', 'of', 'our', 'visiting',
#  'graduate', 'students', 'from', 'the', 'PRC', '.', 'Thinking', 'that', 'I',
#  'was', 'being', 'au', 'courant', ',', 'I', 'mentioned', 'the', 'expression',
#  'DUI4XIANG4', '\u5c0d\u8c61', '("', 'boy', '/', 'girl', 'friend', '"', ...]