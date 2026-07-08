import pandas as pd

df = pd.read_parquet("fundamentals_20260705.parquet")
print(df.head(10))
