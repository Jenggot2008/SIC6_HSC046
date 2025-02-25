from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)
MONGO_URI = "mongodb+srv://HSC046:RGFBAKSO@rgfbakso.mzcsy.mongodb.net/?retryWrites=true&w=majority&appName=RGFBAKSO"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Timeout 5 detik
    db = client['datasensor']
    collection = db['sensor_data']  # Gunakan nama koleksi yang lebih bersih
    client.server_info()  # Tes koneksi
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    exit(1)  # Hentikan aplikasi jika koneksi gagal

# === FUNGSI SIMPAN DATA ===
def save_data(sensor):
    try:
        sensor['timestamp'] = datetime.datetime.utcnow().isoformat()
        result = collection.insert_one(sensor)
        sensor['_id'] = str(result.inserted_id)  # Konversi ObjectId ke string
        return sensor
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return None

# === ENDPOINT TERIMA DATA SENSOR (MULTIPLE SENSORS) ===
@app.route('/sensor/data', methods=['POST'])
def sensor_data():
    try:
        json_data = request.get_json()

        if not json_data or "sensors" not in json_data or not isinstance(json_data["sensors"], list):
            return jsonify({"error": "Invalid JSON format, expected a list under 'sensors'"}), 400
        
        sensors = json_data["sensors"]
        valid_sensors = {"DHT11", "Ultrasonic", "PIR"}
        saved_sensors = []

        for sensor in sensors:
            sensor_type = sensor.get("sensor_type")
            if not sensor_type or sensor_type not in valid_sensors:
                return jsonify({"error": f"Invalid sensor_type in {sensor}"}), 400
            
            # Validasi tambahan untuk masing-masing sensor
            if sensor_type == "Ultrasonic" and "distance" not in sensor:
                return jsonify({"error": "Missing distance value for Ultrasonic sensor"}), 400
            if sensor_type == "DHT11" and ("temperature" not in sensor or "humidity" not in sensor):
                return jsonify({"error": "Missing temperature/humidity values for DHT11"}), 400
            if sensor_type == "PIR" and "motion" not in sensor:
                return jsonify({"error": "Missing motion value for PIR sensor"}), 400

            # Simpan sensor ke MongoDB
            saved_sensor = save_data(sensor)
            if saved_sensor:
                saved_sensors.append(saved_sensor)

        return jsonify({"message": "✅ Data received successfully", "saved_data": saved_sensors}), 201

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    
# === JALANKAN FLASK ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
