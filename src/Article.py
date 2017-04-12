#!/usr/bin/python3

class Article(object):
    ALLOWED_SECTIONS = {"Society","Business","World news","Politics"}
    IGNORED_SECTIONS = {"Music","Opinion","Sport","Film","From the Guardian","Footbal","Stage"}

    def __init__(self, title, sectionName='', headline='', trailtext='', bodyText='', date=''): #Default values '' if one of the parameters is not given.
        self.title       = title;
        self.sectionName = sectionName;
        self.headline    = headline;
        self.trailText   = trailtext;
        self.bodyText    = bodyText;
        self.date        = date;


    def isValidArticle(self):
        return len(self.bodyText)>0 and self.sectionName in self.ALLOWED_SECTIONS;

    def print(self):
        print(self.title + self.date );
