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

from utils.vietnamese import Vietnamese
from utils.dictionary import Dictionary
from utils.logging import exec
from .properties import Assets

from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from imethod.v7 import InputMethod
    from imethod.v7ai import AIInputMethod

from utils.compare import TelexOrVNI
from models import PredictionState
        
HISTORY_PATH = os.path.join('history')
if not os.path.exists(HISTORY_PATH):
    os.makedirs(HISTORY_PATH)

class DictUpdateWindow(QDialog):
    def __init__(
        self, 
        parent = None, 
        assets: Assets = None, 
        session: str = None
    ):
        super().__init__(parent)
        self.assets = assets
        self.session = session
        self.RELOAD = True
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.assets.update_dictionary_title)
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        
        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("background-color: #FFF; color: #224938; border: 1px solid #6D8C68; border-radius: 1px; font-size: 20px; font-weight: bold;")
        self.input_box.keyPressEvent = self.keyPressEventInputBox
        self.input_box.returnPressed.connect(self.update_dict)
        layout.addWidget(self.input_box)
        
        change_log_label_layout = QHBoxLayout()
        
        change_log_label = QLabel(self.assets.change_log)
        change_log_label_layout.addWidget(change_log_label)
        layout.addLayout(change_log_label_layout)
        
        change_log_layout = QHBoxLayout()
        
        self.change_log = QTextEdit()
        self.change_log.setMinimumHeight(230)
        self.change_log.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.change_log.setReadOnly(True)
        change_log_layout.addWidget(self.change_log)
        
        layout.addLayout(change_log_layout)
        
        self.setLayout(layout)
        
    def keyPressEventInputBox(self, event):
        if event.key() == Qt.Key_Backspace:
            current_input_box = self.input_box.text()
            after_backspaced = " ".join(current_input_box.split()[:-1])
            if after_backspaced != "":
                after_backspaced += " "
            self.input_box.setText(after_backspaced)
        else:
            QLineEdit.keyPressEvent(self.input_box, event)
        
    def update_dict(self):
        input = self.input_box.text().lower()
        self.input_box.clear()
        status = ""
        
        if os.path.exists(os.path.join('checkpoints', 'common.json')):
            with open(os.path.join('checkpoints', 'common.json'), mode='r') as common_dict_file:
                common_dict: list = json.load(common_dict_file)
        else:
            common_dict = [] 
        
        if not Vietnamese.areVietnamese(input.split()):
            self.change_log.append(f"{self.assets.invalid}: {input}")
            return
            
        if input not in common_dict:
            common_dict.append(input)
            status = self.assets.added
            status_code = 'A'
        else:
            common_dict.remove(input)
            status = self.assets.removed
            status_code = 'R'
        
        with open(os.path.join('checkpoints', 'common.json'), mode='w') as common_dict_file:
            json.dump(common_dict, common_dict_file, indent=4)
            
        if self.session:
            with open(os.path.join(HISTORY_PATH, f'{self.session}.txt'), 'a') as history:
                history.write(f"{status_code}: {input}\n")
                
        if self.RELOAD:
            Dictionary.reload()
                        
        self.change_log.append(f"{status}: {input}")

