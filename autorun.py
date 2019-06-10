from pywinauto import application
from pywinauto import timings
import time
import os


app = application.Application()
app.start("C:/KiwoomFlash3/bin/nkministarter.exe")

title = "번개3 Login"
dlg = timings.wait_until_passes(20, 0.5, lambda: app.connect(title=title)).Dialog

pass_ctrl = dlg.Edit2
time.sleep(10)
pass_ctrl.set_focus()
pass_ctrl.type_keys("xxx") # 계좌비밀번호

cert_ctrl = dlg.Edit3
cert_ctrl.set_focus()
cert_ctrl.type_keys('yyyy!') # 인증서비밀번호

btn_ctrl = dlg.Button0
btn_ctrl.click()

time.sleep(20)
os.system("taskkill /im nkmini.exe")
# 번개 3 의 옵션 중에 종료 후 파업 닫기 설정 있음.
# 프로그램의 목적
# 키움 Open API++ 버전 업데이트 처리.
# 윈도스케줄러에 의해서 autorun.py가 실행되면 번개3를 실행 하며, 실행과 동시에  Open API++의 버전이 업데이트 처리 된다.
# 이후 몇초간 번개3가 실행된 후에 종료 되므로써, Open API++f가 version update 된다.