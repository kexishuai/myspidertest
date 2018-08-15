# -*- coding: utf-8 -*-

import sqlite3 as db
import threading
from queue import *

import tushare as ts

g_taskList = Queue(0)
g_resList = Queue(0)


def task():
    while True:
        try:
            id, y1, y2 = g_taskList.get(False)
        except:
            break

        try:
            record = []
            flag = 0
            for year in range(y2, y1 - 1, -1):
                if flag >= 2: break
                v1 = ts.get_h_data(id, start='%d-06-01' % year, end='%d-12-31' % year)
                if v1 is None:
                    flag += 1
                    continue
                index = [m.date() for m in v1.index]
                for v in zip(index, v1.open, v1.high, v1.close, v1.low, v1.volume, v1.amount):
                    record.append([id, ] + list(v))
            g_resList.put([id, record])
        except Exception as e:
            g_taskList.put([id, y1, y2])
            break
    g_resList.put([None, []])


def GetAllData(dbFile='all_tushare_data2017.db', y1=1990, y2=2017):
    data = list(ts.get_stock_basics().index)  # 这里可以获取股票代码
    try:
        cxn = db.connect(dbFile)
        cur = cxn.cursor()

        cur.execute(
            'CREATE TABLE IF NOT EXISTS gp_record(code char(6), date DATE, open FLOAT, high FLOAT, close FLOAT, low FLOAT, volume FLOAT, amout FLOAT, PRIMARY KEY  (code, date))')  # 创建表格

        for d in data:
            g_taskList.put([d, y1, y2])

        count = 20  # 启动20个下载线程
        for k in range(count):
            threading.Thread(None, task).start()

        while True:
            if count <= 0:        break
            id, record = g_resList.get()
            if not id:
                count -= 1;
                continue
            print(id, len(record))
            for v in record:
                try:
                    cur.execute('INSERT INTO gp_record VALUES(?,?,?,?,?,?,?,?)', v)
                except:
                    # print('insert error',d)
                    pass
            cxn.commit()
    finally:
        cur.close()
        cxn.commit()
        cxn.close()


if __name__ == '__main__':
    GetAllData()
