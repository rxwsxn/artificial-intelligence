# CS 4710
from collections import OrderedDict

def main():
    """
    Main
    :return:
    """

class Expert(object):


    def __init__(self):
        self.rootVars = OrderedDict()
        self.learnedVars = OrderedDict()
        self.rules = OrderedDict()
        self.facts = OrderedDict()
        self.whyExpr = OrderedDict()

    def parse_input(self, input):
        if input.startwith("Teach"):
            if input.endwith("/"""):
                teach, varType, varName, equal, strValue = input.split()
                self.teach_variable(varType, varName, strValue)
            if input.endwith("False") or input.endwith("True"):
                teach, var, equal, boolean = input.split()
                self.define_variable(var, boolean)

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



    def learn_rules(self):
        pass

    def query(self, expr):
        pass

    def why(self, expr):
        pass


if __name__ == '__main__':
    main()