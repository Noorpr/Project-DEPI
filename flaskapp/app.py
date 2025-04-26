from flask import Flask, render_template, request, redirect, url_for, jsonify
from dashboard import startDashboard
import joblib
import pandas as pd
from typing import List
from tensorflow.keras.models import load_model
# Initialize Flask app
app = Flask(__name__)
dash_app = startDashboard(app)

# Global model variable
model = None

# Function to load the model
def load_the_model():
    global model
    model = load_model("best_model.h5")
    print("Model Loaded")

# Create a simple class for validation
class InputData:
    def __init__(self, features):
        self.features = features

# Flask routes
@app.route('/')
def index():
    return "hello world"

# FastAPI endpoint converted to Flask
@app.route('/predict', methods=['POST'])
def get_result():
    global model
    # Load model if not already loaded
    if model is None:
        load_the_model()
    
    data = request.get_json()
    if not data or 'features' not in data:
        return jsonify({"error": "Invalid input. 'features' field is required"}), 400
    
    # Create InputData object
    input_data = InputData(features=data['features'])
    
    # Make prediction
    prediction = model.predict([input_data.features])
    return jsonify({"prediction": prediction[0]})

# Configure CORS (Cross-Origin Resource Sharing)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == "__main__":
    # Load model at startup
    load_the_model()
    app.run(debug=True)
