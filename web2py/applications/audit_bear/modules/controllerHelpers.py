# helper functions for controller

def generateImageIDs(reports):
    imageIDs = []
    random.seed()

    for report in reports:
        if report.hasImages():
            for image in report.getImagesList():
                done = False
                while not done:
                    tempID = generateRandomID()
                    if tempID in imageIDs:
                        done = False
                    else:
                        done = True

                image.setImageID(tempID)
                imageIDs.append(tempID)

def randAlphaNum():
    chars = string.letters + string.digits
    return chars[random.randint(0, len(chars) - 1)]

def generateRandomID(s=10):
    result = ''
    for i in range(0, s):
        result += randAlphaNum()
    return result

# setEmbedTags and populate session.vcImageMap['imageID'] -> ImageData
def generateTags(reports):
    session.vcImageMap = {}

    for report in reports:
        if report.hasImages():
            for image in report.getImagesList():
                session.vcImageMap[image.getImageID()] = image.getData()
                tag = A(
                    IMG(_src=URL(r=request, f='histogram/' + image.getImageID() + '.png'), alt=''+image.getImageID()), 
                    _href=URL(r=request, f='histogram_download/' + image.getImageID() + '.png')
                )
                image.setEmbedTags(tag)
    
