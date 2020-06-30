'''
한종목의 0796 데이터 연계
예)이엠텍 한 건 만 불러오기.
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
from PyQt5 import uic, QtGui

import numpy as np

import pandas as pd
import sqlite3
import time

from PyQt5.QtWidgets import QTableWidgetItem

import matplotlib.pyplot as plt

form_class = uic.loadUiType("main_window2.ui")[0]

class Analyze():

    def __init__(self):
        pass

    def analysis(self):
        # local varible
        select_sql = "select * from '060250' order by 일자 ASC"
        analyze_db_name = "a060250"

        start_time = time.time()

        con = sqlite3.connect("c:/db/kosdap.db")
        db = pd.read_sql(select_sql, con)

        # DataFrame index setting
        idx = pd.DatetimeIndex(db["일자"])
        db = db.set_index(idx)

        # print(db.head())
        # print()
        # print(db.index)

        # 검색조건
        # 날짜, 한달, 일년, 3년, 5년, 특정기간
        #db = db.loc['2020-03-01':'2020-04-02']

        # print("--------------------------------------------------------------날짜 추출")
        col0_date = db.index

        # print("--------------------------------------------------------------현재가 추출")
        prices = db["현재가"]

        # DataFrame drop column
        db = db.drop(columns=["일자", "현재가", "대비기호", "전일대비", "등락율", "누적거래대금"])

        # print("--------------------------------------------------------------누적합게")
        df_cumsum = db.cumsum()

        col6_sum = df_cumsum["개인투자자"]
        col7_sum = df_cumsum["외국인투자자"]
        col8_sum = df_cumsum["기관계"]
        col9_sum = df_cumsum["금융투자"]
        col10_sum = df_cumsum["보험"]
        col11_sum = df_cumsum["투신"]
        col12_sum = df_cumsum["기타금융"]
        col13_sum = df_cumsum["은행"]
        col14_sum = df_cumsum["연기금등"]
        col15_sum = df_cumsum["사모펀드"]
        col16_sum = df_cumsum["국가"]
        col17_sum = df_cumsum["기타법인"]
        col18_sum = df_cumsum["내외국인"]

        # print(db.head())
        # print()
        # print(df_cumsum

        # print("--------------------------------------------------------------현재가")
        df_cumsum["현재가"] = prices

        # print("---------------------------------------------------------------최고저점")
        col6_min = df_cumsum["개인투자자"].cummin()
        col7_min = df_cumsum["외국인투자자"].cummin()
        col8_min = df_cumsum["기관계"].cummin()
        col9_min = df_cumsum["금융투자"].cummin()
        col10_min = df_cumsum["보험"].cummin()
        col11_min = df_cumsum["투신"].cummin()
        col12_min = df_cumsum["기타금융"].cummin()
        col13_min = df_cumsum["은행"].cummin()
        col14_min = df_cumsum["연기금등"].cummin()
        col15_min = df_cumsum["사모펀드"].cummin()
        col16_min = df_cumsum["국가"].cummin()
        col17_min = df_cumsum["기타법인"].cummin()
        col18_min = df_cumsum["내외국인"].cummin()

        # per_min = df_cumsum["개인투자자"].cummin()
        # for_min = df_cumsum["외국인투자자"].cummin()
        # gik_min = df_cumsum["기관계"].cummin()
        # fin_min = df_cumsum["금융투자"].cummin()
        # ins_min = df_cumsum["보험"].cummin()
        # tos_min = df_cumsum["투신"].cummin()
        # etf_min = df_cumsum["기타금융"].cummin()
        # bnk_min = df_cumsum["은행"].cummin()
        # ygi_min = df_cumsum["연기금등"].cummin()
        # smo_min = df_cumsum["사모펀드"].cummin()
        # nat_min = df_cumsum["국가"].cummin()
        # etb_min = df_cumsum["기타법인"].cummin()
        # pfs_min = df_cumsum["내외국인"].cummin()

        # df_cumsum["최고저점_개인투자자"] = per_min
        # df_cumsum["최고저점_외국인투자자"]=for_min
        # df_cumsum["최고저점_기관계"]=gik_min
        # df_cumsum["최고저점_금융투자"]=fin_min
        # df_cumsum["최고저점_보험"]=ins_min
        # df_cumsum["최고저점_투신"]=tos_min
        # df_cumsum["최고저점_기타금융"]=etf_min
        # df_cumsum["최고저점_은행"]=bnk_min
        # df_cumsum["최고저점_연기금등"]=ygi_min
        # df_cumsum["최고저점_사모펀드"]=smo_min
        # df_cumsum["최고저점_국가"]=nat_min
        # df_cumsum["최고저점_기타법인"]=etb_min
        # df_cumsum["최고저점_내외국인"]=pfs_min

        # print("----------------------------------------------------------------매집수량 = 누적합계 - 최고저점")
        col6_qty = df_cumsum["개인투자자"].subtract(col6_min, fill_value=0)
        col7_qty = df_cumsum["외국인투자자"].subtract(col7_min, fill_value=0)
        col8_qty = df_cumsum["기관계"].subtract(col8_min, fill_value=0)
        col9_qty = df_cumsum["금융투자"].subtract(col9_min, fill_value=0)
        col10_qty = df_cumsum["보험"].subtract(col10_min, fill_value=0)
        col11_qty = df_cumsum["투신"].subtract(col11_min, fill_value=0)
        col12_qty = df_cumsum["기타금융"].subtract(col12_min, fill_value=0)
        col13_qty = df_cumsum["은행"].subtract(col13_min, fill_value=0)
        col14_qty = df_cumsum["연기금등"].subtract(col14_min, fill_value=0)
        col15_qty = df_cumsum["사모펀드"].subtract(col15_min, fill_value=0)
        col16_qty = df_cumsum["국가"].subtract(col16_min, fill_value=0)
        col17_qty = df_cumsum["기타법인"].subtract(col17_min, fill_value=0)
        col18_qty = df_cumsum["내외국인"].subtract(col8_min, fill_value=0)

        # per_tot = df_cumsum["개인투자자"].subtract(per_min, fill_value=0)
        # for_tot = df_cumsum["외국인투자자"].subtract(for_min, fill_value=0)
        # gik_tot = df_cumsum["기관계"].subtract(gik_min, fill_value=0)
        # fin_tot = df_cumsum["금융투자"].subtract(fin_min, fill_value=0)
        # ins_tot = df_cumsum["보험"].subtract(ins_min, fill_value=0)
        # tos_tot = df_cumsum["투신"].subtract(tos_min, fill_value=0)
        # etf_tot = df_cumsum["기타금융"].subtract(etf_min, fill_value=0)
        # bnk_tot = df_cumsum["은행"].subtract(bnk_min, fill_value=0)
        # ygi_tot = df_cumsum["연기금등"].subtract(ygi_min, fill_value=0)
        # smo_tot = df_cumsum["사모펀드"].subtract(smo_min, fill_value=0)
        # nat_tot = df_cumsum["국가"].subtract(nat_min, fill_value=0)
        # etb_tot = df_cumsum["기타법인"].subtract(etb_min, fill_value=0)
        # pfs_tot = df_cumsum["내외국인"].subtract(pfs_min, fill_value=0)

        # df_cumsum["매집수량_개인투자자"] = per_tot
        # df_cumsum["매집수량_외국인투자자"]=for_tot
        # df_cumsum["매집수량_기관계"]=gik_tot
        # df_cumsum["매집수량_금융투자"]=fin_tot
        # df_cumsum["매집수량_보험"]=ins_tot
        # df_cumsum["매집수량_투신"]=tos_tot
        # df_cumsum["매집수량_기타금융"]=etf_tot
        # df_cumsum["매집수량_은행"]=bnk_tot
        # df_cumsum["매집수량_연기금등"]=ygi_tot
        # df_cumsum["매집수량_사모펀드"]=smo_tot
        # df_cumsum["매집수량_국가"]=nat_tot
        # df_cumsum["매집수량_기타법인"]=etb_tot
        # df_cumsum["매집수량_내외국인"]=pfs_tot

        # print("---------------------------------------------------------------매집고점")
        col6_max = col6_qty.cummax()
        col7_max = col7_qty.cummax()
        col8_max = col8_qty.cummax()
        col9_max = col9_qty.cummax()
        col10_max = col10_qty.cummax()
        col11_max = col11_qty.cummax()
        col12_max = col12_qty.cummax()
        col13_max = col13_qty.cummax()
        col14_max = col14_qty.cummax()
        col15_max = col15_qty.cummax()
        col16_max = col16_qty.cummax()
        col17_max = col17_qty.cummax()
        col18_max = col18_qty.cummax()

        # per_max = per_tot.cummax()
        # for_max = for_tot.cummax()
        # gik_max = gik_tot.cummax()
        # fin_max = fin_tot.cummax()
        # ins_max = ins_tot.cummax()
        # tos_max = tos_tot.cummax()
        # etf_max = etf_tot.cummax()
        # bnk_max = bnk_tot.cummax()
        # ygi_max = ygi_tot.cummax()
        # smo_max = smo_tot.cummax()
        # nat_max = nat_tot.cummax()
        # etb_max = etb_tot.cummax()
        # pfs_max = pfs_tot.cummax()
        #
        # df_cumsum["매집고점_개인투자자"] = per_max
        # df_cumsum["매집고점_외국인투자자"]=for_max
        # df_cumsum["매집고점_기관계"]=gik_max
        # df_cumsum["매집고점_금융투자"]=fin_max
        # df_cumsum["매집고점_보험"]=ins_max
        # df_cumsum["매집고점_투신"]=tos_max
        # df_cumsum["매집고점_기타금융"]=etf_max
        # df_cumsum["매집고점_은행"]=bnk_max
        # df_cumsum["매집고점_연기금등"]=ygi_max
        # df_cumsum["매집고점_사모펀드"]=smo_max
        # df_cumsum["매집고점_국가"]=nat_max
        # df_cumsum["매집고점_기타법인"]=etb_max
        # df_cumsum["매집고점_내외국인"]=pfs_max

        # print("---------------------------------------------------------------분산비율 = 매집수량/매집고점")
        col6_r = col6_qty.div(col6_max) * 100
        col7_r = col7_qty.div(col7_max) * 100
        col8_r = col8_qty.div(col8_max) * 100
        col9_r = col9_qty.div(col9_max) * 100
        col10_r = col10_qty.div(col10_max) * 100
        col11_r = col11_qty.div(col11_max) * 100
        col12_r = col12_qty.div(col12_max) * 100
        col13_r = col13_qty.div(col13_max) * 100
        col14_r = col14_qty.div(col14_max) * 100
        col15_r = col15_qty.div(col15_max) * 100
        col16_r = col16_qty.div(col16_max) * 100
        col17_r = col17_qty.div(col17_max) * 100
        col18_r = col18_qty.div(col18_max) * 100

        col6_rate = col6_r.fillna(0)
        col7_rate = col7_r.fillna(0)
        col8_rate = col8_r.fillna(0)
        col9_rate = col9_r.fillna(0)
        col10_rate = col10_r.fillna(0)
        col11_rate = col11_r.fillna(0)
        col12_rate = col12_r.fillna(0)
        col13_rate = col13_r.fillna(0)
        col14_rate = col14_r.fillna(0)
        col15_rate = col15_r.fillna(0)
        col16_rate = col16_r.fillna(0)
        col17_rate = col17_r.fillna(0)
        col18_rate = col18_r.fillna(0)

        # per_rate = per_tot.div(per_max)
        # for_rate = for_tot.div(for_max)
        # gik_rate = gik_tot.div(gik_max)
        # fin_rate = fin_tot.div(fin_max)
        # ins_rate = ins_tot.div(ins_max)
        # tos_rate = tos_tot.div(tos_max)
        # etf_rate = etf_tot.div(etf_max)
        # bnk_rate = bnk_tot.div(bnk_max)
        # ygi_rate = ygi_tot.div(ygi_max)
        # smo_rate = smo_tot.div(smo_max)
        # nat_rate = nat_tot.div(nat_max)
        # etb_rate = etb_tot.div(etb_max)
        # pfs_rate = pfs_tot.div(pfs_max)

        # df_cumsum["분산비율_개인투자자"] = per_rate *100
        # df_cumsum["분산비율_외국인투자자"]=for_rate*100
        # df_cumsum["분산비율_기관계"]=gik_rate*100
        # df_cumsum["분산비율_금융투자"]=fin_rate*100
        # df_cumsum["분산비율_보험"]=ins_rate*100
        # df_cumsum["분산비율_투신"]=tos_rate*100
        # df_cumsum["분신비율_기타금융"]=etf_rate*100
        # df_cumsum["분산비율_은행"]=bnk_rate*100
        # df_cumsum["분산비율_연기금등"]=ygi_rate*100
        # df_cumsum["분산비율_사모펀드"]=smo_rate*100
        # df_cumsum["분산비율_국가"]=nat_rate*100
        # df_cumsum["분산비율_기타법인"]=etb_rate*100
        # df_cumsum["분산비율_내외국인"]=pfs_rate*100

        # df = df_cumsum.fillna(0)

        dict = {'col0_date': col0_date, 'col1_price': prices,
                'col6_sum': col6_sum, 'col6_min': col6_min, 'col6_qty': col6_qty, 'col6_max': col6_max,
                'col6_rate': col6_rate,
                'col7_sum': col7_sum, 'col7_min': col7_min, 'col7_qty': col7_qty, 'col7_max': col7_max,
                'col7_rate': col7_rate,
                'col8_sum': col8_sum, 'col8_min': col8_min, 'col8_qty': col8_qty, 'col8_max': col8_max,
                'col8_rate': col8_rate,
                'col9_sum': col9_sum, 'col9_min': col9_min, 'col9_qty': col9_qty, 'col9_max': col9_max,
                'col9_rate': col9_rate,
                'col10_sum': col10_sum, 'col10_min': col10_min, 'col10_qty': col10_qty, 'col10_max': col10_max,
                'col10_rate': col10_rate,
                'col11_sum': col11_sum, 'col11_min': col11_min, 'col11_qty': col11_qty, 'col11_max': col11_max,
                'col11_rate': col11_rate,
                'col12_sum': col12_sum, 'col12_min': col12_min, 'col12_qty': col12_qty, 'col12_max': col12_max,
                'col12_rate': col12_rate,
                'col13_sum': col13_sum, 'col13_min': col13_min, 'col13_qty': col13_qty, 'col13_max': col13_max,
                'col13_rate': col13_rate,
                'col14_sum': col14_sum, 'col14_min': col14_min, 'col14_qty': col14_qty, 'col14_max': col14_max,
                'col14_rate': col14_rate,
                'col15_sum': col15_sum, 'col15_min': col15_min, 'col15_qty': col15_qty, 'col15_max': col15_max,
                'col15_rate': col15_rate,
                'col16_sum': col16_sum, 'col16_min': col16_min, 'col16_qty': col16_qty, 'col16_max': col16_max,
                'col16_rate': col16_rate,
                'col17_sum': col17_sum, 'col17_min': col17_min, 'col17_qty': col17_qty, 'col17_max': col17_max,
                'col17_rate': col17_rate,
                'col18_sum': col18_sum, 'col18_min': col18_min, 'col18_qty': col18_qty, 'col18_max': col18_max,
                'col18_rate': col18_rate
                }

        noSortDf = pd.DataFrame(dict, columns=['col0_date', 'col1_price', 'col6_sum', 'col6_min', 'col6_qty', 'col6_max',
                                              'col6_rate',
                                              'col7_sum', 'col7_min', 'col7_qty', 'col7_max', 'col7_rate',
                                              'col8_sum', 'col8_min', 'col8_qty', 'col8_max', 'col8_rate',
                                              'col9_sum', 'col9_min', 'col9_qty', 'col9_max', 'col9_rate',
                                              'col10_sum', 'col10_min', 'col10_qty', 'col10_max', 'col10_rate',
                                              'col11_sum', 'col11_min', 'col11_qty', 'col11_max', 'col11_rate',
                                              'col12_sum', 'col12_min', 'col12_qty', 'col12_max', 'col12_rate',
                                              'col13_sum', 'col13_min', 'col13_qty', 'col13_max', 'col13_rate',
                                              'col14_sum', 'col14_min', 'col14_qty', 'col14_max', 'col14_rate',
                                              'col15_sum', 'col15_min', 'col15_qty', 'col15_max', 'col15_rate',
                                              'col16_sum', 'col16_min', 'col16_qty', 'col16_max', 'col16_rate',
                                              'col17_sum', 'col17_min', 'col17_qty', 'col17_max', 'col17_rate',
                                              'col18_sum', 'col18_min', 'col18_qty', 'col18_max', 'col18_rate'
                                              ], index=col0_date)
        df = noSortDf.sort_index(ascending=False)

        print(df.head())
        print(df.tail())

        return df

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def display(self, df):
        print("=============================================================== display")
        print(df.tail())

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

        # con = sqlite3.connect("c:/db/kosdap.db")
        # df = pd.read_sql(select_sql, con, index_col='index')
        #print(df)
        #print(list(df.columns))

        column_idx_lookup = list(df.columns)


        print(column_idx_lookup)


        self.tableWidget.setColumnCount(len(df.columns))
        self.tableWidget.setRowCount(len(df.index))
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        for i in range(len(df.columns)):
            print(column_idx_lookup[i])
            for j in range(len(df.index)):

                if column_idx_lookup[i] == "col0_date":
                    item: QTableWidgetItem = QTableWidgetItem(str(df[column_idx_lookup[i]][j]))
                else:
                    item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]))))

                # item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]))))
                # item: QTableWidgetItem = QTableWidgetItem(str(df[column_idx_lookup[i]][j]))
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
    c = Analyze()
    df = c.analysis()

    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.display(df)
    myWindow.show()
    app.exec_()