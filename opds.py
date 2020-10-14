import numpy as np
import pandas as pd

#Time series data structures
#opsd_daily = pd.read_csv('opsd_germany_daily.csv')
#opsd_daily = opsd_daily.set_index('Date')
opsd_daily = pd.read_csv('opsd_germany_daily.csv', index_col=0, parse_dates=True)

#opsd_daily.shape
#
opsd_daily.head(3)
#opsd_daily.tail(3)

# Add columns with year, month, and weekday name
opsd_daily['Year'] = opsd_daily.index.year
opsd_daily['Month'] = opsd_daily.index.month
#opsd_daily['Weekday Name'] = opsd_daily.index.Weekday_name
# Display a random sampling of 5 rows
#opsd_daily.sample(5, random_state=0)

#Time-based indexing
#opsd_daily.loc['2017-08-10']
#opsd_daily.loc['2014-01-20':'2014-01-22']
#opsd_daily.loc['2012-02']


import matplotlib.pyplot as plt
# Display figures inline in Jupyter notebook
import seaborn as sns
# Use seaborn style defaults and set the default figure size
#sns.set(rc={'figure.figsize':(11, 4)})
#sns.set(rc={'figure.figsize':(11, 8)})
sns.set(rc={'figure.figsize':(40, 15)})

#opsd_daily['Consumption'].plot(linewidth=0.5);

#cols_plot = [['Consumption', 'Solar', 'Wind']]
#axes = opsd_daily[cols_plot].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9), subplots=True)
#for ax in axes:
#    ax.set_ylabel('Daily Totals (GWh)')
    
#ax = opsd_daily.loc['2017', 'Consumption'].plot()
#ax.set_ylabel('Daily Consumption (GWh)');

#ax = opsd_daily.loc['2017-01':'2017-02', 'Consumption'].plot(marker='o', linestyle='-')
#ax.set_ylabel('Daily Consumption (GWh)');

import matplotlib.dates as mdates
#fig, ax = plt.subplots()
#ax.plot(opsd_daily.loc['2017-01':'2017-02', 'Consumption'], marker='o', linestyle='-')
#ax.set_ylabel('Daily Consumption (GWh)')
#ax.set_title('Jan-Feb 2017 Electricity Consumption')
## Set x-axis major ticks to weekly interval, on Mondays
#ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY))
## Format x-tick labels as 3-letter month name and day number
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'));

#fig, axes = plt.subplots(3, 1, figsize=(22, 20), sharex=True)
#for name, ax in zip(['Consumption', 'Solar', 'Wind'], axes):
#    sns.boxplot(data=opsd_daily, x='Month', y=name, ax=ax)
#    ax.set_ylabel('GWh')
#    ax.set_title(name)
## Remove the automatic x-axis label from all but the bottom subplot
#if ax != axes[-1]:
#    ax.set_xlabel('')
    
#sns.boxplot(data=opsd_daily, x='Weekday Name', y='Consumption');

## Specify the data columns we want to include (i.e. exclude Year, Month, Weekday Name)
data_columns = ['Consumption', 'Wind', 'Solar', 'Wind+Solar']
## Resample to weekly frequency, aggregating with mean
opsd_weekly_mean = opsd_daily[data_columns].resample('W').mean()
#opsd_weekly_mean.head(3)
## Start and end of the date range to extract
#start, end = '2017-01', '2017-06'
## Plot daily and weekly resampled time series together
#fig, ax = plt.subplots()
#ax.plot(opsd_daily.loc[start:end, 'Solar'], marker='.', linestyle='-', linewidth=0.5, label='Daily')
#ax.plot(opsd_weekly_mean.loc[start:end, 'Solar'],marker='o', markersize=8, linestyle='-', label='Weekly Mean Resample')
#ax.set_ylabel('Solar Production (GWh)')
#ax.legend();

#import matplotlib.dates as mdates
#data_columns = ['Consumption', 'Wind', 'Solar', 'Wind+Solar']
#opsd_monthly = opsd_daily[data_columns].resample('M').sum(min_count=29)
#opsd_monthly.head(3)
#fig, ax = plt.subplots()
#ax.plot(opsd_monthly['Consumption'], color='black', label='Consumption')
#ax.plot(opsd_monthly['Wind'], color='red', label='Wind')
#ax.plot(opsd_monthly['Solar'], color='blue', label='Solar')
#opsd_monthly[['Wind', 'Solar']].plot.area(ax=ax, linewidth=0)
#ax.xaxis.set_major_locator(mdates.YearLocator())
#ax.legend()
#ax.set_ylabel('Monthly Total (GWh)');


