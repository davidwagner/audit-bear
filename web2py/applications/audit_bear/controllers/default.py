from extractLogs import extractLogs
from dispatcher import dispatcher
from controllerHelpers import *
from auditLog import AuditLog
from ballotImage import BallotImage
from el68a import EL68A
import os

def index():
    form = FORM(
        'Zipped File:', INPUT(_name='zipped_files', _type='file'),
        INPUT(_type='submit'))

    if form.accepts(request.vars, session) and form.vars.zipped_files != '':
        form.vars.zipped_files.file.seek(0)
        try:
            el152, el155, el68a = extractLogs([form.vars.zipped_files.file], request.folder)
        except Exception as e:
            session.file_error = str(e)
            redirect(URL('error'))
        finally:
            del form.vars.zipped_files

        # file name is in el152.name etc.
        # create parsed logs and delete files...
        p_el152 = p_el155 = p_el68a = None
        if el152:
            p_el152 = AuditLog(el152)
            os.unlink(os.path.join(request.folder, 'uploads', el152.name))
            del el152
        if el155 and el68a:
            p_el68a = EL68A(el68a)
            os.unlink(os.path.join(request.folder, 'uploads', el68a.name))
            del el68a
            p_el155 = BallotImage(el155, p_el152, p_el68a)
            os.unlink(os.path.join(request.folder, 'uploads', el155.name))
            del el155
        elif el155 and not el68a:
            p_el155 = BallotImage(el155, p_el152)
            os.unlink(os.path.join(request.folder, 'uploads', el155.name))
            del el155
         
        # parsed logs are passed to dispatcher
        try:
            dictionary = dispatcher(el152=p_el152, el155=p_el155, el68a=p_el68a)
        except Exception as e:
            session.file_error = str(e)
            redirect(URL('error'))

        if dictionary['message'] != 'LOLCAT':
            generateImageIDs(dictionary['results'])
            generateTags(dictionary['results'])
            
        session.results = dictionary
        redirect(URL('results'))

    return dict(message=None, form=form)

# all the results
def results():
    if not session.results:
        redirect(URL('index'))

    return session.results

def about():
    return dict(message='')

def privacy():
    return dict(message='')

def contact():
    return dict(message='')

def error():
    return dict(message=session.file_error)

# stream requested image to browser
def histogram():
    imageID = request.args(0).split('.')[0]
    data = session.vcImageMap[imageID]
    data.seek(0)
    return response.stream(data)
    
# send requested image to browser (for download)
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
    
