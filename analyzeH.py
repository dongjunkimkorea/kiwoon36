# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 05:31:59 2019

@author: DongJun Kim
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3
import time
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.ticker as ticker

if __name__ == "__main__":
    def f(p):
        ret = 1
        if p == 0 :
            ret = 1
        else :
            ret = p
            
        return ret

    def fi(p):
        ret = 0
        if p == 1 :
            ret = 0
        else :
            ret = p
            
        return ret

    select_info = "select 종목코드,일자,현재가 from TR_DATA_OPT10059 where 종목코드= '035900' order by 일자 asc"
    select_sql = "select 일자,개인투자자,외국인투자자,기관계,금융투자,보험,투신,기타금융,은행,연기금등,사모펀드,국가,기타법인,내외국인 from TR_DATA_OPT10059 where 종목코드= '035900' order by 일자 asc"
    
    analyze_db_name = "AY_DATA_OPT10059"
	
    con = sqlite3.connect("c:/db/kosdap.db")

    # 종목코드, 일자, 현재가
    info = pd.read_sql(select_info, con)
    infoSize = info.size
    
    collect = pd.DataFrame([], columns =['종목코드','일자','현재가'
                           ,'개인누적합계','개인최고저점','개인매집수량','개인매집고점','개인분산비율'
                           ,'외국인누적합계','외국인최고저점','외국인매집수량','외국인매집고점','외국인분산비율'
                           ,'금융투자누적합계','금융투자최고저점','금융투자매집수량','금융투자매집고점','금융투자분산비율'
                           ,'보험누적합계','보험최고저점','보험매집수량','보험매집고점','보험분산비율'
                           ,'투신누적합계','투신최고저점','투신매집수량','투신매집고점','투신분산비율'
                           ,'기타금융누적합계','기타금융최고저점','기타금융매집수량','기타금융매집고점','기타금융분산비율'
                           ,'은행누적합계','은행최고저점','은행매집수량','은행매집고점','은행분산비율'
                           ,'연기금누적합계','연기금최고저점','연기금매집수량','연기금매집고점','연기금분산비율'
                           ,'사모펀드누적합계','사모펀드최고저점','사모펀드매집수량','사모펀드매집고점','사모펀드분산비율'
                           ,'국가누적합계','국가최고저점','국가매집수량','국가매집고점','국가분산비율'
                           ,'기타법인누적합계','기타법인최고저점','기타법인매집수량','기타법인매집고점','기타법인분산비율'
                           ,'내외국인누적합계','내외국인최고저점','내외국인매집수량','내외국인매집고점','내외국인분산비율'
                           
                           ,'세력매집추세주가','세력매집추세5일','세력매집추세20일'
                           ,'세력분산비율추세주가','세력분산비율추세개인분산','세력분산비율추세세력분산'
                           ,'부유수량추세주가','부유수량추세외국인','부유수량추세금융투자','부유수량추세보험','부유수량추세투신','부유수량추세기타금융','부유수량추세은행','부유수량추세연기금','부유수량추세사모펀드','부유수량추세국가','부유수량추세기타법인','부유수량추세내외국인'
                           ,'외국인기관합계누적합계','외국인기관합계최고저점','외국인기관합계매집수량','외국인기관합계매집고점','외국인기관합계분산비율','외국인기관합계5일추세','외국인기관합계20일추세','외국인기관합계60일추세']
                        )

    collect['종목코드'] = info['종목코드']
    collect['일자'] = info['일자']
    collect['현재가'] = info['현재가']
    
    # 누적합계
    df   = pd.read_sql(select_sql, con)
    df = df.fillna(0)    
    dfCumSum = df.cumsum()
    
    """ 
    개인
    """
    collect['개인누적합계'] = dfCumSum['개인투자자']
    collect['개인최고저점'] =  dfCumSum['개인투자자'].cummin()
    collect['개인매집수량'] = collect['개인누적합계'].sub(collect['개인최고저점'], axis="index", fill_value=0)
    collect['개인매집고점'] =  collect['개인매집수량'].cummax()
    '''분산비율'''
    collect['개인매집고점'] = collect['개인매집고점'].map(f)
    collect['개인분산비율'] = collect['개인매집수량'].div(collect['개인매집고점']).mul(100) 
    collect['개인매집고점'] = collect['개인매집고점'].map(fi)
    
    """ 
    외국인
    """
    collect['외국인누적합계'] = dfCumSum['외국인투자자']
    collect['외국인최고저점'] =  dfCumSum['외국인투자자'].cummin()
    collect['외국인매집수량'] = collect['외국인누적합계'].sub(collect['외국인최고저점'], axis="index", fill_value=0)
    collect['외국인매집고점'] =  collect['외국인매집수량'].cummax()
    '''분산비율'''
    collect['외국인매집고점'] = collect['외국인매집고점'].map(f)
    collect['외국인분산비율'] = collect['외국인매집수량'].div(collect['외국인매집고점']).mul(100) 
    collect['외국인매집고점'] = collect['외국인매집고점'].map(fi)
	
    """ 
    금융투자
    """
    collect['금융투자누적합계'] = dfCumSum['금융투자']
    collect['금융투자최고저점'] =  dfCumSum['금융투자'].cummin()
    collect['금융투자매집수량'] = collect['금융투자누적합계'].sub(collect['금융투자최고저점'], axis="index", fill_value=0)
    collect['금융투자매집고점'] =  collect['금융투자매집수량'].cummax()
    '''분산비율'''
    collect['금융투자매집고점'] = collect['금융투자매집고점'].map(f)
    collect['금융투자분산비율'] = collect['금융투자매집수량'].div(collect['금융투자매집고점']).mul(100) 
    collect['금융투자매집고점'] = collect['금융투자매집고점'].map(fi)
	
    """ 
    보험
    """
    collect['보험누적합계'] = dfCumSum['보험']
    collect['보험최고저점'] =  dfCumSum['보험'].cummin()
    collect['보험매집수량'] = collect['보험누적합계'].sub(collect['보험최고저점'], axis="index", fill_value=0)
    collect['보험매집고점'] =  collect['보험매집수량'].cummax()
    '''분산비율'''
    collect['보험매집고점'] = collect['보험매집고점'].map(f)
    collect['보험분산비율'] = collect['보험매집수량'].div(collect['보험매집고점']).mul(100) 
    collect['보험매집고점'] = collect['보험매집고점'].map(fi)
	
    """ 
    투신
    """
    collect['투신누적합계'] = dfCumSum['투신']
    collect['투신최고저점'] =  dfCumSum['투신'].cummin()
    collect['투신매집수량'] = collect['투신누적합계'].sub(collect['투신최고저점'], axis="index", fill_value=0)
    collect['투신매집고점'] =  collect['투신매집수량'].cummax()
    '''분산비율'''
    collect['투신매집고점'] = collect['투신매집고점'].map(f)
    collect['투신분산비율'] = collect['투신매집수량'].div(collect['투신매집고점']).mul(100) 
    collect['투신매집고점'] = collect['투신매집고점'].map(fi)
	
    """ 
    기타금융
    """
    collect['기타금융누적합계'] = dfCumSum['기타금융']
    collect['기타금융최고저점'] =  dfCumSum['기타금융'].cummin()
    collect['기타금융매집수량'] = collect['기타금융누적합계'].sub(collect['기타금융최고저점'], axis="index", fill_value=0)
    collect['기타금융매집고점'] =  collect['기타금융매집수량'].cummax()
    '''분산비율'''
    collect['기타금융매집고점'] = collect['기타금융매집고점'].map(f)
    collect['기타금융분산비율'] = collect['기타금융매집수량'].div(collect['기타금융매집고점']).mul(100) 
    collect['기타금융매집고점'] = collect['기타금융매집고점'].map(fi)
	
    """ 
    은행
    """
    collect['은행누적합계'] = dfCumSum['은행']
    collect['은행최고저점'] =  dfCumSum['은행'].cummin()
    collect['은행매집수량'] = collect['은행누적합계'].sub(collect['은행최고저점'], axis="index", fill_value=0)
    collect['은행매집고점'] =  collect['은행매집수량'].cummax()
    '''분산비율'''
    collect['은행매집고점'] = collect['은행매집고점'].map(f)
    collect['은행분산비율'] = collect['은행매집수량'].div(collect['은행매집고점']).mul(100) 
    collect['은행매집고점'] = collect['은행매집고점'].map(fi)
	
    """ 
    연기금
    """
    collect['연기금누적합계'] = dfCumSum['연기금등']
    collect['연기금최고저점'] =  dfCumSum['연기금등'].cummin()
    collect['연기금매집수량'] = collect['연기금누적합계'].sub(collect['연기금최고저점'], axis="index", fill_value=0)
    collect['연기금매집고점'] =  collect['연기금매집수량'].cummax()
    '''분산비율'''
    collect['연기금매집고점'] = collect['연기금매집고점'].map(f)
    collect['연기금분산비율'] = collect['연기금매집수량'].div(collect['연기금매집고점']).mul(100) 
    collect['연기금매집고점'] = collect['연기금매집고점'].map(fi)
	
    """ 
    사모펀드
    """
    collect['사모펀드누적합계'] = dfCumSum['사모펀드']
    collect['사모펀드최고저점'] =  dfCumSum['사모펀드'].cummin()
    collect['사모펀드매집수량'] = collect['사모펀드누적합계'].sub(collect['사모펀드최고저점'], axis="index", fill_value=0)
    collect['사모펀드매집고점'] =  collect['사모펀드매집수량'].cummax()
    '''분산비율'''
    collect['사모펀드매집고점'] = collect['사모펀드매집고점'].map(f)
    collect['사모펀드분산비율'] = collect['사모펀드매집수량'].div(collect['사모펀드매집고점']).mul(100) 
    collect['사모펀드매집고점'] = collect['사모펀드매집고점'].map(fi)
	
    """ 
    국가
    """
    collect['국가누적합계'] = dfCumSum['국가']
    collect['국가최고저점'] =  dfCumSum['국가'].cummin()
    collect['국가매집수량'] = collect['국가누적합계'].sub(collect['국가최고저점'], axis="index", fill_value=0)
    collect['국가매집고점'] =  collect['국가매집수량'].cummax()
    '''분산비율'''
    collect['국가매집고점'] = collect['국가매집고점'].map(f)
    collect['국가분산비율'] = collect['국가매집수량'].div(collect['국가매집고점']).mul(100) 
    collect['국가매집고점'] = collect['국가매집고점'].map(fi)
	
    """ 
    기타법인
    """
    collect['기타법인누적합계'] = dfCumSum['기타법인']
    collect['기타법인최고저점'] =  dfCumSum['기타법인'].cummin()
    collect['기타법인매집수량'] = collect['기타법인누적합계'].sub(collect['기타법인최고저점'], axis="index", fill_value=0)
    collect['기타법인매집고점'] =  collect['기타법인매집수량'].cummax()
    '''분산비율'''
    collect['기타법인매집고점'] = collect['기타법인매집고점'].map(f)
    collect['기타법인분산비율'] = collect['기타법인매집수량'].div(collect['기타법인매집고점']).mul(100) 
    collect['기타법인매집고점'] = collect['기타법인매집고점'].map(fi)
	
    """ 
    내외국인
    """
    collect['내외국인누적합계'] = dfCumSum['내외국인']
    collect['내외국인최고저점'] =  dfCumSum['내외국인'].cummin()
    collect['내외국인매집수량'] = collect['내외국인누적합계'].sub(collect['내외국인최고저점'], axis="index", fill_value=0)
    collect['내외국인매집고점'] =  collect['내외국인매집수량'].cummax()
    '''분산비율'''
    collect['내외국인매집고점'] = collect['내외국인매집고점'].map(f)
    collect['내외국인분산비율'] = collect['내외국인매집수량'].div(collect['내외국인매집고점']).mul(100) 
    collect['내외국인매집고점'] = collect['내외국인매집고점'].map(fi)

    con = sqlite3.connect("c:/db/kosdap.db")
    collect.to_sql(analyze_db_name, con, if_exists='replace', index=False)

    select_ay = "select * from AY_DATA_OPT10059 where 종목코드 = '035900'"
