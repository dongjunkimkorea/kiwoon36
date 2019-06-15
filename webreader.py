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

# what.(과거)현금배당수익률[과거/어제.즉현재][상단]
# where.네이버.상단(WISEFn제공).기업현황.현금배당수익률
# return str.dividend_yield 조회시점의 현금배당수익률(최근 결산 수정DPS(현금)_과거 / 전일자 보통주 수정주가_어제)
# def.name.배당 수익률을 얻다.
# str.dividend_yield.배당수익률
def get_dividend_yield(code):
    url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=" + code + "&cn="
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html5lib')

    # coyp js path
    b_tag_data = soup.select("#pArea > div.wrapper-table > div > table > tbody > tr:nth-child(3) > td > dl > dt:nth-child(6) > b")

    if not b_tag_data :
        return ""

    dividend_yield = b_tag_data[0].text
    dividend_yield = dividend_yield[:-1]

    return dividend_yield

# what.(예상)현금배당수익률[컨센서스][재무제표상 컨센서스]
# where.함수에서.def get_financial_statements(code)
# return 해당년도예상수익률(컨센서스) , 제무재표에서 해당년도 예상수익률을 구한다.
# def.name.예상 배당 수익률을 얻는다.
def get_estimated_dividend_yield(code):

    estimated_dividend_yield = 0

    dividend_yield = get_financial_statements(code)
    # 해당 연도 및 이전 연도에 데이터(현금배당률 DPS)가 존재하는지 확인
    # ETF 는 데이터 없음.
    if len(dividend_yield) == 0:
        return "0"

    sorded_dividend_yield = sorted(dividend_yield.items())

    # print(sorded_dividend_yield)
    # print(sorded_dividend_yield[-1])
    # print(sorded_dividend_yield[-1][1])

    if len(sorded_dividend_yield[-1][1]) == 0 :
        estimated_dividend_yield = sorded_dividend_yield[-2][1]

        if len(estimated_dividend_yield) == 0 :
            estimated_dividend_yield = sorded_dividend_yield[-3][1]

            if len(estimated_dividend_yield) == 0 :
                estimated_dividend_yield = sorded_dividend_yield[-4][1]
    else :
        estimated_dividend_yield = sorded_dividend_yield[-1][1]

    if estimated_dividend_yield == "" :
        estimated_dividend_yield = 0

    return estimated_dividend_yield

# what.현금배당수익률 목록
# where.네이버.하단(WISEFn제공).재무제표전체TAB.현금배당수익률.row
# return dictory.dividend_dict 년도별 현금배당수익률 목록(추정치포함)
# def.name.제무재표에서 배당 수익률을 얻다.
def get_financial_statements(code):
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

    # https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930&cn=
    url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={}&cn".format(code)

    html = requests.get(url).text
    encparam = re_enc.search(html).group(1)
    encid = re_id.search(html).group(1)

    # fin_typ=0,1,2,3,4 / 주재무재표(0)
    # freq_typ=A,Y,Q / 전체,연간,분기
    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(code, encparam, encid)
    # print("===============>",url)

    headers = {"Referer": "HACK"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html5lib")
    # print(html)

    # 년도
    years = soup.select("table:nth-of-type(2) > thead > tr:nth-of-type(2) > th")

    # 현금배당수익률
    dividend = soup.select("table:nth-child(2) > tbody > tr:nth-child(31) > td")

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
    url = "http://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y"
    html = requests.get(url).text
    # print(html)

    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("body > div > table > tbody > tr:nth-child(1) > td:nth-child(2)")

    # print(td_data)
    return td_data[0].text

# what.4년간 수익률
# 직전최신3년수익률 + 현재시점컨센서스수익률1년
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
        # 결산월
        if "y/"+str(year)+"/03" in dividend_yield.keys() :
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/03"]
        if "y/"+str(year)+"/06" in dividend_yield.keys() :
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/06"]
        if "y/"+str(year)+"/09" in dividend_yield.keys() :
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/09"]
        if "y/"+str(year)+"/12" in dividend_yield.keys() :
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/12"]

        # 결산월
        if "y/"+str(year)+"/03(E)" in dividend_yield.keys():
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/03(E)"]
        if "y/"+str(year)+"/06(E)" in dividend_yield.keys():
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/06(E)"]
        if "y/"+str(year)+"/09(E)" in dividend_yield.keys():
            previous_dividend_yield[year] = dividend_yield["y/"+str(year)+"/09(E)"]
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
    # 확인했음.국가지표체계.시장금리추이.시계열조회버튼.팝업.개발자도구사용.url알아냄.pystock.3년 만기 국채 수익률 파싱 코드
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=107303&idx_cd=1073&freq=Y&period=1997:2018"

    html = requests.get(url).text
    # print(html)

    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("#tr_107303_2 > td")

    # print(td_data)

    treasury_3year = {}
    start_year = 1997

    for x in td_data:
        treasury_3year[start_year] = x.text
        start_year += 1

    #print(treasury_3year)
    return treasury_3year

if __name__ == "__main__":

    # jong_mok_code = "058470"
    jong_mok_code = "069460"

    print("=========================================================")
    print("종목 : " + jong_mok_code)

    print("==================================================================================================================")
    estimated_dividend_yield = get_estimated_dividend_yield(jong_mok_code)
    print("what.(예상) 현금배당수익률[컨센서스]")
    print(estimated_dividend_yield )

    print("=========================================================")
    dividend_yield = get_dividend_yield(jong_mok_code)
    print("what.(이전) 현금배당수익률[과거/어제]")
    print(dividend_yield)

    print("==================================================================================================================")
    print("what.(최근4년) =  현금배당수익률(최근3년) + 현금배당수익룰(컨센서스)")
    previous_dividend_yield = get_previous_dividend_yield(jong_mok_code)
    print(previous_dividend_yield)

    print("==================================================================================================================")
    dividend_dict = get_financial_statements(jong_mok_code)
    print("what.(과거) 현금배당수익률 목록")
    print(dividend_dict)

    print("")
    print("")
    print("==================================================================================================================")
    print("Infomation")
    print("==================================================================================================================")
    year_treasury_dict = get_3year_treasury()
    print("what.3년만기국채수익률 목록")
    print(year_treasury_dict)

    print("==================================================================================================================")
    print("what.3년 만기 국채 수익률의 일별 시세")
    print(get_current_3year_treasury())