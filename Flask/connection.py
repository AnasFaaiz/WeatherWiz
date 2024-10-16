from idlelib.run import LOCALHOST

from flask import Flask, jsonify,request
from pymongo import MongoClient

app = Flask(__name__)

#connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["weatherWiz"]
forecasts_collection = db["forecasts"]

#Define API endpoints

@app.route("/api/forecasts", methods=["GET"])
def get_forecasts():
    forecasts = forecasts_collection.find()
    return jsonify([forecast for forecast in forecasts])

@app.route("/api/forecasts/<city>", methods=["GET"])
def get_forecast(city):
    forecast = forecasts_collection.find_one({"city": city})
    return jsonify(forecast)

@app.route("/api/forecasts", methods=["POST"])
def create_forecast():
    forecast = request.json
    forecasts_collection.insert_one(forecast)
    return jsonify(forecast)

@app.route("/api/forecasts/<city>", methods=["PUT"])
def update_forecast(city):
    forecast = request.json
    forecasts_collection.update_one({"city" : city}, {"$set": forecast})
    return jsonify(forecast)

@app.route("/api/forecasts/<city>", methods=["DELETE"])
def delete_forevast(city):
    forecasts_collection.delete_one({"city": city})
    return jsonify({"message": "Forecast deleted"})

if __name__ == "__main__":
    app.run(debug=True)
