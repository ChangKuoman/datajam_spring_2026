import pandas as pd
import os

def process_bart_excel(file_path, year, month):
    all_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
    dfs = []
    
    for sheet_name, df_raw in all_sheets.items():
        mask = df_raw.apply(lambda row: row.astype(str).str.strip().eq('RM').any(), axis=1)
        
        if not mask.any():
            continue
            
        header_idx = mask.idxmax()
        
        df = df_raw.iloc[header_idx:].copy()
        df.columns = [str(c).strip() for c in df.iloc[0]]
        df = df[1:].reset_index(drop=True)
        
        cols = df.columns.tolist()
        df.rename(columns={cols[0]: 'Exit_Station'}, inplace=True)

        valid_cols = [
            c for c in df.columns 
            if c == 'Exit_Station' or (c.lower() != 'nan' and c != 'Entries')
        ]
        df = df[valid_cols]

        df_long = df.melt(id_vars=['Exit_Station'], var_name='Entry_Station', value_name='Trip_Count')
        
        df_long['Trip_Count'] = pd.to_numeric(df_long['Trip_Count'], errors='coerce').fillna(0)
        
        forbidden = ['Station', 'Entries', 'Total', 'Exits', 'nan']
        df_long = df_long[~df_long['Exit_Station'].isin(forbidden)]
        df_long = df_long[~df_long['Entry_Station'].isin(forbidden)]
        
        df_long['Day_Type'] = sheet_name
        df_long['Source'] = 'BART'
        df_long['Year'] = year  
        df_long['Month'] = month
        
        if not df_long.empty:
            dfs.append(df_long)
            
    return dfs

all_dfs = []

for year in [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]:
    for month in [f'{m:02d}' for m in range(1, 13)]:
        bart_path = f'datasets/bart/ridership_{year}/Ridership_{year}{month}.xlsx'
        if os.path.exists(bart_path):
            print(f"Processing: {year}-{month}")
            all_dfs.extend(process_bart_excel(bart_path, year, month))

if all_dfs:
    master_df = pd.concat(all_dfs, ignore_index=True)
    master_df = master_df[master_df['Exit_Station'] != 'Entries']
    master_df = master_df[master_df['Exit_Station'] != 'Grand Total']
    master_df = master_df.dropna(subset=['Exit_Station'])
    master_df.to_csv('all_bart_data.csv', index=False)
    print("Success! File saved as all_bart_data.csv")
else:
    print("No data was collected. Check if station codes (RM) match your files.")