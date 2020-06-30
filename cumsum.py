import pandas as pd
import sqlite3
import numpy as np

if __name__ == "__main__":
    select_sql = "select * from '060250' order by col0 asc"
    select_sql_a = "select * from 'a060250' order by c"


    analyze_db_name = "a060250" #nhn test

    con = sqlite3.connect("c:/db/kosdap.db")
    df = pd.read_sql(select_sql, con)
    df = df.fillna(0)

    df2 = pd.read_sql(select_sql_a, con)

    #
    # print(df.index)
    #
    # print('=====================================')
    #
    # print(df.columns)
    #
    # print('--------------------------------------------------')

    print(df)
    print(df2)

    dsCs = df.apply(np.cumsum)

    print('-----------------------------------')

    print(dsCs)



    # t = pd.DataFrame({"a" : [1,7,15],
    #                   "b" : [-4,2,1]}
    #              )
    # print(t)
    # print()
    # print()
    # print()
    #
    #
    # print("누적합계 -----------------------------------")
    # r1 = t.cumsum()
    # print(r1)
    # print()
    #
    # print("최고저점-----------------------------------")
    # r2 = r1["a"].cummin()
    # r3 = r1["b"].cummin()
    #
    # print(r2)
    # print(r3)
    # print()
    #
    # print("매집수량-----------------------------------")
    # # 누적합계 - 최고저점
    # r4 = r1["a"].subtract(r2, fill_value=0)
    # r5 = r1["b"].subtract(r3, fill_value=0)
    # print(r4)
    # print(r5)
    # print()
    #
    # print("매집고점-----------------------------------")
    # r6 = r4.cummax()
    # r7 = r5.cummax()
    #
    # print(r6)
    # print(r7)
    # print()
    #
    #
    # print("분산비율-----------------------------------")
    # r8 = r4.div(r6, fill_value=0)
    # r9 = r5.div(r7, fill_value=0)
    #
    # print(r8)
    # print(r9)