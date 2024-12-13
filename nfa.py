from graphviz import Digraph

class NFA:
    def __init__(self):
        self.states = set()
        self.symbols = set()
        self.start_state = None
        self.final_states = set()
        self.transitions = {}
    
    def parse_file(self, filename):
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            
            #now we have to parse each line
            
            #first line is states
            self.states = set(lines[0].split())
            #second line is symbols
            self.symbols = set(lines[1].split())
            #third line is start state
            self.start_state = lines[2].strip()
            #fourth is final states
            self.final_states = set(lines[3].split())

            #get transitions for every line after
            for state in self.states:
                self.transitions[state] = {}



            for line in lines[4:]:
                initial_state, symbol, next_state = line.split()
                if symbol not in self.transitions[initial_state]:
                    self.transitions[initial_state][symbol] = []
                self.transitions[initial_state][symbol].append(next_state)
            
    def test_parse(self):
        print(self.states)
        print(self.symbols)
        print(self.start_state)
        print(self.final_states)
        for x in self.transitions.items():
            print(x)
    
    def dfs(self, curr, left):
        visited = set()
        def explore(state, remaining_input):
            if remaining_input:
                print(f'Current state: {state}, remaining input: {remaining_input}')
            else:
                print(f"Current state: {state}, no more input to check")
            if state in visited:
                return False
            visited.add(state)
            if not remaining_input:
                if state in self.final_states:
                    return True
                if "~" in self.transitions.get(state, {}):
                    for next_state in self.transitions[state]["~"]:
                        if explore(next_state, remaining_input):
                            return True
                return False
            curr_sym = remaining_input[0]
            everything_else = remaining_input[1:]
            if "~" in self.transitions.get(state, {}):
                for next_state in self.transitions[state]["~"]:
                    if explore(next_state, remaining_input):
                        return True
            if curr_sym in self.transitions.get(state, {}):
                for next_state in self.transitions[state][curr_sym]:
                    if explore(next_state, everything_else):
                        return True
            return False
        return explore(curr, left)


    def accept(self, w: str):
        return self.dfs(self.start_state, w)
    

    def visualize(self, filename="nfa_visualization"):
        dot = Digraph(format="png")
        
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape="doublecircle")
            else:
                dot.node(state, shape="circle")
        
        # Add transitions
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(state, next_state, label=symbol)
        dot.node("", shape="none")
        dot.edge("", self.start_state)
        dot.render(filename, cleanup=True)
        print(f"Visualization saved to {filename}.png")