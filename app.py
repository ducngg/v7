import sys
from functools import reduce
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel, QPushButton, QHBoxLayout, QSpacerItem
from PyQt5.QtCore import Qt

from inputmethod import InputMethod

class V7App(QWidget):
    def __init__(self, inputAgent: InputMethod):
        super().__init__()
        self.inputAgent = inputAgent
        self.ready = False              # If ready, pressing a number will choose the combination number shown
        self.latestCombs = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('v7 Typing Method')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()
        
        welcome_label = QLabel("""
Type `x0ch2` and press the number of your desired word in the Predicted box.
Special consonants:
- `z` for `gi`. (z6  → giúp, giết, giáp, ...)
- `dd` for `đ`. (dd4 → đã, đãi, đỗ, ...)
*Note: 
1/ Current app shows just first 9 possibilities for easy choose(press a number to choose). Future app will shows the 9 most common combinations.
2/ Please turn off Unikey or other input methods when using this app to avoid conflicts.
3/ Not optimized yet, please type NO MORE THAN 3 terms.
4/ Press enter to append raw output to the text area below.
""")
        layout.addWidget(welcome_label)
        
        self.input_box = QLineEdit()
        self.input_box.keyPressEvent = self.keyPressEventInputBox
        self.input_box.textChanged.connect(self.processing)
        self.input_box.returnPressed.connect(self.addRaw)
        layout.addWidget(self.input_box)
        
        predicted_label = QLabel("Predictions")
        layout.addWidget(predicted_label)
        
        self.predict_box = QTextEdit()
        self.predict_box.setMinimumHeight(155)
        self.predict_box.setReadOnly(True)
        layout.addWidget(self.predict_box)
        
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
            # 
            # TODO: May change to just delete the last term using inputAgent.seperate_raws()
            #
            self.reset_input_box()
        else:
            QLineEdit.keyPressEvent(self.input_box, event)
    
    def reset_input_box(self):
        self.input_box.clear()
        self.latestCombs = []
        self.ready = False
        
    def clear_text(self):
        self.text.clear()
        
    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text.toPlainText())
        
        
        
    def processing(self):
        input = self.input_box.text()
        
        '''
        See below for self.ready activation and combination showing, this `if` will check if the input is a number.
        Then choose the combination of the chosen number.
        '''
        if self.ready:
            try:
                chosen = int(input[-1])
                assert(chosen != 0)
                
                comb = self.latestCombs[chosen - 1]
                self.update_text(comb)

                self.reset_input_box()
                return
            
            except:
                pass
            
        '''
        Check if the current inpot_box is predictable or not.
        '''
        try:
            combination_possibilities = self.inputAgent.predict(input)
            if combination_possibilities is None:
                raise Exception
        # If not predictable
        except:
            self.predict_box.clear()
            self.ready = False
        
        # If predictable  
        else:        
            self.predict_box.clear()            
            self.latestCombs = combination_possibilities[:9]
            
            for i, comb in enumerate(self.latestCombs, start=1):
                self.predict_box.append(f"{i}: {comb}")
                
            self.ready = True
            
    def addRaw(self):
        self.update_text(self.input_box.text(), spaced=False)
        self.reset_input_box()
        
    def update_text(self, new, spaced=True):
        space = ' ' if spaced else ''
        current_text = self.text.toPlainText()
        if current_text == "":
            updated = f"{new}"
        updated = f"{current_text}{space}{new}"
        self.text.setPlainText(updated)
        
    

if __name__ == '__main__':
    inputAgent = InputMethod()
    app = QApplication(sys.argv)
    ex = V7App(inputAgent=inputAgent)
    sys.exit(app.exec_())
