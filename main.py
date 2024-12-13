from cake import Cake  # Assuming the Cake class is in cake.py
from nfa import NFA

def main():
    nfa = NFA()
    nfa.parse_file('cake.txt')
    nfa.visualize()
    fin = True
    while fin:
        print('''g = gather ingredients, i = forgot ingredients, k = go to the market, m = mix cake batter, x = red velvet flavoring added, 
              j = chocolate flavoring added, p = pre heat oven, o = put cake batter in oven, 
              e = burnt cake, b = bake cake, f = frost cake, c = put candle on top.''')
        string = input("Type the string with the symbols above, and type STOP to end the program: ")
        for x in string:
            if x not in nfa.symbols:
                print(f"Character {x} not in language's alphabet")
        if string == 'STOP':
            fin = False
        else:
            print("\n===ANSWER===")
            print(nfa.accept(string))
            print("============\n")


if __name__ == '__main__':
    main()
