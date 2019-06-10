from bs4 import BeautifulSoup
import requests
import re
import datetime

# code = "035720"
#
# re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
# re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)
#
# url = "http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code)
# print(url)
# html = requests.get(url).text
# encparam = re_enc.search(html).group(1)
# encid = re_id.search(html).group(1)
#
# # freq_typ=A , 전체 Tab
# url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(code, encparam, encid)
# headers = {"Referer": "HACK"}
# html = requests.get(url, headers=headers).text
# print(html)
#
# soup = BeautifulSoup(html, "html5lib")
# dividend = soup.select("table:nth-of-type(2) tr:nth-of-type(33) td span")
# years = soup.select("table:nth-of-type(2) th")
#
# print(years)
# print("-------------------------------------------------------------")
# print(years[3:7])
# print(dividend)

# what.현금배당수익률[과거/어제]
# where.네이버.상단(WISEFn제공).기업현황.현금배당수익률
# return str.dividend_yield 조회시점의 현금배당수익률(최근 결산 수정DPS(현금)_과거 / 전일자 보통주 수정주가_어제)
# def.name.배당 수익률을 얻다.
# str.dividend_yield.배당수익률
def get_dividend_yield(code):
    url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html5lib')
    dt_data = soup.select("td dl dt")

    # print(dt_data)

    dividend_yield = dt_data[-2].text
    dividend_yield = dividend_yield.split(' ')[1]
    dividend_yield = dividend_yield[:-1]

    return dividend_yield

# what.현금배당수익률[컨센서스]
# where.함수에서.def get_financial_statements(code)
# return 해당년도예상수익률(컨센서스) , 제무재표에서 해당년도 예상수익률을 구한다.
# def.name.예상 배당 수익률을 얻는다.
def get_estimated_dividend_yield(code):
    dividend_yield = get_financial_statements(code)
    dividend_yield = sorted(dividend_yield.items())[-1]

    return dividend_yield[1]

# what.현금배당수익률 목록
# where.네이버.하단(WISEFn제공).재무제표전체TAB.현금배당수익률.row
# return dictory.dividend_dict 년도별 현금배당수익률 목록(추정치포함)
# def.name.제무재표에서 배당 수익률을 얻다.
def get_financial_statements(code):
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

    url = "http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code)
    html = requests.get(url).text
    encparam = re_enc.search(html).group(1)
    encid = re_id.search(html).group(1)

    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(code, encparam, encid)
    headers = {"Referer": "HACK"}
    html = requests.get(url, headers=headers).text

    # print(html)

    soup = BeautifulSoup(html, "html5lib")
    # 현금배당수익률
    dividend = soup.select("table:nth-of-type(2) tbody tr:nth-of-type(31) td")
    # 년도
    years = soup.select("table:nth-of-type(2) thead tr:nth-of-type(2) th")

    # print(dividend)
    # print(years)

    dividend_dict = {}

    for i in range(len(dividend)):
        # print("------------------------------------------")
        # print(years[i].text.strip())
        # print(years[i].text.strip()[:10].strip())
        # print(dividend[i].text)

        if i < 4 :
            # 년간
            dividend_dict['y/'+ years[i].text.strip()[:10].strip()] = dividend[i].text
        else:
            # 분기
            dividend_dict['n/' + years[i].text.strip()[:10].strip()] = dividend[i].text

    return dividend_dict

# what.3년 만기 국채 수익률의 일별 시세
# where.네이버
# return 3년 만기 국채 수익률 당일 시세
def get_current_3year_treasury():
    url = "http://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("tr td")

    # print(td_data)
    return td_data[1].text

# what.4년간 수익률
# 참조.최근 마지막 수익률은 당해년도 추정치 수익률임.
def get_previous_dividend_yield(code):
    dividend_yield = get_financial_statements(code)

    now = datetime.datetime.now()
    cur_year = now.year

    previous_dividend_yield = {}

    # print(dividend_yield.keys())
    # print(dividend_yield.values())
    # print(dividend_yield)

    for year in range(cur_year-3, cur_year+1):
        # print("year:", year)
        if "y/"+str(year)+"/12" in dividend_yield.keys():
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/12"]
        if "y/"+str(year)+"/12(E)" in dividend_yield.keys():
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/12(E)"]
    return previous_dividend_yield

# what.3년만기국채수익률 목록
# where.www.index.go.kr 에서 가져오기. 국가지표체계 웹 사이트
# return dict.treasury_3year 3년만기국채수익률 목록
# def.name.3년만기국채수익률 목록을 얻다.
# str.treasury.국고
# confirm contents : www.index.go.kr : url에서 가져온 수익률이 정확한 데이터인지 확인 후 사용해야 할 것 같음.
def get_3year_treasury():
    # url.3년만기국채수익률.데이터가 맞는지 한번 확인 필요함.
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=288401&amp;idx_cd=2884&amp;freq=Y&amp;period=1998:2016"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("tr td")

    treasury_3year = {}
    start_year = 1998

    for x in td_data:
        treasury_3year[start_year] = x.text
        start_year += 1

    #print(treasury_3year)
    return treasury_3year

if __name__ == "__main__":

    jong_mok_code = "058470"

    print("=========================================================")
    print("종목 : " + jong_mok_code)

    print("=========================================================")
    dividend_yield = get_dividend_yield(jong_mok_code)
    print("what.현금배당수익률[과거/어제]")
    print(dividend_yield)

    print("==================================================================================================================")
    estimated_dividend_yield = get_estimated_dividend_yield(jong_mok_code)
    print("what.현금배당수익률[컨센서스]")
    print(estimated_dividend_yield )

    print("==================================================================================================================")
    dividend_dict = get_financial_statements(jong_mok_code)
    print("what.현금배당수익률 목록")
    print(dividend_dict)

    print("==================================================================================================================")
    year_treasury_dict = get_3year_treasury()
    print("what.3년만기국채수익률 목록")
    print(year_treasury_dict)

    print("==================================================================================================================")
    print("what.3년 만기 국채 수익률의 일별 시세")
    print(get_current_3year_treasury())

    print("==================================================================================================================")
    print("what.4년간 수익률")
    previous_dividend_yield = get_previous_dividend_yield(jong_mok_code)
    print(previous_dividend_yield)