# Import the 'serial' module so the computer can talk to the Arduino over USB
import serial

# Import the 'time' module so we can use delays
import time

# Set up a serial connection to the Arduino
# 'COM6' is the port your Arduino is connected to (on Windows). 
# Baudrate is the speed of communication (must match what Arduino uses, usually 9600).
# 'timeout=1' means it will wait 1 second for a response before giving up.
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)

# Wait 2 seconds to give the Arduino time to reset and be ready to communicate
time.sleep(2)

# Create an empty dictionary to store when each button was pressed
# This will help us calculate how long the button was held down
press_times = {}

# Let the user know that the program is now waiting for button data
print("Listening for button events...")

# Start an infinite loop to keep checking for messages from the Arduino
while True:
    # Check if there is any data waiting to be read from the Arduino
    if arduino.in_waiting > 0:
        # Read a line of text from the Arduino, decode it to a string, and remove extra spaces/newlines
        line = arduino.readline().decode().strip()

        # If the line is empty, skip this loop and try again
        if not line:
            continue

        # Print what we received, for debugging or understanding
        print("Received:", line)

        # Split the line into parts (should be something like "button1_pressed 123456")
        parts = line.split()

        # If we didn’t get exactly 2 parts (event and timestamp), skip this loop
        if len(parts) != 2:
            continue

        # Separate the message into the event name and the timestamp
        event, timestamp = parts

        # Convert the timestamp from a string to an integer (milliseconds)
        timestamp = int(timestamp)

        # If the event name contains "_pressed", it means the button was pushed down
        if "_pressed" in event:
            # Get the button name or number (e.g., from "button1_pressed", extract "1")
            button = event.split("_")[1]

            # Save the time the button was pressed in the dictionary
            press_times[button] = timestamp

        # If the event contains "_released", it means the button was let go
        elif "_released" in event:
            # Get the button name or number again
            button = event.split("_")[1]

            # Check if we have a saved time for when this button was pressed
            if button in press_times:
                # Calculate how long the button was held (released time - pressed time)
                duration = timestamp - press_times[button]

                # Print how long the button was held down
                print(f"Button {button} was pressed for {duration} ms")

                # Remove the button press time from the dictionary since we’re done with it
                del press_times[button]
