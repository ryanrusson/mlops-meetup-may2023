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

df_os = pd.DataFrame(data["Results"][0].get("Vulnerabilities"))
df_os["Vuln Type"] = "OS"

try:
    df_lib = pd.DataFrame(data["Results"][1].get("Vulnerabilities"))
except IndexError:
    df_lib = pd.DataFrame(data["Results"][0].get("Vulnerabilities"))

df_lib["Vuln Type"] = "LIBRARY"
df = pd.concat([df_os, df_lib], axis=0)
summary = grouping(df)
print()
print(tabulate(summary, headers=["VULN TYPE", "SEVERITY", "COUNT"], showindex=False))
print()
