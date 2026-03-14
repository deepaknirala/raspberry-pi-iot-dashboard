# Deepak Kumar Nirala - 25MCMT17
# Task 3: Python GUI to collect and store DHT11 data in MySQL DB

import tkinter as tk
from tkinter import scrolledtext
import Adafruit_DHT
import mysql.connector
from datetime import datetime

# DHT11 sensor config
sensor = Adafruit_DHT.DHT11
pin    = 17

# MySQL connection
db = mysql.connector.connect(
    host     = "localhost",
    user     = "root",
    password = "",
    database = "25MCMT17"
)
cursor = db.cursor()

# Auto fetch running flag
running = False

def read_and_store():
    """Read DHT11 sensor and store in MySQL."""
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        now = datetime.now()

        # Update GUI labels
        temp_label.config(text=f"{temperature} °C")
        humi_label.config(text=f"{humidity} %")
        time_label.config(text=f"Last updated: {now.strftime('%H:%M:%S')}")

        # Store in MySQL
        sql = "INSERT INTO dht_sensor (temperature, humidity, timestamp) VALUES (%s, %s, %s)"
        val = (temperature, humidity, now)
        cursor.execute(sql, val)
        db.commit()

        log(f"[{now.strftime('%H:%M:%S')}] Temp: {temperature}°C | Humidity: {humidity}% | Saved to DB")
    else:
        log("Sensor read failed!")

    # Auto repeat every 10 seconds if running
    if running:
        root.after(10000, read_and_store)

# Event Handler 1 — Start button
def start_logging():
    global running
    running = True
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
    status_label.config(text="Logging started...", fg="green")
    log("Auto logging started — every 10 seconds")
    read_and_store()

# Event Handler 2 — Stop button
def stop_logging():
    global running
    running = False
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")
    status_label.config(text="Logging stopped", fg="red")
    log("Logging stopped")

# Event Handler 3 — Manual Save button
def manual_save():
    """Manually save one reading."""
    read_and_store()
    log("Manual save done!")

def log(msg):
    log_box.config(state="normal")
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    log_box.config(state="disabled")

# GUI Window
root = tk.Tk()
root.title("DHT11 MySQL Logger - 25MCMT17")
root.geometry("500x580")
root.config(bg="#f0f0f0")

# Title
tk.Label(root, text="DHT11 Sensor Data Logger",
         font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
tk.Label(root, text="Deepak Kumar Nirala | 25MCMT17",
         font=("Arial", 9), fg="gray", bg="#f0f0f0").pack()

# Temp & Humidity display
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

status_label = tk.Label(root, text="Not started",
                        font=("Arial", 10), fg="gray", bg="#f0f0f0")
status_label.pack(pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=5)

# Event Handler 1 - Start Auto Logging
start_btn = tk.Button(btn_frame, text="Start Logging",
                      command=start_logging, bg="green", fg="white",
                      font=("Arial", 11), padx=10)
start_btn.pack(side="left", padx=5)

# Event Handler 2 - Stop Logging
stop_btn = tk.Button(btn_frame, text="Stop Logging",
                     command=stop_logging, bg="red", fg="white",
                     font=("Arial", 11), padx=10,
                     state="disabled")
stop_btn.pack(side="left", padx=5)

# Event Handler 3 - Manual Save
save_btn = tk.Button(btn_frame, text="Save Once",
                     command=manual_save, bg="steelblue", fg="white",
                     font=("Arial", 11), padx=10)
save_btn.pack(side="left", padx=5)

# Log box
tk.Label(root, text="Log:", font=("Arial", 10, "bold"),
         bg="#f0f0f0", anchor="w").pack(fill="x", padx=15)

log_box = scrolledtext.ScrolledText(root, height=8, state="disabled",
                                    font=("Courier", 9))
log_box.pack(fill="x", padx=15, pady=5)

root.mainloop()