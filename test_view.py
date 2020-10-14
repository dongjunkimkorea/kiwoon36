import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

idx = pd.date_range('2000-01-01', '2018-01-01')
df = pd.DataFrame({'x':np.cumsum(np.random.normal(0, 1, len(idx))*10)}, 
                  index = idx)
print(df.head(10))
plt.figure(figsize=(30, 15))
plt.plot(df.index, df['x'])
plt.plot(df.resample('W').mean(), label='Week')
plt.plot(df.resample('M').mean(), label='Month')
plt.plot(df.rolling(180).mean(), label='180D')
plt.plot(df.resample('A').mean(), label='annual')
plt.legend()

plt.show()