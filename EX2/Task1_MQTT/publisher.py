# Deepak Kumar Nirala - 25MCMT17
# This file read DHT11 sensor data (Temperature & Humidity)
# and publish it to ThingSpeak via MQTT protocol

import paho.mqtt.client as mqtt   # MQTT client library
import Adafruit_DHT               # DHT11 sensor library
import time                       # For delay between readings

MQTT_CLIENT_ID = "EDAQJRoQBDcaEDUMNzokLAs"
MQTT_USERNAME  = "EDAQJRoQBDcaEDUMNzokLAs"
MQTT_PASSWORD  = "uD3M1IdnoX79z2VasekjdPuD"
 
# CONFIGURATION

THINGSPEAK_CHANNEL_ID  = "3299623"
THINGSPEAK_WRITE_KEY   = "MTZ009G2EBWHXG4T"
 
# ThingSpeak MQTT broker settings
MQTT_BROKER   = "mqtt3.thingspeak.com"
MQTT_PORT     = 1883
MQTT_TOPIC = f"channels/{THINGSPEAK_CHANNEL_ID}/publish" 
# DHT11 sensor configuration
DHT_SENSOR    = Adafruit_DHT.DHT11   # Sensor type
DHT_PIN       = 17                    # GPIO pin number where DHT11 DATA pin is connected
 
PUBLISH_INTERVAL = 15  #15seconds to publish readings
 
def on_connect(client, userdata, flags, rc):
    """Callback fired when MQTT connection is established."""
    if rc == 0:
        print("[MQTT] Connected to ThingSpeak broker successfully!")
    else:
        print(f"[MQTT] Connection failed with code {rc}")
 
 
def on_publish(client, userdata, mid):
    """Callback fired after a message is successfully published."""
    print(f"[MQTT] Data published successfully (message id: {mid})")
 
def read_dht11():
    """
    Read temperature and humidity from the DHT11 sensor.
    Returns (humidity, temperature) or (None, None) on failure.
    """
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity, temperature
 
 
def main():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_publish  = on_publish
 
    # Connect to ThingSpeak MQTT broker
    print(f"[MQTT] Connecting to {MQTT_BROKER}:{MQTT_PORT} ...")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
 
    # Start background network loop (non-blocking)
    client.loop_start()
    time.sleep(15)
 
    print("[DHT11] Starting sensor readings. Press Ctrl+C to stop.\n")
 
    try:
        while True:
	#Read sensor
            humidity, temperature = read_dht11()
 
            if humidity is not None and temperature is not None:
                # buid Format: field1=<temp>&field2=<humidity>
                payload = f"field1={temperature:.1f}&field2={humidity:.1f}"
                print(f"[DHT11] Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
 
                # Publish to ThingSpeak
                result = client.publish(MQTT_TOPIC, payload)
                if result.rc != mqtt.MQTT_ERR_SUCCESS:
                    print(f"[MQTT] Publish error: {result.rc}")
            else:
                print("[DHT11] Failed to read sensor data. Retrying...")
 
            # Wait before next readings
            time.sleep(PUBLISH_INTERVAL)
 
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[MQTT] Disconnected.")
 
 
if __name__ == "__main__":
    main()

