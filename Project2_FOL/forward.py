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
        
    # return list of submaps
    def getSubs(self):
        # dom[x] = set of values x can take
        dom = defaultdict(lambda: universe.copy())
        
        for pred in self.preds:
            sub_maps = pred.getSubs()
            for var in pred.vars:
                dom[var] &= set(sub[var] for sub in sub_maps)

        sub_maps = []
        # unify
        for sub in itertools.product(*[dom[var] for var in self.vars]):
            sub_map = {x:y for x, y in zip(self.vars, sub)}
            if self.check(sub_map):
                sub_maps.append(sub_map)

        return sub_maps

    def activate(self):
        added = False
        subs = self.getSubs()
        for sub in set(tuple(sub.get(x, x) for x in self.args) for sub in subs):
            if sub not in uni_preds[self.name]:
                added = True
                uni_preds[self.name].add(sub)
        return added

    def check(self, sub_map):
        return all(pred.check(sub_map) for pred in self.preds)
    
    def __lt__(self, other):
        return self.name in set(pred.name for pred in other.preds)

def getPredNVars(pred):
    ls = pred.replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
    return ls[0], ls[1:]

class Predicate:
    def __init__(self, pred):
        self.name, self.vars = getPredNVars(pred)
#         print(self.name, self.vars)
    
    def check(self, subs):
        vars = self.vars[:]
        for i, var in enumerate(vars):
            vars[i] = subs.get(var, var)

        return tuple(vars) in uni_preds[self.name]

    # returns a list of submap for this pred
    def getSubs(self):
        sub_maps = []
        for sub in itertools.product(universe, repeat = len(self.vars)):
            sub_map = {x: y for x, y in zip(self.vars, sub)}
            if self.check(sub_map):
                sub_maps.append(sub_map)
#                 print(self.name, sub_map)
        return sub_maps

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
    for rule in rules:
        rule.activate()
#     while expanded:
#         expanded = False
#         for rule in rules:
#             expanded = expanded or rule.activate()

def serve():
    while True:
        question = Rule("dummy(x):-" + input('?- '))
        subs = question.getSubs()
        if subs:
            print(*subs, sep = '\n')
        print(len(subs) > 0)
        
readKB()
buildKB()
# print(sum(len(x) for x in uni_preds.values()))
# print(*[(x, len(uni_preds[x])) for x in uni_preds.keys()])
serve()
