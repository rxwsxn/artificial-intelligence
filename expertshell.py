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
        self.facts = []
        self.whyExpr = OrderedDict()

    def parse_input(self, input):
        if input.startwith("Teach"):
            if input.endwith("/"""):
                teach, varType, varName, equal, strValue = input.split()
                self.teach_variable(varType, varName, strValue)
            elif input.endwith("false") or input.endwith("true"):
                teach, var, equal, boolean = input.split()
                self.define_variable(var, boolean.title())
            elif "->" in input:
                teach, expression, arrow, value = input.split()
                self.teach_rule(expression, value)
        elif input.startwith("List"):
            self.list_all()
        elif input.startwith("Learn"):
            self.learn_rules()
        elif input.startwith("Query"):
            q, query = input.split()
            self.query(query)
        elif input.startwith("Why"):
            w, question = input.split()
            self.why(question)

    def teach_variable(self, varType, varName, strValue):
        if varType == 'R' and self.rootVars.get(varName) is None:
            self.rootVars[varName] = [strValue, False]
        if varType == 'S' and self.learnedVars.get(varName) is None:
            self.learnedVars[varName] = [strValue, False]

    def define_variable(self, varName, boolean):
        if self.rootVars.get(varName):
            self.rootVars[varName][1] = boolean

    def teach_rule(self, expr, val):


    def list_all(self):
        rootVarsStr = 'Root Variables: \n'
        learnedVarsStr = '\nLearned Variables: \n'
        factsStr = '\nFacts: \n'
        rulesStr = '\nRules: \n'

        for k, v in self.rootVars.items():
            rootVarsStr += '\t {} = "{}"\n'.format(k, v)
        for k, v in self.learnedVars.items():
            learnedVarsStr += '\t {} = "{}"\n'.format(k, v)
        for k, v in self.rules.items():
            rulesStr += '\t {} -> {}\n'.format(k, v)
        for v in self.facts:
            factsStr += '\t {}\n'.format(v)
        return rootVarsStr + learnedVarsStr + factsStr + rulesStr

    def learn_rules(self):
        pass

    def query(self, expr):
        pass

    def why(self, question):
        pass


if __name__ == '__main__':
    main()