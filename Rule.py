import Parser
TERM = 0
RULE = 1

class Rule:

    def __init__(self, name="", start=False):
        self.lhs = []
        self.name = name
        self.start = start
        self.follows = set()
        self.first_plus = set()

    def add_rule(self, production):
        self.lhs.append(production)

    def is_nullable(self):
        for production in self.lhs:
            if [(TERM, 'epsilon')] == production:
                return True
        return False

    def get_matching_rule(self, terminal):
        for production in self.lhs:
            (stype, svalue) = production[0]
            if (TERM, svalue) == (TERM, terminal):
                return production
        return []

    def compute_first_set(self):
        firsts = set()
        for production in self.lhs:
            for term in production:
                (stype, svalue) = term
                if stype == RULE:
                    new_firsts = svalue.compute_first_set()
                    firsts = firsts.union(new_firsts)
                    if 'epsilon' not in new_firsts:
                        break
                if stype == TERM:
                    firsts.add(svalue)
                    break
        return firsts

    def compute_first_plus(self):
        for production in self.lhs:
            (stype, svalue) = production[0]
            if stype == RULE:
                new_firsts = svalue.compute_first_set()
                self.first_plus = self.first_plus.union(new_firsts)
                if 'epsilon' in new_firsts:
                    self.first_plus = self.first_plus.union(self.follows)
            if stype == TERM:
                self.first_plus.add(svalue)
                if 'epsilon' == svalue:
                    self.first_plus = self.first_plus.union(self.follows)


def compute_follow_sets(rules):
    for rule in rules:
        if rule.start:
            rule.follows.add('$')
    for rule in rules:
        for production in rule.lhs:
            if len(production) >= 2:
                (stype, svalue) = production[-1]
                (stype2, svalue2) = production[-2]
                if stype2 == RULE:
                    if stype == RULE:
                        svalue2.follows = svalue2.follows.union(svalue.compute_first_set())
                        if 'epsilon' in svalue.compute_first_set():
                            svalue2.follows = svalue2.follows.union(rule.follows)
                    if stype == TERM:
                        svalue2.follows.add(svalue)
            if len(production) <= 2:
                (stype, svalue) = production[-1]
                if stype == RULE:
                    svalue.follows = svalue.follows.union(rule.follows)
    for rule in rules:
        if 'epsilon' in rule.follows:
            rule.follows.remove('epsilon')

def fixed_point(rules):
    while True:
        start = []
        for rule in rules:
            original = set()
            for x in rule.follows:
                original.add(x)
            start.append(original)
        compute_follow_sets(rules)
        nexts = []
        for rule in rules:
            news = set()
            for x in rule.follows:
                news.add(x)
            nexts.append(news)
        if(start == nexts):
            return

def get_parse_table(productions):
    table = dict()
    fixed_point(productions)
    for g in productions:
        g.compute_first_plus()
        for rule in g.lhs:
            for terminal in g.first_plus:
                (rtype, rvalue) = rule[0]
                if rtype == RULE:
                    table[(g, terminal)] = rule
                else:
                    table[(g, terminal)] = g.get_matching_rule(terminal)
    return table

def print_table(table):
    contents = table.items()
    for item in contents:
        (production, token) = item[0]
        print('Keys:', production.name, token)
        for (stype, svalue) in item[1]:
            if stype == RULE:
                print(stype, svalue.name)
            else: 
                print(stype, svalue)

def table_debug(table, production, token):
    rule = table[production, token]
    res = ""
    for (x, y) in rule:
        if x == RULE:
            res += y.name + " "
        if x == TERM:
            res += y + " "
    print("Production:", production.name, "Token:", token, "RULE:", res)    

E = Rule('E', True)
EP = Rule('EP')
T = Rule('T')
TP = Rule('TP')
F = Rule('F')
E.add_rule([(RULE, T), (RULE, EP)])
EP.add_rule([(TERM, '+'), (RULE, T), (RULE, EP)])
EP.add_rule([(TERM, '-'), (RULE, T), (RULE, EP)])
EP.add_rule([(TERM, 'epsilon')])
T.add_rule([(RULE, F), (RULE, TP)])
TP.add_rule([(TERM, '*'), (RULE, F), (RULE, TP)])
TP.add_rule([(TERM, '/'), (RULE, F), (RULE, TP)])
TP.add_rule([(TERM, 'epsilon')])
F.add_rule([(TERM, '('), (RULE, E), (TERM, ')')])
F.add_rule([(TERM, 'num')])
F.add_rule([(TERM, 'name')])
grammar = [E, EP, T, TP, F]
for g in grammar:
    print(g.name, ': ', g.compute_first_set())
fixed_point(grammar)
print(' ')
for g in grammar:
    print(g.name, ': ', g.follows)
print(' ')
for g in grammar:
    g.compute_first_plus()
    print(g.name, ': ', g.first_plus)
table = get_parse_table(grammar)
tokens = ['num', '*', 'num',  '$']
table_debug(table, E, '(')
table_debug(table, E, 'name')
table_debug(table, E, 'num')
table_debug(table, EP, '$')
table_debug(table, EP, '+')
table_debug(table, EP, '-')
table_debug(table, EP, ')')
table_debug(table, T, '(')
table_debug(table, T, 'name')
table_debug(table, T, 'num')
table_debug(table, TP, '$')
table_debug(table, TP, '+')
table_debug(table, TP, '-')
table_debug(table, TP, '*')
table_debug(table, TP, '/')
table_debug(table, TP, ')')
table_debug(table, F, '(')
table_debug(table, F, 'name')
table_debug(table, F, 'num')
#Parser.syntactic_analysis(tokens, table, [(TERM, '$'), (RULE, E)])
Parser.syntactic_analysis(tokens, table, [(TERM, '$'), (RULE, E)])
