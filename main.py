import argparse
import time
import sys

from PyQt5.QtWidgets import QApplication
from app.app import V7App
from app.utils import str_to_bool

from models import Args

if __name__ == '__main__':
    # Learn more about these configuration in InputMethod
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-l", "--lang", type=str,
        choices=["en", "vi"],
        default="en",
        help="Specify the language."
    )
    # add ai argument: -a --ai, true or false
    parser.add_argument("-a", "--ai", type=str_to_bool,
        default=True,
        help="Use AI (True or False)"
    )
    parser.add_argument("-t", "--flexibletones", type=str_to_bool,
        default=False,
        help="Use flexible tones (True or False)"
    )
    
    args: Args = parser.parse_args()
        
    session = str(time.time())
    if args.ai:
        from imethod.v7ai import AIInputMethod
        inputAgent = AIInputMethod(
            flexible_tones=args.flexibletones,
            strict_k=False,
            flexible_k=False
        )
    else:
        from imethod.v7 import InputMethod
        inputAgent = InputMethod(
            flexible_tones=args.flexibletones,
            strict_k=False,
            flexible_k=False
        )
    app = QApplication(sys.argv)
    run_app = V7App(
        lang=args.lang,
        inputAgent=inputAgent, 
        session=session
    )
    sys.exit(app.exec_())
