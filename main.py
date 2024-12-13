from cake import Cake  # Assuming the Cake class is in cake.py
from nfa import NFA

def main():
    nfa = NFA()
    nfa.parse_file('cake.txt')
    nfa.visualize()

if __name__ == '__main__':
    main()