#    dfAn = pd.read_sql(select_ay, con)
    dfAn = pd.read_sql(select_ay, con, index_col='일자')
#    dfAn.info()
    dfAn.index = pd.to_datetime(dfAn.index)
    
    #collect.plot(colormap='gray', fontsize=14)

    fig = plt.figure(figsize=(60, 10))
    ax1 = fig.add_subplot(111)

    ax1.plot(dfAn.index, dfAn['개인분산비율'], color='r', label='개인분산비율')
    ax1.plot(dfAn.index, dfAn['외국인분산비율'], color='b', label='외국인분산비율')
    
    
#    ax1.xaxis.set_label_text('DDDDDDD')
#    ax1.xaxis.set_major_locator(ticker.FixedLocator(day_list))
#    ax1.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))




    ax2 = ax1.twinx()
    ax2.plot(dfAn.index, dfAn['현재가'], color='k', label='Price')


    plt.rcParams['axes.grid'] = True
    plt.legend(loc='best')
    #plt.tight_layout()
    plt.show()

    """
result = ax1.xaxis

result.get_major_formatter()
Out[78]: <pandas.plotting._converter.PandasAutoDateFormatter at 0x99ae090>

result.get_major_locator()
Out[79]: <pandas.plotting._converter.PandasAutoDateLocator at 0x999cf10>

result.get_minor_formatter()
Out[80]: <matplotlib.ticker.NullFormatter at 0x7c5f990>

result.get_minor_locator()
Out[81]: <matplotlib.ticker.NullLocator at 0x9ab4530>    



    
result = ax1.yaxis

result.get_major_formatter()
Out[73]: <matplotlib.ticker.ScalarFormatter at 0xf030c70>

result.get_major_locator()
Out[74]: <matplotlib.ticker.AutoLocator at 0x7c62550>

result.get_minor_formatter()
Out[75]: <matplotlib.ticker.NullFormatter at 0xed92bf0>

result.get_minor_locator()
Out[76]: <matplotlib.ticker.NullLocator at 0x7c62210>    
    """

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    