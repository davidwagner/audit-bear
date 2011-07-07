import string
import random
from extractLogs import extractLogs
from dispatcher import dispatcher
from controllerHelpers import *

def index():
    form = FORM(
        'zipped files:', INPUT(_name='zipped_files', _type='file'),
        INPUT(_type='submit'))

    if form.accepts(request.vars, session) and form.vars.zipped_files != '':
        form.vars.zipped_files.file.seek(0)
        el152, el155 = extractLogs([form.vars.zipped_files.file])
        dictionary = dispatcher(el152=el152, el155=el155)

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
