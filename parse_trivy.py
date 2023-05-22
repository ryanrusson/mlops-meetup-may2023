import pandas as pd
import json
from tabulate import tabulate

"""
Desired Output

Vuln Type | Severity | Count
----------------------------
OS        | HIGH     | 2
OS        | MED      | 100
LIBRARY   | MED      | 1

"""


def grouping(df):
    if df.empty:
        return pd.DataFrame(columns=["Vuln Type", "Severity", "Count"])
    else:
        return pd.DataFrame(
            {"Count": df.groupby(["Vuln Type", "Severity"])["Severity"].count()}
        ).reset_index()


with open(".cache/results.json", "r") as f:
    data = json.loads(f.read())

df_01 = pd.DataFrame(data["Results"][0].get("Vulnerabilities"))
df_01["Vuln Type"] = data["Results"][0].get("Class").upper()

try: 
    df_02 = pd.DataFrame(data["Results"][1].get("Vulnerabilities"))
    df_02["Vuln Type"] = data["Results"][1].get("Class").upper()
    df = pd.concat([df_01, df_02], axis=0)

except IndexError:
    df = df_01

summary = grouping(df)
print()
print(tabulate(summary, headers=["VULN TYPE", "SEVERITY", "COUNT"], showindex=False))
print()
