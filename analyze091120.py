'''
한종목의 0796 데이터 연계
예)이엠텍 한 건 만 불러오기.
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3
import time

if __name__ == "__main__":

    # yg
    select_sql = "select * from '091120'"
    analyze_db_name = "a091120"

    start_time = time.time()

    con = sqlite3.connect("c:/db/kosdap.db")
    df = pd.read_sql(select_sql, con)
    df = df.fillna(0)

    #df = df[0:39]
    df_len = len(df.index)

    # 날짜
    col0_date = []

    # 종가
    col1_price = []

    # 누적합계
    col6_sum = []
    col7_sum = []
    col8_sum = []
    col9_sum = []
    col10_sum = []
    col11_sum = []
    col12_sum = []
    col13_sum = []
    col14_sum = []
    col15_sum = []
    col16_sum = []
    col17_sum = []
    col18_sum = []

    # 최고저점
    col6_min = []
    col7_min = []
    col8_min = []
    col9_min = []
    col10_min = []
    col11_min = []
    col12_min = []
    col13_min = []
    col14_min = []
    col15_min = []
    col16_min = []
    col17_min = []
    col18_min = []

    # 매집수량
    col6_qty = []
    col7_qty = []
    col8_qty = []
    col9_qty = []
    col10_qty = []
    col11_qty = []
    col12_qty = []
    col13_qty = []
    col14_qty = []
    col15_qty = []
    col16_qty = []
    col17_qty = []
    col18_qty = []

    # 최고고점
    col6_max = []
    col7_max = []
    col8_max = []
    col9_max = []
    col10_max = []
    col11_max = []
    col12_max = []
    col13_max = []
    col14_max = []
    col15_max = []
    col16_max = []
    col17_max = []
    col18_max = []

    # 분산비율
    col6_rate = []
    col7_rate = []
    col8_rate = []
    col9_rate = []
    col10_rate = []
    col11_rate = []
    col12_rate = []
    col13_rate = []
    col14_rate = []
    col15_rate = []
    col16_rate = []
    col17_rate = []
    col18_rate = []

    index_list =[]

    for df_cnt in range(df_len):
        index_list.append(df['index'][df_cnt])

    # 날짜
    col0_trade_date = df['col0']
    for date in col0_trade_date.values:
        col0_date.append(date)

    # 종가
    col1_last_price = df['col1']
    for price in col1_last_price.values:
        col1_price.append(abs(price))

    print("누적합계")
    # 누적합계
    for df_cnt in range(df_len):
        print("누적합계" , df_cnt)
        sum_value_list = df[df_cnt:df_len].sum()

        col6_sum.append(sum_value_list['col6'])
        col7_sum.append(sum_value_list['col7'])
        col8_sum.append(sum_value_list['col8'])
        col9_sum.append(sum_value_list['col9'])
        col10_sum.append(sum_value_list['col10'])
        col11_sum.append(sum_value_list['col11'])
        col12_sum.append(sum_value_list['col12'])
        col13_sum.append(sum_value_list['col13'])
        col14_sum.append(sum_value_list['col14'])
        col15_sum.append(sum_value_list['col15'])
        col16_sum.append(sum_value_list['col16'])
        col17_sum.append(sum_value_list['col17'])
        col18_sum.append(sum_value_list['col18'])

    df['col6_sum'] = col6_sum
    df['col7_sum'] = col7_sum
    df['col8_sum'] = col8_sum
    df['col9_sum'] = col9_sum
    df['col10_sum'] = col10_sum
    df['col11_sum'] = col11_sum
    df['col12_sum'] = col12_sum
    df['col13_sum'] = col13_sum
    df['col14_sum'] = col14_sum
    df['col15_sum'] = col15_sum
    df['col16_sum'] = col16_sum
    df['col17_sum'] = col17_sum
    df['col18_sum'] = col18_sum

    print("최고저점")
    # 최고저점
    for df_cnt in range(df_len):
        df_rows = df[df_cnt:df_len]

        # 누적합계
        min_value_list = df[df_cnt:df_len].min()

        col6_min.append(min_value_list['col6_sum'])
        col7_min.append(min_value_list['col7_sum'])
        col8_min.append(min_value_list['col8_sum'])
        col9_min.append(min_value_list['col9_sum'])
        col10_min.append(min_value_list['col10_sum'])
        col11_min.append(min_value_list['col11_sum'])
        col12_min.append(min_value_list['col12_sum'])
        col13_min.append(min_value_list['col13_sum'])
        col14_min.append(min_value_list['col14_sum'])
        col15_min.append(min_value_list['col15_sum'])
        col16_min.append(min_value_list['col16_sum'])
        col17_min.append(min_value_list['col17_sum'])
        col18_min.append(min_value_list['col18_sum'])

    df['col6_min'] = col6_min
    df['col7_min'] = col7_min
    df['col8_min'] = col8_min
    df['col9_min'] = col9_min
    df['col10_min'] = col10_min
    df['col11_min'] = col11_min
    df['col12_min'] = col12_min
    df['col13_min'] = col13_min
    df['col14_min'] = col14_min
    df['col15_min'] = col15_min
    df['col16_min'] = col16_min
    df['col17_min'] = col17_min
    df['col18_min'] = col18_min

    print("매집수량")
    # 매집수량
    for df_cnt in range(df_len):

        col6_qty.append(int(df['col6_sum'][df_cnt]) - int(df['col6_min'][df_cnt]))
        col7_qty.append(int(df['col7_sum'][df_cnt]) - int(df['col7_min'][df_cnt]))
        col8_qty.append(int(df['col8_sum'][df_cnt]) - int(df['col8_min'][df_cnt]))
        col9_qty.append(int(df['col9_sum'][df_cnt]) - int(df['col9_min'][df_cnt]))
        col10_qty.append(int(df['col10_sum'][df_cnt]) - int(df['col10_min'][df_cnt]))
        col11_qty.append(int(df['col11_sum'][df_cnt]) - int(df['col11_min'][df_cnt]))
        col12_qty.append(int(df['col12_sum'][df_cnt]) - int(df['col12_min'][df_cnt]))
        col13_qty.append(int(df['col13_sum'][df_cnt]) - int(df['col13_min'][df_cnt]))
        col14_qty.append(int(df['col14_sum'][df_cnt]) - int(df['col14_min'][df_cnt]))
        col15_qty.append(int(df['col15_sum'][df_cnt]) - int(df['col15_min'][df_cnt]))
        col16_qty.append(int(df['col16_sum'][df_cnt]) - int(df['col16_min'][df_cnt]))
        col17_qty.append(int(df['col17_sum'][df_cnt]) - int(df['col17_min'][df_cnt]))
        col18_qty.append(int(df['col18_sum'][df_cnt]) - int(df['col18_min'][df_cnt]))

    df['col6_qty'] = col6_qty
    df['col7_qty'] = col7_qty
    df['col8_qty'] = col8_qty
    df['col9_qty'] = col9_qty
    df['col10_qty'] = col10_qty
    df['col11_qty'] = col11_qty
    df['col12_qty'] = col12_qty
    df['col13_qty'] = col13_qty
    df['col14_qty'] = col14_qty
    df['col15_qty'] = col15_qty
    df['col16_qty'] = col16_qty
    df['col17_qty'] = col17_qty
    df['col18_qty'] = col18_qty

    print("매집고점")
    # 매집고점
    for df_cnt in range(df_len):
        max_value_list = df[df_cnt:df_len].max()

        col6_max.append(max_value_list['col6_qty'])
        col7_max.append(max_value_list['col7_qty'])
        col8_max.append(max_value_list['col8_qty'])
        col9_max.append(max_value_list['col9_qty'])
        col10_max.append(max_value_list['col10_qty'])
        col11_max.append(max_value_list['col11_qty'])
        col12_max.append(max_value_list['col12_qty'])
        col13_max.append(max_value_list['col13_qty'])
        col14_max.append(max_value_list['col14_qty'])
        col15_max.append(max_value_list['col15_qty'])
        col16_max.append(max_value_list['col16_qty'])
        col17_max.append(max_value_list['col17_qty'])
        col18_max.append(max_value_list['col18_qty'])

    df['col6_max'] = col6_max
    df['col7_max'] = col7_max
    df['col8_max'] = col8_max
    df['col9_max'] = col9_max
    df['col10_max'] = col10_max
    df['col11_max'] = col11_max
    df['col12_max'] = col12_max
    df['col13_max'] = col13_max
    df['col14_max'] = col14_max
    df['col15_max'] = col15_max
    df['col16_max'] = col16_max
    df['col17_max'] = col17_max
    df['col18_max'] = col18_max

    print("분산비율")
    # 분산비율
    for df_cnt in range(df_len):
        df_rows = df[df_cnt:df_len]

        col6_rate.append(  0 if (int(df_rows['col6_max'][df_cnt])  == 0) else (int(df_rows['col6_sum'][df_cnt])  - int(df_rows['col6_min'][df_cnt]))  / df_rows['col6_max'][df_cnt]  * 100)
        col7_rate.append(  0 if (int(df_rows['col7_max'][df_cnt])  == 0) else (int(df_rows['col7_sum'][df_cnt])  - int(df_rows['col7_min'][df_cnt]))  / df_rows['col7_max'][df_cnt]  * 100)
        col8_rate.append(  0 if (int(df_rows['col8_max'][df_cnt])  == 0) else (int(df_rows['col8_sum'][df_cnt])  - int(df_rows['col8_min'][df_cnt]))  / df_rows['col8_max'][df_cnt]  * 100)
        col9_rate.append(  0 if (int(df_rows['col9_max'][df_cnt])  == 0) else (int(df_rows['col9_sum'][df_cnt])  - int(df_rows['col9_min'][df_cnt]))  / df_rows['col9_max'][df_cnt]  * 100)
        col10_rate.append( 0 if (int(df_rows['col10_max'][df_cnt]) == 0) else (int(df_rows['col10_sum'][df_cnt]) - int(df_rows['col10_min'][df_cnt])) / df_rows['col10_max'][df_cnt] * 100)
        col11_rate.append( 0 if (int(df_rows['col11_max'][df_cnt]) == 0) else (int(df_rows['col11_sum'][df_cnt]) - int(df_rows['col11_min'][df_cnt])) / df_rows['col11_max'][df_cnt] * 100)
        col12_rate.append( 0 if (int(df_rows['col12_max'][df_cnt]) == 0) else (int(df_rows['col12_sum'][df_cnt]) - int(df_rows['col12_min'][df_cnt])) / df_rows['col12_max'][df_cnt] * 100)
        col13_rate.append( 0 if (int(df_rows['col13_max'][df_cnt]) == 0) else (int(df_rows['col13_sum'][df_cnt]) - int(df_rows['col13_min'][df_cnt])) / df_rows['col13_max'][df_cnt] * 100)
        col14_rate.append( 0 if (int(df_rows['col14_max'][df_cnt]) == 0) else (int(df_rows['col14_sum'][df_cnt]) - int(df_rows['col14_min'][df_cnt])) / df_rows['col14_max'][df_cnt] * 100)
        col15_rate.append( 0 if (int(df_rows['col15_max'][df_cnt]) == 0) else (int(df_rows['col15_sum'][df_cnt]) - int(df_rows['col15_min'][df_cnt])) / df_rows['col15_max'][df_cnt] * 100)
        col16_rate.append( 0 if (int(df_rows['col16_max'][df_cnt]) == 0) else (int(df_rows['col16_sum'][df_cnt]) - int(df_rows['col16_min'][df_cnt])) / df_rows['col16_max'][df_cnt] * 100)
        col17_rate.append( 0 if (int(df_rows['col17_max'][df_cnt]) == 0) else (int(df_rows['col17_sum'][df_cnt]) - int(df_rows['col17_min'][df_cnt])) / df_rows['col17_max'][df_cnt] * 100)
        col18_rate.append( 0 if (int(df_rows['col18_max'][df_cnt]) == 0) else (int(df_rows['col18_sum'][df_cnt]) - int(df_rows['col18_min'][df_cnt])) / df_rows['col18_max'][df_cnt] * 100)

    df['col6_rate'] = col6_rate
    df['col7_rate'] = col7_rate
    df['col8_rate'] = col8_rate
    df['col9_rate'] = col9_rate
    df['col10_rate'] = col10_rate
    df['col11_rate'] = col11_rate
    df['col12_rate'] = col12_rate
    df['col13_rate'] = col13_rate
    df['col14_rate'] = col14_rate
    df['col15_rate'] = col15_rate
    df['col16_rate'] = col16_rate
    df['col17_rate'] = col17_rate
    df['col18_rate'] = col18_rate

    dict ={'col0_date':col0_date,'col1_price' : col1_price,
        'col6_sum':  col6_sum,  'col6_min':  col6_min,  'col6_qty':  col6_qty,  'col6_max':  col6_max,  'col6_rate':  col6_rate,
        'col7_sum':  col7_sum,  'col7_min':  col7_min,  'col7_qty':  col7_qty,  'col7_max':  col7_max,  'col7_rate':  col7_rate,
        'col8_sum':  col8_sum,  'col8_min':  col8_min,  'col8_qty':  col8_qty,  'col8_max':  col8_max,  'col8_rate':  col8_rate,
        'col9_sum':  col9_sum,  'col9_min':  col9_min,  'col9_qty':  col9_qty,  'col9_max':  col9_max,  'col9_rate':  col9_rate,
        'col10_sum': col10_sum, 'col10_min': col10_min, 'col10_qty': col10_qty, 'col10_max': col10_max, 'col10_rate': col10_rate,
        'col11_sum': col11_sum, 'col11_min': col11_min, 'col11_qty': col11_qty, 'col11_max': col11_max, 'col11_rate': col11_rate,
        'col12_sum': col12_sum, 'col12_min': col12_min, 'col12_qty': col12_qty, 'col12_max': col12_max, 'col12_rate': col12_rate,
        'col13_sum': col13_sum, 'col13_min': col13_min, 'col13_qty': col13_qty, 'col13_max': col13_max, 'col13_rate': col13_rate,
        'col14_sum': col14_sum, 'col14_min': col14_min, 'col14_qty': col14_qty, 'col14_max': col14_max, 'col14_rate': col14_rate,
        'col15_sum': col15_sum, 'col15_min': col15_min, 'col15_qty': col15_qty, 'col15_max': col15_max, 'col15_rate': col15_rate,
        'col16_sum': col16_sum, 'col16_min': col16_min, 'col16_qty': col16_qty, 'col16_max': col16_max, 'col16_rate': col16_rate,
        'col17_sum': col17_sum, 'col17_min': col17_min, 'col17_qty': col17_qty, 'col17_max': col17_max, 'col17_rate': col17_rate,
        'col18_sum': col18_sum, 'col18_min': col18_min, 'col18_qty': col18_qty, 'col18_max': col18_max, 'col18_rate': col18_rate
    }

    orderDf = pd.DataFrame(dict, columns=['col0_date','col1_price','col6_sum',  'col6_min',  'col6_qty',  'col6_max',  'col6_rate',
                'col7_sum',  'col7_min',  'col7_qty',  'col7_max',  'col7_rate',
                'col8_sum',  'col8_min',  'col8_qty',  'col8_max',  'col8_rate',
                'col9_sum',  'col9_min',  'col9_qty',  'col9_max',  'col9_rate',
                'col10_sum', 'col10_min', 'col10_qty', 'col10_max', 'col10_rate',
                'col11_sum', 'col11_min', 'col11_qty', 'col11_max', 'col11_rate',
                'col12_sum', 'col12_min', 'col12_qty', 'col12_max', 'col12_rate',
                'col13_sum', 'col13_min', 'col13_qty', 'col13_max', 'col13_rate',
                'col14_sum', 'col14_min', 'col14_qty', 'col14_max', 'col14_rate',
                'col15_sum', 'col15_min', 'col15_qty', 'col15_max', 'col15_rate',
                'col16_sum', 'col16_min', 'col16_qty', 'col16_max', 'col16_rate',
                'col17_sum', 'col17_min', 'col17_qty', 'col17_max', 'col17_rate',
                'col18_sum', 'col18_min', 'col18_qty', 'col18_max', 'col18_rate'
                ], index=index_list)



    con = sqlite3.connect("c:/db/kosdap.db")
    orderDf.to_sql(analyze_db_name, con, if_exists='replace')

    # 종료부분 코드
    print("start_time", start_time)  # 출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
    print("--- %s seconds ---" % (time.time() - start_time))

    #ma5 = df['col6'].rolling(window=2).sum()
    #print(ma5)