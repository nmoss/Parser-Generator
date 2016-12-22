TERM = 0
RULE = 1
'''
S = Rule.Rule('S', True)
F = Rule.Rule('F')
rules = [S,F]
S.add_rule([(RULE, F)])
S.add_rule([(TERM, '('), (RULE, S), (TERM, '+'), (RULE, F), (TERM, ')')])
F.add_rule([(TERM, 'a')])
Rule.fixed_point(rules)
table = Rule.generate_parse_table(rules)
'''
'''
E = Rule.Rule('E',True)
EP = Rule.Rule('EP')
T = Rule.Rule('T')
TP = Rule.Rule('TP')
F = Rule.Rule('F')
E.add_rule([(RULE, T), (RULE, EP)])
EP.add_rule([(TERM, '+'), (RULE, T), (RULE, EP)])
#EP.add_rule([(TERM, 'epsilon')])
T.add_rule([(RULE, F), (RULE, TP)])
TP.add_rule([(TERM, '*'), (RULE, F), (RULE, TP)])
#TP.add_rule([(TERM, 'epsilon')])
F.add_rule([(TERM, '('), (RULE, E), (TERM, ')')])
F.add_rule([(TERM, 'id')])
rules = [E, EP, T, TP, F]
Rule.fixed_point(rules)
table = Rule.generate_parse_table(rules)
'''
class node:
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def __repr__(self, level=0):
        ret = "\t"*level+ str(self.value) +"\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret

def ddfs(node, visited, value):
    answer = None
    visited.append(node)
    if node.value == value:
        answer = node
    for child in node.children:
        if child not in visited:
            tmp = ddfs(child, visited, value)
            if tmp != None:
                answer = tmp
    return answer

def syntactic_analysis(tokens, table, stack):
    position = 0
    root = []
    tree = []
    while len(stack) > 0:
        (stype, svalue) = stack.pop()
        token = tokens[position]
        #print('lookahead', token)
        if stype == TERM:
            if svalue == token:
                position += 1
                print('pop', svalue)
                if token == '$':
                    print('input accepted')
            else:
                print('bad term on input', token)
                break
        elif stype == RULE:
            print('svalue', svalue.name, 'lookahead token', token)
            rule = table[svalue, token]
            if(root == []):
                root = node(svalue.name, [])
                tree = root
            else:
                tmp = ddfs(root, [], svalue.name)
                if tmp != None:
                    tree = tmp
            print('tree node: ', tree.value)
            for r in reversed(rule):
                stack.append(r)
            for r in rule:
                (rtype, rvalue) = r
                if rtype == RULE:
                    tree.children.append(node(rvalue.name, []))
                else:
                    tree.children.append(node(rvalue,[]))
            #update the tree to point at the top of the stack
        print_stack(stack)
    print(root)

def parse(position, tokens, table, stack):
    #print_stack(stack)
    if len(stack) > 0:
        (stype, svalue) = stack.pop()
        token = tokens[position]
        if stype == TERM:
            if svalue == token:
                position += 1
                #print('pop', svalue)
                print(svalue, end='')
                if token == '$':
                    return
                    #print('input accepted')
                parse(position, tokens, table, stack)
            else:
                print('bad term on input', token)
        elif stype == RULE:
            #print('svalue', svalue.name, 'lookahead token', token)
            rule = table[svalue, token]
            print('(', svalue.name, ' ', end='')
            for r in reversed(rule):
                stack.append(r)
            parse(position, tokens, table, stack)

def print_stack(stack):
    result = 'stack: '
    for (x, y) in stack:
        if x == RULE:
            result += y.name
        else:
            result += y
        result += ' '
    print(result)

tree = node(1)
x = [1,2,3]
t1 = node(2, [])
t2 = node(1, [])
t3 = node(3, [])
tree.children.append(t1)
tree.children.append(t2)
tree.children.append(t3)

tree = ddfs(tree, [], 1)
print(tree)

#stack = [(TERM, '$'), (RULE,E)]

#syntactic_analysis(['(', 'id',  '+', 'id', ')', '$'])
