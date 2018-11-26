from collections import defaultdict
import itertools
import sys
sys.setrecursionlimit(1000000)

uni_facts = defaultdict(set)
uni_preds = []
universe = set()
uni_rules = []

common_subs = defaultdict(set)
common_forward_list = defaultdict(set)

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

def forwardable(forwarder, reciever):
    if forwarder.name == reciever.name\
            and len(forwarder.args) == len(reciever.args)\
            and all((isVariable(fa) and isVariable(ra)) or (not isVariable(fa) and not isVariable(ra) and fa == ra) or (isVariable(ra) and not isVariable(fa))\
            for fa, ra in zip(forwarder.args, reciever.args))\
            and getNormId(forwarder) != getNormId(reciever):
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
        
        id = getNormId(self)
        self.subs = common_subs[id]
        self.forward_list = common_forward_list[id]
        
        for pred_rule in uni_preds + uni_rules:
            if forwardable(pred_rule, self):
                pred_rule.forward_list.add(id)
            if forwardable(self, pred_rule):
                self.forward_list.add(id)
        uni_rules.append(self)

    def __repr__(self):
        return f'<RULE {self.name} {self.args} {self.vars} {self.preds}>'
        
    def activate(self):
        next = []
        pred_subs = [pred.subs for pred in self.preds]

        for pred_sub in itertools.product(*pred_subs):
            var_subs = set(list(itertools.chain(*[[(x, y) for x, y in zip(pred.args, sub) if isVariable(x)] for pred, sub in zip(self.preds, pred_sub)])))
            if len(var_subs) == len(self.vars):
                sub_map = {x:y for x, y in var_subs}
                v = tuple(sub_map.get(arg, arg) for arg in self.args)
                if v not in self.subs:
                    self.subs.add(v)
                    uni_facts[self.name].add(v)

        for pred_rule in self.forward_list:
            if not (pred_rule.subs >= self.subs):
                next.append(pred_rule)
                pred_rule.subs.update(self.subs)
        
        return next

    def convert_pred(self):
        pred = self.name + '('
        for x in self.args[:-1]:
            pred = pred + x + ','
        pred = pred + self.args[-1] + ')'
        return Predicate(pred)

#CNF form
class Clause:
    def __init__(self, rule = None):
        # self.vars = rule.vars
        self.preds = rule.preds 
        for pred in self.preds:
            pred.set_not()
        pred = rule.convertPred()
        preds.append(pred)
    
    def remove_pred(self, pred):
        while pred in self.preds:
            self.preds.remove(pred)

    def __add__(self, other):
        result = Clause()
        result.preds = self.preds + other.preds 
        return result
       
class Predicate:
    def __init__(self, pred):
        self.name = getName(pred)
        self.vars = set(getVars(pred))
        self.args = getArgs(pred)
        
        id = getNormId(self)
        self.subs = common_subs[id]
        self.forward_list = common_forward_list[id]

        for pred_rule in uni_preds + uni_rules:
            if forwardable(pred_rule, self):
                pred_rule.forward_list.add(id)
            if forwardable(self, pred_rule):
                self.forward_list.add(id)
        
        uni_preds.append(self)

    def __repr__(self):
        return f'<PRED {self.name} {self.args}>'
    
    def check(self, sub_map):
        return tuple(sub_map.get(arg, arg) for arg in self.args) in uni_facts[self.name]
    
    def getSubsInFacts(self):
        subs = set()
        for val in uni_facts[self.name]:
            if all(isVariable(arg) or arg == v for arg, v in zip(self.args, val)):
                subs.add(val)
        return subs
    
    def activate(self):
        next = []
        self.subs.update(self.getSubsInFacts())
                
        for pred_rule in self.forward_list:
            if not (pred_rule.subs >= self.subs):
                next.append(pred_rule)
                pred_rule.subs.update(self.subs)

        return next

    def set_not(self):
        self.is_negated = not self.is_negated

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
        self.cont = Predicate(content)

    def getAns(self):
        return list(map(lambda sub: {x:y for x, y in zip(self.cont.args, sub) if isVariable(x)}, self.cont.getSubsInFacts()))
    
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

    for pr in uni_preds + uni_rules:
        pr.activate()

def removeall(pred, clause):
    clause.remove_pred(pred)
    return clause

# c1, c2: Clause
# return: clause can obtain by resolving c1 and c2
def resolve(c1, c2):
    clause_result = []
    for pred_i in c1.preds:
        for pred_j in c2.preds:
            if check_dual(pred_i, pred_j):
                clause_new = removeall(pred_i, c1) + removeall(pred_j, c2)
                clause_result.append(clause_new)

    return clause_result

# KB: clause list, alpha: predicate 
# return whether alpha follow KB
def resolution(alpha):
    #KB and ~alpha
    clauses = [Clause(rule) for rule in uni_rules]
    alpha.set_not()
    clauses.append(alpha)
    new_clauses = set()
    
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in rang(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if False in resolvents:
                return True
            new_clauses.union(set(resolvents))

        if new_clauses.issubset(set(clauses)):
            return False
        for c in new_clauses:
            if c not in clauses:
                clauses.append(c)

readKB()
buildKB()
print(uni_preds)
