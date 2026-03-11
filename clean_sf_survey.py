import pandas as pd

path = "datasets/sf_survey/TDS_2019_Data.xlsx"
path2 = "datasets/sf_survey/TDS_2021_Data.xlsx"

tab = "Data"

# Read 2019 data
df_2019 = pd.read_excel(path, sheet_name=tab)
df_2019['year'] = 2019
df_2019.to_csv("datasets/sf_survey/TDS_2019_Data.csv", index=False)

# Read 2021 data
df_2021 = pd.read_excel(path2, sheet_name=tab)
df_2021['year'] = 2021
df_2021.to_csv("datasets/sf_survey/TDS_2021_Data.csv", index=False)

# Join both datasets
df_combined = pd.concat([df_2019, df_2021], ignore_index=True)
df_combined.to_csv("datasets/sf_survey/TDS_Combined_Data.csv", index=False)

print("Files converted to CSV successfully")
print(f"Combined dataset shape: {df_combined.shape}")