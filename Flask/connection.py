from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from bson import ObjectId, json_util
from marshmallow import Schema, fields
import json

# Initialize Flask application
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['WeatherWizDB']  # Replace with your database name
collection = db['Weather']  # Replace with your collection name

# Custom JSON encoder to handle ObjectId serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)

app.json_encoder = CustomJSONEncoder

# Marshmallow schema for data serialization
class DataSchema(Schema):
    _id = fields.Str(attribute='_id')  # Convert ObjectId to string

@app.route('/')
def home():
    return "Welcome to the Weather API!"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    api_key = '1ea44da4c58384ff94d17b7d7f428473'  # Replace with your actual API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()

        # Save data to MongoDB
        collection.insert_one(weather_data)

        return jsonify(weather_data), 200
    else:
        return jsonify({'error': 'City not found'}), 404

@app.route('/data', methods=['GET'])
def get_data():
    data = collection.find()  # Fetch data from MongoDB
    result = [data_schema.dump(doc) for doc in data]  # Use marshmallow schema for serialization
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='localhost')