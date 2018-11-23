from collections import defaultdict
import itertools
import sys
sys.setrecursionlimit(1000000)

uni_facts = defaultdict(set)
uni_preds = []
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
        self.arg_vars = [arg for arg in self.args if isVariable(arg)]
        self.vars = set(var for var in self.args + list(itertools.chain(*[pred.vars for pred in self.preds])) if isVariable(var))
        self.cached = None

    def __repr__(self):
        return f'{self.name} {self.args} {self.vars}'
        
    # return set of tuples of subtitutes
    def getSubsInFacts(self):
        subs = set()
        for sub in itertools.product(universe, repeat = len(self.arg_vars)):
            sub_map = {x: y for x, y in zip(self.arg_vars, sub)}
            v = tuple(sub_map.get(arg, arg) for arg in self.args)
            if v in uni_facts[self.name]:
                subs.add(v)
#         print('RULE', 'getSubsInFact', self.name, subs)
        return subs

    def check(self, sub_map):
        return all(pred.check(sub_map) for pred in self.preds)
    
    # return set of submaps
    def getSubsByPreds(self):
        # dom[x] = set of values x can take
        dom = defaultdict(lambda: universe.copy())
        
        for pred in self.preds:
            subs = pred.getSubs()
            for i, var in enumerate(pred.vars):
                dom[var] &= set(sub[i] for sub in subs)

#         print('RULE', 'getSubsByPreds', self.name, 'DOM', *[(x, dom[x]) for x in dom.keys()])
        subs = set()
        # unify
        for sub in itertools.product(*[dom[var] for var in self.vars]):
            sub_map = {x:y for x, y in zip(self.vars, sub)}
            if self.check(sub_map):
                subs.add(tuple(sub_map.get(arg, arg) for arg in self.args))

#         print('RULE', 'getSubsByPred', self.name, subs)
        return subs

    def getSubs(self):
        if self.cached == None:
            self.cached = self.getSubsInFacts() | self.getSubsByPreds()
        return self.cached

def getPredNVars(pred):
    ls = pred.replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
    return ls[0], ls[1:]

class Predicate:
    def __init__(self, pred):
        self.name, self.vars = getPredNVars(pred)
        self.args = getArgs(pred)
        self.cached = None
        uni_preds.append(self)
        self.unifiable_rules = []

    def __repr__(self):
        return f'{self.name} {self.args}'
    
    def checkInFacts(self, subs):
        return tuple(subs.get(arg, arg) for arg in self.args) in uni_facts[self.name]
    
    def check(self, subs):
        return tuple(subs.get(arg, arg) for arg in self.args) in self.getSubs()

    # returns a list of submap for this pred
    def getSubsInFacts(self):
        subs = set()
        for sub in itertools.product(universe, repeat = len(self.vars)):
            sub_map = {x: y for x, y in zip(self.vars, sub)}
            if self.checkInFacts(sub_map):
                subs.add(tuple(sub_map.get(var, var) for var in self.vars))
#         print('PRED', 'getSubsInFact', self.name, subs)
        return subs
        
    def getSubsInRules(self):
        subs = set()
        for rule in self.unifiable_rules:
            subs.update(rule.getSubs())
        return subs

    def getSubs(self):
        if self.cached == None:
            self.cached = self.getSubsInFacts() | self.getSubsInRules()
        return self.cached

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
            uni_facts[self.name].add(v)

def isVariable(s):
    return s[0].isupper() or s[0] == '_'

def unifiable(pred, rule):
    return pred.name == rule.name\
            and len(pred.args) == len(rule.args)\
            and all(isVariable(pa) == isVariable(ra) or isVariable(pa)\
                for pa, ra in zip(pred.args, rule.args))
            
uni_rules = []
facts = []
def readKB():
    with open('script.pl') as fin:
        lines = ''.join(fin.readlines())
        lines = lines.replace('\n', '').replace(' ', '').replace('.', ' ').split()
        for line in lines:
            if ':-' in line:
                uni_rules.append(Rule(line))
            else:
                fact = Fact(line)
                universe.update(fact.insts)
                facts.append(fact)

def buildKB():
    for fact in facts:
        fact.activate()

#     print(*[fact for fact in uni_facts], sep='\n')
    for pred, rule in itertools.product(uni_preds, uni_rules):
        if unifiable(pred, rule):
            pred.unifiable_rules.append(rule)
        
def serve():
    pred = Predicate("grandfather(X, Y).")
    for rule in uni_rules:
        if unifiable(pred, rule):
            pred.unifiable_rules.append(rule)
    print(*pred.getSubs(), sep='\n')
#     while True:
#         question = Rule("dummy(x):-" + input('?- '))
#         subs = question.getSubs()
#         if subs:
#             print(*subs, sep = '\n')
#         print(len(subs) > 0)
        
readKB()
buildKB()
serve()
