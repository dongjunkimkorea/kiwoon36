import sys
from PyQt5.QtWidgets import *
import Kiwoom
import time
from pandas import DataFrame
import datetime
import webreader
import numpy as np

MARKET_KOSPI   = 0
MARKET_KOSDAQ  = 10

class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

        print("코스피 종목 수 :" ,len(self.kospi_codes))
        print("코스닥 종목 수 :" ,len(self.kosdaq_codes))

    def get_ohlcv(self, code, start):
        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(0.2)

        df = DataFrame(self.kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'],
                       index=self.kiwoom.ohlcv['date'])
        return df

    def check_speedy_rising_volume(self, code):
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = self.get_ohlcv(code, today)
        volumes = df['volume']

        if len(volumes) < 21:
            return False

        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            if i == 0:
                today_vol = vol
            elif 1 <= i <= 20:
                sum_vol20 += vol
            else:
                break

        avg_vol20 = sum_vol20 / 20
        if today_vol > avg_vol20 * 10:
            return True

    def update_buy_list(self, buy_list):
        f = open("buy_list.txt", "wt")
        for code in buy_list:
            # f.writelines("매수;", code, ";시장가;10;0;매수전")
            f.writelines("매수;%s;시장가;10;0;매수전\n" % (code))
        f.close()

    def run(self):
        buy_list = []
        num = len(self.kosdaq_codes)

        for i, code in enumerate(self.kosdaq_codes):
            print(i, '/', num)
            if self.check_speedy_rising_volume(code):
                buy_list.append(code)

        self.update_buy_list(buy_list)

    """
    배당률 기반 투자 알고리즘
    
    (과거) ... (n-1)년 (n-2)년 (n-1)년 <=|=> n년 ... (현재)  
    (과거) get_min_max_dividend_to_treasury : 과거(현제 이전 3년간) 국채시가배당률(배) 계산값 중, 최소값과 최대값 조회.
    (현재) calculate_estimated_dividend_to_treasury : 현재 국채시가배당률(배) 계산.
    
    이번에는 현재 시점을 기준으로 계산한 국채시가배당룰이 과거 3년 치 국채시가배당률의 최대값보다 큰 경우 해당 종목을 매수하는 알고리즘을 구현해 보겠습니다,
    buy_check_by_dividend_algorithm
    """


    # 하단.현재[예상] 현금배당수익률 / 현재[실시간] 3년 만기 국채수익률
    # 상단.현재[이전] 현금배당수익률 / 현재[실시간] 3년 만기 국채수익률
    def calculate_estimated_dividend_to_treasury(self, code):
        estimated_dividend_yield = webreader.get_estimated_dividend_yield(code)
        # 예상 배당수익률이 즉, 컨센서스가 없으면 이전년도에 계산된 현금배당수익률(상단)을 사용한다.
        if estimated_dividend_yield == 0 :
            estimated_dividend_yield = webreader.get_dividend_yield(code)

            if estimated_dividend_yield == "":
                estimated_dividend_yield = 0

        current_3year_treasury = webreader.get_current_3year_treasury()

        # print(estimated_dividend_yield)
        # print(current_3year_treasury)

        estimated_dividend_to_treasury = float(estimated_dividend_yield) / float(current_3year_treasury)
        return estimated_dividend_to_treasury

    # 최근 3년간.국채시가배당률.의.최대값.최소값을 튜블로 리턴.
    def get_min_max_dividend_to_treasury(self, jCode):
        # what.해당종목의.4년간수익률[마지막년도는 컨센서스 포함됌.]
        previous_dividend_yield = webreader.get_previous_dividend_yield(jCode)
        # 3년만기국채수익률 목록 조회.
        three_years_treasury = webreader.get_3year_treasury()

        # print(previous_dividend_yield)
        # print(three_years_treasury)

        now = datetime.datetime.now()
        cur_year = now.year
        # 해당 종목의 4년간 국채시가배당률(배) 계산값 저장소 선언.
        previous_dividend_to_treasury = {}

        # for 문에서 최근 구하려는 과거 값을 cur_year-3 으로 설정하여 하드코딩하는 것과 같다.
        for year in range(cur_year-3, cur_year) :
            # print(year)
            if year in previous_dividend_yield.keys() and year in three_years_treasury.keys():
                # print(previous_dividend_yield[year], three_years_treasury[year] , sep="/")
                if previous_dividend_yield[year] == "":
                    previous_dividend_yield[year] = 0

                ratio = float(previous_dividend_yield[year]) / float(three_years_treasury[year])
                previous_dividend_to_treasury[year] = ratio

        # print(previous_dividend_to_treasury)
        min_ratio = 0
        max_ratio = 0
        if len(previous_dividend_to_treasury) != 0 :
            min_ratio = min(previous_dividend_to_treasury.values())
            max_ratio = max(previous_dividend_to_treasury.values())

        return (min_ratio, max_ratio)

    def buy_check_by_dividend_algorithm(self, code):
        # 현재[컨센서스.국채시가배당률] -> 없으면 -> 과거[이전 국채시가배당률]
        estimated_dividend_to_treasury = self.calculate_estimated_dividend_to_treasury(code)
        (min_ratio, max_ratio) = self.get_min_max_dividend_to_treasury(code)

        # print("estimated_dividend_to_treasury :",estimated_dividend_to_treasury)
        # print("(min_ratio, max_ratio)", min_ratio, max_ratio)

        if estimated_dividend_to_treasury >= max_ratio and max_ratio != 0:
            return (1, estimated_dividend_to_treasury)
        else:
            return (0, estimated_dividend_to_treasury)

    def run_dividend(self):
        today = datetime.datetime.today().strftime("%Y%m%d")
        print( today, webreader.get_current_3year_treasury())

        buy_list = []
        buy_list_code = []

        """
        코스피
        """
        # for code in self.kospi_codes[0:10]:
        for i, code in enumerate(self.kospi_codes[667:700]):
        # for code in list(["000970"]):
            # 681
            if code in list(['069260','069460']):
                continue

            # if i % 150 == 0:
            #     print("[ 10초 쉬기 ]")
            #     time.sleep(10)
            # else :
            time.sleep(0.5)
            # print( i,'=> 코스피 : ', code)
            ret = self.buy_check_by_dividend_algorithm(code)

            if ret[0] == 1:
                print( i,'=> 코스피 : ', code   , " S", ret)
                buy_list.append((code, ret[1]))
            else:
                print( i,'=> 코스피 : ', code   , " F", ret)

        # 코스닥
        for i, code in enumerate(self.kosdaq_codes):

            # if i % 150 == 0:
            #     print("[ 10초 쉬기 ]")
            #     time.sleep(10)
            # else :
            time.sleep(0.5)
            # print( i,'=> 코스닥 : ', code)
            ret = self.buy_check_by_dividend_algorithm(code)

            if ret[0] == 1:
                print(i, '=> 코스닥 : ', code, " S", ret)
                buy_list.append((code, ret[1]))
            else:
                print(i, '=> 코스닥 : ', code, " F", ret)

        print("=============Result==============================>")
        sorted_list = sorted(buy_list, key=lambda t: t[1], reverse=True)

        print(len(sorted_list))
        print(sorted_list)

        for i in range(len(sorted_list)):
            code = sorted_list[i][0]
            buy_list_code.append(code)

        self.update_buy_list(buy_list_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    # pymon.run()

    j = '005930'

    # 현금배당수익룰(미래.컨센서스) / 3년만기 국채 수익룰(조회시점)
    # print(pymon.calculate_estimated_dividend_to_treasury(j))

    # print(pymon.get_min_max_dividend_to_treasury(j))

    # print(pymon.buy_check_by_dividend_algorithm(j))

    pymon.run_dividend()