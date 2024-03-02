from vietnamese import Vietnamese
from long_text import *
import utils

def main():
    INPUT = ""
    while True:
        INPUT = input(">>> ")
        if INPUT == "quit()":
            break
        INPUT = utils.separate_words(INPUT)
        for word in INPUT:
            print(Vietnamese.CRT(word.lower()))
    
    
if __name__ == "__main__":
    main()