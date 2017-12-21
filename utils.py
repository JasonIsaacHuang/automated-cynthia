from pprint import pprint


class Log:

    '''
    Verbosity levels
    -1 - silent
     0 - normal
     1 - verbose
     2 - debug
    '''

    def __init__(self, verbosity=0):
        self.verbosity = verbosity

    def i(self, str):
        if (self.verbosity >= 0):
            pprint(str)

    def v(self, str):
        if (self.verbosity >= 1):
            pprint(str)

    def d(self, str):
        if (self.verbosity >= 2):
            pprint(str)

    # disregards all verbosity levels and outputs anyways
    def e(self, str):
        pprint(str)


def invert_dict(dict):
    invert = {}
    for k, v in dict.items():
        if isinstance(v, list):
            for i in v:
                invert[i] = k
        else:
            invert[v] = k
    return invert
