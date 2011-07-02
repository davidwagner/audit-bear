# Model - runs before the controller, defines data structures, methods,
# classes, etc. and passes global names to the controller.
# Dispatcher class might be defined there

# Controller (this file) - application workflow
# uses models objects to run application workflow, passes dictionary
# to view

# index shows the homepage and form, accepts both 152 and 155 file
def index():
    form = FORM(
        # for now, just input a file to make one analysis or multiple files in a zipped package
        #'upload audit log:', INPUT(_name='audit_log', _type='file'),
        #'ballot image:', INPUT(_name='ballot_image', _type='file'),
        #'election report managing tabulation log:', INPUT(_name='erm_log', _type='file'),
        'zipped files:', INPUT(_name='zipped_files', _type='file'),
        INPUT(_type='submit'), _action='results')
    
    return dict(message='Say hello to Audit Bear', form=form)

# all the results
def results():
    from extractLogs import extractLogs
    from dispatcher import dispatcher
    # do not use attribute fp, use file
    f = request.vars.zipped_files.file
    f.seek(0)
    el152, el155 = extractLogs([f]) # extractLogs receives a list of files
    # pass these to the dispatcher, which will collect all reports and pass
    # the resulting dictionary to the view
    dictionary = dispatcher(el152=el152, el155=el155)
    print dictionary['results']
    session.vcImage = dictionary['results'][3].getImage(0).getData()
    image = A(IMG(_src=URL(r=request, f='histogram.png'), _alt='histogram'), _href=URL(r=request, f='histogram_download'))
    dictionary['img'] = image
    #dictionary['message'] = 'YOUR RESULTS: 42'
    return (dictionary)
    
def histogram():
    filename='figure1.png'
    session.vcImage.seek(0)
    return response.stream(session.vcImage)
    
def histogram_download():
    filename='figure1.png'
    response.headers['Content-Disposition']='attachment; filename='+filename
    return response.stream(session.vcImage)
