"""
Run this for the global key listener on your whole computer (currently less stable but you can use v7 everywhere)
"""
import time
import sys

from PyQt5.QtWidgets import QApplication
from app.gui import PredictWindow
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
    run_app = PredictWindow(
        verbose=args.verbose,
        size=args.size,
        lang=args.lang,
        inputAgent=inputAgent, 
        session=session
    )
    sys.exit(app.exec_())
