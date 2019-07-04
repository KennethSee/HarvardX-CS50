from cs50 import get_string
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python bleep.py dictionary")
        sys.exit(1)
    
    # add dictionary words to set
    set_dict = set()
    dict_file = sys.argv[1]
    f = open(dict_file, "r")
    f1 = f.readlines()
    for line in f1:
        x = line.strip("\n")
        set_dict.add(x)
    
    # obtain message from user
    user_input = get_string("What message would you like to censor?\n")
    
    input_list = user_input.split()
    for word in input_list:
        if word.lower() in set_dict:
            for _ in range(len(word)):
                print("*", end="")
            print(" ", end="")
        else:
            print(f"{word} ", end="")
    print("")

if __name__ == "__main__":
    main()
