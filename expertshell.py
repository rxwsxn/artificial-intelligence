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
    with open('test_slide.txt') as f:
        lines = f.readlines()
        for line in lines:
            feedback = expert.parse_input(line.rstrip())
    #
    # while True:
    #     data = input("> ")
    #     feedback = expert.parse_input(data)
            if not feedback:
                print("Wrong command:",line)
    return 0


class Expert(object):

    def __init__(self):
        self.rootVars = OrderedDict() # { (key) variable : (value) [str, booleanValue, taughtBoolean] }
        self.learnedVars = OrderedDict() # { (key) variable : (value) [str, booleanValue, taughtBoolean] }
        self.rules = OrderedDict() # { (key) expression : (value) var }
        self.facts = [] # currently not used
        self.falsehood = []
        self.whyExpr = OrderedDict()

    def parse_input(self, input):
        if input.startswith("Teach"):
            if input.endswith('\"'):
                # print(input.split())
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
            self.list_all()
            return "List"
        elif input.startswith("Learn"):
            self.learn_rules()
            return "Learn"
        elif input.startswith("Query"):
            _, query = input.split(maxsplit=1)
            print("\nQuery: {}, value: {}".format(query, self.query(query)))
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
                    self.learnedVars[k] = [v[0], False, True]
                    # remove from facts and add to falsehood
                    if not k in self.falsehood:
                        self.addFalsehood(k)

            self.rootVars[varName][1] = boolean
            if boolean:
                self.addFact(varName)
            else:
                self.addFalsehood(varName)
        else:
            print("\nCan not set value directly to a learned variable!")
    def getString(self, var):
        if var in self.rootVars:
            return self.rootVars[var][0]
        elif var in self.learnedVars:
            return self.learnedVars[var][0]
        else:
            return "The string of var {} does not exist!".format(var)
        
    def addFact(self, var):
        if var in self.falsehood:
            self.falsehood.remove(var)
        if not var in self.facts:
            self.facts.append(var)
    
    def addFalsehood(self, var):
        if var in self.facts:
            self.facts.remove(var)
        if not var in self.falsehood:
            self.falsehood.append(var)
        
    def teach_rule(self, expr, val):
        if self.all_valid(expr):
            self.rules[expr] = val

    def list_all(self):
        rootVarsStr = '\nRoot Variables: \n'
        learnedVarsStr = '\nLearned Variables: \n'
        factsStr = '\nFacts: \n'
        rulesStr = '\nRules: \n'
        falsehoodStr = '\nFalsehood: \n'

        for k, v in self.rootVars.items():
            rootVarsStr += '\t{} = {}\n'.format(k, v[0])
        for k, v in self.learnedVars.items():
            learnedVarsStr += '\t{} = {}\n'.format(k, v[0])
        for k, v in self.rules.items():
            rulesStr += '\t{} -> {}\n'.format(k, v)
        for v in self.facts:
            factsStr += '\t{} = {}\n'.format(v, self.getString(v))
        for v in self.falsehood:
            falsehoodStr += '\t{} = {}\n'.format(v, self.getString(v))
        print(rootVarsStr + learnedVarsStr + factsStr + falsehoodStr + rulesStr)

    def learn_rules(self):
        # worst case learning scenario, results in O(n^2) time
        # can have further optimizations
        for i in range(len(self.rules)):
            for expr in self.rules:
                var = self.rules[expr]
                if not var in self.facts:
                    self.learnedVars[var][1] = self.parse_expr(expr)
                    # add the var to facts or falsehood
                    if self.parse_expr(expr):
                        self.addFact(var)
                    else:
                        self.addFalsehood(var)
                    self.learnedVars[var][2] = True
                    
                
    def query(self, expr):
        # base case
        if expr in self.facts:
            return True
        elif expr in self.falsehood:
            return False
        # recursive case
        # for all vars in expr, check if it's in facts, replaces with 'True', 
        # if it's in falsehood, replace with 'False', 
        # else recursive call
        variables = re.findall(r"[\w']+", expr)
        for var in variables:
            if var in self.facts:
                expr = expr.replace(var, 'True')
            elif var in self.falsehood:
                expr = expr.replace(var, 'False')
            else:
                # backward chaining, find the rule -> this var
                for key in self.rules:
                    if self.rules[key] == var:
                        expr = expr.replace(var, str(self.query(key)))
        return self.parse_expr(expr)

    def why(self, question):
        factKnown = "I know that"
        ruleApplied = "Because "
        conclusion = "Thus I know that "

    def all_valid(self, expr):
        variables = re.findall(r"[\w']+", expr)
        result = True
        for var in variables:
            result = result and (var in self.learnedVars or var in self.rootVars)
        return result

    def parse_expr(self, expr):
        variables = re.findall(r"[\w']+", expr)
        for v in variables:
            if v == "True" or v in self.facts:
                expr = expr.replace(v, 'True')
            else:
                expr = expr.replace(v, 'False')
        expr = expr.replace('&', ' and ')
        expr = expr.replace('|', ' or ')
        expr = expr.replace('!', ' not ')
        return eval(expr)


if __name__ == '__main__':
    main()