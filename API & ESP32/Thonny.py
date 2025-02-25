#masukkin dulu ke thonny 
# import time
# import network
# import urequests as requests
# from machine import Pin, time_pulse_us
# import dht

# === KONFIGURASI WiFi ===
# SSID = "JENGGOT"  # Ganti dengan SSID WiFi
# PASSWORD = "12345678"  # Ganti dengan password WiFi

# === KONFIGURASI UBIDOTS ===
# DEVICE_ID = "rgf_bakso"
# TOKEN = "BBUS-AdNAy2qyEUmUZCcIkJf5IMKrb5irSS"
# DISTANCE_LABEL = "distance"
# TEMP_LABEL = "temperature"
# HUMIDITY_LABEL = "humidity"

# === KONFIGURASI SENSOR ULTRASONIK ===
# TRIG_PIN = 22
# ECHO_PIN = 23
# trig = Pin(TRIG_PIN, Pin.OUT)
# echo = Pin(ECHO_PIN, Pin.IN)

# === KONFIGURASI SENSOR DHT ===
# DHT_PIN = 15  # Pin sensor DHT22
# sensor_dht = dht.DHT11(Pin(DHT_PIN))

# === LED Indikator ===
# led = Pin(5, Pin.OUT)

# === FUNGSI KONEKSI KE WiFi ===
# def connect_wifi():
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     wlan.connect(SSID, PASSWORD)

#     print("\U0001F504 Connecting to WiFi...")
#     timeout = 10  # Batas waktu 10 detik
#     while not wlan.isconnected() and timeout > 0:
#         time.sleep(1)
#         timeout -= 1

#     if wlan.isconnected():
#         print("✅ Connected to WiFi!")
#         print("📡 IP Address:", wlan.ifconfig()[0])
#     else:
#         print("❌ Failed to connect to WiFi! Check your credentials.")

# === FUNGSI MEMBACA JARAK DENGAN FILTER MEDIAN ===
# def get_distance(samples=5):
#     readings = []
    
#     for _ in range(samples):
#         trig.off()
#         time.sleep_us(2)
#         trig.on()
#         time.sleep_us(10)
#         trig.off()

#         duration = time_pulse_us(echo, 1, 30000)
#         if duration > 0:
#             distance = (duration * 0.0343) / 2
#             readings.append(distance)
#         time.sleep(0.02)

#     if readings:
#         readings.sort()
#         return readings[len(readings) // 2]  # Ambil nilai median
#     else:
#         return None  # Jika tidak ada data yang valid

# === FUNGSI MEMBACA SENSOR DHT22 ===
# def get_dht_data():
#     try:
#         sensor_dht.measure()
#         temp = sensor_dht.temperature()
#         humidity = sensor_dht.humidity()
#         return temp, humidity
#     except Exception as e:
#         print(f"⚠️ Error reading DHT sensor: {e}")
#         return None, None

# === FUNGSI KIRIM DATA KE UBIDOTS ===
# def send_data_to_ubidots(distance, temp, humidity):
#     url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_ID}"
#     headers = {
#         "Content-Type": "application/json",
#         "X-Auth-Token": TOKEN
#     }
    
#     data = {
#         DISTANCE_LABEL: distance,
#         TEMP_LABEL: temp,
#         HUMIDITY_LABEL: humidity
#     }

#     try:
#         response = requests.post(url, json=data, headers=headers)
#         if response.status_code in [200, 201]:
#             print(f"✅ Data sent successfully! Distance: {distance:.2f} cm, Temp: {temp:.2f}°C, Humidity: {humidity:.2f}%")
#             led.value(1)
#             time.sleep(0.5)
#             led.value(0)
#         else:
#             print(f"⚠️ Failed to send data! Response: {response.text}")
#         response.close()
#     except Exception as e:
#         print(f"❌ Error sending data to Ubidots: {e}")

# === PROGRAM UTAMA ===
# connect_wifi()

# while True:
#     distance = get_distance()
#     temp, humidity = get_dht_data()
    
#     if distance is not None and temp is not None and humidity is not None:
#         print(f"📏 Distance: {distance:.2f} cm, 🌡 Temp: {temp:.2f}°C, 💧 Humidity: {humidity:.2f}%")
#         send_data_to_ubidots(distance, temp, humidity)
#     else:
#         print("⚠️ Failed to read sensor data!")

#     time.sleep(0.5)  # Interval pembacaan 5 detik
