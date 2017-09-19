# CS 4710
from collections import OrderedDict
import re

def main():
    """
    Main
    :return:
    """
    expert = Expert()
    print("Hello, Welcome to Our Expert System Shell!")
    with open('test.txt') as f:
        lines = f.readlines()
        for line in lines:
            feedback = expert.parse_input(line.rstrip())
    #
    # while True:
    #     data = input("> ")
    #     feedback = expert.parse_input(data)
    #     if not feedback:
    #         print("Wrong command!")
    #         break
    return 0


class Expert(object):

    def __init__(self):
        self.rootVars = OrderedDict() # { (key) variable : (value) [str, booleanValue, taughtBoolean] }
        self.learnedVars = OrderedDict() # { (key) variable : (value) [str, booleanValue, taughtBoolean] }
        self.rules = OrderedDict() # { (key) expression : (value) var }
        self.facts = [] # currently not used
        self.whyExpr = OrderedDict()

    def parse_input(self, input):
        if input.startswith("Teach"):
            if input.endswith('\"'):
                print(input.split())
                _, varType, varName, _, strValue = input.split(maxsplit=4)
                self.teach_variable(varType, varName, strValue)
            elif input.lower().endswith("false") or input.lower().endswith("true"):
                _, var, _, boolean = input.split(maxsplit=3)
                self.define_variable(var, True if boolean.lower() == "true" else False)
            elif "->" in input:
                _, expression, _, value = input.split(maxsplit=3)
                self.teach_rule(expression, value)
            return "Teach"
        elif input.startswith("List"):
            print(self.list_all())
            return "List"
        elif input.startswith("Learn"):
            self.learn_rules()
            return "Learn"
        elif input.startswith("Query"):
            _, query = input.split(maxsplit=1)
            self.query(query)
            return "Query"
        elif input.startswith("Why"):
            _, question = input.split(maxsplit=1)
            self.why(question)
            return "Why"

    def teach_variable(self, varType, varName, strValue):
        if varType == '-R' and self.rootVars.get(varName) is None:
            self.rootVars[varName] = [strValue, False, False]
        if varType == '-L' and self.learnedVars.get(varName) is None:
            self.learnedVars[varName] = [strValue, False, False]

    def define_variable(self, varName, boolean):
        if self.rootVars.get(varName):
            if not self.rootVars[varName][1] == boolean:
                for k, v in self.learnedVars.items():
                    self.learnedVars[k] = [v[0], v[1], False]
            self.rootVars[varName][1] = boolean

    def teach_rule(self, expr, val):
        if self.all_valid(expr):
            self.rules[expr] = val

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
        # worst case learning scenario, results in O(n^2) time
        # can have further optimizations
        for i in range(len(self.rules)):
            for expr, var in self.rules:
                if not var in self.facts:
                    self.learnedVars[2] = self.parse_expr(expr)
                    self.learnedVars[3] = True
                
    def query(self, expr):
        if self.all_valid(expr):
            return self.parse_expr(expr)

    def why(self, question):
        pass

    def all_valid(self, expr):
        variables = re.findall(r"[\w']+", expr)
        result = True
        for var in variables:
            result = result and (var in self.learnedVars or var in self.rootVars)
        return result

    def parse_expr(self, expr):
        variables = re.findall(r"[\w']+", expr)
        for v in variables:
            if self.rootVars.get(v):
                expr.replace(v, 'True' if self.rootVars[v][1] else 'False')
            elif self.learnedVars.get(v):
                expr.replace(v, 'True' if self.learnedVars[v][1] else 'False')
        expr.replace('&', ' and ')
        expr.replace('|', ' or ')
        expr.replace('!', ' not ')
        return eval(expr)


if __name__ == '__main__':
    main()