import pandas as pd

df = pd.read_csv('all_bart_data.csv')

df['Route'] = df['Entry_Station'] + " -> " + df['Exit_Station']

monthly_summary = df.groupby(['Year', 'Month', 'Day_Type', 'Entry_Station']).agg(
    Total_Records=('Trip_Count', 'count'),
    Unique_Station_Pairs=('Route', 'nunique'), 
    Total_Ridership=('Trip_Count', 'sum')
).reset_index()
print("BART Ridership Summary by Month:")
print(monthly_summary)

monthly_summary.to_csv('bart_monthly_summary.csv', index=False)