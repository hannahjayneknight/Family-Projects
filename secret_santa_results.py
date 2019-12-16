'''
Imports dictionary from another file where the keys is the person and the value 
is the person they need to buy for.

Reads this dictionary and allows the person to find who they are buying for.
'''
def main():

    import ast

    def import_dict():
        with open('/Users/hannahjayneknight/Desktop/git/personal/secret_santa_dict.txt', 'r') as f:
            d = f.read()
        return ast.literal_eval(d)

    def find_secret_santa():
        d = import_dict()
        name = input('Please type in your name: ')
        print('You are buying for... ' + d[name])
        print('Now please clear the terminal for the next user.')
        return 

    find_secret_santa()

if __name__ == "__main__":
    main()
