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
                print("Wrong command:", line)


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
            # print("\nQuery: {}, value: {}".format(query, self.query(query)))
            print("{} is {}\n".format(query, self.query(query)))
            return "Query"
        elif input.startswith("Why"):
            _, query = input.split(maxsplit=1)
            boolean, reason = self.why(query, '')
            if boolean:
                print("{} is {}\n{}Thus I know that {}.\n".format(query, boolean, reason, self.translate_logic(query)))
            else:
                print("{} is {}\n{}Thus I cannot prove that {}.\n".format(query, boolean, reason, self.translate_logic(query)))
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
                    if k not in self.falsehood:
                        self.addFalsehood(k)

            self.rootVars[varName][1] = boolean
            if boolean:
                self.addFact(varName)
            if not boolean:
                self.addFalsehood(varName)
        else:
            print("\nCan not set value directly to a learned variable!")
    def getString(self, var):
        if var in self.rootVars:
            return self.rootVars[var][0]
        elif var in self.learnedVars:
            return self.learnedVars[var][0]
        else:
            return None
        
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
        return self.why(expr, '')[0]

    def why(self, expr, reason):
        # base case
        if expr in self.facts:
            reason += "I know it's true that {}. ".format(self.getString(expr))
            return True, reason
        elif expr in self.falsehood:
            reason += "I know it's not true that {}. ".format(self.getString(expr))
            return False, reason
        # recursive case
        # for all vars in expr, check if it's in facts, replaces with 'True',
        # if it's in falsehood, replace with 'False',
        # else recursive call
        variables = re.findall(r"[\w']+", expr)
        for var in variables:
            if var in self.facts:
                reason += "I know it's true that {}. ".format(self.getString(var))
                expr = expr.replace(var, 'True')
            elif var in self.falsehood:
                reason += "I know it's not true that {}. ".format(self.getString(var))
                expr = expr.replace(var, 'False')
            elif var in self.rules.keys():
                if var in self.learnedVars.keys():
                    if self.learnedVars[var][1]:
                        reason += "I know it's true that {}. ".format(self.getString(var))
                    else:
                        reason += "I know it's not true that {}. ".format(self.getString(var))
                    expr = expr.replace(var, str(self.learnedVars[var][1]))
            else:
                # backward chaining, find the rule -> this var
                for key in self.rules:
                    if self.rules[key] == var:
                        expr = expr.replace(var, str(self.why(key, reason)[0]))
                        if self.getString(key) is not None:
                            reason += "Because it's true that {}, I know that {}. ".format(self.getString(key), self.getString(var))
        return self.parse_expr(expr), reason

    def all_valid(self, expr):
        variables = re.findall(r"[\w']+", expr)
        result = True
        for var in variables:
            result = result and (var in self.learnedVars or var in self.rootVars)
        return result

    def parse_expr(self, expr):
        """
        :param expr:
        :return: Boolean
        """
        variables = re.findall(r"[\w']+", expr)
        for v in variables:
            if v == 'True' or v in self.facts:
                expr = expr.replace(v, 'True')
            else:
                expr = expr.replace(v, 'False')
        expr = expr.replace('&', ' and ')
        expr = expr.replace('|', ' or ')
        expr = expr.replace('!', ' not ')
        return eval(expr)

    def translate_logic(self, expr):
        """
        :param expr: Translate expression to words in conclusion of why
        :return: str
        """
        variables = re.findall(r"[\w']+", expr)
        for v in variables:
            if self.rootVars.get(v):
                expr = expr.replace(v, self.rootVars[v][0])
            elif self.learnedVars.get(v):
                expr = expr.replace(v, self.learnedVars[v][0])
        expr = expr.replace('&', ' and ')
        expr = expr.replace('|', ' or ')
        expr = expr.replace('!', 'not ')
        return expr

if __name__ == '__main__':
    main()