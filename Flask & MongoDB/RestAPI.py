# Flask Server Code
from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Ganti dengan connection string MongoDB Atlas kalian
MONGO_URI = "mongodb+srv://HSC046:RGFBAKSO@rgfbakso.mzcsy.mongodb.net/?retryWrites=true&w=majority&appName=RGFBAKSO"

# Koneksi ke MongoDB
client = MongoClient(MONGO_URI)
db = client['MyDatabase']  # Ganti dengan nama database kalian
collection = db['SensorData']  # Ganti dengan nama collection kalian

def save_data(sensor_type, data):
    data['timestamp'] = datetime.datetime.now().isoformat()
    data['sensor_type'] = sensor_type 
    collection.insert_one(data)
    return jsonify({"message": "Data added successfully", "data": data}), 201

@app.route('/sensor/dht11', methods=['POST'])
def sensor_dht11():
    try:
        json_data = request.json
        temperature = json_data.get('temperature')
        humidity = json_data.get('humidity')
        if temperature is None or humidity is None:
            return jsonify({"error": "temperature and humidity are required"}), 400
        return save_data("DHT11", {"temperature": temperature, "humidity": humidity})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/sensor/ultrasonic', methods=['POST'])
def sensor_ultrasonic():
    try:
        json_data = request.json
        distance = json_data.get('distance')
        if distance is None:
            return jsonify({"error": "distance is required"}), 400
        return save_data("Ultrasonic", {"distance": distance})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/sensor/pir', methods=['POST'])
def sensor_pir():
    try:
        json_data = request.json
        motion_detected = json_data.get('motion_detected')
        if motion_detected is None:
            return jsonify({"error": "motion_detected is required"}), 400
        return save_data("PIR", {"motion_detected": motion_detected})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/data', methods=['GET'])
def get_data():
    all_data = list(collection.find({}, {"_id": 0}))  # Ambil semua data tanpa "_id"
    return jsonify(all_data)

@app.route('/data/average', methods=['GET'])
def get_average():
    pipeline = [
        {"$group": {
            "_id": "$sensor_type",
            "avg_temperature": {"$avg": "$temperature"},
            "avg_humidity": {"$avg": "$humidity"},
            "avg_distance": {"$avg": "$distance"}
        }}
    ]
    avg_data = list(collection.aggregate(pipeline))
    return jsonify(avg_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
