#Gas_TTF_NL_import.py

import pandas as pd

import os
os.system('cls' if os.name == 'nt' else 'clear')



df = pd.read_excel('Gas_TTF_Day-Ahead_daily_20210110-20251006.xlsx')
print(df)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize('Europe/Amsterdam', ambiguous='NaT', nonexistent='NaT')
df.rename(columns={df.columns[1]: 'price'}, inplace=True)

# prices of Gas are Day-Ahead, so we need to add 36 hours to the date:
df['Date'] = df['Date'] + pd.to_timedelta(36, unit='h')


# Print start and end dates
print(df.head(12))



# Create df_all_days with all dates filled and missing dates with last known price
# First, create a complete date range from min to max date
date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='D')
print(f"\nComplete date range:")
print(f"Total days in range: {len(date_range)}")

df_all_days = pd.DataFrame({'Date': date_range})

# Merge with original data
df_all_days = df_all_days.merge(df, on='Date', how='left')

# Forward fill missing prices with last known value
df_all_days['price'] = df_all_days['price'].ffill()

df_all_days['price'] = df_all_days['price'].round(2)


print("\nDataFrame with all days filled:")
print(df_all_days.head(12))
print(df_all_days.tail(12))
print(f"\nOriginal df shape: {df.shape}")
print(f"df_all_days shape: {df_all_days.shape}")
print(f"Missing dates filled: {df_all_days.shape[0] - df.shape[0]}")



df_all_days.to_csv('Gas_20210104-2025106_ICE_andreas_daily.csv', index=False)




