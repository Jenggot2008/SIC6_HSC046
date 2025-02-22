from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Ganti dengan connection string MongoDB Atlas kalian
MONGO_URI = "mongodb+srv://database:samsung2025@cluster0.mongodb.net/MyDatabase?retryWrites=true&w=majority"

# Koneksi ke MongoDB
client = MongoClient(MONGO_URI)
db = client['MyDatabase']  # Ganti dengan nama database kalian
collection = db['SensorData']  # Ganti dengan nama collection kalian

@app.route('/sensor1', methods=['POST'])
def sensor_data():
    try:
        json_data = request.json
        temperature = json_data.get('temperature')
        humidity = json_data.get('humidity')
        timestamp = datetime.datetime.now().isoformat()  # Generate timestamp otomatis

        if temperature is None or humidity is None:
            return jsonify({"error": "temperature and humidity are required"}), 400

        new_entry = {
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": timestamp
        }

        collection.insert_one(new_entry)  # Simpan ke MongoDB
        return jsonify({"message": "Data added successfully", "data": new_entry}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/data', methods=['GET'])
def get_data():
    all_data = list(collection.find({}, {"_id": 0}))  # Ambil semua data tanpa "_id"
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)

#cluster config
#database
#samsung2025