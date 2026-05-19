import pandas as pd

df = pd.read_csv("data/saudi_documents.csv")

print(df.head(20))
print(df.shape)
print(df[df["excel_url"].notna()].head(10))