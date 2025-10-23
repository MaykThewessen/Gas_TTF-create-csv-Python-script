# combine all daily prices into one file and interpolate into hourly values

import pandas as pd
import os
os.system('cls' if os.name == 'nt' else 'clear')

df_monthly = pd.read_csv('Gas_20180116-20250916_investing_monthly.csv')
df_monthly['Date'] = pd.to_datetime(df_monthly['Date'], utc=True).dt.tz_convert('Europe/Amsterdam')
print(f'\ndf_monthly: \n{df_monthly}')


df_daily = pd.read_csv('Gas_20210104-2025106_ICE_andreas_daily.csv')
df_daily['Date'] = pd.to_datetime(df_daily['Date'], utc=True).dt.tz_convert('Europe/Amsterdam')
print(f'\ndf_daily: \n{df_daily}')


# Delete all rows of df_monthly after the beginning date of df_daily
start_daily = df_daily['Date'].min()
df_monthly = df_monthly[df_monthly['Date'] < start_daily]
print(f'\ndf_monthly after deletion: \n{df_monthly}')


start_date = df_monthly['Date'].min().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
end_date = df_daily['Date'].max().replace(hour=23, minute=0, second=0, microsecond=0)


date_range = pd.date_range(start=start_date, end=end_date, freq='h', tz='Europe/Amsterdam')
print(f'\ndate_range: \n{date_range}')


df_all = pd.concat([df_monthly, df_daily], ignore_index=True)
df_all = df_all.sort_values('Date').reset_index(drop=True)

# Reindex df_all to hourly values and interpolate prices
df_all = df_all.set_index('Date').reindex(date_range)
# Interpolate and also allow extrapolation (fillna with method 'ffill'/'bfill' if needed)
df_all['price'] = df_all['price'].interpolate(method='time', limit_direction='both')

df_all = df_all.reset_index().rename(columns={'index': 'Date'})
df_all['price'] = df_all['price'].round(2)
print(f'\ndf_all: \n{df_all}')


#%% plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(df_all['Date'], df_all['price'], label='Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Price over Time')
plt.legend()
plt.ylabel('Gas price TTF €/MWh')
plt.grid(True)
plt.savefig('ttf_gas_price_timeseries.pdf')
plt.show()
plt.close()

#%% Save to csv
df_all.to_csv('Gas_TTF_NL_hourly_interpolated_201801010000_202510072300.csv', index=False)


