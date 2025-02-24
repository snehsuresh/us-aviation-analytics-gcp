import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS

# Load your cleaned and merged data
df = pd.read_csv("data/processed/bigquery_output/did_table.csv")

# Create interaction term for DiD
df["DID"] = df["ULCC_TREATED"] * df["POST_ENTRY"]
df["log_passengers"] = np.log(df["DB1B_PASSENGERS"] + 1)

# Convert YEAR + QUARTER into a datetime for time index
df["time_index"] = pd.to_datetime(
    df["YEAR"].astype(str) + "-" + (df["QUARTER"] * 3).astype(str) + "-01"
)

# Set panel index: (entity = ROUTE_KEY, time = time_index)
df = df.set_index(["ROUTE_KEY", "time_index"])

from linearmodels.panel import PanelOLS

model = PanelOLS.from_formula(
    formula="log_passengers ~ DID + EntityEffects + TimeEffects",
    data=df,
    drop_absorbed=True,
    check_rank=False,
).fit(cov_type="robust")

print(model.summary)

if "DID" in model.params:
    print(f"\n✅ DiD Estimate (Treatment x Post): {model.params['DID']:.4f}")
else:
    print(
        "\n⚠️ DiD term was absorbed by fixed effects. Consider simplifying or re-specifying the model."
    )
