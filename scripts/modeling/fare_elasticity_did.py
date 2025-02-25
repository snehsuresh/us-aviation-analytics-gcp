# modeling/fare_elasticity_did.py

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS

# 📥 1. Load Data
df = pd.read_csv("data/processed/bigquery_output/did_table.csv")

# 🧼 2. Basic Cleaning + Derived Columns
df["DID"] = df["ULCC_TREATED"] * df["POST_ENTRY"]
df["log_passengers"] = np.log(df["DB1B_PASSENGERS"] + 1)
df["log_fare"] = np.log(df["MARKET_FARE"] + 1)

# ⏱️ 3. Create time index (date-like for PanelOLS)
df["time_index"] = pd.to_datetime(
    df["YEAR"].astype(str) + "-" + (df["QUARTER"] * 3).astype(str) + "-01"
)

# 🧱 4. Set panel index (Entity = ROUTE_KEY, Time = time_index)
df = df.set_index(["ROUTE_KEY", "time_index"])

# ✅ 5. Run PanelOLS with Route & Time Fixed Effects
model = PanelOLS.from_formula(
    formula="log_passengers ~ log_fare + DID + EntityEffects + TimeEffects",
    data=df,
    drop_absorbed=True,
    check_rank=False,
).fit(cov_type="robust")

# 📊 6. Output Results
print("📊 Fare Elasticity with DiD (PanelOLS)")
print(model.summary)

# 📈 7. Interpret Coefficients
if "log_fare" in model.params:
    elasticity = model.params["log_fare"]
    print(
        f"\n✅ Fare Elasticity: {elasticity:.4f} → 1% fare drop leads to ~{abs(elasticity):.2f}% change in demand"
    )
else:
    print("\n⚠️ Fare variable was absorbed or missing.")

if "DID" in model.params:
    did_effect = model.params["DID"]
    percent_increase = (np.exp(did_effect) - 1) * 100
    print(
        f"✅ DiD Effect: {did_effect:.4f} → ~{percent_increase:.2f}% demand change after ULCC entry"
    )
else:
    print("\n⚠️ DID variable was absorbed or missing.")
