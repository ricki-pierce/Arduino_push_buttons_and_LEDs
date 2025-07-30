// Button pins
const int buttonPins[3] = {5, 6, 7};  // Creates an array of pin numbers for 3 buttons connected to digital pins 5, 6, and 7

// LED pins
const int ledPins[3] = {10, 11, 12};  // Creates an array of pin numbers for 3 LEDs connected to digital pins 10, 11, and 12

// State tracking
bool lastState[3] = {LOW, LOW};       // Tracks whether each button was previously pressed (HIGH) or not pressed (LOW). Starts with LOW.
unsigned long pressStart[3] = {0, 0}; // Stores the time (in milliseconds) when a button was pressed. Used to measure how long it's held.

void setup() {
  Serial.begin(9600);  // Starts serial communication at 9600 bits per second. Useful for printing messages to your computer.

  // Loop through each button and LED pin to set them up
  for (int i = 0; i < 3; i++) {
    pinMode(buttonPins[i], INPUT);     // Sets each button pin as an input so we can read if it's pressed or not
    pinMode(ledPins[i], OUTPUT);       // Sets each LED pin as an output so we can turn it on or off
    digitalWrite(ledPins[i], LOW);     // Makes sure all LEDs start in the OFF state
  }
}

void loop() {
  // Check each button one by one
  for (int i = 0; i < 3; i++) {
    bool current = digitalRead(buttonPins[i]);  // Read the current state of the button (HIGH = pressed, LOW = not pressed)

    // If the button is currently being pressed and wasn't before
    if (current == HIGH && lastState[i] == LOW) {
      pressStart[i] = millis();                // Save the current time (in ms since the program started) to mark when the button was pressed
      digitalWrite(ledPins[i], HIGH);          // Turn on the LED to show the button is being pressed
      Serial.print("button_");                 // Print to serial monitor: beginning of message
      Serial.print(i + 1);                     // Print which button number (1, 2, or 3)
      Serial.print("_pressed ");               // Add "pressed" text
      Serial.println(pressStart[i]);           // Print the timestamp of when the button was pressed
      lastState[i] = HIGH;                     // Update the last state to show that the button is now pressed
    }

    // If the button is currently NOT being pressed but was before
    else if (current == LOW && lastState[i] == HIGH) {
      unsigned long pressEnd = millis();       // Save the current time as when the button was released
      digitalWrite(ledPins[i], LOW);           // Turn off the LED because the button is no longer being pressed
      Serial.print("button_");                 // Print to serial monitor: beginning of message
      Serial.print(i + 1);                     // Print which button number (1, 2, or 3)
      Serial.print("_released ");              // Add "released" text
      Serial.println(pressEnd);                // Print the timestamp of when the button was released
      lastState[i] = LOW;                      // Update the last state to show that the button is now released
    }
  }

  delay(5); // Short pause (5 milliseconds) to help avoid bouncing issues (where button press is read multiple times quickly)
}
