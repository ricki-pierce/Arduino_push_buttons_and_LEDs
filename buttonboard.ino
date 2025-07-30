// Button pins
const int buttonPins[3] = {5, 6, 7};
// LED pins
const int ledPins[3] = {10, 11, 12};

// State tracking
bool lastState[3] = {LOW, LOW};
unsigned long pressStart[3] = {0, 0};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) {
    pinMode(buttonPins[i], INPUT);
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
}

void loop() {
  for (int i = 0; i < 3; i++) {
    bool current = digitalRead(buttonPins[i]);

    // Button pressed
    if (current == HIGH && lastState[i] == LOW) {
      pressStart[i] = millis();
      digitalWrite(ledPins[i], HIGH);
      Serial.print("button_");
      Serial.print(i + 1);
      Serial.print("_pressed ");
      Serial.println(pressStart[i]);
      lastState[i] = HIGH;
    }

    // Button released
    else if (current == LOW && lastState[i] == HIGH) {
      unsigned long pressEnd = millis();
      digitalWrite(ledPins[i], LOW);
      Serial.print("button_");
      Serial.print(i + 1);
      Serial.print("_released ");
      Serial.println(pressEnd);
      lastState[i] = LOW;
    }
  }

  delay(5); // small debounce delay
}
