#!/usr/bin/env python
# coding: utf8
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
# request, response, session, cache, T, db(s)
# must be passed and cannot be imported!

# Report data structure... contains text and images of report...
# textBoxes are just strings (for now, anyways)
# images are StringIO instances with captions
# possible uses: textBoxes are printed first,
# followed by images with their captions

class Image:
    # images contain the image data and captions
    data = None
    caption = None
    embedTags = None
    ID = None

    def __init__(self, data, caption):
        self.data = data
        self.caption = caption

    def getData(self):
        return self.data

    def getCaption(self):
        return self.caption

    def setData(self, data):
        self.data = data

    def setCaption(self, caption):
        self.caption = caption

    def setEmbedTags(self, tags):
        self.embedTags = tags

    def getEmbedTags(self):
        return self.embedTags

    def getImage(self):
        return self.embedTags

    def setImageID(self, ID):
        self.ID = ID

    def getImageID(self):
        return self.ID

class Report:
    textBoxes = None
    images = None
    # could have chosen a map for association, but StringIO
    # objects are not hashable

    def __init__(self):
        self.textBoxes = []
        self.images = []

    def addTextBox(self, textBox):
        self.textBoxes.append(textBox)

    def addImage(self, image):
        self.images.append(image)

    def getTextBox(self, index):
        return self.textBoxes[index]

    def getImage(self, index):
        return self.images[index]

    def getTextBoxList(self):
        return self.textBoxes

    def getImagesList(self):
        return self.images

    def hasImages(self):
        if len(self.images) > 0:
            return True
        else:
            return False

