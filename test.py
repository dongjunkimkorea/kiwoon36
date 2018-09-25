from pandas import Series, DataFrame
import sqlite3

daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
           'high':  [12100, 11800, 11200, 11100, 11150],
           'low' :  [11600, 11050, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

# daeshin_day = DataFrame(daeshin)
# print(daeshin_day)
#
# daeshin_day = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'])
# print(daeshin_day)

date = ['16.02.29', '16.02.26', '16.02.25', '16.02.24', '16.02.23']
daeshin_day = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'], index=date)
print(daeshin_day)

# daeshin_day = daeshin_day.sort_values(by=['index'])
# print(daeshin_day)

con = sqlite3.connect("c:/db/kosdap.db")
daeshin_day.to_sql('daeshin_day', con, if_exists='replace')

