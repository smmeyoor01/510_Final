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
    # Track visited states to prevent infinite loops with epsilon transitions
        visited = set()

        def explore(state, remaining_input):
            # If we've already visited this state, stop to prevent infinite loops
            if state in visited:
                return False
            visited.add(state)

            # If no input is left, check if we're in a final state
            if not remaining_input:
                if state in self.final_states:
                    return True
                
                # Try epsilon transitions if no input left
                if "~" in self.transitions.get(state, {}):
                    for next_state in self.transitions[state]["~"]:
                        if explore(next_state, remaining_input):
                            return True
                return False

            curr_sym = remaining_input[0]
            everything_else = remaining_input[1:]

            # First, try all possible epsilon transitions without consuming input
            if "~" in self.transitions.get(state, {}):
                for next_state in self.transitions[state]["~"]:
                    if explore(next_state, remaining_input):
                        return True

            # Then try transitions with the current symbol
            if curr_sym in self.transitions.get(state, {}):
                for next_state in self.transitions[state][curr_sym]:
                    if explore(next_state, everything_else):
                        return True

            return False

        # Start exploring from the initial state
        return explore(curr, left)



    
    def accept(self, w: str):
        return self.dfs(self.start_state, w)
    

    
    def to_automathon(self):
        # Convert states, symbols, transitions, start state, and final states into Automathon format
        q = self.states  # Set of states
        sigma = self.symbols  # Set of input symbols
        delta = {}  # Transition dictionary

        # Convert transitions to Automathon format
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    if (state, symbol) not in delta:
                        delta[(state, symbol)] = set()
                    delta[(state, symbol)].add(next_state)

        # Convert transition dictionary values to sets
        delta = {key: frozenset(value) for key, value in delta.items()}

        initial_state = self.start_state  # Initial state
        f = self.final_states  # Final states

        # Create Automathon NFA
        return AutomathonNFA(q, sigma, delta, initial_state, f)

    def visualize(self, filename="nfa_visualization"):
        dot = Digraph(format="png")
        
        # Add states
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape="doublecircle")  # Final states are double circles
            else:
                dot.node(state, shape="circle")
        
        # Add transitions
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(state, next_state, label=symbol)
        
        # Mark the start state
        dot.node("", shape="none")  # Invisible starting point
        dot.edge("", self.start_state)
        
        # Render the graph
        dot.render(filename, cleanup=True)
        print(f"Visualization saved to {filename}.png")