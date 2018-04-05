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

    def _print(self, output):
        if type(output) == list:
            for item in output:
                print(item)
        else:
            print(output)

    def i(self, output):
        if (self.verbosity >= 0):
            self._print(output)

    def v(self, output):
        if (self.verbosity >= 1):
            self._print(output)

    def d(self, output):
        if (self.verbosity >= 2):
            self._print(output)

    # disregards all verbosity levels and outputs anyways
    def e(self, output):
        self._print(output)


def invert_dict(dict):
    invert = {}
    for k, v in dict.items():
        if isinstance(v, list):
            for i in v:
                invert[i] = k
        else:
            invert[v] = k
    return invert
