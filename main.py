import argparse
import time
import sys

from PyQt5.QtWidgets import QApplication
from app.app import V7App
from app.utils import str_to_bool
from utils.vietnamese import Alphabet

from models import Args

USED_COMBINATIONS = Alphabet.VOWELS_Y + ['b', 'c', 'ch', 'd', 'dd', 'g', 'z', 'h', 'k', 'kh', 'l', 'm', 'n', 'ng', 'nh', 'ph', 'q', 'r', 's', 't', 'th', 'tr', 'v', 'x']

if __name__ == '__main__':
    # Learn more about these configuration in InputMethod
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-l", "--lang", type=str,
        choices=["en", "vi"],
        default="en",
        help="Specify the app's language."
    )
    # add ai argument: -a --ai, true or false
    parser.add_argument("-a", "--ai", type=str_to_bool,
        default=True,
        help="Use AI mode."
    )
    parser.add_argument("-v", "--vni_tones", type=str_to_bool,
        default=False,
        help="Use vni tones: Acts like VNI 6-tone system."
    )
    parser.add_argument("-k", "--strict_k", type=str_to_bool,
        default=False,
        help="Use strict k: Only `k` is allowed, you cannot type `c` or `q`."
    )
    parser.add_argument("-n", "--null_consonant", type=str,
        default="hh",
        help="Specify the null consonant (to predict words that have no consonant)."
    )
    parser.add_argument("-e", "--end_of_rhyme", type=str,
        default=".",
        help="Specify the end of rhyme (to yield exact short rhyme)."
    )
    
    args: Args = parser.parse_args()
    input_agent_args = {
        'vni_tones': args.vni_tones,
        'strict_k': args.strict_k,
        'null_consonant': args.null_consonant,
        'end_of_rhyme': args.end_of_rhyme
    }
    
    # You cannot use a number either!
    assert args.null_consonant not in USED_COMBINATIONS, f"ERROR: {args.null_consonant} is a reserved combination!"
    assert len(args.null_consonant) <= 2, f"ERROR: null_consonant must have length of 1 or 2!"
    assert args.end_of_rhyme not in USED_COMBINATIONS, f"ERROR: {args.end_of_rhyme} is a reserved combination!"
    assert len(args.end_of_rhyme) == 1, f"ERROR: end_of_rhyme must have length of 1!"
    
    session = str(time.time())
    if args.ai:
        from imethod.v7ai import AIInputMethod
        inputAgent = AIInputMethod(**input_agent_args)
    else:
        from imethod.v7 import InputMethod
        inputAgent = InputMethod(**input_agent_args)
        
    app = QApplication(sys.argv)
    run_app = V7App(
        lang=args.lang,
        inputAgent=inputAgent, 
        session=session
    )
    sys.exit(app.exec_())
