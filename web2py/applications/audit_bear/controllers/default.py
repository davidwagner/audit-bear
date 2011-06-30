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
    # do not use attribute fp, use file
    f = request.vars.zipped_files.file
    f.seek(0)
    el152, el155 = extractLogs([f]) # extractLogs receives a list of files
    
    # pass these to the dispatcher, which will collect all reports and pass
    # the resulting dictionary to the view
    dictionary = dispatcher(el152=el152, el155=el155)
    #dictionary['message'] = 'YOUR RESULTS: 42'
    return dictionary
