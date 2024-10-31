"""
Run this for the app that you can type in (stable, but can only use v7 in the app)
"""
import time
import sys

from PyQt5.QtWidgets import QApplication
from app.app import V7App
from app.args import parse_args

if __name__ == '__main__':
    args, input_agent_args = parse_args()
    
    session = str(time.time())
    if args.ai:
        from imethod.v7ai import AIInputMethod
        inputAgent = AIInputMethod(**input_agent_args)
        
    else:
        from imethod.v7 import InputMethod
        inputAgent = InputMethod(**input_agent_args)
    
    app = QApplication(sys.argv)
    run_app = V7App(
        verbose=args.verbose,
        minimal=args.minimal,
        size=args.size,
        lang=args.lang,
        inputAgent=inputAgent, 
        session=session
    )
    sys.exit(app.exec_())
