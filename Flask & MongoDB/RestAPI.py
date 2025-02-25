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

@app.route('/sensor/data', methods=['POST'])
def sensor_data():
    try:
        json_data = request.json
        sensor_type = json_data.get('sensor_type')
        if not sensor_type:
            return jsonify({"error": "sensor_type is required"}), 400
        
        valid_sensors = {"DHT11", "Ultrasonic", "PIR"}
        if sensor_type not in valid_sensors:
            return jsonify({"error": "Invalid sensor_type"}), 400
        
        return save_data(sensor_type, json_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
