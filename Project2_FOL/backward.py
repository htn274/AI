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

def getName(pred):
    ls = pred.replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
    return ls[0]

def getVars(pred):
    ls = pred.replace('(', ' ').replace(')', ' ').replace(',', ' ').split()
    return [var for var in ls[1:] if isVariable(var)]

def getPreds(rule):
    rule = rule.replace('.', '').replace(' ', '').split(':-')[1]
    preds = rule.split('),')
    preds[-1] = preds[-1].replace(')', '')

    preds = [pred + ')' for pred in preds]
    preds = [Predicate(pred) for pred in preds]
    return preds

def isVariable(s):
    return s[0].isupper() or s[0] == '_'

def delegable(pred, rule):
    if pred.name == rule.name\
            and len(pred.args) == len(rule.args)\
            and all((isVariable(pa) and isVariable(ra)) or (not isVariable(pa) and not isVariable(ra) and pa == ra) or (isVariable(ra) and not isVariable(pa))\
            for pa, ra in zip(pred.args, rule.args)):
        return True
    return False
 
def getNormId(pred):
    c = 0
    id = [pred.name]
    for arg in pred.args:
        if isVariable(arg):
            id.append(f'X{c}')
            c += 1
        else:
            id.append(arg)
    return tuple(id)

import copy
    
def newRuleWithLessVars(pred, rule):
    new_rule = copy.deepcopy(rule)
    sub_map = {x:y for x, y in zip(rule.args, pred.args) if isVariable(x) and not isVariable(y)}
    new_rule.args = [sub_map.get(arg, arg) for arg in rule.args]
    new_rule.preds = [pred.sub(sub_map) for pred in new_rule.preds]
    new_rule.vars = rule.vars - set(sub_map.keys())
    new_rule.arg_vars = set(new_rule.args) & set(new_rule.vars)
    id = getNormId(new_rule)
    if id not in uni_rules:
        uni_rules[id] = new_rule
    else:
        return uni_rules[id]

    for pred in uni_preds:
        if delegable(pred, new_rule):
            pred.delegable_rules.append(new_rule)
    
    return new_rule
    
class Rule:
    def __init__(self, rule):
        self.name = getName(rule)
        self.preds = getPreds(rule)
        self.args = getArgs(rule)
        self.vars = set(var for var in self.args + list(itertools.chain(*[pred.vars for pred in self.preds])) if isVariable(var))
        self.arg_vars = set(self.args) & set(self.vars)
        uni_rules[getNormId(self)] = self
        for pred in uni_preds:
            if delegable(pred, self):
                pred.delegable_rules.append(self)
        self.locked = False

    def __repr__(self):
        return f'<RULE {self.name} {self.args} {self.vars} {self.preds}>'
        
    # return set of tuples of subtitutes
    def getSubsInFacts(self):
        subs = set()
        for val in uni_facts[self.name]:
            if all(isVariable(arg) or arg == v for arg, v in zip(self.args, val)):
                subs.add(val)
        return subs

    def check(self, sub_map):
        return all(pred.check(sub_map) for pred in self.preds)
    
    # return set of submaps
    def getSubsByPreds(self):
        pred_subs = [pred.getSubs() for pred in self.preds]

        subs = set()
        for pred_sub in itertools.product(*pred_subs):
            var_subs = set(list(itertools.chain(*[[(x, y) for x, y in zip(pred.args, sub) if isVariable(x)] for pred, sub in zip(self.preds, pred_sub)])))
            if len(var_subs) == len(self.vars):
                sub_map = {x:y for x, y in var_subs}
                subs.add(tuple(sub_map.get(arg, arg) for arg in self.args))
            
        return subs

    def getSubs(self):
        if self.locked:
            return self.getSubsInFacts()
        self.locked = True
        id = getNormId(self)
        if id not in uni_subs:
            uni_subs[id] = self.getSubsInFacts() | self.getSubsByPreds()
        self.locked = False
        return uni_subs[id]

class Predicate:
    def __init__(self, pred):
        self.name = getName(pred)
        self.vars = getVars(pred)
        self.vars = set(self.vars)
        self.args = getArgs(pred)
        uni_preds.append(self)
        self.delegable_rules = [rule for rule in uni_rules.values() if delegable(self, rule)]
        self.locked = False

    def __repr__(self):
        return f'<PRED {self.name} {self.args}>'
    
    def sub(self, sub_map):
        pred = copy.deepcopy(self)
        pred.args = [sub_map.get(arg, arg) for arg in self.args]
        pred.vars = [arg for arg in pred.args if isVariable(arg)]
        uni_preds.append(pred)
        pred.delegable_rules = [rule for rule in uni_rules.values() if delegable(pred, rule)]
    
        return pred

    def check(self, subs):
        return tuple(subs.get(arg, arg) for arg in self.args) in self.getSubs()

    def getSubsInFacts(self):
        subs = set()
        for val in uni_facts[self.name]:
            if all(isVariable(arg) or arg == v for arg, v in zip(self.args, val)):
                subs.add(val)
        return subs
        
    def getSubsInRules(self):
        subs = set()
        for rule in self.delegable_rules:
            subs.update(newRuleWithLessVars(self, rule).getSubs())
        return subs

    def getSubs(self):
        if self.locked:
            return self.getSubsInFacts()
        self.locked = True
        id = getNormId(self)
        if id not in uni_subs:
            uni_subs[id] = self.getSubsInFacts() | self.getSubsInRules()
        self.locked = False
        return uni_subs[id]

class Fact:
    def __init__(self, fact):
        self.name = getName(fact)
        self.args = getArgs(fact)
        self.vars = set(arg for arg in self.args if isVariable(arg))
        self.insts = set(arg for arg in self.args if not isVariable(arg))
    
    def activate(self):
        for sub in itertools.product(universe, repeat = len(self.vars)):
            sub_map = {x: y for x, y in zip(self.vars, sub)}
            v = tuple(sub_map.get(arg, arg) for arg in self.args)
            uni_facts[self.name].add(v)

class Question(Rule):
    def __init__(self, content):
        q = 'q():-' + content
        import uuid
        q = str(uuid.uuid4()) + '(' + ','.join(Rule(q).vars) + '):-' + content
#         print(q)
        self.cont = Rule(q)

    def getAns(self):
        return list(map(lambda sub: {x:y for x, y in zip(self.cont.args, sub) if isVariable(x)}, self.cont.getSubs()))
    
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
