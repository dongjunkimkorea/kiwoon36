import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
import sqlite3
import time
from Kiwoom import *
import numpy as np

import matplotlib as mpl

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib import font_manager, rc
import matplotlib.ticker as ticker

from matplotlib.widgets import Cursor



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvas
from matplotlib.backends.backend_gtk3 import (
    NavigationToolbar2GTK3 as NavigationToolbar)






class PurchaseVolumeAnalysis():

    def __init__(self):

        # kiwoom 객체 생성 및 키움과 연결.
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

    def getDailyAmt(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        # vaildation: 종목코드 / 시작일자 / 종료일자
        # request: 키움증권 -> s0796
        # data
        # display: s0796
        # data: QTableWidgetc
        # creturn: s0796
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
            print(dpWidget)

        # self.kiwoom.s0796 = {'col0': [],
        #                 'col1': [],
        #                 'col2': [],
        #                 'col3': [],
        #                 'col4': [],
        #                 'col5': [],
        #                 'col6': [],
        #                 'col7': [],
        #                 'col8': [],
        #                 'col9': [],
        #                 'col10': [],
        #                 'col11': [],
        #                 'col12': [],
        #                 'col13': [],
        #                 'col14': [],
        #                 'col15': [],
        #                 'col16': [],
        #                 'col17': [],
        #                 'col18': []}

        self.kiwoom.s0796 = {'일자': [],
                             '현재가': [],
                             '대비기호': [],
                             '전일대비': [],
                             '등락율': [],
                             '누적거래량': [],
                             '개인투자자': [],
                             '외국인투자자': [],
                             '기관계': [],
                             '금융투자': [],
                             '보험': [],
                             '투신': [],
                             '기타금융': [],
                             '은행': [],
                             '연기금등': [],
                             '사모펀드': [],
                             '국가': [],
                             '기타법인': [],
                             '내외국인': []}

        # opt10059 TR 요청
        self.kiwoom.set_input_value("일자", sSt)
        self.kiwoom.set_input_value("종목코드", sCode)

        self.kiwoom.set_input_value("금액수량구분", "2")
        self.kiwoom.set_input_value("매매구분", "0")
        self.kiwoom.set_input_value("단위구분", "1")
        self.kiwoom.comm_rq_data("opt10059_req", "opt10059", 0, "0101")

        while self.kiwoom.remained_data == True:
            # print("조회")
            time.sleep(0.2)

            self.kiwoom.set_input_value("일자", sSt)
            self.kiwoom.set_input_value("종목코드", sCode)
            self.kiwoom.set_input_value("금액수량구분", "2")
            self.kiwoom.set_input_value("매매구분", "0")
            self.kiwoom.set_input_value("단위구분", "1")
            self.kiwoom.comm_rq_data("opt10059_req", "opt10059", 2, "0796")

        df = pd.DataFrame(self.kiwoom.s0796,
                          columns=['일자', '현재가', '대비기호', '전일대비', '등락율', '누적거래량', '개인투자자', '외국인투자자', '기관계', '금융투자', '보험',
                                   '투신', '기타금융', '은행', '연기금등', '사모펀드', '국가', '기타법인', '내외국인'],
                          index=self.kiwoom.s0796['일자'])

        con = sqlite3.connect("c:/db/kosdap.db")
        df.to_sql(sCode, con, if_exists='replace')
        # print('=====================================================================s0796 >')
        # print(self.kiwoom.s0796)
        # print('========================================================================df >')
        # print(df.head())

        # QTableWidget 에 데이터 표시하기
        column_idx_lookup = list(df.columns)

        dpWidget.setColumnCount(len(df.columns))
        dpWidget.setRowCount(len(df.index))

        for i in range(len(df.columns)):
            # print(column_idx_lookup[i])
            for j in range(len(df.index)):
                #                item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]))))
                item: QTableWidgetItem = QTableWidgetItem(str(df[column_idx_lookup[i]][j]))
                dpWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                # print(df[column_idx_lookup[i]][j])

        dpWidget.resizeColumnsToContents()
        dpWidget.resizeRowsToContents()

        return df

    def getAccAmt(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        print('start---------------------------------------- getAccAmt() ---------------------------------------------')

        print('>>> getAccAmt()  >>>  조건검색 -------------------------------------------------------------------------')
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
            print('dfS0796 : ')
            print(dfS0796.head())

        if dpWidget is None:
            print('dpWidget is None')
        else:
            print('dpWidget : ')
            print(dpWidget)

        # ---------------------------------------------------------------------------------------------------------------
        # local varible
        # select_sql = "select * from '"+sCode+"' order by 일자 ASC"
        # analyze_db_name = "a"+sCode
        #
        start_time = time.time()
        #
        # con = sqlite3.connect("c:/db/kosdap.db")
        # db = pd.read_sql(select_sql, con)

        # DataFrame 날짜 오름 차순으로 정렬하기.
        print('>>> getAccAmt()  >>>  dfS0796 날짜오름차순정렬 ----------------------------------------------------------')
        dfS0796 = dfS0796.sort_index(ascending=True)
        # print('dfS0796.head() : ')
        # print(dfS0796.head())

        print('>>> getAccAmt()  >>>  검색조건 출력  <== 미완성 ---------------------------------------------------------')
        # 검색조건
        # 날짜, 한달, 일년, 3년, 5년, 특정기간
        # dfS0796 = dfS0796.loc['2020-03-01':'2020-04-02']

        print('>>> getAccAmt()  >>>  날짜 추출 ------------------------------------------------------------------------')
        dtList = dfS0796.index

        print('>>> getAccAmt()  >>>  현재가 추출 ----------------------------------------------------------------------')
        prices = dfS0796["현재가"]

        print('>>> getAccAmt()  >>>  누적계산에 방해돼는 컬럼항목 샥제 --------------------------------------------------')
        # DataFrame drop column
        # dfS0796 = dfS0796.drop(columns=["일자", "현재가", "대비기호", "전일대비", "등락율", "누적거래대금"])
        # 알아두기. 일자,현재가를 drop 하는 이유는 cumsum 이 숫자 데이터로 인식하여 계산을 하기 때문이다. 그래서 뺀다.
        dfS0796 = dfS0796.drop(columns=["일자", "현재가", "대비기호", "전일대비", "등락율", "누적거래량"])

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 누적합계 --------------------------------------------------')

        df_cumsum = dfS0796.cumsum()
        df_cumsum["외국인기관"] = df_cumsum["외국인투자자"] + df_cumsum["금융투자"]

        # print('dfS0796 id : ' , id(dfS0796))
        # print('df_cumsum id : ' , id(df_cumsum))
        #
        # print(list(dfS0796.columns))
        # print(list(df_cumsum.columns))

        #        col6_sum = df_cumsum["개인투자자"]
        #        col7_sum = df_cumsum["외국인투자자"]
        #        col8_sum = df_cumsum["기관계"]
        #        col9_sum = df_cumsum["금융투자"]
        #        col10_sum = df_cumsum["보험"]
        #        col11_sum = df_cumsum["투신"]
        #        col12_sum = df_cumsum["기타금융"]
        #        col13_sum = df_cumsum["은행"]
        #        col14_sum = df_cumsum["연기금등"]
        #        col15_sum = df_cumsum["사모펀드"]
        #        col16_sum = df_cumsum["국가"]
        #        col17_sum = df_cumsum["기타법인"]
        #        col18_sum = df_cumsum["내외국인"]
        #
        #        col20_sum = df_cumsum["외국인투자자"] + df_cumsum["금융투자"]

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 누적합계  >>>  검증  --------------------------------------')
        # print('dfS0796.tail()')
        # print(dfS0796.tail())
        # print('df_cumsum.tail()')
        # print(df_cumsum.tail())

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 현재가  ---------------------------------------------------')
        df_cumsum["현재가"] = prices
        df_cumsum["일자"] = dtList

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 최고저점  -------------------------------------------------')
        # col6_min = df_cumsum["개인투자자"].cummin()
        # col7_min = df_cumsum["외국인투자자"].cummin()
        # col8_min = df_cumsum["기관계"].cummin()
        # col9_min = df_cumsum["금융투자"].cummin()
        # col10_min = df_cumsum["보험"].cummin()
        # col11_min = df_cumsum["투신"].cummin()
        # col12_min = df_cumsum["기타금융"].cummin()
        # col13_min = df_cumsum["은행"].cummin()
        # col14_min = df_cumsum["연기금등"].cummin()
        # col15_min = df_cumsum["사모펀드"].cummin()
        # col16_min = df_cumsum["국가"].cummin()
        # col17_min = df_cumsum["기타법인"].cummin()
        # col18_min = df_cumsum["내외국인"].cummin()

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 최고저점  >>> 생성 -----------------------------------------')
        per_min = df_cumsum["개인투자자"].cummin()
        for_min = df_cumsum["외국인투자자"].cummin()
        gik_min = df_cumsum["기관계"].cummin()
        fin_min = df_cumsum["금융투자"].cummin()
        ins_min = df_cumsum["보험"].cummin()
        tos_min = df_cumsum["투신"].cummin()
        etf_min = df_cumsum["기타금융"].cummin()
        bnk_min = df_cumsum["은행"].cummin()
        ygi_min = df_cumsum["연기금등"].cummin()
        smo_min = df_cumsum["사모펀드"].cummin()
        nat_min = df_cumsum["국가"].cummin()
        etb_min = df_cumsum["기타법인"].cummin()
        pfs_min = df_cumsum["내외국인"].cummin()
        forFin_min = df_cumsum["외국인기관"].cummin()

        df_cumsum["최고저점_개인투자자"] = per_min
        df_cumsum["최고저점_외국인투자자"] = for_min
        df_cumsum["최고저점_기관계"] = gik_min
        df_cumsum["최고저점_금융투자"] = fin_min
        df_cumsum["최고저점_보험"] = ins_min
        df_cumsum["최고저점_투신"] = tos_min
        df_cumsum["최고저점_기타금융"] = etf_min
        df_cumsum["최고저점_은행"] = bnk_min
        df_cumsum["최고저점_연기금등"] = ygi_min
        df_cumsum["최고저점_사모펀드"] = smo_min
        df_cumsum["최고저점_국가"] = nat_min
        df_cumsum["최고저점_기타법인"] = etb_min
        df_cumsum["최고저점_내외국인"] = pfs_min
        df_cumsum["최고저점_외국인기관"] = forFin_min

        # print("----------------------------------------------------------------매집수량 = 누적합계 - 최고저점")
        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 매집수량 = 누적합계 - 최고저점  ----------------------------')
        # col6_qty = df_cumsum["개인투자자"].subtract(col6_min, fill_value=0)
        # col7_qty = df_cumsum["외국인투자자"].subtract(col7_min, fill_value=0)
        # col8_qty = df_cumsum["기관계"].subtract(col8_min, fill_value=0)
        # col9_qty = df_cumsum["금융투자"].subtract(col9_min, fill_value=0)
        # col10_qty = df_cumsum["보험"].subtract(col10_min, fill_value=0)
        # col11_qty = df_cumsum["투신"].subtract(col11_min, fill_value=0)
        # col12_qty = df_cumsum["기타금융"].subtract(col12_min, fill_value=0)
        # col13_qty = df_cumsum["은행"].subtract(col13_min, fill_value=0)
        # col14_qty = df_cumsum["연기금등"].subtract(col14_min, fill_value=0)
        # col15_qty = df_cumsum["사모펀드"].subtract(col15_min, fill_value=0)
        # col16_qty = df_cumsum["국가"].subtract(col16_min, fill_value=0)
        # col17_qty = df_cumsum["기타법인"].subtract(col17_min, fill_value=0)
        # col18_qty = df_cumsum["내외국인"].subtract(col8_min, fill_value=0)

        per_tot = df_cumsum["개인투자자"].subtract(per_min, fill_value=0)
        for_tot = df_cumsum["외국인투자자"].subtract(for_min, fill_value=0)
        gik_tot = df_cumsum["기관계"].subtract(gik_min, fill_value=0)
        fin_tot = df_cumsum["금융투자"].subtract(fin_min, fill_value=0)
        ins_tot = df_cumsum["보험"].subtract(ins_min, fill_value=0)
        tos_tot = df_cumsum["투신"].subtract(tos_min, fill_value=0)
        etf_tot = df_cumsum["기타금융"].subtract(etf_min, fill_value=0)
        bnk_tot = df_cumsum["은행"].subtract(bnk_min, fill_value=0)
        ygi_tot = df_cumsum["연기금등"].subtract(ygi_min, fill_value=0)
        smo_tot = df_cumsum["사모펀드"].subtract(smo_min, fill_value=0)
        nat_tot = df_cumsum["국가"].subtract(nat_min, fill_value=0)
        etb_tot = df_cumsum["기타법인"].subtract(etb_min, fill_value=0)
        pfs_tot = df_cumsum["내외국인"].subtract(pfs_min, fill_value=0)
        forFin_tot = df_cumsum["외국인기관"].subtract(forFin_min, fill_value=0)

        df_cumsum["매집수량_개인투자자"] = per_tot
        df_cumsum["매집수량_외국인투자자"] = for_tot
        df_cumsum["매집수량_기관계"] = gik_tot
        df_cumsum["매집수량_금융투자"] = fin_tot
        df_cumsum["매집수량_보험"] = ins_tot
        df_cumsum["매집수량_투신"] = tos_tot
        df_cumsum["매집수량_기타금융"] = etf_tot
        df_cumsum["매집수량_은행"] = bnk_tot
        df_cumsum["매집수량_연기금등"] = ygi_tot
        df_cumsum["매집수량_사모펀드"] = smo_tot
        df_cumsum["매집수량_국가"] = nat_tot
        df_cumsum["매집수량_기타법인"] = etb_tot
        df_cumsum["매집수량_내외국인"] = pfs_tot
        df_cumsum["매집수량_외국인기관"] = forFin_tot

        print(
            '>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 매집수량 5,20,60추세 --------------------------------------------------')
        df_cumsum["외국인기관_5일추세"] = df_cumsum['매집수량_외국인기관'].rolling(window=5).mean()
        df_cumsum["외국인기관_20일추세"] = df_cumsum['매집수량_외국인기관'].rolling(window=20).mean()
        df_cumsum["외국인기관_60일추세"] = df_cumsum['매집수량_외국인기관'].rolling(window=60).mean()

        # print("---------------------------------------------------------------매집고점")
        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 매집고점  -------------------------------------------------')
        # col6_max = col6_qty.cummax()
        # col7_max = col7_qty.cummax()
        # col8_max = col8_qty.cummax()
        # col9_max = col9_qty.cummax()
        # col10_max = col10_qty.cummax()
        # col11_max = col11_qty.cummax()
        # col12_max = col12_qty.cummax()
        # col13_max = col13_qty.cummax()
        # col14_max = col14_qty.cummax()
        # col15_max = col15_qty.cummax()
        # col16_max = col16_qty.cummax()
        # col17_max = col17_qty.cummax()
        # col18_max = col18_qty.cummax()

        per_max = per_tot.cummax()
        for_max = for_tot.cummax()
        gik_max = gik_tot.cummax()
        fin_max = fin_tot.cummax()
        ins_max = ins_tot.cummax()
        tos_max = tos_tot.cummax()
        etf_max = etf_tot.cummax()
        bnk_max = bnk_tot.cummax()
        ygi_max = ygi_tot.cummax()
        smo_max = smo_tot.cummax()
        nat_max = nat_tot.cummax()
        etb_max = etb_tot.cummax()
        pfs_max = pfs_tot.cummax()
        forFin_max = forFin_tot.cummax()

        df_cumsum["매집고점_개인투자자"] = per_max
        df_cumsum["매집고점_외국인투자자"] = for_max
        df_cumsum["매집고점_기관계"] = gik_max
        df_cumsum["매집고점_금융투자"] = fin_max
        df_cumsum["매집고점_보험"] = ins_max
        df_cumsum["매집고점_투신"] = tos_max
        df_cumsum["매집고점_기타금융"] = etf_max
        df_cumsum["매집고점_은행"] = bnk_max
        df_cumsum["매집고점_연기금등"] = ygi_max
        df_cumsum["매집고점_사모펀드"] = smo_max
        df_cumsum["매집고점_국가"] = nat_max
        df_cumsum["매집고점_기타법인"] = etb_max
        df_cumsum["매집고점_내외국인"] = pfs_max

        df_cumsum["매집고점_외국인기관"] = forFin_max

        # print("---------------------------------------------------------------분산비율 = 매집수량/매집고점")
        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 분산비율 = 매집수량/매집고점  -------------------------------')
        # col6_r = col6_qty.div(col6_max) * 100
        # col7_r = col7_qty.div(col7_max) * 100
        # col8_r = col8_qty.div(col8_max) * 100
        # col9_r = col9_qty.div(col9_max) * 100
        # col10_r = col10_qty.div(col10_max) * 100
        # col11_r = col11_qty.div(col11_max) * 100
        # col12_r = col12_qty.div(col12_max) * 100
        # col13_r = col13_qty.div(col13_max) * 100
        # col14_r = col14_qty.div(col14_max) * 100
        # col15_r = col15_qty.div(col15_max) * 100
        # col16_r = col16_qty.div(col16_max) * 100
        # col17_r = col17_qty.div(col17_max) * 100
        # col18_r = col18_qty.div(col18_max) * 100
        #
        # col6_rate = col6_r.fillna(0)
        # col7_rate = col7_r.fillna(0)
        # col8_rate = col8_r.fillna(0)
        # col9_rate = col9_r.fillna(0)
        # col10_rate = col10_r.fillna(0)
        # col11_rate = col11_r.fillna(0)
        # col12_rate = col12_r.fillna(0)
        # col13_rate = col13_r.fillna(0)
        # col14_rate = col14_r.fillna(0)
        # col15_rate = col15_r.fillna(0)
        # col16_rate = col16_r.fillna(0)
        # col17_rate = col17_r.fillna(0)
        # col18_rate = col18_r.fillna(0)

        per_rate = per_tot.div(per_max)
        for_rate = for_tot.div(for_max)
        gik_rate = gik_tot.div(gik_max)
        fin_rate = fin_tot.div(fin_max)
        ins_rate = ins_tot.div(ins_max)
        tos_rate = tos_tot.div(tos_max)
        etf_rate = etf_tot.div(etf_max)
        bnk_rate = bnk_tot.div(bnk_max)
        ygi_rate = ygi_tot.div(ygi_max)
        smo_rate = smo_tot.div(smo_max)
        nat_rate = nat_tot.div(nat_max)
        etb_rate = etb_tot.div(etb_max)
        pfs_rate = pfs_tot.div(pfs_max)
        forFin_rate = for_tot.div(forFin_max)

        df_cumsum["분산비율_개인투자자"] = per_rate * 100
        df_cumsum["분산비율_외국인투자자"] = for_rate * 100
        df_cumsum["분산비율_기관계"] = gik_rate * 100
        df_cumsum["분산비율_금융투자"] = fin_rate * 100
        df_cumsum["분산비율_보험"] = ins_rate * 100
        df_cumsum["분산비율_투신"] = tos_rate * 100
        df_cumsum["분산비율_기타금융"] = etf_rate * 100
        df_cumsum["분산비율_은행"] = bnk_rate * 100
        df_cumsum["분산비율_연기금등"] = ygi_rate * 100
        df_cumsum["분산비율_사모펀드"] = smo_rate * 100
        df_cumsum["분산비율_국가"] = nat_rate * 100
        df_cumsum["분산비율_기타법인"] = etb_rate * 100
        df_cumsum["분산비율_내외국인"] = pfs_rate * 100
        df_cumsum["분산비율_외국인기관"] = forFin_rate * 100

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 세력매집추세  ---------------------------------------------')
        df_cumsum['세력매집추세_주가'] = df_cumsum['현재가']
        df_cumsum['세력매집추세_5일추세'] = df_cumsum['외국인기관_5일추세']
        df_cumsum['세력매집추세_20일추세'] = df_cumsum['외국인기관_20일추세']
        # df_cumsum['세력매집추세_60일추세'] =  df_cumsum["외국인기관_60일추세"]
        #
        # df_cumsum["외국인기관_5일추세"] = df_cumsum['매집수량_외국인기관'].rolling(window=5).mean()
        # df_cumsum["외국인기관_20일추세"] = df_cumsum['매집수량_외국인기관'].rolling(window=20).mean()
        # # df_cumsum["외국인기관_60일추세"] = df_cumsum['매집수량_외국인기관'].rolling(window=60).mean()

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 세력분산비율추세  ------------------------------------------')
        df_cumsum['세력분산비율추세_주가'] = df_cumsum['현재가']
        df_cumsum['세력분산비율추세_개인분산'] = df_cumsum['분산비율_개인투자자']
        df_cumsum['세력분산비율추세_세력분산'] = df_cumsum['분산비율_외국인기관']

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 보유수량추세  --------------------------------------------------')
        df_cumsum['보유수량추세_주가'] = df_cumsum['현재가']
        df_cumsum['보유수량추세_외국인투자자'] = df_cumsum['매집수량_외국인투자자']
        df_cumsum['보유수량추세_금융투자'] = df_cumsum['매집수량_금융투자']
        df_cumsum['보유수량추세_보험'] = df_cumsum['매집수량_보험']
        df_cumsum['보유수량추세_투신'] = df_cumsum['매집수량_투신']
        df_cumsum['보유수량추세_기타금융'] = df_cumsum['매집수량_기타금융']
        df_cumsum['보유수량추세_은행'] = df_cumsum['매집수량_은행']
        df_cumsum['보유수량추세_연기금등'] = df_cumsum['매집수량_연기금등']
        df_cumsum['보유수량추세_사모펀드'] = df_cumsum['매집수량_사모펀드']
        df_cumsum['보유수량추세_국가'] = df_cumsum['매집수량_국가']
        df_cumsum['보유수량추세_기타법인'] = df_cumsum['매집수량_기타법인']
        df_cumsum['보유수량추세_내외국인'] = df_cumsum['매집수량_내외국인']

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> fillna  --------------------------------------------------')
        df_cumsum = df_cumsum.fillna(0)

        # print('------------------------------------------------------------------------------------------>>>  분석결과 1')
        # print(dfS0796.tail())
        # print(df_cumsum.tail())
        # print('------------------------------------------------------------------------------------------>>>  분석결과 2')
        # print('dfS0796 id :')
        # print('df_cumsum id :')
        # print(id(dfS0796))
        # print(id(df_cumsum))
        # print(dfS0796.columns)
        # print(df_cumsum.columns)
        print('>>> getAccAmt()  >>>  분석 DataFrame >>> Table  --------------------------------------------------------')
        df = df_cumsum[['일자', '현재가',
                        '개인투자자', '최고저점_개인투자자', '매집수량_개인투자자', '매집고점_개인투자자', '분산비율_개인투자자',

                        '외국인기관', '최고저점_외국인기관', '매집수량_외국인기관', '매집고점_외국인기관', '분산비율_외국인기관',
                        '외국인기관_5일추세', '외국인기관_20일추세', '외국인기관_60일추세',

                        '외국인투자자', '최고저점_외국인투자자', '매집수량_외국인투자자', '매집고점_외국인투자자', '분산비율_외국인투자자',
                        '금융투자', '최고저점_금융투자', '매집수량_금융투자', '매집고점_금융투자', '분산비율_금융투자',
                        '보험', '최고저점_보험', '매집수량_보험', '매집고점_보험', '분산비율_보험',
                        '투신', '최고저점_투신', '매집수량_투신', '매집고점_투신', '분산비율_투신',
                        '기타금융', '최고저점_기타금융', '매집수량_기타금융', '매집고점_기타금융', '분산비율_기타금융',
                        '은행', '최고저점_은행', '매집수량_은행', '매집고점_은행', '분산비율_은행',
                        '연기금등', '최고저점_연기금등', '매집수량_연기금등', '매집고점_연기금등', '분산비율_연기금등',
                        '사모펀드', '최고저점_사모펀드', '매집수량_사모펀드', '매집고점_사모펀드', '분산비율_사모펀드',
                        '국가', '최고저점_국가', '매집수량_국가', '매집고점_국가', '분산비율_국가',
                        '기타법인', '최고저점_기타법인', '매집수량_기타법인', '매집고점_기타법인', '분산비율_기타법인',
                        '내외국인', '최고저점_내외국인', '매집수량_내외국인', '매집고점_내외국인', '분산비율_내외국인',

                        '세력매집추세_주가', '세력매집추세_5일추세', '세력매집추세_20일추세',
                        '세력분산비율추세_주가', '세력분산비율추세_개인분산', '세력분산비율추세_세력분산',

                        '보유수량추세_주가', '보유수량추세_외국인투자자', '보유수량추세_금융투자', '보유수량추세_보험',
                        '보유수량추세_투신', '보유수량추세_기타금융', '보유수량추세_은행', '보유수량추세_연기금등', '보유수량추세_사모펀드',
                        '보유수량추세_국가', '보유수량추세_기타법인', '보유수량추세_내외국인']]

        df.fillna(0)
        # print(df.head())

        print('>>> getAccAmt()  >>>  분석 DataFrame >>> sort  --------------------------------------------------------')
        df = df.sort_index(ascending=False)

        print('>>> getAccAmt()  >>>  분석 DataFrame >>> Table  --------------------------------------------------------')
        # QTableWidget 에 데이터 표시하기
        column_idx_lookup = list(df.columns)

        # print(list(column_idx_lookup))

        # dpWidget.setColumnCount(len(df.columns))
        dpWidget.setRowCount(len(df.index))

        # print('len(df.index) : ' , len(df.index))
        # print('len(df.columns) : ', len(df.columns))

        for i in range(len(df.columns)):
            # print(column_idx_lookup[i])
            for j in range(len(df.index)):
                item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]), 2)))
                #                item: QTableWidgetItem = QTableWidgetItem(str(round(df[column_idx_lookup[i]][j],2)))
                dpWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                # print(df[column_idx_lookup[i]][j])

        dpWidget.resizeColumnsToContents()
        dpWidget.resizeRowsToContents()

        return df

    def getTrend(self, sCode, sSt=None, sEt=None, dfS0796CumData=None, dpWidget=None):
        print('start---------------------------------------- getTrend() ---------------------------------------------')

        print(
            '>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 매집수량 5,20,60추세 --------------------------------------------------')

        columns = ['일자', '주가',
                   '5일추세_개인', '5일추세_외국인', '5일추세_외국인기관', '5일추세_금융투자', '5일추세_보험', '5일추세_투신', '5일추세_기타금융', '5일추세_은행',
                   '5일추세_연기금', '5일추세_사모펀드', '5일추세_국가', '5일추세_기타법인', '5일추세_내외국인',
                   '10일추세_개인', '10일추세_외국인', '10일추세_외국인기관', '10일추세_금융투자', '10일추세_보험', '10일추세_투신', '10일추세_기타금융',
                   '10일추세_은행', '10일추세_연기금', '10일추세_사모펀드', '10일추세_국가', '10일추세_기타법인', '10일추세_내외국인',
                   '20일추세_개인', '20일추세_외국인', '20일추세_외국인기관', '20일추세_금융투자', '20일추세_보험', '20일추세_투신', '20일추세_기타금융',
                   '20일추세_은행', '20일추세_연기금', '20일추세_사모펀드', '20일추세_국가', '20일추세_기타법인', '20일추세_내외국인',
                   '40일추세_개인', '40일추세_외국인', '40일추세_외국인기관', '40일추세_금융투자', '40일추세_보험', '40일추세_투신', '40일추세_기타금융',
                   '40일추세_은행', '40일추세_연기금', '40일추세_사모펀드', '40일추세_국가', '40일추세_기타법인', '40일추세_내외국인',
                   '60일추세_개인', '60일추세_외국인', '60일추세_외국인기관', '60일추세_금융투자', '60일추세_보험', '60일추세_투신', '60일추세_기타금융',
                   '60일추세_은행', '60일추세_연기금', '60일추세_사모펀드', '60일추세_국가', '60일추세_기타법인', '60일추세_내외국인',
                   '80일추세_개인', '80일추세_외국인', '80일추세_외국인기관', '80일추세_금융투자', '80일추세_보험', '80일추세_투신', '80일추세_기타금융',
                   '80일추세_은행', '80일추세_연기금', '80일추세_사모펀드', '80일추세_국가', '80일추세_기타법인', '80일추세_내외국인',
                   '100일추세_개인', '100일추세_외국인', '100일추세_외국인기관', '100일추세_금융투자', '100일추세_보험', '100일추세_투신', '100일추세_기타금융',
                   '100일추세_은행', '100일추세_연기금', '100일추세_사모펀드', '100일추세_국가', '100일추세_기타법인', '100일추세_내외국인',
                   '120일추세_개인', '120일추세_외국인', '120일추세_외국인기관', '120일추세_금융투자', '120일추세_보험', '120일추세_투신', '120일추세_기타금융',
                   '120일추세_은행', '120일추세_연기금', '120일추세_사모펀드', '120일추세_국가', '120일추세_기타법인', '120일추세_내외국인',
                   '240일추세_개인', '240일추세_외국인', '240일추세_외국인기관', '240일추세_금융투자', '240일추세_보험', '240일추세_투신', '240일추세_기타금융',
                   '240일추세_은행', '240일추세_연기금', '240일추세_사모펀드', '240일추세_국가', '240일추세_기타법인', '240일추세_내외국인']

        df = pd.DataFrame(columns=columns)

        # print('데이터 프레임 정렬')
        # print(dfS0796CumData.head())
        dfAscending = dfS0796CumData.sort_index(ascending=True)
        # print(dfAscending.head())

        df["일자"] = dfAscending["일자"]
        df["주가"] = dfAscending["현재가"]
        df["5일추세_개인"] = dfAscending['매집수량_개인투자자'].rolling(window=5).mean()
        df["5일추세_외국인"] = dfAscending['매집수량_외국인투자자'].rolling(window=5).mean()
        df["5일추세_외국인기관"] = dfAscending['매집수량_외국인기관'].rolling(window=5).mean()
        df["5일추세_금융투자"] = dfAscending['매집수량_금융투자'].rolling(window=5).mean()
        df["5일추세_보험"] = dfAscending['매집수량_보험'].rolling(window=5).mean()
        df["5일추세_투신"] = dfAscending['매집수량_투신'].rolling(window=5).mean()
        df["5일추세_기타금융"] = dfAscending['매집수량_기타금융'].rolling(window=5).mean()
        df["5일추세_은행"] = dfAscending['매집수량_은행'].rolling(window=5).mean()
        df["5일추세_연기금"] = dfAscending['매집수량_연기금등'].rolling(window=5).mean()
        df["5일추세_사모펀드"] = dfAscending['매집수량_사모펀드'].rolling(window=5).mean()
        df["5일추세_국가"] = dfAscending['매집수량_국가'].rolling(window=5).mean()
        df["5일추세_기타법인"] = dfAscending['매집수량_기타법인'].rolling(window=5).mean()
        df["5일추세_내외국인"] = dfAscending['매집수량_내외국인'].rolling(window=5).mean()

        df["10일추세_개인"] = dfAscending['매집수량_개인투자자'].rolling(window=10).mean()
        df["10일추세_외국인"] = dfAscending['매집수량_외국인투자자'].rolling(window=10).mean()
        df["10일추세_외국인기관"] = dfAscending['매집수량_외국인기관'].rolling(window=10).mean()
        df["10일추세_금융투자"] = dfAscending['매집수량_금융투자'].rolling(window=10).mean()
        df["10일추세_보험"] = dfAscending['매집수량_보험'].rolling(window=10).mean()
        df["10일추세_투신"] = dfAscending['매집수량_투신'].rolling(window=10).mean()
        df["10일추세_기타금융"] = dfAscending['매집수량_기타금융'].rolling(window=10).mean()
        df["10일추세_은행"] = dfAscending['매집수량_은행'].rolling(window=10).mean()
        df["10일추세_연기금"] = dfAscending['매집수량_연기금등'].rolling(window=10).mean()
        df["10일추세_사모펀드"] = dfAscending['매집수량_사모펀드'].rolling(window=10).mean()
        df["10일추세_국가"] = dfAscending['매집수량_국가'].rolling(window=10).mean()
        df["10일추세_기타법인"] = dfAscending['매집수량_기타법인'].rolling(window=10).mean()
        df["10일추세_내외국인"] = dfAscending['매집수량_내외국인'].rolling(window=10).mean()

        df["20일추세_개인"] = dfAscending['매집수량_개인투자자'].rolling(window=20).mean()
        df["20일추세_외국인"] = dfAscending['매집수량_외국인투자자'].rolling(window=20).mean()
        df["20일추세_외국인기관"] = dfAscending['매집수량_외국인기관'].rolling(window=20).mean()
        df["20일추세_금융투자"] = dfAscending['매집수량_금융투자'].rolling(window=20).mean()
        df["20일추세_보험"] = dfAscending['매집수량_보험'].rolling(window=20).mean()
        df["20일추세_투신"] = dfAscending['매집수량_투신'].rolling(window=20).mean()
        df["20일추세_기타금융"] = dfAscending['매집수량_기타금융'].rolling(window=20).mean()
        df["20일추세_은행"] = dfAscending['매집수량_은행'].rolling(window=20).mean()
        df["20일추세_연기금"] = dfAscending['매집수량_연기금등'].rolling(window=20).mean()
        df["20일추세_사모펀드"] = dfAscending['매집수량_사모펀드'].rolling(window=20).mean()
        df["20일추세_국가"] = dfAscending['매집수량_국가'].rolling(window=20).mean()
        df["20일추세_기타법인"] = dfAscending['매집수량_기타법인'].rolling(window=20).mean()
        df["20일추세_내외국인"] = dfAscending['매집수량_내외국인'].rolling(window=20).mean()

        df["40일추세_개인"] = dfAscending['매집수량_개인투자자'].rolling(window=40).mean()
        df["40일추세_외국인"] = dfAscending['매집수량_외국인투자자'].rolling(window=40).mean()
        df["40일추세_외국인기관"] = dfAscending['매집수량_외국인기관'].rolling(window=40).mean()
        df["40일추세_금융투자"] = dfAscending['매집수량_금융투자'].rolling(window=40).mean()
        df["40일추세_보험"] = dfAscending['매집수량_보험'].rolling(window=40).mean()
        df["40일추세_투신"] = dfAscending['매집수량_투신'].rolling(window=40).mean()
        df["40일추세_기타금융"] = dfAscending['매집수량_기타금융'].rolling(window=40).mean()
        df["40일추세_은행"] = dfAscending['매집수량_은행'].rolling(window=40).mean()
        df["40일추세_연기금"] = dfAscending['매집수량_연기금등'].rolling(window=40).mean()
        df["40일추세_사모펀드"] = dfAscending['매집수량_사모펀드'].rolling(window=40).mean()
        df["40일추세_국가"] = dfAscending['매집수량_국가'].rolling(window=40).mean()
        df["40일추세_기타법인"] = dfAscending['매집수량_기타법인'].rolling(window=40).mean()
        df["40일추세_내외국인"] = dfAscending['매집수량_내외국인'].rolling(window=40).mean()

        df["80일추세_개인"] = dfAscending['매집수량_개인투자자'].rolling(window=80).mean()
        df["80일추세_외국인"] = dfAscending['매집수량_외국인투자자'].rolling(window=80).mean()
        df["80일추세_외국인기관"] = dfAscending['매집수량_외국인기관'].rolling(window=80).mean()
        df["80일추세_금융투자"] = dfAscending['매집수량_금융투자'].rolling(window=80).mean()
        df["80일추세_보험"] = dfAscending['매집수량_보험'].rolling(window=80).mean()
        df["80일추세_투신"] = dfAscending['매집수량_투신'].rolling(window=80).mean()
        df["80일추세_기타금융"] = dfAscending['매집수량_기타금융'].rolling(window=80).mean()
        df["80일추세_은행"] = dfAscending['매집수량_은행'].rolling(window=80).mean()
        df["80일추세_연기금"] = dfAscending['매집수량_연기금등'].rolling(window=80).mean()
        df["80일추세_사모펀드"] = dfAscending['매집수량_사모펀드'].rolling(window=80).mean()
        df["80일추세_국가"] = dfAscending['매집수량_국가'].rolling(window=80).mean()
        df["80일추세_기타법인"] = dfAscending['매집수량_기타법인'].rolling(window=80).mean()
        df["80일추세_내외국인"] = dfAscending['매집수량_내외국인'].rolling(window=80).mean()

        df["100일추세_개인"] = dfAscending['매집수량_개인투자자'].rolling(window=100).mean()
        df["100일추세_외국인"] = dfAscending['매집수량_외국인투자자'].rolling(window=100).mean()
        df["100일추세_외국인기관"] = dfAscending['매집수량_외국인기관'].rolling(window=100).mean()
        df["100일추세_금융투자"] = dfAscending['매집수량_금융투자'].rolling(window=100).mean()
        df["100일추세_보험"] = dfAscending['매집수량_보험'].rolling(window=100).mean()
        df["100일추세_투신"] = dfAscending['매집수량_투신'].rolling(window=100).mean()
        df["100일추세_기타금융"] = dfAscending['매집수량_기타금융'].rolling(window=100).mean()
        df["100일추세_은행"] = dfAscending['매집수량_은행'].rolling(window=100).mean()
        df["100일추세_연기금"] = dfAscending['매집수량_연기금등'].rolling(window=100).mean()
        df["100일추세_사모펀드"] = dfAscending['매집수량_사모펀드'].rolling(window=100).mean()
        df["100일추세_국가"] = dfAscending['매집수량_국가'].rolling(window=100).mean()
        df["100일추세_기타법인"] = dfAscending['매집수량_기타법인'].rolling(window=100).mean()
        df["100일추세_내외국인"] = dfAscending['매집수량_내외국인'].rolling(window=100).mean()

        df["120일추세_개인"] = dfAscending['매집수량_개인투자자'].rolling(window=120).mean()
        df["120일추세_외국인"] = dfAscending['매집수량_외국인투자자'].rolling(window=120).mean()
        df["120일추세_외국인기관"] = dfAscending['매집수량_외국인기관'].rolling(window=120).mean()
        df["120일추세_금융투자"] = dfAscending['매집수량_금융투자'].rolling(window=120).mean()
        df["120일추세_보험"] = dfAscending['매집수량_보험'].rolling(window=120).mean()
        df["120일추세_투신"] = dfAscending['매집수량_투신'].rolling(window=120).mean()
        df["120일추세_기타금융"] = dfAscending['매집수량_기타금융'].rolling(window=120).mean()
        df["120일추세_은행"] = dfAscending['매집수량_은행'].rolling(window=120).mean()
        df["120일추세_연기금"] = dfAscending['매집수량_연기금등'].rolling(window=120).mean()
        df["120일추세_사모펀드"] = dfAscending['매집수량_사모펀드'].rolling(window=120).mean()
        df["120일추세_국가"] = dfAscending['매집수량_국가'].rolling(window=120).mean()
        df["120일추세_기타법인"] = dfAscending['매집수량_기타법인'].rolling(window=120).mean()
        df["120일추세_내외국인"] = dfAscending['매집수량_내외국인'].rolling(window=120).mean()

        df["240일추세_개인"] = dfAscending['매집수량_개인투자자'].rolling(window=240).mean()
        df["240일추세_외국인"] = dfAscending['매집수량_외국인투자자'].rolling(window=240).mean()
        df["240일추세_외국인기관"] = dfAscending['매집수량_외국인기관'].rolling(window=240).mean()
        df["240일추세_금융투자"] = dfAscending['매집수량_금융투자'].rolling(window=240).mean()
        df["240일추세_보험"] = dfAscending['매집수량_보험'].rolling(window=240).mean()
        df["240일추세_투신"] = dfAscending['매집수량_투신'].rolling(window=240).mean()
        df["240일추세_기타금융"] = dfAscending['매집수량_기타금융'].rolling(window=240).mean()
        df["240일추세_은행"] = dfAscending['매집수량_은행'].rolling(window=240).mean()
        df["240일추세_연기금"] = dfAscending['매집수량_연기금등'].rolling(window=240).mean()
        df["240일추세_사모펀드"] = dfAscending['매집수량_사모펀드'].rolling(window=240).mean()
        df["240일추세_국가"] = dfAscending['매집수량_국가'].rolling(window=240).mean()
        df["240일추세_기타법인"] = dfAscending['매집수량_기타법인'].rolling(window=240).mean()
        df["240일추세_내외국인"] = dfAscending['매집수량_내외국인'].rolling(window=240).mean()

        df = df.sort_index(ascending=False)
        df = df.fillna(0)

        # QTableWidget 에 데이터 표시하기
        column_idx_lookup = list(df.columns)

        # print(list(column_idx_lookup))

        # dpWidget.setColumnCount(len(df.columns))
        dpWidget.setRowCount(len(df.index))

        # print('len(df.index) : ' , len(df.index))
        # print('len(df.columns) : ', len(df.columns))

        for i in range(len(df.columns)):
            # print(column_idx_lookup[i])
            for j in range(len(df.index)):
                item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]), 2)))
                dpWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                # print(df[column_idx_lookup[i]][j])

        dpWidget.resizeColumnsToContents()
        dpWidget.resizeRowsToContents()

        return df

    def getDist(self, sCode, sSt=None, sEt=None, dfS0796CumData=None, dpWidget=None):
        print('start---------------------------------------- getDist() ---------------------------------------------')

        print('>>> getDist()  >>>  조건검색 ------------------------------------------------------------------')
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

        if dfS0796CumData is None:
            print('dfS0796CumData is None')
        else:
            print('dfS0796CumData : ')
            print(dfS0796CumData.head())

        if dpWidget is None:
            print('dpWidget is None')
        else:
            print('dpWidget : ')
            print(dpWidget)

        # print(dfS0796CumData)

        columns = ['일자', '주가',
                   '분산_개인', '분산_외국인', '분산_외국인기관', '분산_금융투자', '분산_보험', '분산_투신', '분산_기타금융', '분산_은행', '분산_연기금', '분산_사모펀드',
                   '분산_국가', '분선_기타법인', '분산_내외국인']

        df = pd.DataFrame(columns=columns)

        df["일자"] = dfS0796CumData["일자"]
        df["주가"] = dfS0796CumData["현재가"]

        df["분산_개인"] = dfS0796CumData["분산비율_개인투자자"]
        df["분산_외국인"] = dfS0796CumData["분산비율_외국인투자자"]
        df["분산_외국인기관"] = dfS0796CumData["분산비율_외국인기관"]
        df["분산_금융투자"] = dfS0796CumData["분산비율_금융투자"]
        df["분산_보험"] = dfS0796CumData["분산비율_보험"]
        df["분산_투신"] = dfS0796CumData["분산비율_투신"]
        df["분산_기타금융"] = dfS0796CumData["분산비율_기타금융"]
        df["분산_은행"] = dfS0796CumData["분산비율_은행"]
        df["분산_연기금"] = dfS0796CumData["분산비율_연기금등"]
        df["분산_사모펀드"] = dfS0796CumData["분산비율_사모펀드"]
        df["분산_국가"] = dfS0796CumData["분산비율_국가"]
        df["분선_기타법인"] = dfS0796CumData["분산비율_기타법인"]
        df["분산_내외국인"] = dfS0796CumData["분산비율_내외국인"]

        # QTableWidget 에 데이터 표시하기
        column_idx_lookup = list(df.columns)

        # print(list(column_idx_lookup))

        # dpWidget.setColumnCount(len(df.columns))
        dpWidget.setRowCount(len(df.index))

        # print('len(df.index) : ' , len(df.index))
        # print('len(df.columns) : ', len(df.columns))

        for i in range(len(df.columns)):
            # print(column_idx_lookup[i])
            for j in range(len(df.index)):
                item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]), 2)))
                dpWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                # print(df[column_idx_lookup[i]][j])

        dpWidget.resizeColumnsToContents()
        dpWidget.resizeRowsToContents()

        return df

    def getAnalysisTable(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        print('start---------------------------------------- getAnalysisTable() --------------------------------------')

        print('>>> getAnalysisTable()  >>>  조건검색 ------------------------------------------------------------------')
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
            print('dfS0796 : ')
            print(dfS0796.head())

        if dpWidget is None:
            print('dpWidget is None')
        else:
            print('dpWidget : ')
            print(dpWidget)

        # 년   - from~to :  240일
        # print("전체크기", len(dfS0796))

        weekCnt = len(dfS0796) / 5
        monthCnt = len(dfS0796) / 20
        bungiCnt = len(dfS0796) / 60
        yearCnt = len(dfS0796) / 240

        # print(weekCnt,monthCnt,bungiCnt,yearCnt)

        columnsList = ['일자', '현재가', '누적거래량', '개인투자자', '세력합', '외국인투자자', '금융투자', '보험', '투신', '기타금융', '은행', '연기금등', '사모펀드',
                       '국가', '기타법인', '내외국인']

        dfCalS0796 = self.cal(dfS0796)

        tableDataWeekExist = False
        tableDataMonthExist = False
        tableDataBunGiExist = False
        tableDataYearExist = False

        print('Day :-----------------------------------------------------------------------')
        # 일 == 1일
        if weekCnt >= 1:

            # dfS0796["세력합"] = dfS0796["외국인투자자"] + dfS0796["금융투자"]
            # dfS0796.drop(columns=["대비기호", "전일대비", "등락율", "기관계"])
            #
            # self.df = dfS0796[0:5][['일자', '현재가', '누적거래량', '개인투자자', '세력합' , '외국인투자자', '금융투자', '보험', '투신', '기타금융', '은행', '연기금등', '사모펀드', '국가', '기타법인', '내외국인']]
            #
            # print(self.df)
            # print(self.df.columns)

            day1st = self.calMeanSum(dfCalS0796, 0, 1, dfCalS0796["일자"][0])
            day2st = self.calMeanSum(dfCalS0796, 1, 2, dfCalS0796["일자"][1])
            day3st = self.calMeanSum(dfCalS0796, 2, 3, dfCalS0796["일자"][2])
            day4st = self.calMeanSum(dfCalS0796, 3, 4, dfCalS0796["일자"][3])
            day5st = self.calMeanSum(dfCalS0796, 4, 5, dfCalS0796["일자"][4])

            data = []
            data.append(day1st)
            data.append(day2st)
            data.append(day3st)
            data.append(day4st)
            data.append(day5st)

            #            self.tableDataDay = pd.DataFrame(data, columns=columnsList, index=[day1st[0],day2st[0],day3st[0],day4st[0],day5st[0]])
            self.tableDataDay = pd.DataFrame(data, columns=columnsList,
                                             index=[day1st[0], day2st[0], day3st[0], day4st[0], day5st[0]])
        else:
            # dfS0796["세력합"] = dfS0796["외국인투자자"] + dfS0796["금융투자"]
            # dfS0796.drop(columns=["대비기호", "전일대비", "등락율" , "기관계"])
            #
            # self.df = dfS0796[0:len(dfS0796)][['일자', '현재가', '누적거래량', '개인투자자', '세력합' , '외국인투자자', '금융투자', '보험', '투신', '기타금융', '은행', '연기금등', '사모펀드', '국가', '기타법인', '내외국인']]
            #
            # print(self.df)
            # print(self.df.columns)

            data = []
            dayList = []
            for i, x in dfCalS0796:
                day = self.calMeanSum(dfCalS0796, i, i + 1, dfCalS0796["일자"][i])
                dayList.append(dfCalS0796["일자"][i])
                data.append(day)

            self.tableDataDay = pd.DataFrame(data, columns=columnsList, index=dayList)

        print('Week :-----------------------------------------------------------------------')
        # 주 == 5일
        if weekCnt >= 5:
            week1st = self.calMeanSum(dfCalS0796, 0, 5, "1주")
            week2st = self.calMeanSum(dfCalS0796, 5, 10, "2주")
            week3st = self.calMeanSum(dfCalS0796, 10, 15, "3주")
            week4st = self.calMeanSum(dfCalS0796, 15, 20, "4주")
            week5st = self.calMeanSum(dfCalS0796, 20, 25, "5주")

            data = []
            data.append(week1st)
            data.append(week2st)
            data.append(week3st)
            data.append(week4st)
            data.append(week5st)

            self.tableDataWeek = pd.DataFrame(data, columns=columnsList, index=["1주", "2주", "3주", "4주", "5주"])
            tableDataWeekExist = True
        elif weekCnt >= 4 and weekCnt < 5:
            week1st = self.calMeanSum(dfCalS0796, 0, 5, "1주")
            week2st = self.calMeanSum(dfCalS0796, 5, 10, "2주")
            week3st = self.calMeanSum(dfCalS0796, 10, 15, "3주")
            week4st = self.calMeanSum(dfCalS0796, 15, 20, "4주")

            data = []
            data.append(week1st)
            data.append(week2st)
            data.append(week3st)
            data.append(week4st)

            self.tableDataWeek = pd.DataFrame(data, columns=columnsList, index=["1주", "2주", "3주", "4주"])
            tableDataWeekExist = True
        elif weekCnt >= 3 and weekCnt < 4:
            week1st = self.calMeanSum(dfCalS0796, 0, 5, "1주")
            week2st = self.calMeanSum(dfCalS0796, 5, 10, "2주")
            week3st = self.calMeanSum(dfCalS0796, 10, 15, "3주")

            data = []
            data.append(week1st)
            data.append(week2st)
            data.append(week3st)

            self.tableDataWeek = pd.DataFrame(data, columns=columnsList, index=["1주", "2주", "3주"])
            tableDataWeekExist = True
        elif weekCnt >= 2 and weekCnt < 3:
            week1st = self.calMeanSum(dfCalS0796, 0, 5, "1주")
            week2st = self.calMeanSum(dfCalS0796, 5, 10, "2주")

            data = []
            data.append(week1st)
            data.append(week2st)

            self.tableDataWeek = pd.DataFrame(data, columns=columnsList, index=["1주", "2주"])
            tableDataWeekExist = True
        elif weekCnt >= 1 and weekCnt < 2:
            week1st = self.calMeanSum(dfCalS0796, 0, 5, "1주")

            data = []
            data.append(week1st)

            self.tableDataWeek = pd.DataFrame(data, columns=columnsList, index=["1주"])
            tableDataWeekExist = True
        print('Month :-----------------------------------------------------------------------')
        # 달   - from~to :  20일
        if monthCnt >= 3:
            month1st = self.calMeanSum(dfCalS0796, 0, 20, "1달")
            month2st = self.calMeanSum(dfCalS0796, 20, 40, "2달")
            month3st = self.calMeanSum(dfCalS0796, 40, 60, "3달")

            data = []
            data.append(month1st)
            data.append(month2st)
            data.append(month3st)

            self.tableDataMonth = pd.DataFrame(data, columns=columnsList, index=["1달", "2달", "3달"])
            tableDataMonthExist = True
        elif monthCnt >= 2 and monthCnt < 3:
            month1st = self.calMeanSum(dfCalS0796, 0, 20, "1달")
            month2st = self.calMeanSum(dfCalS0796, 20, 40, "2달")

            data = []
            data.append(month1st)
            data.append(month2st)

            self.tableDataMonth = pd.DataFrame(data, columns=columnsList, index=["1달", "2달"])
            tableDataMonthExist = True
        elif monthCnt >= 1 and monthCnt < 2:
            month1st = self.calMeanSum(dfCalS0796, 0, 20, "1달")

            data = []
            data.append(month1st)

            self.tableDataMonth = pd.DataFrame(data, columns=columnsList, index=["1달"])
            tableDataMonthExist = True
        print('BunGi :-----------------------------------------------------------------------')
        # 분기 - from~to :  60일
        if bungiCnt >= 4:
            bunGi1st = self.calMeanSum(dfCalS0796, 0, 60, "1분기")
            bunGi2st = self.calMeanSum(dfCalS0796, 60, 120, "2분기")
            bunGi3st = self.calMeanSum(dfCalS0796, 120, 180, "3분기")
            bunGi4st = self.calMeanSum(dfCalS0796, 180, 240, "4분기")

            data = []
            data.append(bunGi1st)
            data.append(bunGi2st)
            data.append(bunGi3st)
            data.append(bunGi4st)

            self.tableDataBunGi = pd.DataFrame(data, columns=columnsList, index=["1분기", "2분기", "3분기", "4분기"])
            tableDataBunGiExist = True
        elif bungiCnt >= 3 and bungiCnt < 4:
            bunGi1st = self.calMeanSum(dfCalS0796, 0, 60, "1분기")
            bunGi2st = self.calMeanSum(dfCalS0796, 60, 120, "2분기")
            bunGi3st = self.calMeanSum(dfCalS0796, 120, 180, "3분기")

            data = []
            data.append(bunGi1st)
            data.append(bunGi2st)
            data.append(bunGi3st)

            self.tableDataBunGi = pd.DataFrame(data, columns=columnsList, index=["1분기", "2분기", "3분기"])
            tableDataBunGiExist = True
        elif bungiCnt >= 2 and bungiCnt < 3:
            bunGi1st = self.calMeanSum(dfCalS0796, 0, 60, "1분기")
            bunGi2st = self.calMeanSum(dfCalS0796, 60, 120, "2분기")

            data = []
            data.append(bunGi1st)
            data.append(bunGi2st)

            self.tableDataBunGi = pd.DataFrame(data, columns=columnsList, index=["1분기", "2분기"])
            tableDataBunGiExist = True
        elif bungiCnt >= 1 and bungiCnt < 2:
            bunGi1st = self.calMeanSum(dfCalS0796, 0, 60, "1분기")

            data = []
            data.append(bunGi1st)

            self.tableDataBunGi = pd.DataFrame(data, columns=columnsList, index=["1분기"])
            tableDataBunGiExist = True
        print('year :-----------------------------------------------------------------------')
        if yearCnt >= 7:
            year1st = self.calMeanSum(dfCalS0796, 0, 240, "1년")
            year2st = self.calMeanSum(dfCalS0796, 240, 480, "2년")
            year3st = self.calMeanSum(dfCalS0796, 480, 720, "3년")
            year4st = self.calMeanSum(dfCalS0796, 720, 960, "4년")
            year5st = self.calMeanSum(dfCalS0796, 960, 1200, "5년")
            year6st = self.calMeanSum(dfCalS0796, 1200, 1440, "6년")
            year7st = self.calMeanSum(dfCalS0796, 1440, 1680, "7년")

            data = []
            data.append(year1st)
            data.append(year2st)
            data.append(year3st)
            data.append(year4st)
            data.append(year5st)
            data.append(year6st)
            data.append(year7st)

            self.tableDataYear = pd.DataFrame(data, columns=columnsList,
                                              index=["1년", "2년", "3년", "4년", "5년", "6년", "7년"])
            tableDataYearExist = True
        elif yearCnt >= 6 and yearCnt < 7:
            year1st = self.calMeanSum(dfCalS0796, 0, 240, "1년")
            year2st = self.calMeanSum(dfCalS0796, 240, 480, "2년")
            year3st = self.calMeanSum(dfCalS0796, 480, 720, "3년")
            year4st = self.calMeanSum(dfCalS0796, 720, 960, "4년")
            year5st = self.calMeanSum(dfCalS0796, 960, 1200, "5년")
            year6st = self.calMeanSum(dfCalS0796, 1200, 1440, "6년")

            data = []
            data.append(year1st)
            data.append(year2st)
            data.append(year3st)
            data.append(year4st)
            data.append(year5st)
            data.append(year6st)

            self.tableDataYear = pd.DataFrame(data, columns=columnsList, index=["1년", "2년", "3년", "4년", "5년", "6년"])
            tableDataYearExist = True
        elif yearCnt >= 5 and yearCnt < 6:
            year1st = self.calMeanSum(dfCalS0796, 0, 240, "1년")
            year2st = self.calMeanSum(dfCalS0796, 240, 480, "2년")
            year3st = self.calMeanSum(dfCalS0796, 480, 720, "3년")
            year4st = self.calMeanSum(dfCalS0796, 720, 960, "4년")
            year5st = self.calMeanSum(dfCalS0796, 960, 1200, "5년")

            data = []
            data.append(year1st)
            data.append(year2st)
            data.append(year3st)
            data.append(year4st)
            data.append(year5st)

            self.tableDataYear = pd.DataFrame(data, columns=columnsList, index=["1년", "2년", "3년", "4년", "5년"])
            tableDataYearExist = True
        elif yearCnt >= 4 and yearCnt < 5:
            year1st = self.calMeanSum(dfCalS0796, 0, 240, "1년")
            year2st = self.calMeanSum(dfCalS0796, 240, 480, "2년")
            year3st = self.calMeanSum(dfCalS0796, 480, 720, "3년")
            year4st = self.calMeanSum(dfCalS0796, 720, 960, "4년")

            data = []
            data.append(year1st)
            data.append(year2st)
            data.append(year3st)
            data.append(year4st)

            self.tableDataYear = pd.DataFrame(data, columns=columnsList, index=["1년", "2년", "3년", "4년"])
            tableDataYearExist = True
        elif yearCnt >= 3 and yearCnt < 4:
            year1st = self.calMeanSum(dfCalS0796, 0, 240, "1년")
            year2st = self.calMeanSum(dfCalS0796, 240, 480, "2년")
            year3st = self.calMeanSum(dfCalS0796, 480, 720, "3년")

            data = []
            data.append(year1st)
            data.append(year2st)
            data.append(year3st)

            self.tableDataYear = pd.DataFrame(data, columns=columnsList, index=["1년", "2년", "3년"])
            tableDataYearExist = True
        elif yearCnt >= 2 and yearCnt < 3:
            year1st = self.calMeanSum(dfCalS0796, 0, 240, "1년")
            year2st = self.calMeanSum(dfCalS0796, 240, 480, "2년")

            data = []
            data.append(year1st)
            data.append(year2st)

            self.tableDataYear = pd.DataFrame(data, columns=columnsList, index=["1년", "2년"])
            tableDataYearExist = True
        elif yearCnt >= 1 and yearCnt < 2:
            year1st = self.calMeanSum(dfCalS0796, 0, 240, "1년")

            data = []
            data.append(year1st)

            self.tableDataYear = pd.DataFrame(data, columns=columnsList, index=["1년"])
            tableDataYearExist = True

        dataFList = []

        dataFList.append(self.tableDataDay)

        if tableDataWeekExist == True:
            dataFList.append(self.tableDataWeek)
        if tableDataMonthExist == True:
            dataFList.append(self.tableDataMonth)
        if tableDataBunGiExist == True:
            dataFList.append(self.tableDataBunGi)
        if tableDataYearExist == True:
            dataFList.append(self.tableDataYear)

        df = pd.concat(dataFList)

        # print('00000000000000000000000000000000000000000000000000000')
        # print(df)

        # QTableWidget 에 데이터 표시하기
        column_idx_lookup = list(df.columns)

        dpWidget.setRowCount(len(df.index))

        for i in range(len(df.columns)):
            # print(column_idx_lookup[i])
            for j in range(len(df.index)):
                item: QTableWidgetItem = QTableWidgetItem(str(df[column_idx_lookup[i]][j]))
                dpWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                # print(df[column_idx_lookup[i]][j])

        dpWidget.resizeColumnsToContents()
        dpWidget.resizeRowsToContents()
        # print("End----------------------------------------------------------------")

        return df

    # 계산 : 세력합 계산
    def cal(self, dfS0796=None):

        dfS0796["세력합"] = dfS0796["외국인투자자"] + dfS0796["금융투자"]

        return dfS0796

        # mean, sum

    def calMeanSum(self, dfS0796=None, stIdx=None, etIdx=None, dayName=None):

        col0 = dayName
        col1 = dfS0796[stIdx:etIdx][['현재가']].apply(np.abs).mean()  # 숫자형
        col2 = dfS0796[stIdx:etIdx][['누적거래량']].sum()
        col3 = dfS0796[stIdx:etIdx][['개인투자자']].sum()
        col4 = dfS0796[stIdx:etIdx][['세력합']].sum()
        col5 = dfS0796[stIdx:etIdx][['외국인투자자']].sum()
        col6 = dfS0796[stIdx:etIdx][['금융투자']].sum()
        col7 = dfS0796[stIdx:etIdx][['보험']].sum()
        col8 = dfS0796[stIdx:etIdx][['투신']].sum()
        col9 = dfS0796[stIdx:etIdx][['기타금융']].sum()
        col10 = dfS0796[stIdx:etIdx][['은행']].sum()
        col11 = dfS0796[stIdx:etIdx][['연기금등']].sum()
        col12 = dfS0796[stIdx:etIdx][['사모펀드']].sum()
        col13 = dfS0796[stIdx:etIdx][['국가']].sum()
        col14 = dfS0796[stIdx:etIdx][['기타법인']].sum()
        col15 = dfS0796[stIdx:etIdx][['내외국인']].sum()

        return [col0, col1[0], col2[0], col3[0], col4[0], col5[0], col6[0], col7[0], col8[0], col9[0], col10[0],
                col11[0], col12[0], col13[0], col14[0], col15[0]]

    def drawDist(self, df0796=None, drawLayout=None):

        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/HMFMOLD.TTF").get_name()
        rc('font', family=font_name)

        # fig = plt.figure(figsize=(12, 8))
        #
        # top_axes = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
        # bottom_axes = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
        # bottom_axes.get_yaxis().get_major_formatter().set_scientific(False)
        #
        # top_axes.plot(df.index, df['분산_개인'], label='Adjusted Close')
        # bottom_axes.plot(df.index, df['분산_외국인'])
        #
        # plt.tight_layout()
        # plt.show()

        # df = df0796.sort_index(ascending=True)['20180102':'20200904']
        df = df0796.sort_index(ascending=True)

        # plt.rcParams['figure.figsize'] = (10, 5)
        plt.rcParams['font.size'] = 15

        plt.ion()

        # self.fig = plt.Figure(figsize=(48, 10))

        self.fig = plt.Figure(figsize=(30, 5))


        print("=================================>", type(self.fig))


        self.canvas = FigureCanvas(self.fig)

        drawLayout.addWidget(self.canvas)

        ax = self.fig.add_subplot(111)

        axTwinx = ax.twinx()

        # mpl.rcParams['path.simplify'] = True
        # mpl.rcParams['path.simplify_threshold'] = 1.0
        # mpl.rcParams['agg.path.chunksize'] = 10000

        axTwinx.plot(df["주가"].apply(np.abs), label='주가', color='k', linewidth=2)

        ax.plot(df["분산_개인"], label='개인', color='g')
        ax.plot(df["분산_외국인"], label='외국인', color='r')
        ax.plot(df["분산_금융투자"], label='금융투자', color='b')
        # # ax.plot(df.index, df["분산_보험"], label='보험')
        # # ax.plot(df.index, df["분산_투신"], label='투신')
        # # ax.plot(df.index, df["분산_기타금융"], label='기타금융')
        # # ax.plot(df.index, df["분산_은행"], label='은행')
        # # ax.plot(df.index, df["분산_연기금"], label='연기금')
        # # ax.plot(df.index, df["분산_사모펀드"], label='사모펀드')
        # # ax.plot(df.index, df["분산_국가"], label='국가')
        # # ax.plot(df.index, df["분선_기타법인"], label='기타법인')
        # # ax.plot(df.index, df["분산_내외국인"], label='내외국인')

        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

        # ax.xaxis.set_major_locator(ticker.FixedLocator([20190101,20200101]))
        # ax.xaxis.set_minor_locator(ticker.FixedLocator(np.linspace(0,50,100)))

        ax.legend(loc='upper right')
        axTwinx.legend(loc='upper left')
        ax.grid()

        self.fig.tight_layout()

        cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

        self.canvas.show()

    def drawDist2(self, df0796=None, drawLayout=None):

        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/HMFMOLD.TTF").get_name()
        rc('font', family=font_name)


        df = df0796.sort_index(ascending=True)

        # plt.rcParams['figure.figsize'] = (10, 5)
        plt.rcParams['font.size'] = 15

        plt.ion()

        # self.fig = plt.Figure(figsize=(48, 10))

        self.fig = plt.Figure(figsize=(30, 5))


        print("=================================>", type(self.fig))


        self.canvas = FigureCanvas(self.fig)

        drawLayout.addWidget(self.canvas)

        ax = self.fig.add_subplot(111)

        axTwinx = ax.twinx()

        # mpl.rcParams['path.simplify'] = True
        # mpl.rcParams['path.simplify_threshold'] = 1.0
        # mpl.rcParams['agg.path.chunksize'] = 10000

        axTwinx.plot(df["주가"].apply(np.abs), label='주가', color='k', linewidth=2)

        ax.plot(df["분산_개인"], label='개인', color='g')
        ax.plot(df["분산_외국인"], label='외국인', color='r')
        ax.plot(df["분산_금융투자"], label='금융투자', color='b')
        # # ax.plot(df.index, df["분산_보험"], label='보험')
        # # ax.plot(df.index, df["분산_투신"], label='투신')
        # # ax.plot(df.index, df["분산_기타금융"], label='기타금융')
        # # ax.plot(df.index, df["분산_은행"], label='은행')
        # # ax.plot(df.index, df["분산_연기금"], label='연기금')
        # # ax.plot(df.index, df["분산_사모펀드"], label='사모펀드')
        # # ax.plot(df.index, df["분산_국가"], label='국가')
        # # ax.plot(df.index, df["분선_기타법인"], label='기타법인')
        # # ax.plot(df.index, df["분산_내외국인"], label='내외국인')

        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

        # ax.xaxis.set_major_locator(ticker.FixedLocator([20190101,20200101]))
        # ax.xaxis.set_minor_locator(ticker.FixedLocator(np.linspace(0,50,100)))

        ax.legend(loc='upper right')
        axTwinx.legend(loc='upper left')
        ax.grid()

        self.fig.tight_layout()

        cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

        self.canvas.show()

if __name__ == "__main__":
    pass