import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel, QPushButton, QHBoxLayout, QSpacerItem
from PyQt5.QtCore import Qt

from inputmethod import InputMethod
# from timeout import run_function_with_timeout

class V7App(QWidget):
    def __init__(self, inputAgent: InputMethod):
        super().__init__()
        self.inputAgent = inputAgent
        self.ready = False              # If ready, pressing a number will choose the combination number shown
        self.predictions = {
            'lst': [],
            'page': 0,
            'maxpage': 0
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle('v7 Typing Method')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()
        
        welcome_label = QLabel("""
Welcome to v7!
Special consonants:
- `z` for `gi`. (z6  → giúp, giết, giáp, ...)
- `dd` for `đ`. (dd4 → đã, đãi, đỗ, ...)
*Note: 
1/ Please turn off Unikey or other keyboard input tools when using this app to avoid conflicts.
2/ Not optimized yet, if you want to use more than 3 terms, please provide rhymes for less computing. 
(don't type `ng0l2ng0ng4`, instead type something like `nguy0li1ngon0ngu4` for `nguyên lý ngôn ngữ`)
3/ Press `Enter` to append raw input to the text area at the bottom.
""")
        layout.addWidget(welcome_label)
        
        self.input_box = QLineEdit()
        self.input_box.keyPressEvent = self.keyPressEventInputBox
        self.input_box.textChanged.connect(self.predict)
        self.input_box.returnPressed.connect(self.addRaw)
        layout.addWidget(self.input_box)
        
        pred_label_layout = QHBoxLayout()
        
        pred_label = QLabel("Predictions")
        pred_label_layout.addWidget(pred_label)
        pred_help = QLabel("Usage: Press key [①-⑨] / ← → / ⌫ / ⏎ ")
        pred_label_layout.addWidget(pred_help)
        layout.addLayout(pred_label_layout)
        
        pred_result_layout = QHBoxLayout()
        
        self.predict_box = QTextEdit()
        self.predict_box.setMinimumHeight(155)
        self.predict_box.setReadOnly(True)
        pred_result_layout.addWidget(self.predict_box)
        
        self.predict_info = QLabel("")
        pred_result_layout.addWidget(self.predict_info)
        
        layout.addLayout(pred_result_layout)
        
        self.text = QTextEdit()
        layout.addWidget(self.text)
        
        button_layout = QHBoxLayout()
        
        copy_button = QPushButton("Copy")
        copy_button.clicked.connect(self.copy_text)
        button_layout.addWidget(copy_button)

        button_layout.addSpacerItem(QSpacerItem(20, 20))

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)
        
        self.setLayout(layout)

        self.show()
    
    def keyPressEventInputBox(self, event):
        if event.key() == Qt.Key_Backspace:
            # Remove the last term
            input = self.input_box.text()
            raws = inputAgent.seperate_raws(input)
            self.input_box.setText("".join(raws[:-1]))
        elif self.ready and event.key() == Qt.Key_Left:
            if self.predictions['page'] > 1:
                self.predictions['page'] -= 1
            self.update_pred_result()
        elif self.ready and event.key() == Qt.Key_Right:
            if self.predictions['page'] < self.predictions['maxpage']:
                self.predictions['page'] += 1
            self.update_pred_result()
        elif self.ready and (event.key() >= Qt.Key_1 and event.key() <= Qt.Key_9):
            number = int(event.text())
            true_index = number - 1
            try:                
                comb = self.predictions['lst'][true_index + 9*(self.predictions['page'] - 1)]
                self.update_text(comb)
                self.reset_input_box()            
            except:
                pass
        else:
            QLineEdit.keyPressEvent(self.input_box, event)
    
    def reset_input_box(self):
        self.input_box.clear()
        self.predictions = {
            'lst': [],
            'page': 0,
            'maxpage': 0
        }
        self.ready = False
        
    def clear_text(self):
        self.text.clear()
        
    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text.toPlainText())
        
    def predict(self):
        input = self.input_box.text()
        
        '''
        Check if the current inpot_box is predictable or not.
        '''
        try:
            # combination_possibilities = run_function_with_timeout(self.inputAgent.predict, timeout_seconds=3, input_string=input)
            combination_possibilities = self.inputAgent.predict(input)
            if combination_possibilities is None:
                raise Exception
            '''
            # If predicting process is timed out
            except TimeoutError:
                print("Function execution exceeded timeout")
                self.reset_input_box()
            '''
            
        # If not predictable
        except:
            self.predict_box.clear()
            self.predict_info.setText(f"")
            self.ready = False
        
        # If predictable  
        else:
            self.predictions['lst'] = combination_possibilities
            self.predictions['page'] = 1
            self.predictions['maxpage'] = (len(combination_possibilities) - 1) // 9 + 1
            self.update_pred_result()    
            self.ready = True
    
    def addRaw(self):
        self.update_text(self.input_box.text(), spaced=False)
        self.reset_input_box()
    
    def update_predict_box(self):
        self.predict_box.clear()            
        showing = self.predictions['lst'][
            0 + 9*(self.predictions['page'] - 1):
            9 + 9*(self.predictions['page'] - 1)
        ]
        for i, comb in enumerate(showing, start=1):
            self.predict_box.append(f"{i}\t {comb}")
    def update_predict_info(self):
        self.predict_info.setText(f"Showing\n{self.predictions['page']}/{self.predictions['maxpage']}")
    def update_pred_result(self):
        self.update_predict_box()
        self.update_predict_info()
        
    def update_text(self, new, spaced=True):
        current_text = self.text.toPlainText()
        if current_text == "":
            self.text.setPlainText(new)
            return
        
        space = ' ' if spaced else ''
        updated = f"{current_text}{space}{new}"
        self.text.setPlainText(updated)
        
    

if __name__ == '__main__':
    # Learn more about these configuration in InputMethod
    inputAgent = InputMethod(
        flexible_tones=False,
        strict_k=False,
        flexible_k=False
    )
    app = QApplication(sys.argv)
    run_app = V7App(inputAgent=inputAgent)
    sys.exit(app.exec_())
