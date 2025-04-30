from contextlib import contextmanager

from pynput.keyboard import Key, KeyCode, Listener
from PyQt5.QtCore import QThread, pyqtSignal
from typing import List
import time

import logging
logging.basicConfig(level=logging.DEBUG)

class ListenerThread(QThread):
    """Keyboard listenser, will return the set of keys pressed.
    """
    # https://www.youtube.com/watch?v=k5tIk7w50L4
    any_signal = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.activating = True
        self.current_keys: List[Key | KeyCode] = []
    
    def run(self):
        # Create a listener for detecting key presses
        with Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        ) as listener:
            listener.join()  # Keep the listener running 
            
    def _on_press(self, key: KeyCode | Key):
        """Handles key press events."""
        if not self.activating:
            return 

        logging.debug(f"Received {key} at time: {time.time() % 1000}")

        if key not in self.current_keys:  # Prevent duplicate keys
            self.current_keys.append(key)

        logging.debug(f"Current: {self.current_keys} and {self.activating=}")

        if self.activating:
            logging.debug(f"Sending {self.current_keys}...")
            self.any_signal.emit(self.current_keys)  # Emit signal with current keys

    def _on_release(self, key: KeyCode | Key):
        """Handles key release events."""
        if not self.activating:
            return    

        try:
            if key in self.current_keys:
                self.current_keys.remove(key)

            if key in (Key.shift, Key.shift_r):
                self.current_keys = [k for k in self.current_keys if not (hasattr(k, "char") and k.char.isupper())]
                logging.debug(f"Shift released, clean -> {self.current_keys=}")

            if key == Key.backspace:
                logging.debug(f"Backspace pressed, clean {self.current_keys=} -> []")
                self.current_keys.clear()

        except Exception as e:
            logging.info(e)
            pass
        
    def on(self):
        self.activating = True
        logging.info(f"On at time: {time.time() % 1000}")
        
    
    def off(self):
        self.activating = False
        logging.info(f"Off at time: {time.time() % 1000}")
        
    @contextmanager
    def deactivated(self):
        """Context manager to temporarily turn off the listener."""
        self.off()
        try:
            yield
        finally:
            time.sleep(0.05)
            self.on()

    def clean_up(self):
        self.current_keys = []
    