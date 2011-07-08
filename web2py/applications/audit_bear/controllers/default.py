from extractLogs import extractLogs
from dispatcher import dispatcher
from controllerHelpers import *

def index():
    form = FORM(
        'Zipped File:', INPUT(_name='zipped_files', _type='file'),
        INPUT(_type='submit'))

    if form.accepts(request.vars, session) and form.vars.zipped_files != '':
        form.vars.zipped_files.file.seek(0)
        el152, el155, el68a = extractLogs([form.vars.zipped_files.file])
        dictionary = dispatcher(el152=el152, el155=el155, el68a=el68a)

        if dictionary['message'] != 'LOLCAT':
            generateImageIDs(dictionary['results'])
            generateTags(dictionary['results'])
            
        session.results = dictionary
        redirect(URL('results'))

    return dict(message='Say hello to Audit Bear', form=form)

# all the results
def results():
    if not session.results:
        print 'Redirect'
        redirect(URL('index'))

    return session.results

def about():
    return dict(message='')

def privacy():
    return dict(message='')

def contact():
    return dict(message='')

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

# setEmbedTags and populate session.vcImageMap['imageID'] -> ImageData
def generateTags(reports):
    session.vcImageMap = {}

    for report in reports:
        if report.hasImages():
            for image in report.getImagesList():
                session.vcImageMap[image.getImageID()] = image.getData()
                tag = A(
                    IMG(_src=URL(r=request, f='histogram/' + image.getImageID() + '.png'),
                        _alt=''+image.getImageID(), 
                        _width=640
                     ),
                    _href=URL(r=request, f='histogram_download/' + image.getImageID() + '.png')
                )
                image.setEmbedTags(tag)
    
