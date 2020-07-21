import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
import sqlite3
import time
from Kiwoom import *


form_class = uic.loadUiType("main.ui")[0]

# TR_REQ_TIME_INTERVAL = 0.2

class MainUi(QMainWindow, form_class):




    def __init__(self):

        super().__init__()
        self.setupUi(self)

        # ui 의 name 명칭 정의하기

        # slot singal 정의하기
        self.pushButton.clicked.connect(self.btn_Clicked)

        # kiwoom 객체 생성 및 키움과 연결.
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

    def btn_Clicked(self):

        dtFrom = "20200715"
        dtTo = "20200715"
        jCode = "019170"

        self.getDailyAmt(jCode, dtFrom, dtTo, None, self.tableWidget_2)


    def getDailyAmt(self, sCode, sSt=None, sEt=None, dfS0796 = None, dpWidget = None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 request: 키움증권 -> s0796
        # data display: s0796
        # data: QTableWidget return: s0796
        # data: DataFrame

        if sCode is None:
            print('sCode is None')
        else:
            print('sCode : ' + sCode)

        if sSt is None:
            print('sSt is None')
        else:
            print('sSt : ' + sSt)

        if sEt is None:
            print('sEt is None')
        else:
            print('sEt : ' + sEt)

        if dfS0796 is None:
            print('dfS0796 is None')
        else:
            print(dfS0796)

        if dpWidget is None:
            print('dpWidget is None')
        else:
            print('555555555-2222222')
            print(dpWidget)

        self.kiwoom.s0796 = {'col0': [],
                        'col1': [],
                        'col2': [],
                        'col3': [],
                        'col4': [],
                        'col5': [],
                        'col6': [],
                        'col7': [],
                        'col8': [],
                        'col9': [],
                        'col10': [],
                        'col11': [],
                        'col12': [],
                        'col13': [],
                        'col14': [],
                        'col15': [],
                        'col16': [],
                        'col17': [],
                        'col18': []}

        # opt10059 TR 요청
        self.kiwoom.set_input_value("일자", sSt)
        self.kiwoom.set_input_value("종목코드", sCode)

        self.kiwoom.set_input_value("금액수량구분", "2")
        self.kiwoom.set_input_value("매매구분", "0")
        self.kiwoom.set_input_value("단위구분", "1")
        self.kiwoom.comm_rq_data("opt10059_req", "opt10059", 0, "0101")

        while self.kiwoom.remained_data == True:
            time.sleep(0.2)

            self.kiwoom.set_input_value("일자", sSt)
            self.kiwoom.set_input_value("종목코드", sCode)
            self.kiwoom.set_input_value("금액수량구분", "2")
            self.kiwoom.set_input_value("매매구분", "0")
            self.kiwoom.set_input_value("단위구분", "1")
            self.kiwoom.comm_rq_data("opt10059_req", "opt10059", 2, "0796")

        df = pd.DataFrame(self.kiwoom.s0796,
                          columns=['col0', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9',
                                   'col10',
                                   'col11', 'col12', 'col13', 'col14', 'col15', 'col16', 'col17', 'col18'],
                          index=self.kiwoom.s0796['col0'])

        con = sqlite3.connect("c:/db/kosdap.db")
        df.to_sql(sCode, con, if_exists='replace')

        # QTableWidget 에 데이터 표시하기
        column_idx_lookup = list(df.columns)

        dpWidget.setColumnCount(len(df.columns))
        dpWidget.setRowCount(len(df.index))

        for i in range(len(df.columns)):
            #print(column_idx_lookup[i])
            for j in range(len(df.index)):
                item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]))))
                dpWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                #print(df[column_idx_lookup[i]][j])

        dpWidget.resizeColumnsToContents()
        dpWidget.resizeRowsToContents()

    def getAccAmt(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 analysis: s0796 -> 누적량
        # data display: 누적량
        # data ->  QTableWidget return: 누적량
        # data ->  DataFrame
        pass

    def getTrend(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 analysis: s0796 -> 추세
        # Data(평균) display: 추세
        # Data(평균)  ->  QTableWidget return: 추세
        # Data(평균)  ->  DataFrame
        pass

    def getDist(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 analysis: s0796 -> 분포
        # Data(비율) display: 분포
        # Data(비율)  ->  QTableWidget return: 분포
        # Data(비율)  ->  DataFrame
        pass

    def getAnalysisTable(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 analysis: s0796
        # data -> 분석표
        # 데이터 display: 분석표
        # data: QTableWidget return: 분석표
        # data: DataFrame
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    app.exec_()