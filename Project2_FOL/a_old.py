from collections import defaultdict
import itertools

uni_preds = defaultdict(set)
universe = set()

def getName(rule):
    return rule[:rule.index('(')]

def getArgs(rule):
    rule = rule.replace(' ', '').replace('.', '').split(':-')[0]
    args = rule[rule.index('(') + 1:].replace(')', '').replace(',', ' ').split()
    return args

def getPreds(rule):
    rule = rule.replace('.', '').replace(' ', '').split(':-')[1]
    preds = rule.split('),')
    preds[-1] = preds[-1].replace(')', '')

    preds = [pred + ')' for pred in preds]
    preds = [Predicate(pred) for pred in preds]
    return preds

class Rule:
    # args: list of PlaceHolder
    # eval string
    def __init__(self, rule):
        self.name = getName(rule)
        self.preds = getPreds(rule)
        self.args = getArgs(rule)
        self.vars = set(var for var in self.args + list(itertools.chain(*[pred.vars for pred in self.preds])) if isVariable(var))
        
    def activate(self):
        added = False
        for sub in itertools.product(universe, repeat = len(self.vars)):
            sub_map = {x: y for x, y in zip(self.vars, sub)}
            if all(pred.check(sub_map) for pred in self.preds):
                v = tuple(sub_map.get(x, x) for x in self.args)
                if v not in uni_preds[self.name]:
                    uni_preds[self.name].add(v)
                    added = True
        return added

    def check(self):
        ok = False
        for sub in itertools.product(universe, repeat = len(self.vars)):
            sub_map = {x: y for x, y in zip(self.vars, sub)}
            if all(pred.check(sub_map) for pred in self.preds):
                v = tuple(sub_map.get(x, x) for x in self.args)
                ok = True
                if sub_map:
                    print(sub_map)
        return ok

def getPredNVars(pred):
    ls = pred.replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
    return ls[0], ls[1:]

class Predicate:
    def __init__(self, pred):
        self.name, self.vars = getPredNVars(pred)
#         print(self.name, self.vars)
    
    def check(self, subs = None):
        vars = self.vars[:]
        for i, var in enumerate(vars):
            vars[i] = subs.get(var, var)

        return tuple(vars) in uni_preds[self.name]

class Fact:
    def __init__(self, fact):
        self.name = getName(fact)
        self.args = getArgs(fact)
        self.vars = set(arg for arg in self.args if isVariable(arg))
        self.insts = set(arg for arg in self.args if not isVariable(arg))
#         print(self.name, self.insts, self.vars)
    
    def activate(self):
        for sub in itertools.product(universe, repeat = len(self.vars)):
            sub_map = {x: y for x, y in zip(self.vars, sub)}
            v = tuple(sub_map.get(arg, arg) for arg in self.args)
            uni_preds[self.name].add(v)

def isVariable(s):
    return s[0].isupper() or s[0] == '_'

rules = []
facts = []
def readKB():
    with open('script.pl') as fin:
        lines = ''.join(fin.readlines())
        lines = lines.replace('\n', '').replace(' ', '').replace('.', ' ').split()
        for line in lines:
            if ':-' in line:
                rules.append(Rule(line))
            else:
                fact = Fact(line)
                universe.update(fact.insts)
                facts.append(fact)

def buildKB():
    for fact in facts:
        fact.activate()
        
    expanded = True
    while expanded:
        expanded = False
        for rule in rules:
            expanded = expanded or rule.activate()

def serve():
    while True:
        question = Rule("dummy(x):-" + input('?- '))
        print(question.check())
        
readKB()
buildKB()
print(*[(x, len(uni_preds[x])) for x in uni_preds.keys()])
# serve()
