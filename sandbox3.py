from vietnamese import Vietnamese
from long_text import *
import utils


def main():
    INPUT = ""
    while True:
        INPUT = input(">>> ")
        if INPUT == "quit()":
            break
        
        try:
            print(Vietnamese.synthesize(*INPUT.split(' ')))
        except Exception:
            pass
    
if __name__ == "__main__":
    main()