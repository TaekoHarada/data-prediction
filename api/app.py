# API to send prediction data as a csv file

from flask import Flask, send_file, jsonify
from flask_cors import CORS
import pandas as pd

import os


app = Flask(__name__)
CORS(app, resources={"/predict": {"origins": "http://localhost:3000"}})


# "/"というルート（URL）にアクセスしたときの動作を定義
@app.route("/")
def hello():
    return "Hello, World!"


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
    file_path = '../data/predicted_orders_this_year.csv'

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

if __name__ == "__main__":
    app.run(debug=True)


