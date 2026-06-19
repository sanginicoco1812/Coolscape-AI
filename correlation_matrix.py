import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/Delhi_Master_Dataset_V3.csv")

corr = df[
    ["NDVI","Humidity","WindSpeed","BuildingDensity","LST"]
].corr()

plt.figure(figsize=(8,6))

plt.imshow(corr, cmap="coolwarm")
plt.colorbar()

plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)

for i in range(len(corr)):
    for j in range(len(corr)):
        plt.text(
            j,
            i,
            f"{corr.iloc[i,j]:.2f}",
            ha="center",
            va="center"
        )

plt.title("Feature Correlation Matrix")
plt.tight_layout()

plt.savefig(
    "images/correlation_matrix.png",
    dpi=300
)

plt.show()