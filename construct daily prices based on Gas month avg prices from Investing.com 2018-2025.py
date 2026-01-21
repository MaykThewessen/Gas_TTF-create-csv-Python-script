#construct daily prices based on months.py
import pandas as pd
import os
os.system('cls' if os.name == 'nt' else 'clear')

df = pd.read_excel('Gas_TTF_monthly_investing.com.xlsx')
print(df)


# Convert Date column to Datetime
df['Month'] = pd.to_datetime(df['Month'])
df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
df.rename(columns={df.columns[1]: 'price'}, inplace=True)

# Shift Dates to middle of each month (15th day) and set to Amsterdam timezone
df['Date'] = df['Date'].dt.to_period('M').dt.to_timestamp() + pd.DateOffset(days=15) + pd.to_timedelta(12, unit='h')
df['Date'] = df['Date'].dt.tz_localize('Europe/Amsterdam')

print(df.head(12))
print(df.tail(12))

df.to_csv('Gas_20180116-20250916_investing_monthly.csv', index=False)
