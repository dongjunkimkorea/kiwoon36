import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
import sqlite3
import time
from Kiwoom import *
import numpy as np

class PurchaseVolumeAnalysis():
    
    def __init__(self):

        # kiwoom 객체 생성 및 키움과 연결.
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

    def getDailyAmt(self, sCode, sSt=None, sEt=None, dfS0796 = None, dpWidget = None):
        # vaildation: 종목코드 / 시작일자 / 종료일자
        #request: 키움증권 -> s0796
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
                        '누적거래대금': [],
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
            print("조회")
            time.sleep(0.2)

            self.kiwoom.set_input_value("일자", sSt)
            self.kiwoom.set_input_value("종목코드", sCode)
            self.kiwoom.set_input_value("금액수량구분", "2")
            self.kiwoom.set_input_value("매매구분", "0")
            self.kiwoom.set_input_value("단위구분", "1")
            self.kiwoom.comm_rq_data("opt10059_req", "opt10059", 2, "0796")

        df = pd.DataFrame(self.kiwoom.s0796,
                          columns=['일자', '현재가', '대비기호', '전일대비', '등락율', '누적거래대금', '개인투자자', '외국인투자자', '기관계', '금융투자', '보험',
                                   '투신', '기타금융', '은행', '연기금등', '사모펀드', '국가', '기타법인', '내외국인'], index=self.kiwoom.s0796['일자'])

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
            #print(column_idx_lookup[i])
            for j in range(len(df.index)):
                item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]))))
                dpWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                #print(df[column_idx_lookup[i]][j])

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

    #---------------------------------------------------------------------------------------------------------------
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
        print('dfS0796.head() : ')
        print(dfS0796.head())

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
        dfS0796 = dfS0796.drop(columns=["일자","현재가","대비기호", "전일대비", "등락율", "누적거래대금"])

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 누적합계 --------------------------------------------------')
        
        df_cumsum = dfS0796.cumsum()
        df_cumsum["외국인기관"] = df_cumsum["외국인투자자"] + df_cumsum["금융투자"]
		
        print('dfS0796 id : ' , id(dfS0796))
        print('df_cumsum id : ' , id(df_cumsum))

        print(list(dfS0796.columns))
        print(list(df_cumsum.columns))

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
        print('dfS0796.tail()')
        print(dfS0796.tail())
        print('df_cumsum.tail()')
        print(df_cumsum.tail())

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

        # print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 최고저점  >>> 최고저점을 계산하기 위한 데이터 생성 후 삽입과정--')

        # print(df_cumsum.head(5))
        # x = df_cumsum[df_cumsum.개인투자자 != 0]
        # print(x.head(5))
        
        # index = df_cumsum[df_cumsum.개인투자자 != 0].index[0]
        # print('index:', index)
        #
        # value = df_cumsum[df_cumsum.개인투자자 != 0].loc[index,"개인투자자"]
        # print('value : ', value)
        #
        #
        # print(df_cumsum.loc[:index, "개인투자자"])
        # print(df_cumsum[:index])
        #
        #
        # df_cumsum.loc[:index, "개인투자자"] = np.array([value] * len(df_cumsum[:index]))
        #
        # print(df_cumsum[:"20060102"])

        # dfRow = df_cumsum[df_cumsum["개인투자자" != 0]].loc[0:1]
        #
        # print('dfRow : ')
        # print(dfRow)
        #
        # dataIndex = dfRow.index[0]
        #
        # print('dataIndex : ' + dataIndex)
        #
        # dataValue = dfRow.loc[0:1,'개인투자자']
        #
        # print('dataValue : ' + dataValue)

        # print(not_zero_row)
        #
        # print(df_cumsum.index[0])
        # print(not_zero_row.index[0])
        # print(not_zero_row.at[not_zero_row.index[0],"개인투자자"])
        #
        # df_cumsum[df_cumsum.index[0]:not_zero_row.index[0]]["개인투자자"] =
        #
        #
        # 누적데이터 0 인 행을 찾아서, 최초거래일에 해당하는 데이터를 최초의 최고저점 데이터 생성하여 삽입하기.
        # df_per_zoro_first_not = df_cumsum[df_cumsum["개인투자자"] != 0][0:1]
        # df_for_zoro_first_not = df_cumsum[df_cumsum["외국인투자자"] != 0][0:1]
        # df_gir_zoro_first_not = df_cumsum[df_cumsum["기관계"] != 0][0:1]
        # df_fin_zoro_first_not = df_cumsum[df_cumsum["금융투자"] != 0][0:1]
        # df_ins_zoro_first_not = df_cumsum[df_cumsum["보험"] != 0][0:1]
        # df_tos_zoro_first_not = df_cumsum[df_cumsum["투신"] != 0][0:1]
        # df_etf_zoro_first_not = df_cumsum[df_cumsum["기타금융"] != 0][0:1]
        # df_bnk_zoro_first_not = df_cumsum[df_cumsum["은행"] != 0][0:1]
        # df_ygi_zoro_first_not = df_cumsum[df_cumsum["연기금등"] != 0][0:1]
        # df_smo_zoro_first_not = df_cumsum[df_cumsum["사모펀드"] != 0][0:1]
        # df_nat_zoro_first_not = df_cumsum[df_cumsum["국가"] != 0][0:1]
        # df_etb_zoro_first_not = df_cumsum[df_cumsum["기타법인"] != 0][0:1]
        # df_pfs_zoro_first_not = df_cumsum[df_cumsum["내외국인"] != 0][0:1]
        #
        # df_cumsum[df_cumsum.index[0]:df_per_zoro_first_not.index[0]]["개인투자자"] = df_per_zoro_first_not.iat[0,0]
        # df_cumsum[df_cumsum.index[0]:df_for_zoro_first_not.index[0]]["외국인투자자"]= df_for_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_gir_zoro_first_not.index[0]]["기관계"]= df_gir_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_fin_zoro_first_not.index[0]]["금융투자"]= df_fin_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_ins_zoro_first_not.index[0]]["보험"] = df_ins_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_tos_zoro_first_not.index[0]]["투신"] = df_tos_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_etf_zoro_first_not.index[0]]["기타금융"] = df_etf_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_bnk_zoro_first_not.index[0]]["은행"] = df_bnk_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_ygi_zoro_first_not.index[0]]["연기금등"] = df_ygi_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_smo_zoro_first_not.index[0]]["사모펀드"] = df_smo_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_nat_zoro_first_not.index[0]]["국가"] = df_nat_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_etb_zoro_first_not.index[0]]["기타법인"] = df_etb_zoro_first_not.iat[0, 0]
        # df_cumsum[df_cumsum.index[0]:df_pfs_zoro_first_not.index[0]]["내외국인"] = df_pfs_zoro_first_not.iat[0, 0]

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
        df_cumsum["최고저점_외국인투자자"]=for_min
        df_cumsum["최고저점_기관계"]=gik_min
        df_cumsum["최고저점_금융투자"]=fin_min
        df_cumsum["최고저점_보험"]=ins_min
        df_cumsum["최고저점_투신"]=tos_min
        df_cumsum["최고저점_기타금융"]=etf_min
        df_cumsum["최고저점_은행"]=bnk_min
        df_cumsum["최고저점_연기금등"]=ygi_min
        df_cumsum["최고저점_사모펀드"]=smo_min
        df_cumsum["최고저점_국가"]=nat_min
        df_cumsum["최고저점_기타법인"]=etb_min
        df_cumsum["최고저점_내외국인"]=pfs_min
        df_cumsum["최고저점_외국인기관"]=forFin_min

        # print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 최고저점  >>> 최고저점을 계산하기 위한 데이터 생성 후 삽입과정 >>> 후 데이터 삭제')
        #
        # df_cumsum.loc[:index, "개인투자자"] = np.array([0] * len(df_cumsum[:index]))
        # df_cumsum.loc[:index, "최고저점_개인투자자"] = np.array([0] * len(df_cumsum[:index]))



        # print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 최고저점  >>> 최고저점을 계산하기 위한 데이터 생성 후 삽입과정 >>> 데이터 "0" 으로 되돌리기--')
        # df_cumsum[df_cumsum.index[0]:df_per_zoro_first_not.index[0]]["개인투자자"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_for_zoro_first_not.index[0]]["외국인투자자"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_gir_zoro_first_not.index[0]]["기관계"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_fin_zoro_first_not.index[0]]["금융투자"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_ins_zoro_first_not.index[0]]["보험"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_tos_zoro_first_not.index[0]]["투신"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_etf_zoro_first_not.index[0]]["기타금융"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_bnk_zoro_first_not.index[0]]["은행"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_ygi_zoro_first_not.index[0]]["연기금등"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_smo_zoro_first_not.index[0]]["사모펀드"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_nat_zoro_first_not.index[0]]["국가"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_etb_zoro_first_not.index[0]]["기타법인"].loc[:] = 0
        # df_cumsum[df_cumsum.index[0]:df_pfs_zoro_first_not.index[0]]["내외국인"].loc[:] = 0
        
        
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
        df_cumsum["매집수량_외국인투자자"]=for_tot
        df_cumsum["매집수량_기관계"]=gik_tot
        df_cumsum["매집수량_금융투자"]=fin_tot
        df_cumsum["매집수량_보험"]=ins_tot
        df_cumsum["매집수량_투신"]=tos_tot
        df_cumsum["매집수량_기타금융"]=etf_tot
        df_cumsum["매집수량_은행"]=bnk_tot
        df_cumsum["매집수량_연기금등"]=ygi_tot
        df_cumsum["매집수량_사모펀드"]=smo_tot
        df_cumsum["매집수량_국가"]=nat_tot
        df_cumsum["매집수량_기타법인"]=etb_tot
        df_cumsum["매집수량_내외국인"]=pfs_tot
        df_cumsum["매집수량_외국인기관"]=forFin_tot

        print('>>> getAccAmt()  >>>  분석 DataFrame 생성 >>> 매집수량 5,20,60추세 --------------------------------------------------')		
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
        df_cumsum["매집고점_외국인투자자"]=for_max
        df_cumsum["매집고점_기관계"]=gik_max
        df_cumsum["매집고점_금융투자"]=fin_max
        df_cumsum["매집고점_보험"]=ins_max
        df_cumsum["매집고점_투신"]=tos_max
        df_cumsum["매집고점_기타금융"]=etf_max
        df_cumsum["매집고점_은행"]=bnk_max
        df_cumsum["매집고점_연기금등"]=ygi_max
        df_cumsum["매집고점_사모펀드"]=smo_max
        df_cumsum["매집고점_국가"]=nat_max
        df_cumsum["매집고점_기타법인"]=etb_max
        df_cumsum["매집고점_내외국인"]=pfs_max
		
        df_cumsum["매집고점_외국인기관"]=forFin_max

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

        df_cumsum["분산비율_개인투자자"] = per_rate *100
        df_cumsum["분산비율_외국인투자자"]=for_rate*100
        df_cumsum["분산비율_기관계"]=gik_rate*100
        df_cumsum["분산비율_금융투자"]=fin_rate*100
        df_cumsum["분산비율_보험"]=ins_rate*100
        df_cumsum["분산비율_투신"]=tos_rate*100
        df_cumsum["분산비율_기타금융"]=etf_rate*100
        df_cumsum["분산비율_은행"]=bnk_rate*100
        df_cumsum["분산비율_연기금등"]=ygi_rate*100
        df_cumsum["분산비율_사모펀드"]=smo_rate*100
        df_cumsum["분산비율_국가"]=nat_rate*100
        df_cumsum["분산비율_기타법인"]=etb_rate*100
        df_cumsum["분산비율_내외국인"]=pfs_rate*100
        df_cumsum["분산비율_외국인기관"]=forFin_rate*100

        df_cumsum = df_cumsum.fillna(0)

        print('------------------------------------------------------------------------------------------>>>  분석결과 1')
        print(dfS0796.tail())
        print(df_cumsum.tail())
        print('------------------------------------------------------------------------------------------>>>  분석결과 2')
        print('dfS0796 id :')
        print('df_cumsum id :')
        print(id(dfS0796))
        print(id(df_cumsum))
        print(dfS0796.columns)
        print(df_cumsum.columns)
        print('>>> getAccAmt()  >>>  분석 DataFrame >>> Table  --------------------------------------------------------')
        df = df_cumsum[['일자','현재가',
                        '개인투자자','최고저점_개인투자자','매집수량_개인투자자','매집고점_개인투자자','분산비율_개인투자자',
                        '외국인투자자','최고저점_외국인투자자', '매집수량_외국인투자자', '매집고점_외국인투자자', '분산비율_외국인투자자',
                        
                        
                        '외국인기관','최고저점_외국인기관', '매집수량_외국인기관', '매집고점_외국인기관', '분산비율_외국인기관',
						'외국인기관_5일추세','외국인기관_20일추세','외국인기관_60일추세',
                        
                        
                        '금융투자', '최고저점_금융투자', '매집수량_금융투자', '매집고점_금융투자', '분산비율_금융투자',
                        '보험', '최고저점_보험', '매집수량_보험', '매집고점_보험', '분산비율_보험',
                        '투신', '최고저점_투신', '매집수량_투신', '매집고점_투신', '분산비율_투신',
                        '기타금융', '최고저점_기타금융', '매집수량_기타금융', '매집고점_기타금융', '분산비율_기타금융',
                        '은행', '최고저점_은행', '매집수량_은행', '매집고점_은행', '분산비율_은행',
                        '연기금등', '최고저점_연기금등', '매집수량_연기금등', '매집고점_연기금등', '분산비율_연기금등',
                        '사모펀드', '최고저점_사모펀드', '매집수량_사모펀드', '매집고점_사모펀드', '분산비율_사모펀드',
                        '국가', '최고저점_국가', '매집수량_국가', '매집고점_국가', '분산비율_국가',
                        '기타법인', '최고저점_기타법인', '매집수량_기타법인', '매집고점_기타법인', '분산비율_기타법인',
                        '내외국인', '최고저점_내외국인', '매집수량_내외국인', '매집고점_내외국인', '분산비율_내외국인']]

        df.fillna(0)
        print(df.head())


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
            print(column_idx_lookup[i])
            for j in range(len(df.index)):
                item: QTableWidgetItem = QTableWidgetItem(str(round(float(df[column_idx_lookup[i]][j]))))
                # item: QTableWidgetItem = QTableWidgetItem(str(df[column_idx_lookup[i]][j]))
                dpWidget.setItem(j, i, item)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                #print(df[column_idx_lookup[i]][j])

        dpWidget.resizeColumnsToContents()
        dpWidget.resizeRowsToContents()


        # dict = {'col0_date': col0_date, 'col1_price': prices,
        #         'col6_sum': col6_sum, 'col6_min': col6_min, 'col6_qty': col6_qty, 'col6_max': col6_max,
        #         'col6_rate': col6_rate,
        #         'col7_sum': col7_sum, 'col7_min': col7_min, 'col7_qty': col7_qty, 'col7_max': col7_max,
        #         'col7_rate': col7_rate,
        #         'col8_sum': col8_sum, 'col8_min': col8_min, 'col8_qty': col8_qty, 'col8_max': col8_max,
        #         'col8_rate': col8_rate,
        #         'col9_sum': col9_sum, 'col9_min': col9_min, 'col9_qty': col9_qty, 'col9_max': col9_max,
        #         'col9_rate': col9_rate,
        #         'col10_sum': col10_sum, 'col10_min': col10_min, 'col10_qty': col10_qty, 'col10_max': col10_max,
        #         'col10_rate': col10_rate,
        #         'col11_sum': col11_sum, 'col11_min': col11_min, 'col11_qty': col11_qty, 'col11_max': col11_max,
        #         'col11_rate': col11_rate,
        #         'col12_sum': col12_sum, 'col12_min': col12_min, 'col12_qty': col12_qty, 'col12_max': col12_max,
        #         'col12_rate': col12_rate,
        #         'col13_sum': col13_sum, 'col13_min': col13_min, 'col13_qty': col13_qty, 'col13_max': col13_max,
        #         'col13_rate': col13_rate,
        #         'col14_sum': col14_sum, 'col14_min': col14_min, 'col14_qty': col14_qty, 'col14_max': col14_max,
        #         'col14_rate': col14_rate,
        #         'col15_sum': col15_sum, 'col15_min': col15_min, 'col15_qty': col15_qty, 'col15_max': col15_max,
        #         'col15_rate': col15_rate,
        #         'col16_sum': col16_sum, 'col16_min': col16_min, 'col16_qty': col16_qty, 'col16_max': col16_max,
        #         'col16_rate': col16_rate,
        #         'col17_sum': col17_sum, 'col17_min': col17_min, 'col17_qty': col17_qty, 'col17_max': col17_max,
        #         'col17_rate': col17_rate,
        #         'col18_sum': col18_sum, 'col18_min': col18_min, 'col18_qty': col18_qty, 'col18_max': col18_max,
        #         'col18_rate': col18_rate
        #         }
        #
        # noSortDf = pd.DataFrame(dict, columns=['col0_date', 'col1_price', 'col6_sum', 'col6_min', 'col6_qty', 'col6_max',
        #                                       'col6_rate',
        #                                       'col7_sum', 'col7_min', 'col7_qty', 'col7_max', 'col7_rate',
        #                                       'col8_sum', 'col8_min', 'col8_qty', 'col8_max', 'col8_rate',
        #                                       'col9_sum', 'col9_min', 'col9_qty', 'col9_max', 'col9_rate',
        #                                       'col10_sum', 'col10_min', 'col10_qty', 'col10_max', 'col10_rate',
        #                                       'col11_sum', 'col11_min', 'col11_qty', 'col11_max', 'col11_rate',
        #                                       'col12_sum', 'col12_min', 'col12_qty', 'col12_max', 'col12_rate',
        #                                       'col13_sum', 'col13_min', 'col13_qty', 'col13_max', 'col13_rate',
        #                                       'col14_sum', 'col14_min', 'col14_qty', 'col14_max', 'col14_rate',
        #                                       'col15_sum', 'col15_min', 'col15_qty', 'col15_max', 'col15_rate',
        #                                       'col16_sum', 'col16_min', 'col16_qty', 'col16_max', 'col16_rate',
        #                                       'col17_sum', 'col17_min', 'col17_qty', 'col17_max', 'col17_rate',
        #                                       'col18_sum', 'col18_min', 'col18_qty', 'col18_max', 'col18_rate'
        #                                       ], index=col0_date)

        # dict = {'col0_date': col0_date, 'col1_price': prices,
        #         'col6_sum': col6_sum, 'col6_min': col6_min, 'col6_qty': col6_qty, 'col6_max': col6_max,
        #         'col6_rate': col6_rate,
        #         'col7_sum': col7_sum, 'col7_min': col7_min, 'col7_qty': col7_qty, 'col7_max': col7_max,
        #         'col7_rate': col7_rate,
        #         'col8_sum': col8_sum, 'col8_min': col8_min, 'col8_qty': col8_qty, 'col8_max': col8_max,
        #         'col8_rate': col8_rate,
        #         'col9_sum': col9_sum, 'col9_min': col9_min, 'col9_qty': col9_qty, 'col9_max': col9_max,
        #         'col9_rate': col9_rate,
        #         'col10_sum': col10_sum, 'col10_min': col10_min, 'col10_qty': col10_qty, 'col10_max': col10_max,
        #         'col10_rate': col10_rate,
        #         'col11_sum': col11_sum, 'col11_min': col11_min, 'col11_qty': col11_qty, 'col11_max': col11_max,
        #         'col11_rate': col11_rate,
        #         'col12_sum': col12_sum, 'col12_min': col12_min, 'col12_qty': col12_qty, 'col12_max': col12_max,
        #         'col12_rate': col12_rate,
        #         'col13_sum': col13_sum, 'col13_min': col13_min, 'col13_qty': col13_qty, 'col13_max': col13_max,
        #         'col13_rate': col13_rate,
        #         'col14_sum': col14_sum, 'col14_min': col14_min, 'col14_qty': col14_qty, 'col14_max': col14_max,
        #         'col14_rate': col14_rate,
        #         'col15_sum': col15_sum, 'col15_min': col15_min, 'col15_qty': col15_qty, 'col15_max': col15_max,
        #         'col15_rate': col15_rate,
        #         'col16_sum': col16_sum, 'col16_min': col16_min, 'col16_qty': col16_qty, 'col16_max': col16_max,
        #         'col16_rate': col16_rate,
        #         'col17_sum': col17_sum, 'col17_min': col17_min, 'col17_qty': col17_qty, 'col17_max': col17_max,
        #         'col17_rate': col17_rate,
        #         'col18_sum': col18_sum, 'col18_min': col18_min, 'col18_qty': col18_qty, 'col18_max': col18_max,
        #         'col18_rate': col18_rate
        #         }
        #
        # noSortDf = pd.DataFrame(dict, columns=['col0_date', 'col1_price', 'col6_sum', 'col6_min', 'col6_qty', 'col6_max',
        #                                       'col6_rate',
        #                                       'col7_sum', 'col7_min', 'col7_qty', 'col7_max', 'col7_rate',
        #                                       'col8_sum', 'col8_min', 'col8_qty', 'col8_max', 'col8_rate',
        #                                       'col9_sum', 'col9_min', 'col9_qty', 'col9_max', 'col9_rate',
        #                                       'col10_sum', 'col10_min', 'col10_qty', 'col10_max', 'col10_rate',
        #                                       'col11_sum', 'col11_min', 'col11_qty', 'col11_max', 'col11_rate',
        #                                       'col12_sum', 'col12_min', 'col12_qty', 'col12_max', 'col12_rate',
        #                                       'col13_sum', 'col13_min', 'col13_qty', 'col13_max', 'col13_rate',
        #                                       'col14_sum', 'col14_min', 'col14_qty', 'col14_max', 'col14_rate',
        #                                       'col15_sum', 'col15_min', 'col15_qty', 'col15_max', 'col15_rate',
        #                                       'col16_sum', 'col16_min', 'col16_qty', 'col16_max', 'col16_rate',
        #                                       'col17_sum', 'col17_min', 'col17_qty', 'col17_max', 'col17_rate',
        #                                       'col18_sum', 'col18_min', 'col18_qty', 'col18_max', 'col18_rate'
        #                                       ], index=col0_date)
        # df = noSortDf.sort_index(ascending=False)
        #
        # print(df.head())
        # print(df.tail())

        return df


    def getTrend(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        pass

    def getDist(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        pass

    def getAnalysisTable(self, sCode, sSt=None, sEt=None, dfS0796=None, dpWidget=None):
        pass

if __name__ == "__main__":
    pass