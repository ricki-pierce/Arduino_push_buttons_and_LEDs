#This code records which button is pressed and released. data is timestamped. also tells you duration that buttons were pressed. 
#data printed in excel file

import serial
import time
import threading
import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook
from datetime import datetime

# --- Serial Setup ---
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)  # Update COM port if needed
time.sleep(2)

# --- Global Data ---
event_log = []  # [(timestamp, event, duration)]
press_times = {}  # {'1': start_time_in_ms}


# --- Serial Reader Thread ---
def read_serial():
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode().strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue

            event = parts[0]
            arduino_ms = int(parts[1])
            system_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]

            if "_pressed" in event:
                button = event.split("_")[1]
                press_times[button] = arduino_ms
                event_text = f"#{button} - pressed"
                event_log.append((system_time, event_text, None))
                print(f"[{system_time}] {event_text}")

            elif "_released" in event:
                button = event.split("_")[1]
                if button in press_times:
                    duration = arduino_ms - press_times[button]
                    event_text = f"#{button} - released"
                    event_log.append((system_time, event_text, duration))
                    print(f"[{system_time}] {event_text} (Duration: {duration} ms)")
                    del press_times[button]


# --- Excel Export Function ---
def export_to_excel():
    if not event_log:
        messagebox.showwarning("No Data", "No events to export.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Button Events"

    # Headers
    ws['A1'] = 'Timestamp'
    ws['B1'] = 'Event'
    ws['C1'] = 'Duration (ms)'

    for idx, (timestamp, event, duration) in enumerate(event_log, start=2):
        ws[f"A{idx}"] = timestamp
        ws[f"B{idx}"] = event
        if duration is not None:
            ws[f"C{idx}"] = duration

    filename = f"button_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb.save(filename)
    messagebox.showinfo("Export Successful", f"Saved as {filename}")


# --- GUI Setup ---
def start_gui():
    root = tk.Tk()
    root.title("Button Logger")

    label = tk.Label(root, text="Monitoring button events from Arduino...")
    label.pack(padx=10, pady=10)

    export_btn = tk.Button(root, text="Print Results", command=export_to_excel)
    export_btn.pack(padx=10, pady=10)

    root.mainloop()


# --- Start Everything ---
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

start_gui()
