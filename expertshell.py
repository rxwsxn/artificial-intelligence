# CS 4710
from collections import OrderedDict
import re

def main():
    """
    Main
    :return:
    """
    expert = Expert
    print ("Hello, Welcome to Our Expert System Shell!")
    while True:
        data = input("> ")
        feedback = expert.parse_input(expert,data)
        if not feedback:
            print("Wrong command!")
            break
    return 0

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
            return "Teach"
        elif input.startwith("List"):
            self.list_all()
            return "List"
        elif input.startwith("Learn"):
            self.learn_rules()
            return "Learn"
        elif input.startwith("Query"):
            q, query = input.split()
            self.query(query)
            return "Query"
        elif input.startwith("Why"):
            w, question = input.split()
            self.why(question)
            return "Why"

    def teach_variable(self, varType, varName, strValue):
        if varType == 'R' and self.rootVars.get(varName) is None:
            # string text, boolean value, has been teached (always false for root variables initially??) (boolean)
            self.rootVars[varName] = [strValue, False, False]
        if varType == 'S' and self.learnedVars.get(varName) is None:
            self.learnedVars[varName] = [strValue, False, False]

    def define_variable(self, varName, boolean):
        if self.rootVars.get(varName):
            self.rootVars[varName][1] = boolean
            if self.rootVars[varName][2]:  # if set to True
                for k, v in self.learnedVars.items(): # set all learned vars to False per assignment
                    self.learnedVars[k] = [v[0], v[1], False]
            self.rootVars[varName][2] = True

    def teach_rule(self, expr, val):
        self.rules[val] = 
        # self.learnedVars[val] = [self.learnedVars[val][0], self.parse_expr(expr, val)]

    def learn_rules(self):
        pass

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

    def query(self, expr):
        self.learnedVars[val] = [self.l]

    def why(self, question):
        pass

    def parse_expr(self, expr):
        val = expr.split(' -> ')[1]
        if not self.learnedVars.get(val):
            return False
        variables = re.findall(r"[\w']+", expr)
        for v in variables:
            if not self.rootVars.get(v) and not self.learnedVars.get(v):
                return False
            elif self.rootVars.get(v):
                expr.replace(v, 'True' if self.rootVars[v][1] else 'False')
            elif self.learnedVars.get(v):
                expr.replace(v, 'True' if self.learnedVars[v][1] else 'False')
        expr.replace('&', ' and ')
        expr.replace('|', ' or ')
        expr.replace('!', ' not ')
        return eval(expr)


if __name__ == '__main__':
    main()