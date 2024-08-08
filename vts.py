from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app) 

# Load the saved model
model = joblib.load('D:/Akash_Tripathi/transporter_performance_model.pkl')

# Optional: If you used a scaler during training, load it as well
# scaler = joblib.load('scaler.pkl')  # Uncomment this if you have a scaler

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = pd.DataFrame([data['features']])
    prediction = model.predict(features)
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
