import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3

TR_REQ_TIME_INTERVAL = 0.2


# QWidget, QAxBase
#     QAxWidget
# QAxBase.dynamicCall()
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
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
        self.OnReceiveRealData.connect(self._receive_real_data)

    def comm_connect(self):
        # 키움 Open API++ 접속, 명령어 CommConnect()
        # 설명 : 로그인 윈도우를 실행한다.
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    # todo. 7에러코드표 반영해야 함.
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

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    """ 주문 start """
    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print("_receive_chejan_data-")
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret
    """ 주문 end """

    """
    OpenAPI.KOA_Functions(_T("GetServerGubun"), _T(""));// 접속서버 구분을 알려준다. 1 : 모의투자 접속, 나머지 : 실서버 접속 
    """
    def get_server_gubun(self):
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        if(ret == '1'):
            print('모의투자서버_접속')
        else :
            print('실서버_접속')
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):

        print('def _receive_tr_data')
        print('     rqname : ', rqname)
        print('     trcode : ', trcode)
        print('     record_name : ', record_name)
        print('     next : ', next)
        print('     screen_no : ', screen_no)

        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
        elif rqname == "opw00001_req": # 잔고. d+2추정예수금.
            self._opw00001(rqname, trcode)
        elif rqname == "opw00018_req":
            self._opw00018(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    @staticmethod
    def change_format(data):
        strip_data = data.lstrip('-0')
        if strip_data == '' or strip_data == '.00':
            strip_data = '0'

        format_data = format(int(strip_data), ',d')
        if data.startswith('-'):
            format_data = '-' + format_data

        return format_data

    @staticmethod
    def change_format2(data):
        strip_data = data.lstrip('-0')

        if strip_data == '':
            strip_data = '0'

        if strip_data.startswith('.'):
            strip_data = '0' + strip_data

        if data.startswith('-'):
            strip_data = '-' + strip_data

        return strip_data

    def _opw00001(self, rqname, trcode):
        d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format2(d2_deposit)

    # 조회 정보 요청 : GetCommData()
    def _get_comm_data(self, trCode, recordName, index, itemName):
        """
        수신 데이터를 반환한다.
        :param strTrCode: Tran 코드
        :param strRecordName: 레코드명
        :param nIndex: 복수데이터 인덱스
        :param strItemName: 아이템명
        :return: 수신 데이터
        """
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString"
                               , trCode,recordName, index, itemName)
        return ret.strip()

    # 실시간정보 요청 : GetCommRealData()

    # 체결정보 요청 : GetChejanData()



    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

    def reset_opw00018_output(self):
        self.opw00018_output = {'single': [], 'multi': []}

    def _opw00018_test(self, rqname, trcode):
        single = self._get_repeat_cnt(trcode, "계좌평가결과")
        nulti = self._get_repeat_cnt(trcode, "계좌평가잔고개별합산")
        print("single m", single, nulti)

    def _opw00018(self, rqname, trcode):

        # single data
        total_purchase_price = self._comm_get_data(trcode, "", rqname, 0, "총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(trcode, 0, rqname, 0, "총평가손익금액")
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        self.opw00018_output['single'].append(Kiwoom.change_format2(total_purchase_price))
        self.opw00018_output['single'].append(Kiwoom.change_format2(total_eval_price))
        self.opw00018_output['single'].append(Kiwoom.change_format2(total_eval_profit_loss_price))

        print("total_earning_rate")
        print(total_earning_rate)
        total_earning_rate = Kiwoom.change_format2(total_earning_rate)
        print("total_earning_rate 2")
        print(total_earning_rate)
        if self.get_server_gubun():
            total_earning_rate = float(total_earning_rate) / 100
            total_earning_rate = str(total_earning_rate)

        self.opw00018_output['single'].append(total_earning_rate)

        self.opw00018_output['single'].append(Kiwoom.change_format2(estimated_deposit))

        print('======kdj>',total_earning_rate)
        name1 = self._comm_get_data(trcode, "", rqname, 0, "종목명")
        print('name1==>',name1)

        # multi data
        rows = self._get_repeat_cnt(trcode, rqname)
        for i in range(rows):
            name = self._comm_get_data(trcode, "", rqname, i, "종목명")
            quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
            purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
            current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
            eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
            earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")

            quantity = Kiwoom.change_format2(quantity)
            purchase_price = Kiwoom.change_format2(purchase_price)
            current_price = Kiwoom.change_format2(current_price)
            eval_profit_loss_price = Kiwoom.change_format2(eval_profit_loss_price)
            earning_rate = Kiwoom.change_format2(earning_rate)

            self.opw00018_output['multi'].append([name, quantity, purchase_price, current_price, eval_profit_loss_price,
                                                  earning_rate])

    def _receive_real_data(self, code, realType, realData):
        print("_receive_real_data")
        print(code,realType,realData)
    def set_real_reg(self):
        print("_set_real_reg")
        ret = self.dynamicCall("SetRealReg(QString, QString, QString, QString)", '0099',
                               '035900', "9001;302;10;11;25;12;13", "0")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    kiwoom.reset_opw00018_output()
    account_number = kiwoom.get_login_info("ACCNO")
    account_number = account_number.split(';')[0]

    kiwoom.set_input_value("계좌번호", account_number)
    kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")
    print(kiwoom.opw00018_output['single'])
    print(kiwoom.opw00018_output['multi'])

