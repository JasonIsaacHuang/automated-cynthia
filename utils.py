
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
            print(str)

    def v(self, str):
        if (self.verbosity >= 1):
            print(str)

    def d(self, str):
        if (self.verbosity >= 2):
            print(str)

    # disregards all verbosity levels and outputs anyways
    def e(self, str):
        print(str)
