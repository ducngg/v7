from contextlib import contextmanager

from pynput.keyboard import Key, KeyCode, Listener
from PyQt5.QtCore import QThread, pyqtSignal
from typing import List
import time

import logging
logging.basicConfig(level=logging.DEBUG)

CURRENT_KEYS: List[Key | KeyCode] = []

class ListenerThread(QThread):
    """Keyboard listenser, will return the set of keys pressed.
    """
    # https://www.youtube.com/watch?v=k5tIk7w50L4
    any_signal = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.activating = True
    
    def run(self):
        # Create a listener for detecting key presses
        with Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        ) as listener:
            listener.join()  # Keep the listener running 
            
    def _on_press(self, key: KeyCode | Key):
        global CURRENT_KEYS
        
        # print time hh mm ss below
        logging.debug(f"Received {key} at time: {time.time() % 1000}")
        CURRENT_KEYS.append(key)
        logging.debug(f"Current: {CURRENT_KEYS} and {self.activating=}")
        if self.activating:
            logging.debug(f"Sending {CURRENT_KEYS}...")
            self.any_signal.emit(CURRENT_KEYS)
            
    def _on_release(self, key: KeyCode | Key):
        global CURRENT_KEYS
        
        # https://github.com/moses-palmer/pynput/issues/20
        try:
            # TODO: Sometimes CURRENT_KEYS is not removing all
            CURRENT_KEYS.remove(key)
            if key == Key.backspace:
                logging.debug(f"Backspace pressed, clean {CURRENT_KEYS=} -> []")
                CURRENT_KEYS = []

        except Exception as e:
            logging.info(e)
            pass
        
    def on(self):
        self.activating = True
        logging.info(f"On at time: {time.time() % 1000}")
        
    
    def off(self):
        self.activating = False
        logging.info(f"Off at time: {time.time() % 1000}")
        time.sleep(0.1)
        
    @contextmanager
    def deactivated(self):
        """Context manager to temporarily turn off the listener."""
        self.off()
        try:
            yield
        finally:
            time.sleep(0.1)
            self.on()
