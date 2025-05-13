from re import M
import sys, time, os
import argparse
import json
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QTextEdit, 
    QLineEdit, 
    QLabel, 
    QPushButton, 
    QHBoxLayout, 
    QSpacerItem, 
    QMessageBox, 
    QDialog
)
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtCore import Qt

from utils.logging import exec
from app.properties import Assets

# from imethod.v7ai import AIInputMethod
from imethod.v7 import InputMethod

from utils.compare import TelexOrVNI
from models import PredictionState
from typing import Set, List
from utils.path import resource_path

HISTORY_PATH = resource_path(os.path.join('history'))

if not os.path.exists(HISTORY_PATH):
    os.makedirs(HISTORY_PATH)
    
###
from pynput.keyboard import Key, KeyCode, Controller

from .combinations import *
from .listener import ListenerThread

import time

class PredictWindow(QWidget):
    def __init__(
        self, 
        lang, 
        inputAgent, #: AIInputMethod,
        session: str = None, 
        verbose: int = 0,
        size: str = 's',
        **kwargs
    ):
        super().__init__()
        self.verbose = verbose
        self._size = size
        self.assets = Assets(lang, size)
        self.session = session
        self.inputAgent = inputAgent
                
        self.ready = False              # If ready, pressing a number will choose the combination number shown
        self.prediction_state = PredictionState()
        self.context = ""
        self.controller = Controller()
        self.isActivate = True
        self.isEmitting = False
        self.vni_tones = False

        self.initUI()

    def initUI(self):
        desktop_dim = QApplication.desktop().screenGeometry()
        W = desktop_dim.width()
        H = desktop_dim.height()
        _, _, w, h = self.assets.geometry
        self.old_pos = None

        self.setGeometry((W-w)//2, 0, w, h) # Middle top
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.assets.title)
        self.setStyleSheet(self.assets.app_styleSheet)
        self.setWindowOpacity(0.5) 

        layout = QVBoxLayout()
        
        top_line_layout = QHBoxLayout()
        
        self.raw_label = QLabel(self.prediction_state.raw)
        self.raw_label.setStyleSheet(self.assets.default_styleSheet)
        top_line_layout.addWidget(self.raw_label)
        
        self.help_label = QLabel(self.assets.gui_help)
        self.help_label.setStyleSheet(self.assets.default_styleSheet)
        self.help_label.setFixedWidth(self.assets.help_button_width)
        top_line_layout.addWidget(self.help_label)
        
        self.tone_toggle_btn = QPushButton("6 dấu" if self.vni_tones else "8 Thanh")
        self.tone_toggle_btn.setStyleSheet(self.assets.default_styleSheet)
        self.tone_toggle_btn.setFixedWidth(self.assets.toggle_mode_button_width)
        self.tone_toggle_btn.clicked.connect(self.toggle_tone_mode)
        top_line_layout.addWidget(self.tone_toggle_btn)
                
        layout.addLayout(top_line_layout)
        
        pred_result_layout = QHBoxLayout()
        
        self.predict_box = QTextEdit()
        self.predict_box.setMinimumHeight(self.assets.predict_box_height)
        self.predict_box.setStyleSheet(self.assets.predict_box_styleSheet)
        self.predict_box.setFontFamily("monaco")
        self.predict_box.setReadOnly(True)
        pred_result_layout.addWidget(self.predict_box)
        
        self.predict_info = QLabel("")
        self.predict_info.setStyleSheet(self.assets.default_styleSheet)
        pred_result_layout.addWidget(self.predict_info)
        
        layout.addLayout(pred_result_layout)
        
        self.improvement_log = QLabel(" ")
        self.improvement_log.setStyleSheet(self.assets.default_styleSheet)
        self.improvement_log.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.improvement_log)
        
        self.setLayout(layout)
        self.show()
        
        self.listener_thread = ListenerThread(parent=None)
        self.listener_thread.start()
        self.listener_thread.any_signal.connect(self.process_emitted_keys)

        self.warm_up()

    def warm_up(self):
        print("WARMING UP UI...")
        start_time = time.time()
        self.predict_box.clear()
        self.predict_box.append("abc def ghi jkl")
        self.predict_box.clear()
        print(f"WARMED UP IN {time.time() - start_time}s")

    def toggle_tone_mode(self):
        self.vni_tones = not self.vni_tones
        self.tone_toggle_btn.setText("6 dấu" if self.vni_tones else "8 Thanh")
    
    def show_help(self):
        help_text = self.assets.gui_instruction
        help_box = QMessageBox(parent=self)
        help_box.setText(help_text)
        help_box.setWindowTitle(self.assets.help)
        help_box.setFixedWidth(1200) 
        help_box.exec_()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    
    def emit(self, phrase, end):
        self.emit_backspace(len(self.prediction_state.raw) + 1)
        # Extra space for backspace later
        self.controller.type(phrase + end + ' ')
        
        # Maybe don't need this as backspace is pressed after all
        self.listener_thread.clean_up()
        
    def emit_backspace(self, n):
        for _ in range(n):
            # time.sleep(0.01)
            self.controller.tap(Key.backspace)
            # time.sleep(0.01)
    
    def process_emitted_keys(self, emitted_keys: List[Key | KeyCode]):

        if self.isEmitting:
            return

        if set(emitted_keys).issuperset(QUIT_COMBINATION):
            print('Quitting the application')
            QApplication.quit()  # Gracefully quit the app
        
        if set(emitted_keys) == TOGGLE_ENABLE_COMBINATION:
            if self.isActivate:
                print('Disabling and hiding the GUI')
                self.isActivate = False
                self.hide()  # Hide the app GUI
            else:
                print('Enabling and showing the GUI')
                self.isActivate = True
                self.show()  # Show the app GUI
                
            return

        if not self.isActivate:
            return
        
        if set(emitted_keys) == HELP_COMBINATION:
            print("CASE HELP", emitted_keys)
            self.show_help()
            return
        
        if set(emitted_keys).issuperset(REMOVE_LAST_TERM_COMBINATION):
            print("CASE DEL", emitted_keys)
            if self.prediction_state.raw != "":
                
                raws = self.inputAgent.seperate_raws(self.prediction_state.raw)
                will_be_updated_raw = "".join(raws[:-1])
                
                difference = len(self.prediction_state.raw) - len(will_be_updated_raw)
                difference -= 1
                print(f"Should delete {difference} more")
                
                # Backspace with deactivate
                self.isEmitting = True
                with self.listener_thread.deactivated():
                    self.emit_backspace(difference)
                self.isEmitting = False
                
                self.update_raw(will_be_updated_raw)
                if len(self.prediction_state.raw) == 0:
                    self.setWindowOpacity(0.5) 

                self.prediction_state.buffer = self.prediction_state.buffer[:-1]
                self.predict()
                                
            else:
                pass
            
            return
                        
        if self.ready and set(emitted_keys) == PREV_PAGE_COMBINATION:
            print("CASE PREV", emitted_keys)
            if self.prediction_state.page > 1:
                self.prediction_state.page -= 1
            chosen_index = 0 + 9*(self.prediction_state.page - 1)
            top_comb = self.prediction_state.lst[chosen_index]
            self.prediction_state.buffer = top_comb.split()
            self.update_pred_result()
            
            return
        
        if self.ready and set(emitted_keys) == NEXT_PAGE_COMBINATION:
            print("CASE NEXT", emitted_keys)
            if self.prediction_state.page < self.prediction_state.maxpage:
                self.prediction_state.page += 1
            chosen_index = 0 + 9*(self.prediction_state.page - 1)
            top_comb = self.prediction_state.lst[chosen_index]
            self.prediction_state.buffer = top_comb.split()
            self.update_pred_result()
            
            return

        # ADVANCED: Handle Control(Mac) + 1-9 key combinations: Move the chosen one to top
        if SPECIAL_KEY in emitted_keys:
            print("CASE MOVE", emitted_keys)
            try:
                # Get the main key
                emitted_keys = emitted_keys.copy()
                emitted_keys.remove(SPECIAL_KEY)
                number_key = emitted_keys[0]
                
                # Corresponding index in prediction_state.lst
                true_index = int(number_key.char) - 1
                chosen_index = true_index + 9*(self.prediction_state.page - 1)

                # Move to top
                chosen_comb = self.prediction_state.lst.pop(chosen_index)
                self.prediction_state.lst.insert(0, chosen_comb)
                self.prediction_state.buffer = chosen_comb.split()
                
                # Navigate to first page
                self.prediction_state.page = 1
                self.update_pred_result()
                
                return
            except:
                
                return
        
        # # Handle 1-9 key: Choose the combination
        if self.ready:
            number = None
            end = ' '
            
            if emitted_keys[-1] in PUNCTUATIONS:
                number = 1
                end = emitted_keys[-1].char + end
                
            try:
                number_key = emitted_keys[0]
                number = int(number_key.char)
                
                if number == 0:
                    raise Exception
            except:
                pass

            print("CASE CHOOSE", emitted_keys, number, end)
            # Not choosing any combination
            if number is None:
                pass
            else:
                true_index = number - 1
                chosen_index = true_index + 9*(self.prediction_state.page - 1)
                try:
                    comb = self.prediction_state.lst[chosen_index]
                    
                    # Emit with deactivate
                    self.isEmitting = True
                    with self.listener_thread.deactivated():
                        self.emit(comb, end)
                    self.isEmitting = False
                        
                    # Backspace without deactivate
                    self.emit_backspace(1)
                    
                    self.update_improvement_log(comb)
                    
                    if self.session:
                        with open(os.path.join(HISTORY_PATH, f'{self.session}.txt'), 'a', encoding='utf-8') as history:
                            history.write(f"{self.prediction_state.raw} {comb}\n")
                    
                    self.setWindowOpacity(0.5) 
                    self.update_raw('')
                    self.reset_predict_box()
                    self.prediction_state.reset()
                    self.context += " " + comb
                    
                    return
                except Exception as e:
                    print(e)
                    pass
                    
                
        if set(emitted_keys).issuperset(ADD_RAW_COMBINATION):
            print("CASE ADD RAW", emitted_keys)
            
            self.update_raw('')
            self.setWindowOpacity(0.5) 
            self.reset_predict_box()
            self.prediction_state.reset()
            
            return
        
        if Key.cmd not in emitted_keys \
            and Key.cmd_r not in emitted_keys \
            and Key.ctrl not in emitted_keys \
            and Key.ctrl_r not in emitted_keys \
            and Key.alt not in emitted_keys \
            and Key.alt_r not in emitted_keys:

            print("BASE", emitted_keys)
            try:
                only_key = emitted_keys[-1]
                if isinstance(only_key, KeyCode):
                    code = ord(only_key.char)

                    if (
                        (97 <= code <= 122) # Lowercase
                        or (65 <= code <= 90) # Uppercase
                        or (48 <= code <= 57) # Digit
                    ):

                        self.setWindowOpacity(1) 
                        self.update_raw(
                            self.prediction_state.raw + only_key.char
                        )
                        if only_key.char.isalpha() or only_key.char.isdigit():
                            self.predict()
            except:
                print("Fail")
                pass

    def update_raw(self, new):
        self.prediction_state.raw = new
        self.raw_label.setText(self.prediction_state.raw)
    
    def reset_predict_box(self):
        self.predict_box.clear()
        self.predict_info.setText(f"")
        self.ready = False
        
    def call_predict(self):
        input = self.prediction_state.raw
        context = self.context
        
        # AI Mode
        if "AI" in self.inputAgent.mode:
            # Nothing in buffer
            if not self.prediction_state.buffer:
                combination_possibilities = self.inputAgent.predict(input, context=context, vni_tones=self.vni_tones)
                
            # Buffer has something
            else:
                raws = self.inputAgent.seperate_raws(input)
                last = raws[-1]
                
                # len(raws) == len(buffer) => Just after delete
                if len(raws) == len(self.prediction_state.buffer):
                    buffer = ' '.join(self.prediction_state.buffer[:-1])
                
                    combination_possibilities = self.inputAgent.predict(
                        last, 
                        context=context+' '+buffer,
                        vni_tones=self.vni_tones
                    )
                    
                    # Still let the word in buffer to the top
                    combination_possibilities.remove(self.prediction_state.buffer[-1])
                    combination_possibilities.insert(0, self.prediction_state.buffer[-1])
                    
                    combination_possibilities = [
                        (buffer + ' ' + combination_possibility).strip()
                        for combination_possibility in combination_possibilities
                    ]
      
                # Forward predicting
                else:
                    buffer = ' '.join(self.prediction_state.buffer)

                    # Just predict the last term, then concatenate with buffer
                    combination_possibilities = self.inputAgent.predict(
                        last, 
                        context=context+' '+buffer,
                        vni_tones=self.vni_tones
                    )
                    
                    combination_possibilities = [
                        buffer + ' ' + combination_possibility
                        for combination_possibility in combination_possibilities
                    ]
                    
                if self.verbose:
                    print(f"{raws=} -> {last=} || {context=} + {buffer=}")
                    
        # Dictionary Mode
        else:
            combination_possibilities = self.inputAgent.predict(input, context=context)
            
        return combination_possibilities
        
    def predict(self):
        '''
        Check if the current inpot_box is predictable or not.
        '''
        try:
            combination_possibilities = exec(
                "call_predict",
                self.call_predict,
                verbose=1 #self.verbose
            )
            
            if combination_possibilities is None:
                raise Exception # TODO: may raise something more clever
            
        # If not predictable
        except:
            self.reset_predict_box()
        
        # If predictable  
        else:
            self.prediction_state.lst = combination_possibilities
            self.prediction_state.page = 1
            self.prediction_state.maxpage = (len(combination_possibilities) - 1) // 9 + 1
            self.prediction_state.buffer = self.prediction_state.lst[0].split()
            self.update_pred_result()    
            self.ready = True
    
    def update_predict_box(self):
        self.predict_box.clear()            
        showing = self.prediction_state.lst[
            0 + 9*(self.prediction_state.page - 1):
            9 + 9*(self.prediction_state.page - 1)
        ]

        self.predict_box.append(f"{1} {showing[0]} ←")
        for i, comb in enumerate(showing[1:], start=2):
            self.predict_box.append(f"{i} {comb}")
            # self.predict_box.append(f"{i} ⎯⎯⎯ {comb}")
            # self.predict_box.append(f"{i}{' '*(3+(i-1)//3*2)}{comb}")
            
    def update_predict_info(self):
        self.predict_info.setText(f"{self.assets.page}\n{self.prediction_state.page}/{self.prediction_state.maxpage}")

    def update_pred_result(self):
        self.update_predict_box()
        self.update_predict_info()
        
    def update_improvement_log(self, phrase: str):
        phrase = phrase.split()
        v7_keys = len(self.prediction_state.raw) + 1 # Plus choosing key
        original_keys = sum([TelexOrVNI.get_keys_needed_from_word(word) for word in phrase]) + (len(phrase) - 1) # Plus spacing
        improvements = 100 * (original_keys - v7_keys) / original_keys
        if improvements < 0:
            color = "red"
        elif improvements > 0:
            color = "#00FF00"
        else:
            color = "yellow"

        self.improvement_log.setText(f"{self.assets.percent_keys}: {improvements:.2f}%")
        self.improvement_log.setStyleSheet(self.assets.default_styleSheet + f"color: {color};")
