from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS
import pandas as pd
import numpy as np
import random

app = Flask(__name__)
CORS(app)
# Load the pre-trained model
model = joblib.load('D:\\Akash_Tripathi\\Data\\forecasting_model.pkl')

def predict_future_violations(features):
    return model.predict(features)

def generate_future_data(num_transporters, month, year):
    # Sample transporter names
    sample_names = [
        'BABA BAIDYANATH ENTERPRISES', 'ADITYA ENTERPRISES', 'FOUJI ROADLINES','ARSH ENTERPRISES','USHA ENTERPRISES','UDAY SHANKAR PRASAD SINGH', 'MAA KANTI INDANE',
        'TARA ENTERPRISES', 'MAA KALI ROADWAYS', 'PRIYANKA SINGH'
    ]

    if num_transporters > len(sample_names):
        raise ValueError("Number of transporters requested exceeds the number of sample names available.")
    
    future_data = pd.DataFrame({
        'TransportersName': random.choices(sample_names, k=num_transporters),
        'Truck_Count': np.random.randint(1, 20, size=num_transporters),
        'Invoice_Count': np.random.randint(100, 2000, size=num_transporters),
        'Route_Violation_Count': np.random.randint(0, 100, size=num_transporters),
        'Speed_Violation_Count': np.random.randint(0, 50, size=num_transporters),
        'Stoppage_Violation_Count': np.random.randint(0, 60, size=num_transporters),
        'Night_Violation_Count': np.random.randint(0, 30, size=num_transporters)
    })

    # Drop non-numeric columns used only for display
    features = future_data.drop(columns=['TransportersName'])
    
    # Predict
    future_data['Predicted_Violations'] = predict_future_violations(features)
    
    return future_data


@app.route('/forecast', methods=['POST'])
def forecast():
    data = request.json
    month = data.get('month')
    year = data.get('year')
    num_transporters = data.get('num_transporters', 10)

    if month is None or year is None:
        return jsonify({"error": "Month and year are required"}), 400

    future_data = generate_future_data(num_transporters, month, year)
    future_data_sorted = future_data.sort_values(by='Predicted_Violations', ascending=False)
    top_10_future_transporters = future_data_sorted.head(10).to_dict(orient='records')

    return jsonify(top_10_future_transporters)

if __name__ == '__main__':
    app.run(debug=True)
