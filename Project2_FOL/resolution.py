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

rule = input('?- ')
print(getArgs(rule))


