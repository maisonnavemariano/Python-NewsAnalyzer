import re

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class Document(object):
    PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

    def __init__(self, title,sectionName = "", date=""):
        self.sectionName = sectionName.replace(" ","")
        self.words = {}
        self.date = date
        self.title = "".join(c for c in title if c in self.PERMITTED_CHARS)

    def hasInvalidCharacter(self, cadena):
        return len("".join(c for c in cadena if c in self.PERMITTED_CHARS))< len(cadena)


    def addText(self, text, stopwords):
        text = text.lower()
        text = cleanhtml(text)
        #text = "".join(c for c in text if c in self.PERMITTED_CHARS)
        words_array = text.split(" ")
        for word in words_array:
            if not word in stopwords and len(word) > 0 and not hasNumbers(word) and not self.hasInvalidCharacter(word):
                if word in self.words:
                    self.words[word] = self.words[word] + 1
                else:
                    self.words[word] = 1

