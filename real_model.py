import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("datasets/Delhi_Training_Dataset.csv")

print("Dataset Shape:", df.shape)

# ==========================
# FEATURES & TARGET
# ==========================

X = df[['NDVI']]
y = df['LST']

# ==========================
# TRAIN TEST SPLIT
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================
# MODEL
# ==========================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================
# PREDICTIONS
# ==========================

predictions = model.predict(X_test)

# ==========================
# EVALUATION
# ==========================

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nMean Absolute Error:")
print(round(mae, 2))

print("\nR² Score:")
print(round(r2, 3))