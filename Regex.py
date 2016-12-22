import Automata

def expand_character_sets(regex):
    lowers = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
    uppers = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
    digits = "0|1|2|3|4|5|6|7|8|9"
    if("[a-zA-Z0-9]" in regex):
        new = "(" + lowers + "|" + uppers + "|" + digits + ")"
        regex = regex.replace("[a-zA-Z0-9]", new)
    if("[a-zA-Z]" in regex):
        new = "(" + lowers + "|" + uppers + ")"
        regex = regex.replace("[a-zA-Z]", new)
    if("[0-9]" in regex):
        new = "(" + digits + ")"
        regex = regex.replace("[0-9]", new)
    if("[a-z]" in regex):
        new = "(" + lowers + ")"
        regex = regex.replace("[a-z]", new)
    if("[A-Z]" in regex):
        new = "(" + uppers + ")"
        regex = regex.replace("[A-Z]", new)
    return regex

def single_nfa(x):
    nfa = Automata.Automata(x)
    s0 = Automata.State()
    s1 = Automata.State()
    s0.add_transition(x,s1)
    nfa.add_state(s0)
    nfa.add_state(s1)
    return nfa

def crush(stack):
    nfa = stack.pop()
    while len(stack) > 0:
        nfa2 = stack.pop()
        nfa = nfa2.concat(nfa)
    return nfa

def find_matching(start, regex):
    close = start
    count = 1
    while(count > 0):
        close = close + 1
        character = regex[close]
        if(character == '('):
            count = count + 1
        if(character == ')'):
            count = count - 1
    return close

def create_NFA(regex):
    regex = expand_character_sets(regex)
    stack = []
    i = 0
    while i < len(regex):
        if(regex[i] == '\\'):
            i = i + 1
            nfa = single_nfa(regex[i])
            stack.append(nfa)
        elif(regex[i] == '*'):
            nfa = stack.pop()
            nfa = nfa.kleene()
            stack.append(nfa)
        elif(regex[i] == '('):
            end = find_matching(i, regex)
            nfa = create_NFA(regex[i+1:end])
            stack.append(nfa)
            i = end 
        elif(regex[i] == '|'):
            nfa = crush(stack)
            nfa1 = create_NFA(regex[i+1:len(regex)])
            nfa = nfa.union(nfa1)
            stack.append(nfa)
            break
        else:
            nfa = single_nfa(regex[i])
            stack.append(nfa)
        i = i + 1
    nfa = crush(stack)
    return nfa

def get_matcher(regex):
    nfa = create_NFA(regex)
    dfa = nfa.to_DFA()
    return dfa

#print(get_matcher("__*[a-zA-Z0-9][a-zA-Z0-9]*_*|[a-zA-Z]").to_string())
