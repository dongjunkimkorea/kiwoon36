import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui

import pandas as pd
import sqlite3
import time
from PyQt5.QtWidgets import QTableWidgetItem

import matplotlib.pyplot as plt

form_class = uic.loadUiType("main_window.ui")[0]

# column_idx_lookup = {'col1_price': 0,
#         'col6_sum': 1, 'col6_min': 2, 'col6_qty': 3, 'col6_max': 4, 'col6_rate': 5,
#         'col7_sum': 6, 'col7_min': 7, 'col7_qty': 8, 'col7_max': 9, 'col7_rate': 10,
#         'col8_sum': 11, 'col8_min': 12, 'col8_qty': 13, 'col8_max': 14, 'col8_rate': 15,
#         'col9_sum': 16, 'col9_min': 17, 'col9_qty': 18, 'col9_max': 19, 'col9_rate': 20,
#         'col10_sum': 21, 'col10_min': 22, 'col10_qty': 23, 'col10_max': 24,'col10_rate': 25,
#         'col11_sum': 26, 'col11_min': 27, 'col11_qty': 28, 'col11_max': 29,'col11_rate': 30,
#         'col12_sum': 31, 'col12_min': 32, 'col12_qty': 33, 'col12_max': 34,'col12_rate': 35,
#         'col13_sum': 36, 'col13_min': 37, 'col13_qty': 38, 'col13_max': 39,'col13_rate': 40,
#         'col14_sum': 41, 'col14_min': 42, 'col14_qty': 43, 'col14_max': 44,'col14_rate': 45,
#         'col15_sum': 46, 'col15_min': 47, 'col15_qty': 48, 'col15_max': 49,'col15_rate': 50,
#         'col16_sum': 51, 'col16_min': 52, 'col16_qty': 53, 'col16_max': 54,'col16_rate': 55,
#         'col17_sum': 56, 'col17_min': 57, 'col17_qty': 58, 'col17_max': 59,'col17_rate': 60,
#         'col18_sum': 61, 'col18_min': 62, 'col18_qty': 63, 'col18_max': 64,'col18_rate': 65
#         }



class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def display(self):
        column_headers = ['일자','현재가',
                          '\n누적합계\n(개인)','최고저점(개인)','매집수량(개인)','매집고점(개인)','분산비율(개인)',
                          '\n누적합계\n(외국인)','최고저점(외국인)','매집수량(외국인)','매집고점(외국인)','분산비율(외국인)',
                          '\n누적합계\n(기관)', '최고저점(기관)', '매집수량(기관)', '매집고점(기관)', '분산비율(기관)',
                          '\n누적합계\n(금융투자)','최고저점(금융투자)','매집수량(금융투자)','매집고점(금융투자)','분산비율(금융투자)',
                          '\n누적합계\n(보험)','최고저점(보험)','매집수량(보험)','매집고점(보험)','분산비율(보험)',
                          '\n누적합계\n(투신)','최고저점(투신)','매집수량(투신)','매집고점(투신)','분산비율(투신)',
                          '\n누적합계\n(기타금융)','최고저점(기타금융)','매집수량(기타금융)','매집고점(기타금융)','분산비율(기타금융)',
                          '\n누적합계\n(은행)','최고저점(은행)','매집수량(은행)','매집고점(은행)','분산비율(은행)',
                          '\n누적합계\n(연기금)','최고저점(연기금)','매집수량(연기금)','매집고점(연기금)','분산비율(연기금)',
                          '\n누적합계\n(사모펀드)','최고저점(사모펀드)','매집수량(사모펀드)','매집고점(사모펀드)','분산비율(사모펀드)',
                          '\n누적합계\n(국가)','최고저점(국가)','매집수량(국가)','매집고점(국가)','분산비율(국가)',
                          '\n누적합계\n(기타법인)','최고저점(기타법인)','매집수량(기타법인)','매집고점(기타법인)','분산비율(기타법인)',
                          '\n누적합계\n(내외국인)','최고저점(내외국인)','매집수량(내외국인)','매집고점(내외국인)','분산비율(내외국인)']

        con = sqlite3.connect("c:/db/kosdap.db")
        df = pd.read_sql("SELECT * FROM d0796", con, index_col='index')
        #print(df)
        #print(list(df.columns))

        column_idx_lookup = list(df.columns)


        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setRowCount(len(df.index))
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        for i in range(len(df.columns)):
            #print(column_idx_lookup[i])
            for j in range(len(df.index)):
                item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]))))
                self.tableWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                #print(df[column_idx_lookup[i]][j])

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        # plt.plot(df.index, df['col1_price'], label="현재가")
        #
        # plt.plot(df.index, df['col6_rate'], label="개인")
        # plt.plot(df.index, df['col7_rate'], label="외국인")
        # plt.plot(df.index, df['col8_rate'], label="기관")
        # plt.plot(df.index, df['col9_rate'], label="금융투자")
        # plt.plot(df.index, df['col10_rate'], label="보험")
        # plt.plot(df.index, df['col11_rate'], label="투신")
        # plt.plot(df.index, df['col12_rate'], label="기타금융")
        # plt.plot(df.index, df['col13_rate'], label="은행")
        # plt.plot(df.index, df['col14_rate'], label="연기금")
        # plt.plot(df.index, df['col15_rate'], label="사모펀드")
        # plt.plot(df.index, df['col16_rate'], label="국가")
        # plt.plot(df.index, df['col17_rate'], label="기타법인")
        # plt.plot(df.index, df['col18_rate'], label="내외국인")
        #
        # plt.legend(loc="best")
        # plt.grid()
        # plt.show()
if __name__ == "__main__":
    start_time = time.time()

    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.display()
    myWindow.show()
    app.exec_()
