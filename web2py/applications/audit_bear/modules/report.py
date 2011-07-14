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
    def __del__(self):
        del self.data
        del self.caption
        del self.embedTags
        del self.ID

    def __init__(self, data, caption):
        self.data = data
        self.caption = caption
        self.embedTags = None
        self.ID = None

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

class Table:
    # tables contain rows and cells for each row

    def __del__(self):
        del self.rows
        del self.headers
        del self.html

    def __init__(self, tableData = None):
        self.rows = None
        self.headers = None
        self.html = None

        if tableData:
            rows = tableData
            self.generateHTML()

        self.rows = []
        self.headers = []
        self.html = ''
        
    def generateHTML(self):
        self.html = '<table id = "data_collected"> <thead>'
        # TODO add headers
        if len(self.headers) > 0:
            self.html += '<tr>'
            for header in self.headers:
                self.html += '<th>' + header + '</th>'
            self.html += '</tr>'
        self.html += '</thead><tbody>'

        for row in self.rows:
            self.html += '<tr>'
            for cell in row:
                self.html += '<td>' + cell + '</td>'
            self.html += '</tr>'
        self.html += '</tbody></table>'

    def addRow(self, cells):
        # cells must be a list of cells (strings)
        self.rows.append(cells)
        self.generateHTML()
        
    def addCell(self, index, cell):
        self.rows[index].append(cell)
        self.generateHTML()

    def addHeader(self, header):
        self.headers.append(header)
        self.generateHTML()

    def getHTML(self):
        return self.html

class Report:
    # could have chosen a map for association, but StringIO
    # objects are not hashable

    def __del__(self):
        del self.textBoxes
        del self.images
        del self.tables
        del self.title

    def __init__(self):
        self.textBoxes = []
        self.images = []
        self.tables = []
        self.title = None

    def addTextBox(self, textBox):
        self.textBoxes.append(textBox)

    def addImage(self, image):
        self.images.append(image)

    def addTitle(self, title):
        self.title = title

    def addTable(self, table):
        self.tables.append(table)

    def getTextBox(self, index):
        return self.textBoxes[index]

    def getImage(self, index):
        return self.images[index]

    def getTextBoxList(self):
        return self.textBoxes

    def getImagesList(self):
        return self.images

    def getTablesList(self):
        return self.tables

    def hasImages(self):
        if len(self.images) > 0:
            return True
        else:
            return False

