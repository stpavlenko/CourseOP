from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt6 import uic
from PyQt6.QtCore import Qt

import sys


class Myapp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('area_size.ui',self)
        self.setWindowTitle('Sprinkle')
        self.pushButton.clicked.connect(self.sayHello)

    def sayHello(self):
        inputText = self.input.text()
        try:
            self.status.setText(f"Участок размером: {int(inputText)}, успешно записан")
        except:
            self.status.setText("введены неверные данные")

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Myapp()
    window.show()

    app.exec()