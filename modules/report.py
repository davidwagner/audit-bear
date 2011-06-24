# Report data structure... contains text and images of report...
# textBoxes are just strings (for now, anyways)
# images are StringIO instances with captions
# possible uses: textBoxes are printed first,
# followed by images with their captions

class Image:
    # images contain the image data and captions
    data = None
    caption = None

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

class Report:
    textBoxes = []
    images = []
    # could have chosen a map for association, but StringIO
    # objects are not hashable

    def __init__(self, textBoxes=[], images=[]):
        self.textBoxes = textBoxes
        self.images = images

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

