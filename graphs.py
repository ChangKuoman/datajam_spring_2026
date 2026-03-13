import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("clean_datasets/WFH.csv")

print(df)

df2 = df.groupby(["method", "year"]).agg({"estimate": "sum"}).reset_index()
print(df2)

line_df = df2.pivot(index="year", columns="method", values="estimate")
line_df.plot(kind="line", marker="o", figsize=(10, 6))

plt.title("WFH Estimate by Method Over Time")
plt.xlabel("Year")
plt.ylabel("Estimate")
plt.legend(title="Method", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.show()