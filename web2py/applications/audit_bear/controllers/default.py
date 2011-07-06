# Model - runs before the controller, defines data structures, methods,
# classes, etc. and passes global names to the controller.
# Dispatcher class might be defined there

# Controller (this file) - application workflow
# uses models objects to run application workflow, passes dictionary
# to view

# index shows the homepage and form, accepts both 152 and 155 file
import string
import random
from extractLogs import extractLogs
from dispatcher import dispatcher


def index():
    form = FORM(
        # for now, just input a file to make one analysis or multiple files in a zipped package
        #'upload audit log:', INPUT(_name='audit_log', _type='file'),
        #'ballot image:', INPUT(_name='ballot_image', _type='file'),
        #'election report managing tabulation log:', INPUT(_name='erm_log', _type='file'),
        'zipped files:', INPUT(_name='zipped_files', _type='file'),
        INPUT(_type='submit'))
    if form.accepts(request.vars, session):
        form.vars.zipped_files.file.seek(0)
        el152, el155 = extractLogs([form.vars.zipped_files.file])
        dictionary = dispatcher(el152=el152, el155=el155)
        generateImageIDs(dictionary['results'])
        generateTags(dictionary['results'])
        session.results = dictionary
        print 'checking in'
        redirect(URL('results'))
    return dict(message='Say hello to Audit Bear', form=form)

# all the results
def results():
    print 'checking out'
    if not request.function=='index':
        #redirect(URL('index'))
        pass

    return session.results

def about():
    return dict(message='')
def privacy():
    return dict(message='')
def contact():
    return dict(message='')


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
    
# stream requested image to browser
def histogram():
    imageID = request.args(0).split('.')[0]
    data = session.vcImageMap[imageID]
    data.seek(0)
    return response.stream(data)
    
# send requested image to browser
def histogram_download():
    imageID = request.args(0).split('.')[0]
    filename = 'graph_' + imageID + '.png'
    response.headers['Content-Disposition']='attachment; filename='+filename
    data = session.vcImageMap[imageID]
    data.seek(0)
    return response.stream(data)
