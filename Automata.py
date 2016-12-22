# A NFA or DFA representation
# Contains a list of states
class Automata:

    def __init__(self, expr, accept=-1):
        self.states = []
        self.regex = expr
        self.accept = accept
        self.alphabet = set()

    def add_state(self, state):
        self.states.append(state)

    def epsilon_closure(self, state):
        out = set()
        out.add(state)
        states = state.get_next('$')
        for s in states:
            out.add(s)
            out = out.union(self.epsilon_closure(s))
        return out

    def get_containing(self, closed, result):
        for s in result.states:
            if(s.nfa_set == closed):
                return s

    def subset_construction(self, set_states, start, result, visited):
        for c in self.alphabet:
            nexts = set()
            closed = frozenset()
            for si in set_states:
                nexts = nexts.union(si.get_next(c))
                for sj in nexts:
                    closed = closed.union(self.epsilon_closure(sj))
            if(closed == set_states):
                start.add_transition(c, start)
            elif(len(closed) != 0):
                if closed in visited:
                    s1 = self.get_containing(closed, result)
                    start.add_transition(c, s1)
                else:
                    s1 = State(closed)
                    start.add_transition(c, s1)
                    result.add_state(s1)
                    visited.add(closed)
                    self.subset_construction(closed, s1, result, visited)
    
    def to_DFA(self):
        for s in self.states:
            self.alphabet = self.alphabet.union(s.alphabet)
        self.alphabet.remove('$')
        result = Automata(self.regex, self.states[-1].name)
        new_start = State(self.epsilon_closure(self.states[0]))
        result.add_state(new_start)
        visited = set()
        visited = visited.union(self.epsilon_closure(self.states[0]))
        #self.subset_construction(self.epsilon_closure(self.states[0]), new_start, result, visited)
        self.build_on_inputs(self.epsilon_closure(self.states[0]), new_start, result, visited)
        return result

    def build_on_inputs(self, starting_states, start, result, visited):
        for input_character in self.alphabet:
            next_states = self.run_next_character(starting_states, input_character)
            closed = self.closure_on_next_states(next_states)
            if(closed == starting_states):
                start.add_transition(input_character, start)
            elif closed in visited:
                existing_state = self.get_containing(closed, result)
                start.add_transition(input_character, existing_state)
            elif(len(closed) != 0):
                new_state = State(closed)
                start.add_transition(input_character, new_state)
                result.add_state(new_state)
                visited.add(closed)
                self.build_on_inputs(closed, new_state, result, visited)

    def run_next_character(self, initial_states, input_symbol):
        next_states = set()
        for state in initial_states:
            next_states = next_states.union(state.get_next(input_symbol))
        return next_states
    
    def closure_on_next_states(self, initial_states):
        closed = frozenset()
        for state in initial_states:
            closed = closed.union(self.epsilon_closure(state))
        return closed

    def union(self, automata):
        new_start = State()
        new_start.add_transition('$', self.states[0])
        new_start.add_transition('$', automata.states[0])
        new_accept = State()
        self.states[-1].add_transition('$', new_accept)
        automata.states[-1].add_transition('$', new_accept)
        result = Automata(self.regex + "|" + automata.regex)
        result.add_state(new_start)
        for s in self.states:
            result.add_state(s)
        for s in automata.states:
            result.add_state(s)
        result.add_state(new_accept)
        return result

    def concat(self, automata):
        f = self.states[-1]
        f.add_transition('$', automata.states[0])
        result = Automata(self.regex + automata.regex)
        for s in self.states:
            result.add_state(s)
        for s in automata.states:
            result.add_state(s)
        return result

    def kleene(self):
        result = Automata(self.regex + "*")
        start = State()
        accept = State()
        start.add_transition('$', self.states[0])
        start.add_transition('$', accept)
        self.states[-1].add_transition('$', accept)
        self.states[-1].add_transition('$', self.states[0])
        result.add_state(start)
        for s in self.states:
            result.add_state(s)
        result.add_state(accept)
        return result

    def to_string(self):
        automata_str = "digraph g {\nrankdir = LR; \nedge [arrowsize=0.8];\n"
        automata_str += "label=\"" + self.regex + "\";\n"
        if(self.accept == -1):
            automata_str += "node [shape=doublecircle]; " + str(self.states[-1].name) + ";\n"
        else:
            automata_str += "node [shape=doublecircle]; " + self.accepting_to_str() + "\n"
        automata_str += "node [shape=circle];\n"
        for s in self.states:
            automata_str += s.to_string()
        automata_str += "}"
        return automata_str

    def accepting_to_str(self):
        result = ""
        for s in self.states:
            for sj in s.nfa_set:
                if(sj.name == self.accept):
                    result += str(s.name) + "; "
        return result

    def match_input(self, expression):
        start_state = self.states[0]
        for character in expression:
            possible_states = start_state.get_next(character)
            if(len(possible_states) == 0):
                return False
            start_state = possible_states.pop()

        for nfa_state in start_state.nfa_set:
            if(nfa_state.name == self.accept):
                return True
        return False


class State:
    names = 0

    def __init__(self, nfa_set=set()):
        self.transitions = []
        self.alphabet = set()
        self.name = State.names
        State.names = State.names + 1
        self.nfa_set = nfa_set

    def add_transition(self, symbol, state):
        self.alphabet.add(symbol)
        self.transitions.append((symbol, state))

    def get_next(self, symbol):
        states = set()
        for pair in self.transitions:
            if(symbol in pair):
                states.add(pair[1])
        return states

    def to_string(self):
        state = ""
        for pair in self.transitions:
            state += str(self.name) + " -> " + str(pair[1].name) + " [label=" + "\""+ str(pair[0]) + "\"" + "];\n"
        return state

