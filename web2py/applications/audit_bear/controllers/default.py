from extractLogs import extractLogs
from dispatcher import dispatcher
from controllerHelpers import *
from auditLog import AuditLog
from ballotImage import BallotImage
from el68a import EL68A

def index():
    form = FORM(
        'Zipped File:', INPUT(_name='zipped_files', _type='file'),
        INPUT(_type='submit'))

    if form.accepts(request.vars, session) and form.vars.zipped_files != '':
        form.vars.zipped_files.file.seek(0)
        el152, el155, el68a = extractLogs([form.vars.zipped_files.file])
        del form.vars.zipped_files

        # create parsed logs and delete files...
        p_el152 = p_el155 = p_el68a = None
        if el152:
            p_el152 = AuditLog(el152)
            del el152
        if el155 and el68a:
            p_el68a = EL68A(el68a)
            del el68a
            p_el155 = BallotImage(el155, p_el152, p_el68a)
            del el155
        elif el155 and not el68a:
            p_el155 = BallotImage(el155, p_el152)
            del el155
         
        # parsed logs are passed to dispatcher
        dictionary = dispatcher(el152=p_el152, el155=p_el155, el68a=p_el68a)

        if dictionary['message'] != 'LOLCAT':
            generateImageIDs(dictionary['results'])
            generateTags(dictionary['results'])
            
        session.results = dictionary
        redirect(URL('results'))

    return dict(message=None, form=form)

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
    
