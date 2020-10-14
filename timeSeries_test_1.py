import numpy as np
import pandas as pd

# DatetiemIndex
dates = pd.date_range('2020-01-01', periods=48, freq='M')

# additive model: trend + cycle + seasonality + irregular factor

timestamp = np.arange(len(dates))

trend_factor = timestamp*1.1
cycle_factor = 10*np.sin(np.linspace(0, 3.14*2, 48))
seasonal_factor = 7*np.sin(np.linspace(0, 3.14*8, 48))

np.random.seed(2004)
irregular_factor = 2*np.random.randn(len(dates))

df = pd.DataFrame({'timeseries': trend_factor + cycle_factor + seasonal_factor + irregular_factor,

                   'trend': trend_factor,

                   'cycle': cycle_factor,

                   'seasonal': seasonal_factor,

                   'irregular': irregular_factor},

                   index=dates)

# Time series plot
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12, 8

df.plot()

plt.ylim(-12, 55)

plt.show()

#(1) Python을 이용한 시계열 분해 (Time series decomposition using Python)
#출처: https://rfriend.tistory.com/510?category=675919 [R, Python 분석과 프로그래밍의 친구 (by R Friend)]
from statsmodels.tsa.seasonal import seasonal_decompose

ts = df.timeseries
result = seasonal_decompose(ts, model='additive')

plt.rcParams['figure.figsize'] = [12, 8]

result.plot()

plt.show()

#------------------------------------------------------------
# ground truth & timeseries decompostion all together

# -- observed data

plt.figure(figsize=(12, 12))
plt.subplot(4,1, 1)
result.observed.plot()
#df.timeseries.plot()
plt.grid(True)

plt.ylabel('Observed', fontsize=14)



# -- trend & cycle factor

plt.subplot(4, 1, 2)
result.trend.plot()        # from timeseries decomposition
df.trend.plot()     # groud truth
plt.grid(True)

plt.ylabel('Trend', fontsize=14)



# -- seasonal factor

plt.subplot(4, 1, 3)
result.seasonal.plot()  # from timeseries decomposition
df.seasonal.plot()        # groud truth
plt.grid(True)

plt.ylabel('Seasonality', fontsize=14)



# -- irregular factor (noise)

plt.subplot(4, 1, 4)

result.resid.plot()    # from timeseries decomposition
df.irregular.plot()    # groud truth
plt.grid(True)

plt.ylabel('Residual', fontsize=14)

plt.show()