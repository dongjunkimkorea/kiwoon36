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

TR_REQ_TIME_INTERVAL = 0.2


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)

        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    # 조회 정보 요청 : GetCommData()
    def _get_comm_data(self, trCode, recordName, index, itemName):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString"
                               , trCode, recordName, index, itemName)
        return ret.strip()

    # 실시간정보 요청 : GetCommRealData()

    # 체결정보 요청 : GetChejanData()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        print("_receive_tr_data : " + next)
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10059_req":
            self._opt10059(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10059(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            col0 = self._get_comm_data(trcode, "종목별투자자기관별", i, "일자")
            col1 = self._get_comm_data(trcode, "종목별투자자기관별", i, "현재가")
            col2 = self._get_comm_data(trcode, "종목별투자자기관별", i, "대비기호")
            col3 = self._get_comm_data(trcode, "종목별투자자기관별", i, "전일대비")
            col4 = self._get_comm_data(trcode, "종목별투자자기관별", i, "등락율")
            col5 = self._get_comm_data(trcode, "종목별투자자기관별", i, "누적거래대금")
            col6 = self._get_comm_data(trcode, "종목별투자자기관별", i, "개인투자자")
            col7 = self._get_comm_data(trcode, "종목별투자자기관별", i, "외국인투자자")
            col8 = self._get_comm_data(trcode, "종목별투자자기관별", i, "기관계")
            col9 = self._get_comm_data(trcode, "종목별투자자기관별", i, "금융투자")
            col10 = self._get_comm_data(trcode, "종목별투자자기관별", i, "보험")
            col11 = self._get_comm_data(trcode, "종목별투자자기관별", i, "투신")
            col12 = self._get_comm_data(trcode, "종목별투자자기관별", i, "기타금융")
            col13 = self._get_comm_data(trcode, "종목별투자자기관별", i, "은행")
            col14 = self._get_comm_data(trcode, "종목별투자자기관별", i, "연기금등")
            col15 = self._get_comm_data(trcode, "종목별투자자기관별", i, "사모펀드")
            col16 = self._get_comm_data(trcode, "종목별투자자기관별", i, "국가")
            col17 = self._get_comm_data(trcode, "종목별투자자기관별", i, "기타법인")
            col18 = self._get_comm_data(trcode, "종목별투자자기관별", i, "내외국인")

            self.s0796['일자'].append(col0)
            self.s0796['현재가'].append(int(col1))
            self.s0796['대비기호'].append(int(col2))
            self.s0796['전일대비'].append(int(col3))
            self.s0796['등락율'].append(float(col4))
            self.s0796['누적거래대금'].append(int(col5))
            self.s0796['개인투자자'].append(int(col6))
            self.s0796['외국인투자자'].append(int(col7))
            self.s0796['기관계'].append(int(col8))
            self.s0796['금융투자'].append(int(col9))
            self.s0796['보험'].append(int(col10))
            self.s0796['투신'].append(int(col11))
            self.s0796['기타금융'].append(int(col12))
            self.s0796['은행'].append(int(col13))
            self.s0796['연기금등'].append(int(col14))
            self.s0796['사모펀드'].append(int(col15))
            self.s0796['국가'].append(int(col16))
            self.s0796['기타법인'].append(int(col17))
            self.s0796['내외국인'].append(int(col18))


if __name__ == "__main__":

    dt = "20200403"
    jCode = "060250"

    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    kiwoom.s0796 = {'일자': [],
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
    kiwoom.set_input_value("일자", dt)
    kiwoom.set_input_value("종목코드", jCode)
    # kiwoom.set_input_value("종목코드", "091120")#이엠텍
    # kiwoom.set_input_value("종목코드", "105630")#한세시업
    # kiwoom.set_input_value("종목코드", "122870")#yg
    # kiwoom.set_input_value("종목코드", "091990")#셀트로온 헬스케어
    # kiwoom.set_input_value("종목코드", "068760")#셀트로운제약
    # kiwoom.set_input_value("종목코드", "008930")#한미사이언스
    # kiwoom.set_input_value("종목코드", "000270")#기아자동차
    # kiwoom.set_input_value("종목코드", "030200")#kt
    # kiwoom.set_input_value("종목코드", "066570")#LG전자
    # kiwoom.set_input_value("종목코드", "060250")#사이버결제 (기관/외국인)
    # kiwoom.set_input_value("종목코드", "035900")#jyp
    # kiwoom.set_input_value("종목코드", "015760")#한전
    # kiwoom.set_input_value("종목코드", "068270")#셀트리온

    # kiwoom.set_input_value("종목코드", "215600")#신라젠
    # kiwoom.set_input_value("종목코드", "032640")#LG유플러스
    # kiwoom.set_input_value("종목코드", "123040")#엠에스오토텍
    # kiwoom.set_input_value("종목코드", "000660")#하이닉스
    # kiwoom.set_input_value("종목코드", "140410")#메지온

    kiwoom.set_input_value("금액수량구분", "2")
    kiwoom.set_input_value("매매구분", "0")
    kiwoom.set_input_value("단위구분", "1")
    kiwoom.comm_rq_data("opt10059_req", "opt10059", 0, "0101")

    while kiwoom.remained_data == True:
        time.sleep(TR_REQ_TIME_INTERVAL)

        kiwoom.set_input_value("일자", dt)
        kiwoom.set_input_value("종목코드", jCode)
        kiwoom.set_input_value("금액수량구분", "2")
        kiwoom.set_input_value("매매구분", "0")
        kiwoom.set_input_value("단위구분", "1")
        kiwoom.comm_rq_data("opt10059_req", "opt10059", 2, "0796")

    df = pd.DataFrame(kiwoom.s0796,
                      columns=['일자', '현재가', '대비기호', '전일대비', '등락율', '누적거래대금', '개인투자자', '외국인투자자', '기관계', '금융투자', '보험',
                               '투신', '기타금융', '은행', '연기금등', '사모펀드', '국가', '기타법인', '내외국인'], index=kiwoom.s0796['일자'])

    con = sqlite3.connect("c:/db/kosdap.db")
    df.to_sql(jCode, con, if_exists='replace', index=False)
