import sys

def import_conf(name, folder=None):
    sys.path.insert(0, folder)

    m = __import__(name, fromlist='*')

    sys.path.pop(0)

    return m

