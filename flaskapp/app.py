from flask import Flask, render_template, request, redirect, url_for, jsonify
from dashboard import startDashboard
import pandas as pd
from tensorflow.keras.models import load_model
import numpy as np

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

# Route to handle file upload and prediction
@app.route('/predict', methods=['POST'])
def get_result():
    global model
    # Load model if not already loaded
    if model is None:
        load_the_model()

    # Check if file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part", "message": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file", "message": "No selected file"}), 400
    
    try:
        # Read the uploaded CSV file into a Pandas DataFrame
        data = pd.read_csv(file)
        
        # Log the shape for debugging
        print(f"Original data shape: {data.shape}")
        
        # Take the last 96 rows if there are more than 96 rows
        if data.shape[0] > 96:
            data = data.tail(96).reset_index(drop=True)
            print(f"Resized data shape to: {data.shape}")
        
        # Ensure that the data has the correct shape (96, 11)
        if data.shape[0] != 96 or data.shape[1] != 11:
            return jsonify({"error": f"Invalid CSV shape. Got {data.shape}, expected (96, 11).", 
                           "message": f"Invalid CSV shape. Got {data.shape}, expected (96, 11)."}), 400
        
        # Convert DataFrame to numpy array
        features = data.values
        
        # Reshape to (1, 96, 11) to match the model input
        reshaped_features = np.expand_dims(features, axis=0)
        
        # Prediction
        prediction = model.predict(reshaped_features)
        prediction_list = prediction.tolist()
        
        # Return a more structured response
        return jsonify({"prediction": prediction_list[0]})  # Assuming prediction is a list of lists
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e), "message": str(e)}), 400

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