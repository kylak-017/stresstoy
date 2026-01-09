const int JOYSTICK_X = A0;
const int JOYSTICK_Y = A1;
const int BUTTON_PIN = 2;

const int THRESHOLD = 512;
const int DEADZONE = 100;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int xValue = analogRead(JOYSTICK_X);
  int yValue = analogRead(JOYSTICK_Y);
  int buttonState = digitalRead(BUTTON_PIN);
  
  bool highEnergy = (yValue > THRESHOLD + DEADZONE);
  bool lowEnergy = (yValue < THRESHOLD - DEADZONE);
  
  bool energyRight = highEnergy && !lowEnergy;
  
  bool outside = (xValue > THRESHOLD + DEADZONE);
  bool inside = (xValue < THRESHOLD - DEADZONE);
  
  bool locationRight = outside && !inside;
  
  bool timeRight = (buttonState == LOW);
  
  byte dataByte = 0;
  if (energyRight) {
    dataByte |= (1 << 0);
  }
  if (timeRight) {
    dataByte |= (1 << 1);
  }
  if (locationRight) {
    dataByte |= (1 << 2);
  }
  
  Serial.write(dataByte);
  
  delay(100);
}
