#construct daily prices based on months.py
import pandas as pd
import os
os.system('cls' if os.name == 'nt' else 'clear')


df = pd.read_excel('Gas_TTF_monthly_investing.com.xlsx')
print(df)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Month'])
df.rename(columns={df.columns[1]: 'price'}, inplace=True)