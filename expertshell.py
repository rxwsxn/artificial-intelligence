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
        self.facts = []
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
        rootVarsStr = 'Root Variables: \n'
        learnedVarsStr = '\nLearned Variables: \n'
        factsStr = '\nFacts: \n'
        rulesStr = '\nRules: \n'

        for k, v in self.rootVars.items():
            rootVarsStr += '\t {} = "{}"\n'.format(k, v)
        for k, v in self.learnedVars.items():
            learnedVarsStr += '\t {} = "{}"\n'.format(k, v)
        for k, v in self.rules.items():
            rulesStr += '\t {}\n'.format(v)
        for v in self.facts:
            factsStr += '\t {}\n'.format(v)
        return rootVarsStr + learnedVarsStr + factsStr + rulesStr

    def learn_rules(self):
        pass

    def query(self, expr):
        pass

    def why(self, expr):
        pass


if __name__ == '__main__':
    main()