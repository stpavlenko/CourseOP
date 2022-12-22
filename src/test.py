import csv
import datetime
from datetime import timedelta
r = csv.reader(open(f'db.csv',encoding='utf-8')) # Here your csv file
lines = list(r)
line = '1;1;annonymous;5;2022-12-22 22:15:32.282729;'.split(';')
tdelta = datetime.datetime.now() - datetime.datetime(int(line[4].split('-')[0]),int(line[4].split('-')[1]),\
int(line[4].split(' ')[0].split('-')[2]),int(line[4].split(' ')[1].split(':')[0]),int(line[4].split(' ')[1].split(':')[1]),\
    int(line[4].split(' ')[1].split(':')[2].split('.')[0]),int(line[4].split('.')[1]))
tdeltasec = tdelta.total_seconds()
