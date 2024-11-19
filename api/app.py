# API to send prediction data as a csv file

from flask import Flask, send_file, jsonify
from flask_cors import CORS
import pandas as pd

import os


app = Flask(__name__)
CORS(app, resources={"/predict": {"origins": "http://localhost:3000"}})

file_path = os.path.join(os.getcwd(), 'data', 'predicted_orders_this_year.csv')

# "/"というルート（URL）にアクセスしたときの動作を定義
@app.route("/")
def home():
    try:
        # Attempt to open the file
        with open(file_path, 'r') as file:
            # Do something with the file
            data = file.read()
        return "File accessed successfully!"
    except FileNotFoundError:
        return f"File not found: {file_path}"

# @app.route('/predict', methods=['GET'])
# def send_csv_file():
#     # Path to your CSV file
#     file_path = '../data/predicted_orders_this_year.csv'
    
#     try:
#         # Send the file to the frontend
#         return send_file(file_path, as_attachment=True, mimetype='text/csv')
#     except Exception as e:
#         return str(e), 500

@app.route('/predict', methods=['GET'])
def send_json_data():
    # Load the CSV file into a pandas DataFrame
    file_path = './data/predicted_orders_this_year.csv'

    print("Current working directory:", os.getcwd())

    if not os.path.exists(file_path):
        print("File not found:", file_path)

    try:
        data = pd.read_csv(file_path)
        
        # Convert the DataFrame to a list of dictionaries
        json_data = data.to_dict(orient='records')
        
        # Send the data as a JSON response
        return jsonify(json_data)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Get the PORT from the environment variables or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
