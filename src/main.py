from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6 import QtGui, QtCore
# from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QRegion

import sys
import time
import math



main_w = ''
size = 0
button_list = []

class Myapp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('area_size.ui',self)
        self.setWindowTitle('Sprinkle')
        self.send.clicked.connect(self.sayHello)

    def sayHello(self):
        global main_w
        global size
        inputText = self.input.text()
        try:
            self.status.setText(f"Участок размером: {int(inputText)}, успешно записан")
            size = int(inputText)
            # a = Main()
            # a.show()
            self.close()
            main_w = Main()
            main_w.show()
        except:
            self.status.setText("введены неверные данные")

cell_w = ''
class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()
        global size
        uic.loadUi('main.ui',self)
        self.setWindowTitle('Sprinkle')

        # print(operator.attrgetter("pushButton_1")(self))

    
        # eval("self.pushButton_2").setIcon(QtGui.QIcon('img/apple.png'))
        # eval("self.pushButton_2").setText(' ')
        # eval("self.pushButton_2").setIconSize(QtCore.QSize(50,50))

        self.label_2.setText(f"1 клетка это {round(size/64,2)} м^2")
        
        global button_list
        for i in range(64):
            if i != 0:
                button_list.append(eval(f"self.pushButton_{i+1}"))
            else:
                button_list.append(eval("self.pushButton"))

        for i in range(64):
            button_list[i].clicked.connect(lambda:self.on_key_click())


    def on_key_click(self):
        global cell_w
        cell_w = cell()
        cell_w.show()

class cell(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('cell.ui',self)
        global button_list

        button = self.sender()
        number = 0
        for i in button_list:
            if i == button:
                number = button_list.index(i)
                break
        self.setWindowTitle(f'{number+1} ячейка')
        

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Myapp()
    window.show()

    app.exec()