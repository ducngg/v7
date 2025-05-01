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
        LEFT_CONTROL_KEY,
        RIGHT_CONTROL_KEY
    }
    QUIT_COMBINATION = {
        LEFT_CONTROL_KEY,
        RIGHT_CONTROL_KEY,
        SPECIAL_KEY
    }
    NEXT_PAGE_COMBINATION = {
        Key.alt_r
    }
    PREV_PAGE_COMBINATION = {
        RIGHT_CONTROL_KEY
    }

else:
    CONTROL_KEY = Key.ctrl
    LEFT_CONTROL_KEY = Key.ctrl_l
    RIGHT_CONTROL_KEY = Key.ctrl_r
    SPECIAL_KEY = Key.alt_l
    
    HELP_COMBINATION = {
        SPECIAL_KEY,
        KeyCode(char='h')
    }
    TOGGLE_ENABLE_COMBINATION = {
        LEFT_CONTROL_KEY,
        RIGHT_CONTROL_KEY
    }
    QUIT_COMBINATION = {
        LEFT_CONTROL_KEY,
        RIGHT_CONTROL_KEY,
        SPECIAL_KEY,
    }
    NEXT_PAGE_COMBINATION = {
        Key.ctrl_r
    }
    PREV_PAGE_COMBINATION = {
        Key.alt_gr
    }

REMOVE_LAST_TERM_COMBINATION = {
    Key.backspace
}

PUNCTUATIONS = {
    KeyCode(char='!'),
    # KeyCode(char='"'),
    # KeyCode(char='#'),
    # KeyCode(char='$'),
    # KeyCode(char='%'),
    # KeyCode(char='&'),
    # KeyCode(char="'"),
    # KeyCode(char='('),
    # KeyCode(char=')'),
    # KeyCode(char='*'),
    # KeyCode(char='+'),
    KeyCode(char=','),
    # KeyCode(char='-'),
    KeyCode(char='.'),
    # KeyCode(char='/'),
    KeyCode(char=':'),
    KeyCode(char=';'),
    # KeyCode(char='<'),
    # KeyCode(char='='),
    # KeyCode(char='>'),
    KeyCode(char='?'),
}
ADD_RAW_COMBINATION = {
    Key.space
}
