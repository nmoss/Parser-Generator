

Term = 0
Rule = 1

T_LPAR = 0
T_RPAR = 1
T_A = 2
T_PLUS = 3
T_END = 4
T_INVALID = 5

N_S = 0
N_F = 1


###
# Columns indexed by N_S and N_F
# Rows indexed by Terminals
# The number in the cell refers to which rule to put on the stack 
## 
table = [[1, -1, 0, -1, -1, -1],
         [-1, -1, 2, -1, -1, -1]]

rules = [[(Rule,N_F)],
        [(Term, T_LPAR), (Rule,N_S), (Term, T_PLUS), (Rule,N_F), (Term, T_RPAR)],
        [(Term,T_A)]]

stack = [(Term,T_END), (Rule,N_S)]

def lexer(inputstring):
    tokens = []
    for c in inputstring:
        if c == '+' : tokens.append(T_PLUS)
        elif c == '(' : tokens.append(T_LPAR)
        elif c == ')' : tokens.append(T_RPAR)
        elif c == 'a' : tokens.append(T_A)
    tokens.append(T_END)
    print(tokens)
    return tokens
        
def syntactic_analysis(tokens):
    position = 0
    while len(stack) > 0:
        (stype, svalue) = stack.pop()
        token = tokens[position]
        if stype == Term:
            if svalue == token:
                position += 1
                print('pop', svalue)
                if token == T_END:
                    print('input accepted')
            else:
                print('bad term on input:', token)
                break
        elif stype == Rule:
            print('svalue', svalue, 'token', token)
            rule = table[svalue][token]
            print('rule', rule)
            for r in reversed(rules[rule]):
                stack.append(r)
        print('stack', stack)

tokens = lexer("(a+a)")
syntactic_analysis(tokens)
