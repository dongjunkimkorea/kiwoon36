import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("main.ui")[0]

class MainUi(QMainWindow, form_class):
    def __init__(self):

        super().__init__()
        self.setupUi(self)
        # ui 의 name 명칭 정의하기


        # slot singal 정의하기



    def getAnalysisTable(self, sCode, sSt=None, sEt=None, dfS0796=None, dpTable=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 analysis: s0796
        # data -> 분석표
        # 데이터 display: 분석표
        # data: QTableWidget return: 분석표
        # data: DataFrame
        pass

    def getDailyAmt(self, sCode, sSt=None, sEt=None, dfS0796=None, dpTable=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 request: 키움증권 -> s0796
        # data display: s0796
        # data: QTableWidget return: s0796
        # data: DataFrame
        pass

    def getAccAmt(self, sCode, sSt=None, sEt=None, dfS0796=None, dpTable=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 analysis: s0796 -> 누적량
        # data display: 누적량
        # data ->  QTableWidget return: 누적량
        # data ->  DataFrame
        pass

    def getTrend(self, sCode, sSt=None, sEt=None, dfS0796=None, dpTable=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 analysis: s0796 -> 추세
        # Data(평균) display: 추세
        # Data(평균)  ->  QTableWidget return: 추세
        # Data(평균)  ->  DataFrame
        pass

    def getDist(self, sCode, sSt=None, sEt=None, dfS0796=None, dpTable=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자 analysis: s0796 -> 분포
        # Data(비율) display: 분포
        # Data(비율)  ->  QTableWidget return: 분포
        # Data(비율)  ->  DataFrame
        pass










if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    app.exec_()