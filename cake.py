from nfa import NFA
import string

class Cake(NFA):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.legend = None

    def convert_to_machine(self, filename, output_file):
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            cakes = lines[0].split(',')
            frostings = lines[1].split(",")
            candles = lines[2].split(",")

            states = lines[3].split()
            start = lines[4]
            end = lines[5]

            # Create a map of ingredients to symbols (a-z)
            letters = string.ascii_lowercase
            ingredients = cakes + frostings + candles
            symbols = {}
            for x, ingredient in enumerate(ingredients):
                symbol = letters[x % 26]  # Assign a symbol from a to z
                symbols[ingredient] = symbol

            self.legend = symbols

            rules = []
            for line in lines[6:]:
                parts = line.split()
                rule = ""  # Initialize rule as an empty string

                if len(parts) == 2:  # e.g., q0 q1 (no symbol used, direct state transition)
                    c, n = parts
                    rule = f"{c} ~ {n}"  # Placeholder transition with '~' (no ingredient)
                elif len(parts) == 3:  # e.g., q0 chocolatecake q1
                    c, ingredient, n = parts
                    symbol = symbols.get(ingredient, '~')  # Get the symbol for the ingredient, default to '~'
                    rule = f"{c} {symbol} {n}"  # Use the symbol for the transition
                else:
                    print(f"Warning: Invalid line format - {line}")
                    continue  # Skip invalid lines

                rules.append(rule)

            # Write the output to the file
            with open(output_file, 'w') as out_file:
                out_file.write(" ".join(states) + "\n")
                out_file.write(" ".join(symbols.values()) + "\n")
                out_file.write(start + "\n")
                out_file.write(end + "\n")
                for rule in rules:
                    out_file.write(rule + "\n")

            self.parse_file(output_file)

    
    def get_keys(self):
        for x in self.legend.items():
            print("Legend")
