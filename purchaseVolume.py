import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
import sqlite3
import time
from Kiwoom import *
from PurchaseVolumeAnalysis import *
import time

form_class = uic.loadUiType("purchaseUi.ui")[0]

class PurchaseVolume(QMainWindow, form_class):

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        # ui 의 name 명칭 정의하기

        # slot singal 정의하기
        self.pushButton.clicked.connect(self.btn_Clicked)

        self.purch = PurchaseVolumeAnalysis()

    def btn_Clicked(self):

        dtFrom = "20200730"
        dtTo = "20200730"
        sCode = self.lineEdit.text()
        
        print("sCode ==>" , sCode)
        
        
        # sCode = "012790"
        # sCode = "026890"


        dateEdit_1 = self.dateEdit_1.text()
        print('dateEdit_1 : ' + dateEdit_1 )


        start_time_1 = time.time()
        # 매집량_일별
        dfS0796 = self.purch.getDailyAmt(sCode, dtFrom, dtTo, None, self.tableWidget_2)
        end_time_1 = time.time()
        print("매집량_일별")
        print(end_time_1-start_time_1)


        # 매집량_누적
        start_time_2 = time.time()
        dfCumSum = self.purch.getAccAmt(sCode, dtFrom, dtTo, dfS0796, self.tableWidget_3)
        end_time_2 = time.time()
        print("매집량_누적")
        print(end_time_2-start_time_2)

        # 매집량 추세
        start_time_3 = time.time()
        # dfTrend = self.purch.getTrend(sCode, dtFrom, dtTo, dfCumSum, self.tableWidget_4)
        end_time_3 = time.time()
        print("end_time_1")
        print(end_time_3-start_time_3)

        # 매집량 분포
        start_time_4 = time.time()
        dfDist = self.purch.getDist(sCode, dtFrom, dtTo, dfCumSum, self.tableWidget_5)
        end_time_4 = time.time()
        print("매집량_분포 (초): ")
        print(end_time_4-start_time_4)

        # 매집량 분석표
        start_time_5 = time.time()
        dfTable  = self.purch.getAnalysisTable(sCode, dtFrom, dtTo, dfS0796, self.tableWidget_1)
        end_time_5 = time.time()
        print("매집량_분석표 (초): ")
        print(end_time_5-start_time_5)

        self.purch.drawDist(dfDist, self.graph_1_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = PurchaseVolume()
    ui.show()
    app.exec_()