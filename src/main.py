from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import pyqtSignal
# from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QRegion

import sys
import datetime
import math
import csv



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

        # 1 загрузка бд
        r = csv.reader(open(f'db.csv',encoding='utf-8'))
        lines = list(r)
        for i in lines[1:]:
            box = i[0].split(';')[0]
            img = i[0].split(';')[2]

            eval(f"self.pushButton_{box}").setIcon(QtGui.QIcon(f'img/{img}.png'))
            eval(f"self.pushButton_{box}").setText(' ')
            eval(f"self.pushButton_{box}").setIconSize(QtCore.QSize(50,50))

        self.label_2.setText(f"1 клетка это {round(size/64,2)} м^2")
        
        global button_list
        for i in range(64):
            button_list.append(eval(f"self.pushButton_{i+1}"))

        for i in range(64):
            button_list[i].clicked.connect(lambda:self.on_key_click())
        self.updateTime.clicked.connect(self.update)

    # def on_key_click(self):
    #     global cell_w
    #     cell_w = cell()
    #     cell_w.show()
    def update(self):
        r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)
        for i in lines[1:]:
            line = i[0].split(';')
            box = i[0].split(';')[0]
            tdelta = datetime.datetime.now() - datetime.datetime(int(line[4].split('-')[0]),int(line[4].split('-')[1]),\
            int(line[4].split(' ')[0].split('-')[2]),int(line[4].split(' ')[1].split(':')[0]),int(line[4].split(' ')[1].split(':')[1]),\
            int(line[4].split(' ')[1].split(':')[2].split('.')[0]),int(line[4].split('.')[1]))
            tdeltasec = tdelta.total_seconds()
            if tdeltasec > float(line[3]):  
                eval(f"self.pushButton_{box}").setStyleSheet('background-color: #E10600}')
            else:
                eval(f"self.pushButton_{box}").setStyleSheet('background-color: #F0F0F0}')



    def on_key_click(self):
        self.win = cell()
        self.win.window_closed.connect(self.add)
        self.win.show()

    # обновление бд
    def add(self):
        r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)

        boxes = []

        for i in lines[1:]:
            box = i[0].split(';')[0]
            boxes.append(box)
            img = i[0].split(';')[2]

            eval(f"self.pushButton_{box}").setIcon(QtGui.QIcon(f'img/{img}.png'))
            eval(f"self.pushButton_{box}").setText(' ')
            eval(f"self.pushButton_{box}").setIconSize(QtCore.QSize(50,50))

        clear_boxes = []
        for j in range(1,65):
            if str(j) not in boxes:
                clear_boxes.append(int(j))

        for i in clear_boxes:
                eval(f"self.pushButton_{i}").setIcon(QtGui.QIcon(''))
                eval(f"self.pushButton_{i}").setText('+')
                eval(f"self.pushButton_{i}").setIconSize(QtCore.QSize(50,50))
                eval(f"self.pushButton_{i}").setStyleSheet('background-color: #F0F0F0}')

number = 0

class cell(QWidget):

    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('input.ui',self)
        global button_list

        button = self.sender()
        global number

        for i in button_list:
            if i == button:
                number = button_list.index(i) + 1
                break
        self.setWindowTitle(f'{number} ячейка')

        r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)
        for i in lines[1:]:
            line = i[0].split(';')
            if int(number) == int(line[0]):
                self.status.setText(f"Название: {line[1]} Поливать каждые {line[3]} сек.")  
                
        self.save.clicked.connect(self.plants)
        self.delite.clicked.connect(self.delit)
        self.water.clicked.connect(self.pour)

    def plants(self):
        inputText = self.textEdit.toPlainText()
        inputTime = self.timeEdit.time().second()
        createTime = datetime.datetime.now()

        r = csv.reader(open(f'plants.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)
        img = 'annonymous'
        for i in lines:
            i[0] = i[0].replace('\ufeff', '') 
            if inputText == i[0].split(';')[0]:
                img = i[0].split(';')[1]
        global number
        
        output = f"\n{number};{inputText};{img};{inputTime};{createTime};"
        with open('db.csv','a', encoding='utf-8', newline='\n') as file:
            file.write(output)

        self.status.setText('данные успешно сохранены')  

    def delit(self):
        r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)
        global number
        output = 'номер ячейки;растение;картинка;время полива (дни)'
        for i in lines[1:]:
            line = i[0].split(';')
            if int(number) != int(line[0]):
                output += f"\n{line[0]};{line[1]};{line[2]};{line[3]};{line[4]}"


        with open('db.csv','w', encoding='utf-8', newline='\n') as file:
            file.write(output)

    def pour(self):
        r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)
        output = ''
        for i in lines[1:]:
            line = i[0].split(';')
            if int(number) != int(line[0]):
                output += f"\n{line[0]};{line[1]};{line[2]};{line[3]};{line[4]}"
            else:
                output += f"\n{line[0]};{line[1]};{line[2]};{line[3]};{datetime.datetime.now()}"

        with open('db.csv','w', encoding='utf-8', newline='\n') as file:
            file.write(output)

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()

    def timerEvent():
        global time
        time = time.addSecs(1)
        print(time.toString("hh:mm:ss"))

    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)

    timer.timeout.connect(timerEvent)
    timer.start(10)
        

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Myapp()
    window.show()

    app.exec()