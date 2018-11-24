from collections import defaultdict
import itertools
import sys
sys.setrecursionlimit(1000000)

uni_facts = defaultdict(set)
uni_preds = []
uni_subs = defaultdict(set)
universe = set()
uni_rules = dict()

def getName(rule):
    return rule[:rule.index('(')]

def getArgs(rule):
    rule = rule.replace(' ', '').replace('.', '').split(':-')[0]
    args = rule[rule.index('(') + 1:].replace(')', '').replace(',', ' ').split()
    return args

def getPredNVars(pred):
    ls = pred.replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
    return ls[0], [var for var in ls[1:] if isVariable(var)]


def getPreds(rule):
    rule = rule.replace('.', '').replace(' ', '').split(':-')[1]
    preds = rule.split('),')
    preds[-1] = preds[-1].replace(')', '')

    preds = [pred + ')' for pred in preds]
    preds = [Predicate(pred) for pred in preds]
    return preds

def isVariable(s):
    return s[0].isupper() or s[0] == '_'

def unifiable(pred, rule):
    if pred.name == rule.name\
            and len(pred.args) == len(rule.args)\
            and all((isVariable(pa) and isVariable(ra)) or (not isVariable(pa) and not isVariable(ra) and pa == ra) or (isVariable(ra) and not isVariable(pa))\
            for pa, ra in zip(pred.args, rule.args)):
        return True
    return False
 
def getID(pred):
    args = pred.args[:]
    c = 0
    id = [pred.name]
    for arg in args:
        if isVariable(arg):
            id.append(f'X{c}')
            c += 1
        else:
            id.append(arg)
    return tuple(id)

import copy
def newPredWithLessVars(pred, sub_map):
    newPred = copy.deepcopy(pred)
    newPred.args = [sub_map.get(arg, arg) for arg in pred.args]
    newPred.vars = [arg for arg in newPred.args if isVariable(arg)]
    newPred.unifiable_rules = [rule for rule in uni_rules.values() if unifiable(newPred, rule)]
    
    return newPred
    
def newRuleWithLessVars(pred, rule):
    newRule = copy.deepcopy(rule)
    sub_map = {x:y for x, y in zip(rule.args, pred.args) if isVariable(x) and not isVariable(y)}
    newRule.args = [sub_map.get(arg, arg) for arg in rule.args]
    newRule.preds = [newPredWithLessVars(pred, sub_map) for pred in newRule.preds]
    newRule.vars = rule.vars - set(sub_map.keys())
    newRule.arg_vars = set(newRule.args) & set(newRule.vars)
    id = getID(newRule)
    if id not in uni_rules:
        uni_rules[id] = newRule
    else:
        return uni_rules[id]
    for pred in uni_preds:
        if unifiable(pred, newRule):
            pred.unifiable_rules.append(newRule)
    
#     print('newRuleWithLessVars', pred, rule, newRule, sep='\n')
#     exit(0)
    return newRule
    
class Rule:
    # args: list of PlaceHolder
    # eval string
    def __init__(self, rule):
        self.name = getName(rule)
        self.preds = getPreds(rule)
        self.args = getArgs(rule)
        self.vars = set(var for var in self.args + list(itertools.chain(*[pred.vars for pred in self.preds])) if isVariable(var))
        self.arg_vars = set(self.args) & set(self.vars)
        uni_rules[getID(self)] = self
        for pred in uni_preds:
            if unifiable(pred, self):
                pred.unifiable_rules.append(self)

    def __repr__(self):
        return f'<RULE {self.name} {self.args} {self.vars} {self.preds}>'
        
    # return set of tuples of subtitutes
    def getSubsInFacts(self):
        subs = set()
        for sub in itertools.product(universe, repeat = len(self.arg_vars)):
            sub_map = {x: y for x, y in zip(self.arg_vars, sub)}
            v = tuple(sub_map.get(arg, arg) for arg in self.args)
            if v in uni_facts[self.name]:
                subs.add(v)
#         print('RULE', 'getSubsInFact', self, subs)
        return subs

    def check(self, sub_map):
        return all(pred.check(sub_map) for pred in self.preds)
    
    # return set of submaps
    def getSubsByPreds(self):
        pred_subs = [pred.getSubs() for pred in self.preds]

#         print('>> preds', self, self.preds)
        subs = set()
        for pred_sub in itertools.product(*pred_subs):
            var_subs = set(list(itertools.chain(*[[(x, y) for x, y in zip(pred.args, sub) if isVariable(x)] for pred, sub in zip(self.preds, pred_sub)])))
#             print('>> varsubs', self, var_subs)
            if len(var_subs) == len(self.vars):
                sub_map = {x:y for x, y in var_subs}
                subs.add(tuple(sub_map.get(arg, arg) for arg in self.args))
#         print('>> RULE getSubsByPreds', self, subs)
            
        return subs

    def getSubs(self):
        id = getID(self)
        if id not in uni_subs:
            uni_subs[id] = self.getSubsInFacts() | self.getSubsByPreds()
#             print('>> RULE getSubs', id, uni_subs[id])
        return uni_subs[id]

class Predicate:
    def __init__(self, pred):
        self.name, self.vars = getPredNVars(pred)
        self.vars = set(self.vars)
        self.args = getArgs(pred)
        self.unifiable_rules = [rule for rule in uni_rules.values() if unifiable(self, rule)]
        uni_preds.append(self)

    def __repr__(self):
        return f'<PRED {self.name} {self.args}>'
    
    def check(self, subs):
        return tuple(subs.get(arg, arg) for arg in self.args) in self.getSubs()

    def getSubsInFacts(self):
        subs = set()
        for sub in itertools.product(universe, repeat = len(self.vars)):
            sub_map = {x: y for x, y in zip(self.vars, sub)}
            v = tuple(sub_map.get(arg, arg) for arg in self.args)
            if v in uni_facts[self.name]:
                subs.add(v)
#         print('PRED', 'getSubsInFact', self.name, subs)
        return subs
        
    def getSubsInRules(self):
        subs = set()
        for rule in self.unifiable_rules:
            subs.update(newRuleWithLessVars(self, rule).getSubs())
        return subs

    def getSubs(self):
        id = getID(self)
        if id not in uni_subs:
            uni_subs[id] = self.getSubsInFacts() | self.getSubsInRules()
#             print('>> PRED getSubs', id, uni_subs[id], '\n')
        return uni_subs[id]

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

class Question:
    def __init__(self, question):
        self.pred = Predicate(question)
        self.pred.unifiable_rules = [rule for rule in uni_rules.values() if unifiable(self.pred, rule)]

    def getAns(self):
        return list(map(lambda sub: {x:y for x, y in zip(self.pred.args, sub) if isVariable(x)}, self.pred.getSubs()))
    
           
facts = []
def readKB():
    with open('script.pl') as fin:
        lines = ''.join(fin.readlines())
        lines = lines.replace('\n', '').replace(' ', '').replace('.', ' ').split()
        for line in lines:
            if ':-' in line:
                Rule(line)
            else:
                fact = Fact(line)
                universe.update(fact.insts)
                facts.append(fact)

def buildKB():
    for fact in facts:
        fact.activate()

def serve():
    while True:
        question = Question(input('?- '))
        subs = question.getAns()
        if subs:
            print(*subs, sep = '\n')
        print(len(subs) > 0)
        
readKB()
buildKB()
serve()
