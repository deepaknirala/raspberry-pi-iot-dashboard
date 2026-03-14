# Deepak Kumar Nirala - 25MCMT17
# Task 1: MQTT Subscriber GUI using Tkinter
# Fetches live DHT11 data from ThingSpeak and displays it

import tkinter as tk
from tkinter import scrolledtext
import urllib.request
import json
import csv
import os
from datetime import datetime
import threading

# ThingSpeak config
CHANNEL_ID = "3299623"
READ_KEY   = "499O1LIMFZO7H6UT"
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_KEY}"

running = False

# Event Handler 1 — Fetch latest data from ThingSpeak
def fetch_data():
    try:
        with urllib.request.urlopen(URL) as response:
            data = json.loads(response.read().decode())
            temp = data.get("field1", "N/A")
            humi = data.get("field2", "N/A")
            now  = datetime.now().strftime("%H:%M:%S")

            temp_label.config(text=f"{temp} °C")
            humi_label.config(text=f"{humi} %")
            time_label.config(text=f"Last updated: {now}")
            log(f"[{now}] Temp: {temp}°C | Humidity: {humi}%")

    except Exception as e:
        log(f"Error: {e}")

    # Auto fetch every 15 seconds
    if running:
        root.after(15000, fetch_data)

# Start polling
def connect():
    global running
    running = True
    connect_btn.config(state="disabled")
    status_label.config(text="Connected - fetching data...", fg="green")
    log("Started fetching from ThingSpeak...")
    fetch_data()

# Event Handler 2 — Save Data to CSV
def save_data():
    temp = temp_label.cget("text")
    humi = humi_label.cget("text")
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if temp == "-- °C":
        log("No data yet! Click Connect first.")
        return

    filepath = os.path.expanduser(
        "~/25MCMT17/EX2/Task1_MQTT/sensor_log.csv"
    )
    file_exists = os.path.exists(filepath)

    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Temperature", "Humidity"])
        writer.writerow([now, temp, humi])

    log(f"Saved: {now} | {temp} | {humi}")

def log(msg):
    log_box.config(state="normal")
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    log_box.config(state="disabled")

# GUI
root = tk.Tk()
root.title("DHT11 MQTT Subscriber - 25MCMT17")
root.geometry("500x550")
root.config(bg="#f0f0f0")

tk.Label(root, text="DHT11 Live Sensor Data",
         font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
tk.Label(root, text="Deepak Kumar Nirala | 25MCMT17",
         font=("Arial", 9), fg="gray", bg="#f0f0f0").pack()

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=15)

tk.Label(frame, text="Temperature",
         font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=40)
tk.Label(frame, text="Humidity",
         font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=1, padx=40)

temp_label = tk.Label(frame, text="-- °C",
                      font=("Arial", 30, "bold"), fg="tomato", bg="#f0f0f0")
temp_label.grid(row=1, column=0, padx=40)

humi_label = tk.Label(frame, text="-- %",
                      font=("Arial", 30, "bold"), fg="steelblue", bg="#f0f0f0")
humi_label.grid(row=1, column=1, padx=40)

time_label = tk.Label(root, text="Last updated: --",
                      font=("Arial", 9), fg="gray", bg="#f0f0f0")
time_label.pack()

status_label = tk.Label(root, text="Not connected",
                        font=("Arial", 10), fg="gray", bg="#f0f0f0")
status_label.pack(pady=5)

btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=5)

connect_btn = tk.Button(btn_frame, text="Connect & Subscribe",
                        command=connect, bg="green", fg="white",
                        font=("Arial", 11), padx=10)
connect_btn.pack(side="left", padx=10)

save_btn = tk.Button(btn_frame, text="Save Data",
                     command=save_data, bg="steelblue", fg="white",
                     font=("Arial", 11), padx=10)
save_btn.pack(side="left", padx=10)

tk.Label(root, text="Log:", font=("Arial", 10, "bold"),
         bg="#f0f0f0", anchor="w").pack(fill="x", padx=15)

log_box = scrolledtext.ScrolledText(root, height=8, state="disabled",
                                    font=("Courier", 9))
log_box.pack(fill="x", padx=15, pady=5)

root.mainloop()