## Compute the annual sums, setting the value to NaN for any year which has
## fewer than 360 days of data
#opsd_annual = opsd_daily[data_columns].resample('A').sum(min_count=360)
#print(id(opsd_annual))
## The default index of the resampled DataFrame is the last day of each year,
## ('2006-12-31', '2007-12-31', etc.) so to make life easier, set the index
## to the year component
#opsd_annual = opsd_annual.set_index(opsd_annual.index.year)
#opsd_annual.index.name = 'Year'
#print(id(opsd_annual))
## Compute the ratio of Wind+Solar to Consumption
#opsd_annual['Wind+Solar/Consumption'] = opsd_annual['Wind+Solar'] / opsd_annual['Consumption'] * 100
#opsd_annual.tail(3)
## Plot from 2012 onwards, because there is no solar production data in earlier years
#ax = opsd_annual.loc[2012:, 'Wind+Solar/Consumption'].plot.bar(color='C0')
#ax.set_ylabel('Fraction')
#ax.set_ylim(0, 0.3*100)
#ax.set_title('Wind + Solar Share of Annual Electricity Consumption')
#plt.xticks(rotation=0);

opsd_7d = opsd_daily[data_columns].rolling(7, center=True).mean()
#opsd_7d.head(10)
## Start and end of the date range to extract
#start, end = '2017-01', '2017-06'
## Plot daily, weekly resampled, and 7-day rolling mean time series together
#fig, ax = plt.subplots()
#ax.plot(opsd_daily.loc[start:end, 'Solar'], marker='.', linestyle='-', linewidth=0.5, label='Daily')
#ax.plot(opsd_weekly_mean.loc[start:end, 'Solar'], marker='o', markersize=8, linestyle='-', label='Weekly Mean Resample')
#ax.plot(opsd_7d.loc[start:end, 'Solar'], marker='.', linestyle='-', label='7-d Rolling Mean')
#ax.set_ylabel('Solar Production (GWh)')
#ax.legend();

# The min_periods=360 argument accounts for a few isolated missing days in the
# wind and solar production time series
opsd_365d = opsd_daily[data_columns].rolling(window=365, center=True, min_periods=360).mean()
## Plot daily, 7-day rolling mean, and 365-day rolling mean time series
#fig, ax = plt.subplots()
#ax.plot(opsd_daily['Consumption'], marker='.', markersize=2, color='0.6',linestyle='None', label='Daily')
#ax.plot(opsd_7d['Consumption'], linewidth=2, label='7-d Rolling Mean')
#ax.plot(opsd_365d['Consumption'], color='0.2', linewidth=3, label='Trend (365-d Rolling Mean)')
## Set x-ticks to yearly interval and add legend and labels
#ax.xaxis.set_major_locator(mdates.YearLocator())
#ax.legend()
#ax.set_xlabel('Year')
#ax.set_ylabel('Consumption (GWh)')
#ax.set_title('Trends in Electricity Consumption');

## Plot 365-day rolling mean time series of wind and solar power
#fig, ax = plt.subplots()
#for nm in ['Wind', 'Solar', 'Wind+Solar']:
#    ax.plot(opsd_365d[nm], label=nm)
#    # Set x-ticks to yearly interval, adjust y-axis limits, add legend and labels
#    ax.xaxis.set_major_locator(mdates.YearLocator())
#    ax.set_ylim(0, 400)
#    ax.legend()
#    ax.set_ylabel('Production (GWh)')
#    ax.set_title('Trends in Electricity Production (365-d Rolling Means)');


# apply a frequency to the data
goog = goog.asfreq('D', method='pad')

goog.plot(ax=ax[0])
goog.shift(900).plot(ax=ax[1])
goog.tshift(900).plot(ax=ax[2])

# legends and annotations
local_max = pd.to_datetime('2007-11-05')
offset = pd.Timedelta(900, 'D')

ax[0].legend(['input'], loc=2)
ax[0].get_xticklabels()[2].set(weight='heavy', color='red')
ax[0].axvline(local_max, alpha=0.3, color='red')

ax[1].legend(['shift(900)'], loc=2)
ax[1].get_xticklabels()[2].set(weight='heavy', color='red')
ax[1].axvline(local_max + offset, alpha=0.3, color='red')

ax[2].legend(['tshift(900)'], loc=2)
ax[2].get_xticklabels()[1].set(weight='heavy', color='red')
ax[2].axvline(local_max + offset, alpha=0.3, color='red');
