import pandas as pd

df = pd.read_csv(r'C:\Users\16466\Desktop\cis4400Homework\Data Sources\bedBugData.csv')

#Making date/time more granular
date_columns = ['filing_date', 'filing_period_start_date', 'filling_period_end_date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col]).dt.date

#Y/Q/M/D
df['Year'] = pd.to_datetime(df['filing_date']).dt.year
df['Quarter'] = pd.to_datetime(df['filing_date']).dt.quarter
df['Month'] = pd.to_datetime(df['filing_date']).dt.month
df['Day'] = pd.to_datetime(df['filing_date']).dt.day

# Removing rows with null
df.dropna(inplace=True)


# Removing duplicate rows
df.drop_duplicates(inplace=True)

# Seasons!
df['Season'] = df['Month'].apply(lambda x: 'Winter' if x in (12, 1, 2) 
                                 else 'Spring' if x in (3, 4, 5) 
                                 else 'Summer' if x in (6, 7, 8) 
                                 else 'Fall')

# Weekday/Weekend 
df['Weekday'] = pd.to_datetime(df['filing_date']).dt.weekday
df['Is_Weekend'] = df['Weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

#AVG infestion
df['percent of units infested'] = (df['infested_dwelling_unit_count']/ df['of_dwelling_units']) * 100

#Business problem -->How Often bed-bug infestions happen per borough


df.to_csv(r'C:\Users\16466\Desktop\cis4400Homework\Data Sources\transformed_bedBugData.csv', index=False)
