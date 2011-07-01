# receive a list of files, zipped or unzipped,
# extract zipped files, determine which logs are which, and
# return a tuple with (el152, el155, el68)

import re
import zipfile
# these three boolean functions could be implemented in the
# data structure classes instead...
def is_68(fh):
    fh.seek(0)
    # TODO implement this function
    return False

def is_152(fh):
    fh.seek(0)
    # check first couple of lines
    pattern = r"^(\d*?)\s+(\d*?)\s+(\w+?)\s+(\d+?/\d+?/\d+?\s+\d+?:\d+?:\d+?)\s+(\d+?)\s+(.*?)\s+$"
    lineRe = re.compile(pattern)
    i = 0
    # there is a problem with the file handle...
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

def extractLogs(files):
    totalReceivedFiles = []
    for f in files:
        if zipfile.is_zipfile(f):
            # extract
            z = zipfile.ZipFile(f, 'r')
            for member in z.infolist():
                m = z.open(member, 'r')
                # m is NOT SEEKABLE
                # make a new file and pass everything to a seekable one...
                import StringIO
                fNew = StringIO.StringIO()
                for l in m:
                    fNew.writelines(m.readlines())
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
                raise Exception('More than one el68 files were given')
            else:
                first68 = f
        elif is_152(f):
            if first152 != None:
                # TODO same as above
                raise Exception('More than one el152 files were given')
            else:
                first152 = f
        elif is_155(f):
            if first155 != None:
                # TODO same as above
                raise Exception('more than one el155 files were given')
            else:
                first155 = f
        else:
            # the file is not recognized, ignore it
            pass

    # reset all seeks
    if first68 != None:
        first68.seek(0)
    if first152 != None:
        first152.seek(0)
    if first155 != None:
        first155.seek(0)

    return (first152, first155)
    # TODO uncomment next line after el68 implemented
    #return (first68, first152, first155)
