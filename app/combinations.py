import sys

from pynput.keyboard import Key, KeyCode

if sys.platform == 'darwin':
    CONTROL_KEY = Key.cmd
    LEFT_CONTROL_KEY = Key.cmd_l
    RIGHT_CONTROL_KEY = Key.cmd_r
    SPECIAL_KEY = Key.ctrl
    
    HELP_COMBINATION = {
        SPECIAL_KEY,
        KeyCode(char='h')
    }
    TOGGLE_ENABLE_COMBINATION = {
        CONTROL_KEY,
        Key.alt,
        KeyCode(char='√')
    }
    QUIT_COMBINATION = {
        SPECIAL_KEY,
        KeyCode(char='v')
    }
    
else:
    CONTROL_KEY = Key.ctrl
    LEFT_CONTROL_KEY = Key.ctrl_l
    RIGHT_CONTROL_KEY = Key.ctrl_r
    SPECIAL_KEY = Key.ctrl
    
    # TODO: Implement for window
    HELP_COMBINATION = None
    TOGGLE_ENABLE_COMBINATION = {
        CONTROL_KEY,
        Key.alt,
        KeyCode(char='v')
    }
    # TODO: Implement for window
    QUIT_COMBINATION = None

REMOVE_LAST_TERM_COMBINATION = {
    Key.backspace
}
NEXT_PAGE_COMBINATION = {
    Key.alt_r
}
PREV_PAGE_COMBINATION = {
    RIGHT_CONTROL_KEY
}

FAST_COMBINATION = None
ADD_RAW_COMBINATION = {
    Key.space
}
