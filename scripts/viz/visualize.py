import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the same dataset you used
df = pd.read_csv("data/processed/bigquery_output/did_table.csv")

# Prepare variables
df["log_passengers"] = np.log(df["DB1B_PASSENGERS"] + 1)
df["log_fare"] = np.log(df["MARKET_FARE"] + 1)
df["DID"] = df["ULCC_TREATED"] * df["POST_ENTRY"]
df["time_index"] = pd.to_datetime(
    df["YEAR"].astype(str) + "-" + (df["QUARTER"] * 3).astype(str) + "-01"
)

# ==== 1. Fare Elasticity Scatter Plot ====
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x="log_fare",
    y="log_passengers",
    data=df.sample(10000, random_state=42),  # sample for performance
    alpha=0.3,
)
sns.regplot(
    x="log_fare",
    y="log_passengers",
    data=df,
    scatter=False,
    color="red",
    label="Fitted Line",
)
plt.figure(figsize=(10, 6))
plt.hexbin(df["log_fare"], df["log_passengers"], gridsize=50, cmap="Blues", mincnt=5)
plt.colorbar(label="Frequency")
plt.title("Fare Elasticity: log(Fare) vs log(Passengers)")
plt.xlabel("log(Fare)")
plt.ylabel("log(Passengers)")
plt.grid(True)
plt.tight_layout()
plt.savefig("fare_elasticity_plot.png")


# ==== 2. DiD Trend Plot (Treated vs Control over time) ====
# Compute group means by treated + time
avg_by_group = (
    df.groupby(["time_index", "ULCC_TREATED"])["DB1B_PASSENGERS"].mean().reset_index()
)

plt.figure(figsize=(12, 6))
sns.lineplot(x="time_index", y="DB1B_PASSENGERS", hue="ULCC_TREATED", data=avg_by_group)
plt.title("Passenger Demand Over Time (Treated vs Control Routes)")
plt.xlabel("Quarter")
plt.ylabel("Average Passengers")
plt.legend(title="ULCC Treated", labels=["Control (0)", "Treated (1)"])
plt.grid(True)
plt.tight_layout()
plt.savefig("did_treatment_trend.png")
plt.show()
