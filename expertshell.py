# CS 4710
from collections import OrderedDict

def main():
    """
    Main
    :return:
    """
def parse_input(input):
    pass

class Expert(object):

    def __init__(self):
        self.rootVars = OrderedDict()
        self.learnedVars = OrderedDict()
        self.rules = OrderedDict()
        self.facts = OrderedDict()
        self.whyExpr = OrderedDict()

    def teach_variable(self, varType, varName, strValue):
        if varType == 'R' and self.rootVars.get(varName) is None:
            self.rootVars[varName] = [strValue, False]
        if varType == 'S' and self.learnedVars.get(varName) is None:
            self.learnedVars[varName] = [strValue, False]

    def define_variable(self, varName, boolean):
        if self.rootVars.get(varName):
            self.rootVars[varName][1] = boolean

    def teach_rule(self, rule):
        pass

    def list_rules(self):
        rootVar = 'Root Variables: \n'
        learnedVar = '\nLearned Variables: \n'
        facts = '\nFacts: \n'
        rules = '\nRules: \n'

        for k, v in variables.items():


    def learn_rules(self):
        pass

    def query(self, expr):
        pass

    def why(self, expr):
        pass


if __name__ == '__main__':
    main()