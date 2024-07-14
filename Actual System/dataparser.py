import pandas as pd
df = pd.read_csv("sample.csv")

# Get all domains from the dataframe
print(df["domainName"])

# Break each domain up into it's components (domain, Extension)
domain_names_clean = [i.partition(".")[0::2] for i in df["domainName"]]
print(domain_names_clean)

