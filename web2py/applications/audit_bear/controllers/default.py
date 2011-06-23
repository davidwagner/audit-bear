# Model - runs before the controller, defines data structures, methods,
# classes, etc. and passes global names to the controller.
# Dispatcher class might be defined there

# Controller (this file) - application workflow
# uses models objects to run application workflow, passes dictionary
# to view

# index shows the homepage and form, accepts both 152 and 155 file
def index():
    form = FORM('upload audit log:', INPUT(_name='audit_log', _type='file'),
        INPUT(_name='ballot_image', _type='file'),
        INPUT(_type='submit'), _action='results')
    return dict(message='Say hello to Audit Bear', form=form)

# all the results
def results():
    return dict(message='YOUR RESULTS: LOLOLOLOL')
