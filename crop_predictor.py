"""
Crop Condition Predictor
=========================
Python port of the crop-predictor.html tool.

Trains a DecisionTreeClassifier on 20 field records (Temperature, Humidity,
Rainfall -> Condition) and lets you predict whether a new set of readings
will produce a "Good" or "Poor" crop condition. Also reproduces the
Temperature vs. Rainfall scatter chart using matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_text

# ----------------------------------------------------------------------
# 1. Dataset (same 20 records as the HTML page)
# ----------------------------------------------------------------------
data = [
    {"t": 20, "h": 60, "r": 80,  "c": "Poor"},
    {"t": 22, "h": 65, "r": 90,  "c": "Good"},
    {"t": 25, "h": 70, "r": 100, "c": "Good"},
    {"t": 28, "h": 75, "r": 120, "c": "Good"},
    {"t": 30, "h": 80, "r": 150, "c": "Good"},
    {"t": 32, "h": 85, "r": 160, "c": "Good"},
    {"t": 18, "h": 55, "r": 50,  "c": "Poor"},
    {"t": 24, "h": 68, "r": 95,  "c": "Good"},
    {"t": 27, "h": 72, "r": 110, "c": "Good"},
    {"t": 35, "h": 40, "r": 30,  "c": "Poor"},
    {"t": 21, "h": 62, "r": 85,  "c": "Good"},
    {"t": 26, "h": 74, "r": 105, "c": "Good"},
    {"t": 29, "h": 78, "r": 130, "c": "Good"},
    {"t": 31, "h": 45, "r": 40,  "c": "Poor"},
    {"t": 23, "h": 66, "r": 88,  "c": "Good"},
    {"t": 19, "h": 58, "r": 60,  "c": "Poor"},
    {"t": 33, "h": 42, "r": 35,  "c": "Poor"},
    {"t": 25, "h": 71, "r": 115, "c": "Good"},
    {"t": 28, "h": 76, "r": 125, "c": "Good"},
    {"t": 22, "h": 64, "r": 82,  "c": "Good"},
]

df = pd.DataFrame(data)
df.columns = ["Temperature", "Humidity", "Rainfall", "Condition"]

# ----------------------------------------------------------------------
# 2. Train the decision tree
# ----------------------------------------------------------------------
X = df[["Temperature", "Humidity", "Rainfall"]]
y = df["Condition"]

model = DecisionTreeClassifier(random_state=0)
model.fit(X, y)

print("Trained decision tree rules:\n")
print(export_text(model, feature_names=list(X.columns)))
# Note: with this dataset the tree learns that Humidity alone separates the
# classes cleanly (every "Poor" record has Humidity <= 61, every "Good"
# record has Humidity > 61) -- same rule the HTML version hardcodes.


# ----------------------------------------------------------------------
# 3. Predict function
# ----------------------------------------------------------------------
def predict_condition(temp: float, hum: float, rain: float) -> str:
    """Predict crop condition ('Good' or 'Poor') from the three readings."""
    features = pd.DataFrame([[temp, hum, rain]], columns=X.columns)
    return model.predict(features)[0]


def predict_interactive():
    """Prompt the user for readings and print the prediction (CLI mode)."""
    try:
        temp = float(input("Temperature (°C): "))
        hum = float(input("Humidity (%): "))
        rain = float(input("Rainfall (mm): "))
    except ValueError:
        print("Missing/invalid values — please enter numeric readings.")
        return

    result = predict_condition(temp, hum, rain)
    if result == "Good":
        print("\nGood ✅ — These conditions favor healthy crop growth.")
    else:
        print("\nPoor ⚠️ — These conditions are unfavorable for the crop.")


# ----------------------------------------------------------------------
# 4. Temperature vs. Rainfall scatter chart (matplotlib version of the SVG)
# ----------------------------------------------------------------------
def plot_chart(save_path: str = "temp_vs_rainfall.png"):
    colors = {"Good": "#4c6b3f", "Poor": "#b5563c"}
    fig, ax = plt.subplots(figsize=(7, 4.5))

    for condition, group in df.groupby("Condition"):
        ax.scatter(
            group["Temperature"],
            group["Rainfall"],
            c=colors[condition],
            label=condition,
            s=60,
            edgecolors="#fffdf8",
            linewidths=1.2,
            alpha=0.9,
        )

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_title("Temperature vs. Rainfall")
    ax.legend(title="Condition")
    ax.set_facecolor("#fffdf8")
    fig.patch.set_facecolor("#f6f1e6")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    print(f"\nChart saved to {save_path}")


# ----------------------------------------------------------------------
# 5. Run as a script
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("\nDataset:")
    print(df.to_string(index=False))

    plot_chart()

    # Example prediction (mirrors the HTML page's default input values)
    example = predict_condition(25, 65, 100)
    print(f"\nExample prediction for T=25, H=65, R=100 -> {example}")

    # Uncomment to prompt for your own readings in the terminal:
    # predict_interactive()
