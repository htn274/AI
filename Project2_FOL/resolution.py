def main(filename):
    from collections import defaultdict
    import itertools
    import sys
    import copy
    sys.setrecursionlimit(1000000)

    uni_facts = []
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
    
    def getId(clause):
        clause.preds.sort(key = lambda pred: pred.name)
        return ','.join(str(pred) for pred in clause.preds)

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


        # def __repr__(self):
        #     return '<RULE {self.name} {self.args} {self.vars} {self.preds}>'
        def toClauses(self):
            # [X, Y, Z], {cat', dog, cat2}
            # -> (cat, cat, cat)
            # (cat, cat, dog) -> sub
            # ...
            clauses = dict()
            for sub in itertools.product(universe, repeat = len(self.vars)):
                sub_map = {var:val for var, val in zip(self.vars, sub)}
                new_preds = [pred.sub(sub_map) for pred in self.preds]
                for pred in new_preds:
                    pred.is_negated = True
                new_preds.append(self.convert_pred().sub(sub_map))
                clause = Clause(new_preds)
                clauses[getId(clause)] = clause
            return clauses

        def convert_pred(self):
            pred = self.name + '('
            for x in self.args[:-1]:
                pred = pred + x + ','
            pred = pred + self.args[-1] + ')'
            return Predicate(pred)

    #CNF form
    class Clause:
        def __init__(self, predList = []):
            self.preds = predList
        
        def __repr__(self):
            return getId(self)

        def remove_pred(self, pred):
            while pred in self.preds:
                self.preds.remove(pred)

        def __add__(self, other):
            result = Clause()
            result.preds = self.preds + other.preds 
            return result
        
    class Predicate:
        def __init__(self, pred = None):
            if pred:
                self.name = getName(pred)
                self.vars = set(getVars(pred))
                self.args = getArgs(pred)
            self.is_negated = False
        
        def sub(self, sub_map):
            pred = copy.deepcopy(self)
            pred.args = [sub_map.get(arg, arg) for arg in self.args]
        
            return pred

        def __repr__(self):
            return ('~' if self.is_negated else '') + self.name + '(' + ','.join(self.args) + ')'
        
        def set_not(self):
            self.is_negated = not self.is_negated

    class Fact:
        def __init__(self, fact):
            self.name = getName(fact)
            self.args = getArgs(fact)
            self.vars = set(arg for arg in self.args if isVariable(arg))
            self.insts = set(arg for arg in self.args if not isVariable(arg))
        
        def toClauses(self):
            clauses = dict()
            for sub in itertools.product(universe, repeat = len(self.vars)):
                sub_map = {x: y for x, y in zip(self.vars, sub)}
                v = list(sub_map.get(arg, arg) for arg in self.args)
                pred = Predicate()
                pred.name = self.name
                pred.args = v
                clause = Clause([pred])
                clauses[getId(clause)] = clause
            return clauses

    class Question(Rule):
        def __init__(self, content):
            self.cont = Predicate(content)

        def getAns(self):
            ans = []
            content = self.cont
            for sub in itertools.product(universe, repeat = len(content.vars)):
                sub_map = {x: y for x, y in zip(content.vars, sub)}
                tmp = content
                pred = tmp.sub(sub_map)
                if resolution(pred):
                    ans.append(sub_map)
            return ans
            # return list(map(lambda sub: {x:y for x, y in zip(self.cont.args, sub) if isVariable(x)}, self.cont.getSubsInFacts()))
        
    def readKB():
        import sys
        with open(filename, 'r') as fin:
            lines = ''.join(fin.readlines())
            lines = lines.replace('\n', '').replace(' ', '').replace('.', ' ').split()
            for line in lines:
                if ':-' in line:
                    uni_rules.append(Rule(line))
                else:
                    uni_facts.append(Fact(line))

    uni_clauses = dict()
    def buildKB():
        for fact in uni_facts:
            universe.update(fact.insts)

        for c in uni_facts + uni_rules:
            uni_clauses.update(c.toClauses()) 

    def removeall(pred, clause):
        clause.remove_pred(pred)
        return clause

    def check_dual(pred_1, pred_2):
        if pred_1.is_negated == pred_2.is_negated:
            return False
        return pred_1.args == pred_2.args and pred_1.name == pred_2.name

    # c1, c2: Clause
    # return: clause can obtain by resolving c1 and c2
    def resolve(c1, c2):
        clause_result = dict()
        for pred_i in c1.preds:
            for pred_j in c2.preds:
                if check_dual(pred_i, pred_j):
                    clause_new = removeall(pred_i, c1) + removeall(pred_j, c2)
                    clause_result[getId(clause_new)] = clause_new

        return clause_result

    # KB: clause list, alpha: predicate 
    # return whether alpha follow KB
    def resolution(alpha):
        clauses = copy.deepcopy(uni_clauses)

        alpha.set_not()
        alpha = Clause([alpha])
        clauses[getId(alpha)] = alpha
        new_clauses = dict()
        
        while True:
            n = len(clauses)
            for (ci, cj) in itertools.combinations(clauses.values(), 2):
                resolvents = resolve(ci, cj)
                if "" in resolvents:
                    return True
                new_clauses.update(resolvents)

            if set(new_clauses.keys()).issubset(set(clauses.keys())):
                return False
            clauses.update(new_clauses)
        
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
