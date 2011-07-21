# receive a list of files, zipped or unzipped,
# extract zipped files, determine which logs are which, and
# return a tuple with (el152, el155, el68)

import re
import zipfile
import os
import controllerHelpers

class InvalidFilesException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def is_68(fh):
    fh.seek(0)
    pattern = r"SYSTEM LOG LISTING"
    lineRe = re.compile(pattern, re.IGNORECASE)
    i = 0
    for l in fh:
        r = lineRe.search(l)
        if r:
            return True
        elif i >= 10:
            break
        i += 1

    return False

def is_152(fh):
    fh.seek(0)
    # check first couple of lines
    pattern = r"^(\d*?)\s+(\d*?)\s+(\w+?)\s+(\d+?/\d+?/\d+?\s+\d+?:\d+?:\d+?)\s+(\d+?)\s+(.*?)\s+$"
    lineRe = re.compile(pattern)
    i = 0

    for l in fh:
        r = lineRe.match(l)
        if r:
            return True
        elif i >= 10:
            break
        i += 1

    return False

def is_155(fh):
    fh.seek(0)
    # check header...
    precinctPattern = r"PRECINCT\s*(\d+)\s*-\s*(.*)ELECTION"
    precinctRe = re.compile(precinctPattern, re.IGNORECASE)
    i = 0
    for l in fh:
        r = precinctRe.search(l)
        if r:
            return True
        elif i >= 10:
            break
        i += 1

    return False

# intelligently choose a path name
def choosePath(applicationDirectory):
    uploadPath = os.path.join(applicationDirectory, 'uploads')
    while True:
        fullPath = os.path.join(uploadPath, controllerHelpers.generateRandomID())
        if not os.path.isfile(fullPath):
            return fullPath

def clean(applicationDirectory, files):
    uploadPath = os.path.join(applicationDirectory, 'uploads')
    for f in files:
        os.unlink(os.path.join(uploadPath, f.name))

def extractLogs(files, applicationDirectory):
    totalReceivedFiles = []
    for f in files:
        if zipfile.is_zipfile(f):
            # extract
            z = zipfile.ZipFile(f, 'r')
            for member in z.infolist():
                m = z.open(member, 'r')
                path = choosePath(applicationDirectory)
                fNew = open(path, 'w+')
                for l in m:
                    fNew.write(l)
                fNew.flush()
                totalReceivedFiles.append(fNew)

            z.close()
        else:
            totalReceivedFiles.append(f)

    # now determine what each file is
    first68 = None
    first152 = None
    first155 = None
    for f in totalReceivedFiles:
        if is_68(f):
            if first68 != None:
                # TODO Create different exception for this
                clean(applicationDirectory, totalReceivedFiles)
                raise InvalidFilesException('More than one el68 files was given')
            else:
                first68 = f
        elif is_152(f):
            if first152 != None:
                # TODO same as above
                clean(applicationDirectory, totalReceivedFiles)
                raise InvalidFilesException('More than one el152 files was given')
            else:
                first152 = f
        elif is_155(f):
            if first155 != None:
                # TODO same as above
                clean(applicationDirectory, totalReceivedFiles)
                raise InvalidFilesException('More than one el155 files was given')
            else:
                first155 = f
        else:
            # the file is not recognized, ignore it and delete file from disk
            os.unlink(os.path.join(applicationDirectory, 'uploads', f.name))

    if not (first152 and first155):
        clean(applicationDirectory, totalReceivedFiles)
        raise InvalidFilesException("Both el152 and el155 must be given.")
    
    # reset all seeks
    if first68 != None:
        first68.seek(0)
    if first152 != None:
        first152.seek(0)
    if first155 != None:
        first155.seek(0)

    return (first152, first155, first68)

