# ESP32 Code (MicroPython - Thonny)
import network
import urequests
import dht
import machine
import time

SSID = "your_wifi_ssid"
PASSWORD = "your_wifi_password"
API_URL = "http://your_flask_server_ip:5000"

# Setup WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PASSWORD)
while not sta_if.isconnected():
    pass
print("Connected to WiFi")

# Setup Sensors
dht_sensor = dht.DHT11(machine.Pin(4))  # Pin DHT11 di GPIO4
ultrasonic_trigger = machine.Pin(5, machine.Pin.OUT)
ultrasonic_echo = machine.Pin(18, machine.Pin.IN)
pir_sensor = machine.Pin(19, machine.Pin.IN)

# Function to get ultrasonic distance
def get_distance():
    ultrasonic_trigger.value(1)
    time.sleep_us(10)
    ultrasonic_trigger.value(0)
    pulse_time = machine.time_pulse_us(ultrasonic_echo, 1)
    distance = (pulse_time / 2) / 29.1  # Convert to cm
    return distance

# Function to send sensor data
def send_data():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        distance = get_distance()
        motion_detected = pir_sensor.value()

        data = {
            "temperature": temperature,
            "humidity": humidity,
            "distance": distance,
            "motion_detected": motion_detected
        }
        
        response = urequests.post(f"{API_URL}/sensor/dht11", json={"temperature": temperature, "humidity": humidity})
        print(response.text)
        response = urequests.post(f"{API_URL}/sensor/ultrasonic", json={"distance": distance})
        print(response.text)
        response = urequests.post(f"{API_URL}/sensor/pir", json={"motion_detected": motion_detected})
        print(response.text)
    except Exception as e:
        print("Error:", str(e))

# Loop to send data periodically
while True:
    send_data()
    time.sleep(10)
