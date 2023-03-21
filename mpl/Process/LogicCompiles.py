class LogicCompiles(object):

    def __init__(self):
        self.compiles = list()

    def increase(self):
        self.var += 1

    def getCompiles(self):
        return self.compiles

    def appendCompile(self,compile):
        self.compiles.append(compile)

    def getValue(self):
        return self.var