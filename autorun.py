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
pass_ctrl.type_keys("")

cert_ctrl = dlg.Edit3
cert_ctrl.set_focus()
cert_ctrl.type_keys('')

btn_ctrl = dlg.Button0
btn_ctrl.click()

time.sleep(20)
os.system("taskkill /im nkmini.exe")
# 번개 3 의 옵션 중에 종료 후 파업 닫기 설정 있음.