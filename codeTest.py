# import plotly.graph_objects as go
# from datetime import datetime
#
# open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
# high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
# low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
# close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
# dates = [datetime(year=2013, month=10, day=10),
#          datetime(year=2013, month=11, day=10),
#          datetime(year=2013, month=12, day=10),
#          datetime(year=2014, month=1, day=10),
#          datetime(year=2014, month=2, day=10)]
#
# fig = go.Figure(data=[go.Candlestick(x=dates,
#                        open=open_data, high=high_data,
#                        low=low_data, close=close_data)])
#
# fig.update_layout(xaxis_rangeslider_visible=False)
#
# print(type(fig))
# fig.show()a/

import plotly.offline as po
import plotly.graph_objs as go

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore, QtWidgets
import sys
from datetime import datetime

def show_qt(fig):
    raw_html = '<html><head><meta charset="utf-8" />'
    raw_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
    raw_html += '<body>'
    raw_html += po.plot(fig, include_plotlyjs=False, output_type='div')
    raw_html += '</body></html>'

    fig_view = QWebEngineView()
    # setHtml has a 2MB size limit, need to switch to setUrl on tmp file
    # for large figures.
    fig_view.setHtml(raw_html)
    fig_view.show()
    fig_view.raise_()
    return fig_view


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
    high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
    low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
    close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
    dates = [datetime(year=2013, month=10, day=10),
             datetime(year=2013, month=11, day=10),
             datetime(year=2013, month=12, day=10),
             datetime(year=2014, month=1, day=10),
             datetime(year=2014, month=2, day=10)]

    fig = go.Figure(data=[go.Candlestick(x=dates,
                           open=open_data, high=high_data,
                           low=low_data, close=close_data)])

    fig.update_layout(xaxis_rangeslider_visible=False)


    fig_view = show_qt(fig)
    sys.exit(app.exec_())
