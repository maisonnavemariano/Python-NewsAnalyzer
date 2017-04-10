#!/usr/bin/python3

class Article(object):


    def __init__(self, title, sectionName='', headline='', trailtext='', bodyText='', date=''): #Default values '' if one of the parameters is not given.
        self.title       = title;
        self.sectionName = sectionName;
        self.headline    = headline;
        self.trailText   = trailtext;
        self.bodyText    = bodyText;
        self.date        = date;

    def validArticle(self):
        return len(self.BodyText)>0;

    def setSection(self, sectionName):
        self.sectionName = sectionName;

    def setHeadline(self, headline):
        self.headline = headline;

    def setTrailText(self, trailText):
        self.trailText = trailText;

    def setBodyText(self, bodyText):
        self.bodyText = bodyText;

    def setDate(self, date):
        self.date = date;
    def isValidArticle(self):
        return len(self.bodyText)>0;
    def print(self):
        print(self.title + self.date );