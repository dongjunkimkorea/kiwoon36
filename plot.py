import sys

from PyQt5.QtWidgets import *
import pandas as pd
import sqlite3
import time


import matplotlib.dates as mdates

# 2
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange

import matplotlib.ticker as ticker

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def display3(self):

        con = sqlite3.connect("c:/db/kosdap.db")
        df = pd.read_sql("SELECT * FROM a005930", con, index_col='index')
        df = df.sort_values(by=['col0_date'])

        pd.to_datetime(df['col0_date'])

        print("================start")
        print(df.info())
        print(df)
        print("=================end")

        plt.rcParams['axes.grid'] = True
        fig = plt.figure(figsize=(55, 10))




        ax1 = fig.add_subplot(111)


        ax1.plot(df.index, df['col6_rate'], color='g', label='M1')
        ax1.plot(df.index, df['col7_rate'], color='r', label='Forien',linewidth=4)
        ax1.plot(df.index, df['col8_rate'], color='b', label='M3', linewidth=2)

        ax2 = ax1.twinx()
        ax2.plot(df.index, df['col1_price'], 'k.', label="Price", linewidth=5)

        day_list = []
        name_list = []
        for i, day in enumerate(df.index):
            # print(day)
            print(day[4:8])
            if day[4:8] == '0101':
                day_list.append(i)
                #name_list.append(day.strftime('%Y-%m-%d') + '(Mon)')
                name_list.append(day)
                continue
            if day[4:8] == '0102':
                day_list.append(i)
                #name_list.append(day.strftime('%Y-%m-%d') + '(Mon)')
                name_list.append(day)
                continue
            if day[4:8] == '0103':
                day_list.append(i)
                #name_list.append(day.strftime('%Y-%m-%d') + '(Mon)')
                name_list.append(day)
                continue
            if day[4:8] == '0104':
                day_list.append(i)
                #name_list.append(day.strftime('%Y-%m-%d') + '(Mon)')
                name_list.append(day)
                continue
        ax1.xaxis.set_major_locator(ticker.FixedLocator(day_list))
        ax1.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

        print(day_list)
        print(name_list)

        plt.legend('best')
        plt.show()
    def display2(self):
        con = sqlite3.connect("c:/db/kosdap.db")
        df = pd.read_sql("SELECT * FROM d091120", con, index_col='index')
        df = df.sort_values(by=['col0_date'])


        date1 = datetime.datetime(int(df['col0_date'][0][0:4]), int(df['col0_date'][0][4:6]), int(df['col0_date'][0][6:8]))
        date2 = datetime.datetime(int(df['col0_date'][len(df)-1][0:4]), int(df['col0_date'][len(df)-1][4:6]), int(df['col0_date'][len(df)-1][6:8]))
        delta = datetime.timedelta(hours=24)
        dates = drange(date1, date2, delta)



        fig, ax = plt.subplots()
        ax.plot_date(dates, list(df['col1_price']))

        # this is superfluous, since the autoscaler should get it right, but
        # use date2num and num2date to convert between dates and floats if
        # you want; both date2num and num2date convert an instance or sequence
        ax.set_xlim(dates[0], dates[-1])

        # The hour locator takes the hour or sequence of hours you want to
        # tick, not the base multiple

        ax.xaxis.set_major_locator(DayLocator())
        ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
        fig.autofmt_xdate()

        plt.show()







    def display(self):
        # con = sqlite3.connect("c:/db/kosdap.db")
        # df = pd.read_sql("SELECT * FROM d0796", con, index_col='index')
        #
        # df = df.sort_values(by=['col0_date'])
        # print(df)
        #
        #
        # fig = plt.figure(figsize=(60,25))
        # ax1 = fig.add_subplot(111)
        #
        # ax1.plot(df['col0_date'], df['col1_price'])
        #
        # years = mdates.YearLocator()  # every year
        # months = mdates.MonthLocator()  # every month
        # yearsFmt = mdates.DateFormatter('%Y')
        #
        # # format the ticks
        # ax1.xaxis.set_major_locator(years)
        # ax1.xaxis.set_major_formatter(yearsFmt)
        # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # ax1.xaxis.set_minor_locator(months)
        #
        # ax1.set_xlim(df['col0_date'].min(),df['col0_date'].max())
        #
        # # format the coords message box
        # def price(x):
        #     print(x)
        #     return '$%1.2f' % x
        #
        # #ax1.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        #
        # ax1.format_ydata = price
        # ax1.grid(True)
        #
        #
        #
        #
        # #ax1.set_xticks(['20070520','20160101','20170101','20180807'])
        # fig.autofmt_xdate()
        # plt.show()














        # con = sqlite3.connect("c:/db/kosdap.db")
        # df = pd.read_sql("SELECT * FROM d0796", con)
        # df = df.sort_values(by=['index'])
        # print(df)
        # #col1_price = df['col1_price']




        # dict = {'col1_price': col1_price,
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
        # orderDf = pd.DataFrame(dict, columns=['col1_price', 'col6_sum', 'col6_min', 'col6_qty', 'col6_max', 'col6_rate',
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
        #                                       ], index=index_list)



        #df = pd.read_sql("SELECT * FROM d0796", con, index_col='col0_date')
        #print("===================================================>>>>>>>>>>>>>>>")
        #df.sort_values(by=['col1_price'])
        #df.sort_values(by='col0_date', ascending=True)


        #print(df)
        #plt.xlim(100, 3000)
        #plt.ylim(50, 100)
        # plt.xlabel('x axis')
        # plt.ylabel('y axis')
        # plt.title('matplotlib sample')
        #
        #
        # plt.subplot(15, 1, 1)
        # plt.plot(df.index, df['col6_rate'], 'r', label='개인')
        # plt.plot(df.index, df['col7_rate'], 'g', label='fo')
        # plt.plot(df.index, df['col8_rate'], 'b', label='gi')
        #
        # plt.subplot(15,1, 2)
        # plt.plot(df.index, df['col1_price'], label="현재가")
        #
        # plt.subplot(15, 1, 3)
        # plt.plot(df.index, df['col6_rate'], 'r', label='개인')
        #
        # plt.subplot(15, 1, 4)
        # plt.plot(df.index, df['col7_rate'], 'g', label='fo')
        #
        # plt.subplot(15, 1, 5)
        # plt.plot(df.index, df['col8_rate'], 'b', label='gi')
        #
        # plt.subplot(15, 1, 6)
        # plt.plot(df.index, df['col9_rate'], label="금융투자")
        #
        # plt.subplot(15, 1, 7)
        # plt.plot(df.index, df['col10_rate'], label="보험")
        #
        # plt.subplot(15, 1, 8)
        # plt.plot(df.index, df['col11_rate'], label="투신")
        #
        # plt.subplot(15, 1, 9)
        # plt.plot(df.index, df['col12_rate'], label="기타금융")
        #
        # plt.subplot(15, 1, 10)
        # plt.plot(df.index, df['col13_rate'], label="은행")
        #
        # plt.subplot(15, 1, 11)
        # plt.plot(df.index, df['col14_rate'], label="연기금")
        #
        # plt.subplot(15, 1, 12)
        # plt.plot(df.index, df['col15_rate'], label="사모펀드")
        #
        # plt.subplot(15, 1, 13)
        # plt.plot(df.index, df['col16_rate'], label="국가")
        #
        # plt.subplot(15, 1, 14)
        # plt.plot(df.index, df['col17_rate'], label="기타법인")
        #
        # plt.subplot(15, 1, 15)
        # plt.plot(df.index, df['col18_rate'], label="내외국인")

        '''
        Y 축 2개 , 매집비울/종가
        '''
        con = sqlite3.connect("c:/db/kosdap.db")
        df = pd.read_sql("SELECT * FROM d091120", con, index_col='index')

        df = df.sort_values(by=['col0_date'])

        fig = plt.figure(figsize=(50,10))
        ax1 = fig.add_subplot(111)
        # print(df['col6_rate'])
        # print(df.index)
        ax1.plot(df.index, df['col6_rate'], color='r', label='개인')
        ax1.plot(df.index, df['col7_rate'], color='g', label='외국인')
        ax1.plot(df.index, df['col8_rate'], color='b', label='기관')

        ax2 = ax1.twinx()
        ax2.plot(df.index, df['col1_price'], label="현재가", linewidth=2)

        ax1.set_xlabel('매집비율 / 가격 ')
        ax1.set_ylabel('매집비율')
        ax2.set_ylabel('가격')



        years = mdates.YearLocator()  # every year
        months = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')

        # format the ticks
        ax1.xaxis.set_major_locator(years)
        ax1.xaxis.set_major_formatter(yearsFmt)
        ax1.xaxis.set_minor_locator(months)


        print(df['col0_date'][0])

        ax1.set_xlim(df['col0_date'][0], df['col0_date'][2787])

        # format the coords message box
        def price(x):
            return '$%1.2f' % x

        ax1.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax1.format_ydata = price
        ax1.grid(True)

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()

        plt.show()









        '''
        graph
        '''
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
        # plt.show()
if __name__ == "__main__":
    start_time = time.time()

    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.display3()
    myWindow.show()
    app.exec_()
