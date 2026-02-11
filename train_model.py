
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def retrain_model():
    data = pd.read_csv("bamboo_salt_data.csv")
    X = data[['cycles', 'temperature', 'sulfur_ppm', 'pH', 'ash']]
    y = data['quality_score']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "quality_model.pkl")
    print("✅ Model retrained")

if __name__ == "__main__":
    retrain_model()
