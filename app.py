import sys
from functools import reduce
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel, QPushButton, QHBoxLayout, QSpacerItem
from PyQt5.QtCore import Qt

from vietnamese import Vietnamese, Dictionary, InputMethod

class V7App(QWidget):
    def __init__(self, inputAgent):
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
- `hh` for none consonant.  (hh3 → ở, ảnh, ẩn, ...)
- `z` for `gi`.             (z6  → giúp, giết, giáp, ...)
- `dd` for `đ`.             (dd4 → đã, đãi, đỗ, ...)
8-tones system:
- 0 for none
- 1 for accute
- 2 for grave
- 3 for hook
- 4 for tilde
- 5 for underdot
- 6 for accute, ends with (p | t | c | ch)
- 7 for underdot, ends with (p | t | c | ch)
""")
        layout.addWidget(welcome_label)
        
        self.input_box = QLineEdit()
        self.input_box.keyPressEvent = self.keyPressEventInputBox
        self.input_box.textChanged.connect(self.processing)
        # self.input_box.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_box)
        
        predicted_label = QLabel("Predicted")
        layout.addWidget(predicted_label)
        
        self.predict_box = QTextEdit()
        self.predict_box.setMinimumHeight(200)
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
        
        if self.ready:
            try:
                chosen = int(input[-1])
                assert(chosen != 0)
                # print(chosen)
                # print(self.latestCombs)
                comb = self.latestCombs[chosen - 1]
                # print(comb)
                self.update_text(comb)
                
                self.reset_input_box()
                return
            
            except:
                pass
            

        raws = self.inputAgent.seperate_raws(input)
        try:
            inputs = [self.inputAgent.rawToCVT(raw) for raw in raws]
            words_possibilities = Dictionary.get(inputs, max=50)
            
        except:
            self.predict_box.clear()
            self.ready = False
            
        else:        
            self.predict_box.clear()
            combination_possibilities = Dictionary.predict(words_possibilities)
            
            self.latestCombs = combination_possibilities[:9]
            
            for i, comb in enumerate(self.latestCombs, start=1):
                self.predict_box.append(f"{i}: {comb}")
                
            self.ready = True
        
    def update_text(self, new):
        current_text = self.text.toPlainText()
        if current_text == "":
            new_history = f"{new}"
        new_history = f"{current_text} {new}"
        self.text.setPlainText(new_history)
        



if __name__ == '__main__':
    inputAgent = InputMethod()
    app = QApplication(sys.argv)
    ex = V7App(inputAgent=inputAgent)
    sys.exit(app.exec_())
