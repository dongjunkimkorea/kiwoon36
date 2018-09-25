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
    start_time = time.time()

    con = sqlite3.connect("c:/db/kosdap.db")
    df = pd.read_sql("select * from '0796'", con)
    df = df.fillna(0)

    df_len = len(df.index)
    # 누적합계
    col1_sum = []
    col2_sum = []
    col3_sum = []
    col4_sum = []
    col5_sum = []
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
    col1_low = []
    col2_low = []
    col3_low = []
    col4_low = []
    col5_low = []
    col6_low = []
    col7_low = []
    col8_low = []
    col9_low = []
    col10_low = []
    col11_low = []
    col12_low = []
    col13_low = []
    col14_low = []
    col15_low = []
    col16_low = []
    col17_low = []
    col18_low = []

    # 매집수량
    col1_qty = []
    col2_qty = []
    col3_qty = []
    col4_qty = []
    col5_qty = []
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
    col1_hight = []
    col2_hight = []
    col3_hight = []
    col4_hight = []
    col5_hight = []
    col6_hight = []
    col7_hight = []
    col8_hight = []
    col9_hight = []
    col10_hight = []
    col11_hight = []
    col12_hight = []
    col13_hight = []
    col14_hight = []
    col15_hight = []
    col16_hight = []
    col17_hight = []
    col18_hight = []

    # 분산비율
    col1_rate = []
    col2_rate = []
    col3_rate = []
    col4_rate = []
    col5_rate = []
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

    for df_cnt in range(df_len):
        df_rows = df[df_cnt:df_len]


        # 누적합계
        #df_rows_sum_value = df[df_cnt:df_len].sum()
        df_rows_sum_value = df_rows.sum()
        df_rows_low_value = df_rows.min()
        df_rows_hight_value = df_rows.max()

        col1_sum.append(df_rows_sum_value['col1'])
        col2_sum.append(df_rows_sum_value['col2'])
        col3_sum.append(df_rows_sum_value['col3'])
        col4_sum.append(df_rows_sum_value['col4'])
        col5_sum.append(df_rows_sum_value['col5'])
        col6_sum.append(df_rows_sum_value['col6'])
        col7_sum.append(df_rows_sum_value['col7'])
        col8_sum.append(df_rows_sum_value['col8'])
        col9_sum.append(df_rows_sum_value['col9'])
        col10_sum.append(df_rows_sum_value['col10'])
        col11_sum.append(df_rows_sum_value['col11'])
        col12_sum.append(df_rows_sum_value['col12'])
        col13_sum.append(df_rows_sum_value['col13'])
        col14_sum.append(df_rows_sum_value['col14'])
        col15_sum.append(df_rows_sum_value['col15'])
        col16_sum.append(df_rows_sum_value['col16'])
        col17_sum.append(df_rows_sum_value['col17'])
        col18_sum.append(df_rows_sum_value['col18'])

        # 최고저점
        #df_rows_low_value = df[df_cnt:df_len].min()

        col1_low.append(df_rows_low_value['col1'])
        col2_low.append(df_rows_low_value['col2'])
        col3_low.append(df_rows_low_value['col3'])
        col4_low.append(df_rows_low_value['col4'])
        col5_low.append(df_rows_low_value['col5'])
        col6_low.append(df_rows_low_value['col6'])
        col7_low.append(df_rows_low_value['col7'])
        col8_low.append(df_rows_low_value['col8'])
        col9_low.append(df_rows_low_value['col9'])
        col10_low.append(df_rows_low_value['col10'])
        col11_low.append(df_rows_low_value['col11'])
        col12_low.append(df_rows_low_value['col12'])
        col13_low.append(df_rows_low_value['col13'])
        col14_low.append(df_rows_low_value['col14'])
        col15_low.append(df_rows_low_value['col15'])
        col16_low.append(df_rows_low_value['col16'])
        col17_low.append(df_rows_low_value['col17'])
        col18_low.append(df_rows_low_value['col18'])

        # 매집수량
        col1_qty.append(df_rows_sum_value['col1']-df_rows_low_value['col1'])
        col2_qty.append(df_rows_sum_value['col2']-df_rows_low_value['col2'])
        col3_qty.append(df_rows_sum_value['col3']-df_rows_low_value['col3'])
        col4_qty.append(df_rows_sum_value['col4']-df_rows_low_value['col4'])
        col5_qty.append(df_rows_sum_value['col5']-df_rows_low_value['col5'])
        col6_qty.append(df_rows_sum_value['col6']-df_rows_low_value['col6'])
        col7_qty.append(df_rows_sum_value['col7']-df_rows_low_value['col7'])
        col8_qty.append(df_rows_sum_value['col8']-df_rows_low_value['col8'])
        col9_qty.append(df_rows_sum_value['col9']-df_rows_low_value['col9'])
        col10_qty.append(df_rows_sum_value['col10']-df_rows_low_value['col10'])
        col11_qty.append(df_rows_sum_value['col11']-df_rows_low_value['col11'])
        col12_qty.append(df_rows_sum_value['col12']-df_rows_low_value['col12'])
        col13_qty.append(df_rows_sum_value['col13']-df_rows_low_value['col13'])
        col14_qty.append(df_rows_sum_value['col14']-df_rows_low_value['col14'])
        col15_qty.append(df_rows_sum_value['col15']-df_rows_low_value['col15'])
        col16_qty.append(df_rows_sum_value['col16']-df_rows_low_value['col16'])
        col17_qty.append(df_rows_sum_value['col17']-df_rows_low_value['col17'])
        col18_qty.append(df_rows_sum_value['col18']-df_rows_low_value['col18'])

        # 매집고점
        #df_rows_hight_value = df[df_cnt:df_len].max()

        col1_hight.append(df_rows_hight_value['col1'])
        col2_hight.append(df_rows_hight_value['col2'])
        col3_hight.append(df_rows_hight_value['col3'])
        col4_hight.append(df_rows_hight_value['col4'])
        col5_hight.append(df_rows_hight_value['col5'])
        col6_hight.append(df_rows_hight_value['col6'])
        col7_hight.append(df_rows_hight_value['col7'])
        col8_hight.append(df_rows_hight_value['col8'])
        col9_hight.append(df_rows_hight_value['col9'])
        col10_hight.append(df_rows_hight_value['col10'])
        col11_hight.append(df_rows_hight_value['col11'])
        col12_hight.append(df_rows_hight_value['col12'])
        col13_hight.append(df_rows_hight_value['col13'])
        col14_hight.append(df_rows_hight_value['col14'])
        col15_hight.append(df_rows_hight_value['col15'])
        col16_hight.append(df_rows_hight_value['col16'])
        col17_hight.append(df_rows_hight_value['col17'])
        col18_hight.append(df_rows_hight_value['col18'])

        # 분산비율
        col1_rate.append( 0 if (df_rows_hight_value['col1'] == 0) else (abs(df_rows_sum_value['col1']-df_rows_low_value['col1'])) / df_rows_hight_value['col1'])
        col2_rate.append( 0 if (df_rows_hight_value['col2'] == 0) else (abs(df_rows_sum_value['col2']-df_rows_low_value['col2'])) / df_rows_hight_value['col2'])
        col3_rate.append( 0 if (df_rows_hight_value['col3'] == 0) else (abs(df_rows_sum_value['col3']-df_rows_low_value['col3'])) / df_rows_hight_value['col3'])
        col4_rate.append( 0 if (df_rows_hight_value['col4'] == 0) else (abs(df_rows_sum_value['col4']-df_rows_low_value['col4'])) / df_rows_hight_value['col4'])
        col5_rate.append( 0 if (df_rows_hight_value['col5'] == 0) else (abs(df_rows_sum_value['col5']-df_rows_low_value['col5'])) / df_rows_hight_value['col5'])
        col6_rate.append( 0 if (df_rows_hight_value['col6'] == 0) else (abs(df_rows_sum_value['col6']-df_rows_low_value['col6'])) / df_rows_hight_value['col6'])
        col7_rate.append( 0 if (df_rows_hight_value['col7'] == 0) else (abs(df_rows_sum_value['col7']-df_rows_low_value['col7'])) / df_rows_hight_value['col7'])
        col8_rate.append( 0 if (df_rows_hight_value['col8'] == 0) else (abs(df_rows_sum_value['col8']-df_rows_low_value['col8'])) / df_rows_hight_value['col8'])
        col9_rate.append( 0 if (df_rows_hight_value['col9'] == 0) else (abs(df_rows_sum_value['col9']-df_rows_low_value['col9'])) / df_rows_hight_value['col9'])
        col10_rate.append( 0 if (df_rows_hight_value['col10'] == 0) else (abs(df_rows_sum_value['col10']-df_rows_low_value['col10'])) / df_rows_hight_value['col10'])
        col11_rate.append( 0 if (df_rows_hight_value['col11'] == 0) else (abs(df_rows_sum_value['col11']-df_rows_low_value['col11'])) / df_rows_hight_value['col11'])
        col12_rate.append( 0 if (df_rows_hight_value['col12'] == 0) else (abs(df_rows_sum_value['col12']-df_rows_low_value['col12'])) / df_rows_hight_value['col12'])
        col13_rate.append( 0 if (df_rows_hight_value['col13'] == 0) else (abs(df_rows_sum_value['col13']-df_rows_low_value['col13'])) / df_rows_hight_value['col13'])
        col14_rate.append( 0 if (df_rows_hight_value['col14'] == 0) else (abs(df_rows_sum_value['col14']-df_rows_low_value['col14'])) / df_rows_hight_value['col14'])
        col15_rate.append( 0 if (df_rows_hight_value['col15'] == 0) else (abs(df_rows_sum_value['col15']-df_rows_low_value['col15'])) / df_rows_hight_value['col15'])
        col16_rate.append( 0 if (df_rows_hight_value['col16'] == 0) else (abs(df_rows_sum_value['col16']-df_rows_low_value['col16'])) / df_rows_hight_value['col16'])
        col17_rate.append( 0 if (df_rows_hight_value['col17'] == 0) else (abs(df_rows_sum_value['col17']-df_rows_low_value['col17'])) / df_rows_hight_value['col17'])
        col18_rate.append( 0 if (df_rows_hight_value['col18'] == 0) else (abs(df_rows_sum_value['col18']-df_rows_low_value['col18'])) / df_rows_hight_value['col18'])

        '''
        if df_cnt == 1:
            #sum target data
            #print(df[df_cnt:df_len])

            #print(df_rows_sum_value['col1'])
            #print(df_rows_sum_value['col2'])
            #print(df_rows_sum_value['col3'])
            #print(df_rows_sum_value['col4'])
            #print(df_rows_sum_value['col5'])
            #print(df_rows_sum_value['col6'])
            #print(df_rows_sum_value['col7'])
            #print(df_rows_sum_value['col8'])
            #print(df_rows_sum_value['col9'])
            #print(df_rows_sum_value['col10'])
            #print(df_rows_sum_value['col11'])
            #print(df_rows_sum_value['col12'])
            #print(df_rows_sum_value['col13'])
            #print(df_rows_sum_value['col14'])
            #print(df_rows_sum_value['col15'])
            #print(df_rows_sum_value['col16'])
            #print(df_rows_sum_value['col17'])
            #print(df_rows_sum_value['col18'])
        '''

    df['col1_sum'] = col1_sum
    df['col2_sum'] = col2_sum
    df['col3_sum'] = col3_sum
    df['col4_sum'] = col4_sum
    df['col5_sum'] = col5_sum
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

    df['col1_low'] = col1_low
    df['col2_low'] = col2_low
    df['col3_low'] = col3_low
    df['col4_low'] = col4_low
    df['col5_low'] = col5_low
    df['col6_low'] = col6_low
    df['col7_low'] = col7_low
    df['col8_low'] = col8_low
    df['col9_low'] = col9_low
    df['col10_low'] = col10_low
    df['col11_low'] = col11_low
    df['col12_low'] = col12_low
    df['col13_low'] = col13_low
    df['col14_low'] = col14_low
    df['col15_low'] = col15_low
    df['col16_low'] = col16_low
    df['col17_low'] = col17_low
    df['col18_low'] = col18_low

    df['col1_qty'] = col1_qty
    df['col2_qty'] = col2_qty
    df['col3_qty'] = col3_qty
    df['col4_qty'] = col4_qty
    df['col5_qty'] = col5_qty
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

    df['col1_hight'] = col1_hight
    df['col2_hight'] = col2_hight
    df['col3_hight'] = col3_hight
    df['col4_hight'] = col4_hight
    df['col5_hight'] = col5_hight
    df['col6_hight'] = col6_hight
    df['col7_hight'] = col7_hight
    df['col8_hight'] = col8_hight
    df['col9_hight'] = col9_hight
    df['col10_hight'] = col10_hight
    df['col11_hight'] = col11_hight
    df['col12_hight'] = col12_hight
    df['col13_hight'] = col13_hight
    df['col14_hight'] = col14_hight
    df['col15_hight'] = col15_hight
    df['col16_hight'] = col16_hight
    df['col17_hight'] = col17_hight
    df['col18_hight'] = col18_hight

    df['col1_rate'] = col1_rate
    df['col2_rate'] = col2_rate
    df['col3_rate'] = col3_rate
    df['col4_rate'] = col4_rate
    df['col5_rate'] = col5_rate
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

    con = sqlite3.connect("c:/db/kosdap.db")
    df.to_sql('d0796', con, if_exists='replace')

    # 종료부분 코드
    print("start_time", start_time)  # 출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
    print("--- %s seconds ---" % (time.time() - start_time))

    #ma5 = df['col6'].rolling(window=2).sum()
    #print(ma5)