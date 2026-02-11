
from flask import Flask, render_template, request
from train_model import retrain_model
from generate_qr import generate_qr
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

DATA_FILE = "bamboo_salt_data.csv"
model = joblib.load("quality_model.pkl")

def edible_status(score):
    if score >= 75:
        return "EDIBLE"
    elif score >= 60:
        return "REPROCESS"
    else:
        return "REJECT"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        batch_id = request.form["batch_id"]
        df = pd.read_csv(DATA_FILE)
        row = df[df["batch_id"] == batch_id]

        if not row.empty:
            values = row.iloc[0]
            X = np.array([[values["cycles"],
                           values["temperature"],
                           values["sulfur_ppm"],
                           values["pH"],
                           values["ash"]]])

            quality = round(float(model.predict(X)[0]), 2)
            status = edible_status(quality)
            qr_filename = generate_qr(batch_id, quality, status)

            result = {
                "batch_id": batch_id,
                "product": "Bamboo Salt",
                "cycles": f'{values["cycles"]}×',
                "quality": f"{quality} / 100",
                "status": status,
                "qr": qr_filename
            }
        else:
            result = {
                "batch_id": batch_id,
                "product": "Not Found",
                "cycles": "-",
                "quality": "-",
                "status": "INVALID BATCH"
            }

    return render_template("index.html", data=result)

@app.route("/add_batch", methods=["GET", "POST"])
def add_batch():
    msg = None
    if request.method == "POST":
        new_data = {
            "batch_id": request.form["batch_id"],
            "cycles": int(request.form["cycles"]),
            "temperature": float(request.form["temperature"]),
            "sulfur_ppm": float(request.form["sulfur_ppm"]),
            "pH": float(request.form["pH"]),
            "ash": float(request.form["ash"]),
            "quality_score": float(request.form["quality_score"])
        }

        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        retrain_model()

        global model
        model = joblib.load("quality_model.pkl")

        msg = "Batch added successfully ✅"

    return render_template("add_batch.html", msg=msg)

if __name__ == "__main__":
    app.run()
