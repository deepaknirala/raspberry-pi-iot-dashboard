# Deepak Kumar Nirala - 25MCMT17
# Task 2: RESTful API to collect and store DHT11 sensor data
# Run on Raspberry Pi using Flask

from flask import Flask, jsonify
import Adafruit_DHT
from datetime import datetime
import json
import os

app = Flask(__name__)

# DHT11 sensor config
sensor = Adafruit_DHT.DHT11
pin    = 17

# Local file to store data
DATA_FILE = os.path.expanduser(
    "~/25MCMT17/EX2/Task2_REST_API/sensor_data.json"
)

def read_sensor():
    """Read temperature and humidity from DHT11."""
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return temperature, humidity

def save_to_file(data):
    """Save sensor reading to local JSON file."""
    records = []

    # Load existing records if file exists
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                records = json.load(f)
            except:
                records = []

    # Append new record
    records.append(data)

    # Save back to file
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=2)

# ── API Routes ──

@app.route("/")
def home():
    """Home route — basic info."""
    return jsonify({
        "message": "DHT11 REST API - 25MCMT17",
        "routes": {
            "/sensor":  "Get latest sensor reading",
            "/history": "Get all stored readings",
            "/save":    "Save current reading to file"
        }
    })

@app.route("/sensor")
def get_sensor():
    """GET /sensor — returns latest DHT11 reading."""
    temperature, humidity = read_sensor()

    if temperature is not None and humidity is not None:
        return jsonify({
            "temperature": temperature,
            "humidity":    humidity,
            "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status":      "success"
        })
    else:
        return jsonify({
            "status":  "error",
            "message": "Sensor read failed"
        }), 500

@app.route("/save")
def save_reading():
    """GET /save — reads sensor and saves to JSON file."""
    temperature, humidity = read_sensor()

    if temperature is not None and humidity is not None:
        data = {
            "temperature": temperature,
            "humidity":    humidity,
            "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_to_file(data)
        return jsonify({
            "status":  "saved",
            "data":    data
        })
    else:
        return jsonify({
            "status":  "error",
            "message": "Sensor read failed"
        }), 500

@app.route("/history")
def get_history():
    """GET /history — returns all stored readings."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                records = json.load(f)
                return jsonify({
                    "status":  "success",
                    "count":   len(records),
                    "records": records
                })
            except:
                pass

    return jsonify({
        "status":   "empty",
        "records":  []
    })

if __name__ == "__main__":
    # Run on all interfaces so accessible from PC browser too
    app.run(host="0.0.0.0", port=5000, debug=True)