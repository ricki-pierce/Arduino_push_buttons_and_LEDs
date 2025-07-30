import serial
import time

# Change 'COM3' to your actual port on Windows, or '/dev/ttyACM0' on Linux/Mac
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
time.sleep(2)  # wait for Arduino to reset

press_times = {}

print("Listening for button events...")

while True:
    if arduino.in_waiting > 0:
        line = arduino.readline().decode().strip()
        if not line:
            continue
        print("Received:", line)
        parts = line.split()
        if len(parts) != 2:
            continue

        event, timestamp = parts
        timestamp = int(timestamp)

        if "_pressed" in event:
            button = event.split("_")[1]
            press_times[button] = timestamp
        elif "_released" in event:
            button = event.split("_")[1]
            if button in press_times:
                duration = timestamp - press_times[button]
                print(f"Button {button} was pressed for {duration} ms")
                del press_times[button]
