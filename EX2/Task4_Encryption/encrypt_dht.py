# Deepak Kumar Nirala - 25MCMT17
# Task 4: Encrypt DHT11 sensor data using Fernet encryption
# Also implemented data masking as privacy method

import Adafruit_DHT
import json
from cryptography.fernet import Fernet
from datetime import datetime

# DHT11 sensor config
sensor = Adafruit_DHT.DHT11
pin    = 17

#Step 1: Generate Fernet encryption ke
key    = Fernet.generate_key()
cipher = Fernet(key)
print("Encryption Key:", key.decode())
print("-" * 50)

#Step 2: Read DHT11 sensor
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is None or temperature is None:
    print("Sensor read failed!")
    exit()

# Step 3: Convert sensor data to JSON
sensor_data = {
    "device_id":   "25MCMT17-RPi",
    "temperature": temperature,
    "humidity":    humidity,
    "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

json_data = json.dumps(sensor_data)
print("Original JSON Data:")
print(json_data)
print("-" * 50)

#Step 4: Encrypt using Fernet
encrypted_data = cipher.encrypt(json_data.encode())
print("Encrypted Data:")
print(encrypted_data.decode())
print("-" * 50)

#Step 5: Decrypt to verify
decrypted_data = cipher.decrypt(encrypted_data)
print("Decrypted Data (verified):")
print(decrypted_data.decode())
print("-" * 50)

# Step 6: Privacy Method - Data Masking 
# Masking hides exact values - only range is shown
# This protects user privacy if data is shared publicly

def mask_temperature(temp):
    """Show only range instead of exact value."""
    if temp < 20:
        return "Below 20°C (Cool)"
    elif temp < 30:
        return "20-30°C (Normal)"
    else:
        return "Above 30°C (Warm)"

def mask_humidity(humi):
    """Show only range instead of exact value."""
    if humi < 40:
        return "Below 40% (Dry)"
    elif humi < 70:
        return "40-70% (Comfortable)"
    else:
        return "Above 70% (Humid)"

masked_data = {
    "device_id":   "25MCMT17-RPi",
    "temperature": mask_temperature(temperature),
    "humidity":    mask_humidity(humidity),
    "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

print("Privacy Method — Data Masking:")
print(json.dumps(masked_data, indent=2))
print("-" * 50)
print("Done!")