class V7App(QWidget):
    def __init__(
        self, 
        lang, 
        inputAgent: Union["InputMethod", "AIInputMethod"], 
        session: str = None, 
        verbose: int = 0,
        minimal: bool = True,
        size: str = 's',
        **kwargs
    ):
        super().__init__()
        self.verbose = verbose
        self.minimal = minimal
        self._size = size
        self.assets = Assets(lang, size)
        self.session = session
        self.inputAgent = inputAgent
        self.ready = False              # If ready, pressing a number will choose the combination number shown
        self.prediction_state = PredictionState()
        
        self.initUI()

    def initUI(self):
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(self.assets.title + ' ' + self.inputAgent.mode)
        self.setGeometry(*self.assets.geometry)
        self.setStyleSheet(self.assets.app_styleSheet)

        layout = QVBoxLayout()
        
        welcome_layout = QHBoxLayout()
        
        welcome_label = QLabel(self.assets.welcome)
        welcome_label.setStyleSheet(self.assets.default_styleSheet)
        welcome_layout.addWidget(welcome_label)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap(self.assets.logo_path)
        logo_pixmap = logo_pixmap.scaledToHeight(self.assets.logo_height, Qt.SmoothTransformation)
        # logo_pixmap = logo_pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        welcome_layout.addWidget(logo_label)
        
        help_button = QPushButton(self.assets.help)
        help_button.setStyleSheet(self.assets.default_styleSheet)
        help_button.setFixedWidth(self.assets.help_button_width)
        help_button.clicked.connect(self.show_help)
        welcome_layout.addWidget(help_button)
        layout.addLayout(welcome_layout)
        
        self.input_box = QLineEdit()
        self.input_box.setStyleSheet(self.assets.input_box_styleSheet)
        self.input_box.keyPressEvent = self.keyPressEventInputBox
        # self.input_box.textChanged.connect(self.predict) # No need anymore
        self.input_box.returnPressed.connect(self.addRaw)
        layout.addWidget(self.input_box)
        
        pred_label_layout = QHBoxLayout()
        
        pred_label = QLabel(self.assets.pred_label)
        pred_label.setStyleSheet(self.assets.default_styleSheet)
        pred_label_layout.addWidget(pred_label)
        pred_help = QLabel(self.assets.usage)
        pred_help.setStyleSheet(self.assets.default_styleSheet)
        pred_label_layout.addWidget(pred_help)
        layout.addLayout(pred_label_layout)
        
        pred_result_layout = QHBoxLayout()
        
        self.predict_box = QTextEdit()
        self.predict_box.setMinimumHeight(self.assets.predict_box_height)
        self.predict_box.setStyleSheet(self.assets.predict_box_styleSheet)
        self.predict_box.setReadOnly(True)
        pred_result_layout.addWidget(self.predict_box)
        
        self.predict_info = QLabel("")
        self.predict_info.setStyleSheet(self.assets.default_styleSheet)
        pred_result_layout.addWidget(self.predict_info)
        
        layout.addLayout(pred_result_layout)
        
        self.result_box = QTextEdit()
        self.result_box.setMinimumHeight(self.assets.result_box_height)
        self.result_box.setStyleSheet(self.assets.result_box_styleSheet)
        layout.addWidget(self.result_box)
        
        self.improvement_log = QLabel(" ")
        self.improvement_log.setStyleSheet(self.assets.default_styleSheet)
        self.improvement_log.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.improvement_log)
        
        button_layout = QVBoxLayout()
        
        if not self.minimal:
            button_row_layout_1 = QHBoxLayout()

            copy_button = QPushButton(self.assets.copy)
            copy_button.setStyleSheet(self.assets.default_styleSheet)
            copy_button.clicked.connect(self.copy_text)
            button_row_layout_1.addWidget(copy_button)

            button_row_layout_1.addSpacerItem(QSpacerItem(10, 10))

            clear_button = QPushButton(self.assets.clear)
            clear_button.setStyleSheet(self.assets.default_styleSheet)
            clear_button.clicked.connect(self.clear_text)
            button_row_layout_1.addWidget(clear_button)

            button_layout.addLayout(button_row_layout_1)

        # Only need `Add your common phrase` button if in Dictionary mode
        if "Dictionary" in self.inputAgent.mode:
            button_row_layout_2 = QHBoxLayout()
            
            common_dict_window_button = QPushButton(self.assets.add_phrase_button)
            common_dict_window_button.setStyleSheet(self.assets.default_styleSheet)
            common_dict_window_button.clicked.connect(self.open_update_common_dict_window)
            
            button_row_layout_2.addWidget(common_dict_window_button)

            button_layout.addLayout(button_row_layout_2)

        # check if button_layout has something
        if button_layout.count() > 0:
            layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.show()
    
    def show_help(self):
        help_text = self.assets.instruction
        help_box = QMessageBox(parent=self)
        help_box.setText(help_text)
        help_box.setWindowTitle(self.assets.help)
        help_box.setFixedWidth(800) 
        help_box.exec_()
        
    def open_update_common_dict_window(self):
        self.common_dict_window = DictUpdateWindow(
            parent=self, 
            assets=self.assets,
            session=self.session
        )
        self.common_dict_window.show()
    
    def keyPressEventInputBox(self, event: QKeyEvent):
        
        modifiers = event.modifiers()
        # print(modifiers)
        # print('\t', modifiers == Qt.ControlModifier)
        # modifiers == Qt.MetaModifier
        
        # Remove the last term
        if event.key() == Qt.Key_Backspace:
            input = self.input_box.text()
            if input != "":
                raws = self.inputAgent.seperate_raws(input)
                self.input_box.setText("".join(raws[:-1]))
                
                self.prediction_state.buffer = self.prediction_state.buffer[:-1]
                self.predict()
            
            # Remove the last word from result_box
            else:
                current_result_box = self.result_box.toPlainText()
                self.result_box.setPlainText(" ".join(current_result_box.split()[:-1]))
        
        # Previous page
        elif self.ready and event.key() == Qt.Key_Left:
            if self.prediction_state.page > 1:
                self.prediction_state.page -= 1
            chosen_index = 0 + 9*(self.prediction_state.page - 1)
            top_comb = self.prediction_state.lst[chosen_index]
            self.prediction_state.buffer = top_comb.split()
            self.update_pred_result()
        
        # Next page
        elif self.ready and event.key() == Qt.Key_Right:
            if self.prediction_state.page < self.prediction_state.maxpage:
                self.prediction_state.page += 1
            chosen_index = 0 + 9*(self.prediction_state.page - 1)
            top_comb = self.prediction_state.lst[chosen_index]
            self.prediction_state.buffer = top_comb.split()
            self.update_pred_result()
            
        # ADVANCED: Handle Ctrl/Cmd + 1-9 key combinations: Move the chosen one to top
        elif self.ready and modifiers & Qt.ControlModifier and Qt.Key_1 <= event.key() <= Qt.Key_9:
            number = event.key() - Qt.Key_0  # Convert Qt.Key_1, Qt.Key_2,... to 1, 2, ...
            true_index = number - 1
            chosen_index = true_index + 9*(self.prediction_state.page - 1)
            try:
                chosen_comb = self.prediction_state.lst.pop(chosen_index)
                self.prediction_state.lst.insert(0, chosen_comb)
                self.prediction_state.buffer = chosen_comb.split()
                
                self.prediction_state.page = 1
                self.update_pred_result()
            except:
                pass
        
        # Handle 1-9 key: Choose the combination
        elif self.ready and (event.key() == Qt.Key_Space or (event.key() >= Qt.Key_1 and event.key() <= Qt.Key_9)):
            if event.key() == Qt.Key_Space:
                number = 1
            else:
                number = int(event.text())
                
            true_index = number - 1
            chosen_index = true_index + 9*(self.prediction_state.page - 1)
            try:
                comb = self.prediction_state.lst[chosen_index]
                self.update_result_box(comb)
                self.update_improvement_log(comb)
                
                if self.session:
                    with open(os.path.join(HISTORY_PATH, f'{self.session}.txt'), 'a') as history:
                        history.write(f"{self.input_box.text()} {comb}\n")
                
                self.reset_input_box()
                self.reset_predict_box()   
            except:
                pass
        
        # Base case: normal input to the input_box
        else:
            QLineEdit.keyPressEvent(self.input_box, event)
        
            # just predict if event is key A -> Z or 0 -> 9       
            if (event.key() >= Qt.Key_A and event.key() <= Qt.Key_Z) or \
            (event.key() >= Qt.Key_0 and event.key() <= Qt.Key_9):
                self.predict()
    
    def reset_input_box(self):
        self.input_box.clear()
        self.prediction_state.reset()
        self.ready = False
    
    def reset_predict_box(self):
        self.predict_box.clear()
        self.predict_info.setText(f"")
        self.ready = False
        
    def clear_text(self):
        self.result_box.clear()
        
    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_box.toPlainText())
        
    def call_predict(self):
        input = self.input_box.text()
        context = self.result_box.toPlainText()
        
        # AI Mode
        if "AI" in self.inputAgent.mode:
            # Nothing in buffer
            if not self.prediction_state.buffer:
                combination_possibilities = self.inputAgent.predict(input, context=context)
                
            # Buffer has something
            else:
                raws = self.inputAgent.seperate_raws(input)
                last = raws[-1]
                
                # len(raws) == len(buffer) => Just after delete
                if len(raws) == len(self.prediction_state.buffer):
                    buffer = ' '.join(self.prediction_state.buffer[:-1])
                
                    combination_possibilities = self.inputAgent.predict(
                        last, 
                        context=context+' '+buffer
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
                        context=context+' '+buffer
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
                verbose=self.verbose
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
    
    def addRaw(self):
        self.update_result_box(self.input_box.text(), spaced=False)
        self.reset_input_box()
    
    def update_predict_box(self):
        self.predict_box.clear()            
        showing = self.prediction_state.lst[
            0 + 9*(self.prediction_state.page - 1):
            9 + 9*(self.prediction_state.page - 1)
        ]
        
        self.predict_box.append(f"{1}\t{showing[0]}\t←")
        for i, comb in enumerate(showing[1:], start=2):
            self.predict_box.append(f"{i}\t{comb}")
            # self.predict_box.append(f"{i} ⎯⎯⎯ {comb}")
            # self.predict_box.append(f"{i}{' '*(3+(i-1)//3*2)}{comb}")
            
    def update_predict_info(self):
        self.predict_info.setText(f"{self.assets.page}\n{self.prediction_state.page}/{self.prediction_state.maxpage}")
    def update_pred_result(self):
        self.update_predict_box()
        self.update_predict_info()
        
    def update_result_box(self, new, spaced=True):
        current_result_box = self.result_box.toPlainText()
        if current_result_box == "":
            self.result_box.setPlainText(new)
            return
        
        space = ' ' if spaced else ''
        updated = f"{current_result_box}{space}{new}"
        self.result_box.setPlainText(updated)
        
    def update_improvement_log(self, phrase: str):
        phrase = phrase.split()
        v7_keys = len(self.input_box.text()) + 1 # Plus choosing key
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
