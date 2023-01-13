from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import *

import sys
import datetime
import time
import math
import csv
import asyncio



main_w = ''
count = 0
length = 0
button_list = []

class Myapp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('area_size.ui',self)
        self.setWindowTitle('Sprinkle')
        self.send.clicked.connect(self.sayHello)

    def sayHello(self):
        global main_w
        global count
        global length 
        try:
            count = int(self.input.text())
            length = int(self.input_2.text())
            if count > 6 or length > 6:
                raise
            self.close()
            main_w = Main()
            main_w.show()
        except:
            self.status.setText("введены неверные данные")

class Main(QWidget):
    
    def __init__(self):
        super().__init__()
        f = open("db.csv", "w")
        f.truncate()
        f.close()
        self.initUI()
        
    def initUI(self):
        global count
        global length
        global button_list

        self.setWindowTitle('Smart greenhouse')
        self.setGeometry(0, 0, 1050, 740)

        l_count = math.floor(length*100/80)
        title = QLabel('Выберете ячейку и укажите растение')
        title.setFont(QFont('Montseratt Medium', 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main = QVBoxLayout()
        main.setSpacing(1)

        hl = QHBoxLayout()
        hl.setSpacing(10)

        main.addWidget(title)
        main.addLayout(hl)
        
        for i in range(count):
            vl = QVBoxLayout()
            vl.setSpacing(10)
            hl.addLayout(vl)
            for j in range(l_count):
                push = QPushButton('+')
                push.setMaximumSize(64,64)
                push.setMinimumSize(64,64)
                push.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
                vl.addWidget(push)
                button_list.append(push)
                push.clicked.connect(self.on_key_click)

        info = QLabel(f"всего {l_count*count} мест для размещения растений\nРекомендуемое расстояние между растениями 80см")
        info.setFont(QFont('Montseratt Medium', 12))
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(info)

        compat = QPushButton('посмотреть таблицу совместимости')
        compat.setFont(QFont('Montseratt Medium', 8))
        compat.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        compat.setMaximumSize(200,64)
        compat.clicked.connect(self.table)
        main.addWidget(compat)

        self.setLayout(main)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        

    def table(self):
        self.win = compat_table()
        self.win.show()

    def on_key_click(self):
        self.win = cell()
        self.win.window_closed.connect(self.add)
        self.win.show()

    def update(self):
        global button_list
        r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)
        for i in lines[1:]:
            line = i[0].split(';')
            box = int(i[0].split(';')[0]) -1 
            tdelta = datetime.datetime.now() - datetime.datetime(int(line[4].split('-')[0]),int(line[4].split('-')[1]),\
            int(line[4].split(' ')[0].split('-')[2]),int(line[4].split(' ')[1].split(':')[0]),int(line[4].split(' ')[1].split(':')[1]),\
            int(line[4].split(' ')[1].split(':')[2].split('.')[0]),int(line[4].split('.')[1]))
            tdeltasec = tdelta.total_seconds()
            if tdeltasec > float(line[3]):  
                button_list[box].setStyleSheet('background-color: #E10600}')
            else:
                button_list[box].setStyleSheet('background-color: #F0F0F0}')

    # обновление бд
    def add(self):
        global button_list
        global count
        global length
        r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)

        boxes = []

        for i in lines[1:]:
            box = int(i[0].split(';')[0]) -1
            boxes.append(box)
            img = i[0].split(';')[2]

            button_list[box].setIcon(QtGui.QIcon(f'img/{img}.png'))
            button_list[box].setText(' ')
            button_list[box].setIconSize(QtCore.QSize(50,50))

        all_cell = count*math.floor(length*100/80)
        for j in range(all_cell):
            if j not in boxes:
                button_list[j].setIcon(QtGui.QIcon(''))
                button_list[j].setText('+')
                button_list[j].setIconSize(QtCore.QSize(50,50))
                button_list[j].setStyleSheet('background-color: #F0F0F0}')

class compat_table(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('table.ui',self)

number = 0
class cell(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('input.ui',self)
        self.setGeometry(0, 0, 600, 400)
        global button_list

        button = self.sender()
        global number

        for i in button_list:
            if i == button:
                number = button_list.index(i) + 1
                break
        self.setWindowTitle(f'{number} ячейка')
        flag = False
        r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)
        for i in lines[1:]:
            line = i[0].split(';')
            if int(number) == int(line[0]):
                self.status.setText(f"Название: {line[1]}\nПоливать каждые {line[3]} сек.") 
                flag = True
        if flag == False:
            self.spravka.hide()
            self.water.hide()
            self.delite.hide()
            self.status.hide()
            self.change.hide()
        else:
            self.choose.hide()
            self.label.hide()
            self.save.hide()                

        self.save.clicked.connect(self.plants)
        self.change.clicked.connect(self.changes)
        self.delite.clicked.connect(self.delit)
        self.water.clicked.connect(self.pour)
        self.spravka.clicked.connect(self.info)

    def plants(self):
        inputText = str(self.choose.currentText())
        createTime = datetime.datetime.now()

        r = csv.reader(open(f'plants.csv',encoding='utf-8')) # Here your csv file
        lines = list(r)
        img = 'annonymous'
        lines[0][0] = lines[0][0].replace('\ufeff', '') 
        for i in lines:
            if inputText == i[0].split(';')[0]:
                img = i[0].split(';')[1]
                inputTime = i[0].split(';')[2]
        global number
        
        output = f"\n{number};{inputText};{img};{inputTime};{createTime};"
        with open('db.csv','a', encoding='utf-8', newline='\n') as file:
            file.write(output)

        self.status.setText('данные успешно сохранены')  
    
    def changes(self):
        self.choose.show()
        self.label.show() 
        self.save.show()       

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

    def info(self):
        self.win = help()
        self.win.show()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()

class help(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 400, 400)
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
                name = line[1]

        title = QLabel(name)
        title.setFont(QFont('Montseratt Medium', 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        f = open(f'info/{name}.txt',encoding='utf-8')
        lines = f.readlines()
        text =''
        for line in lines:
            text +=line
        desc = QLabel(text)
        desc.setWordWrap(True)  
        
        main = QVBoxLayout()
        main.setSpacing(1)

        main.addWidget(title) 
        main.addWidget(desc) 
        self.setLayout(main)
        

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Myapp()
    window.show()
    app.exec()
