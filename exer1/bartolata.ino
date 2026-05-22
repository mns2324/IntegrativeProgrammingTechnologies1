#define CLOCKWISE 1
#define COUNTERCLOCKWISE 0

// =============================
// MOTOR PIN ARRAYS
// =============================
int motor1Pins[] = {10, 11, 12, 13};
int motor2Pins[] = {A2, A3, A4, A5};

// =============================
// STEP VARIABLES
// =============================
int currentStep1 = 0;
int currentStep2 = 0;
char currentBasket = 'b'; // basket b as the default center

// =============================
// SERIAL COMMAND VARIABLE
// =============================
char command;

// step sequence for handling motor rotation
int stepSequence[4][4] = {

  {HIGH, HIGH, LOW, LOW},
  {LOW, HIGH, HIGH, LOW},
  {LOW, LOW, HIGH, HIGH},
  {HIGH, LOW, LOW, HIGH}
};

void setup() {

  Serial.begin(9600);

  // =============================
  // INITIALIZE MOTOR 1 PINS
  // =============================
  for (int i = 0; i < 4; i++) {

    pinMode(motor1Pins[i], OUTPUT);
  }

  // =============================
  // INITIALIZE MOTOR 2 PINS
  // =============================
  for (int i = 0; i < 4; i++) {

    pinMode(motor2Pins[i], OUTPUT);
  }

  Serial.println("Dual Stepper Motor System Ready");
}

void loop() {

  // =============================
  // READ SERIAL COMMAND
  // =============================
  if (Serial.available() > 0) {

    command = Serial.read();
  }

  // ignore repeated commands
  if (command == currentBasket) {
    command = '\0';
  }

  //// motor control for shifting basket position
  // if command a: basket b -> ccw for 1 second, basket c -> ccw for 2 seconds
  if (command == 'a') {

    if (currentBasket == 'b'){
      for(int i = 0; i < 1000; i++){
        moveMotor(motor2Pins, currentStep2, COUNTERCLOCKWISE);
      }
    }
    else if (currentBasket == 'c'){
      for(int i = 0; i < 2000; i++){
        moveMotor(motor2Pins, currentStep2, COUNTERCLOCKWISE);
      }     
    }

    stopAllMotors();

    currentBasket = 'a';
    command = '\0'; // set command to null again
  }

  // if command b: basket a -> cw for 1 second, basket c -> ccw for 1 second
  else if (command == 'b') {
    
    if (currentBasket == 'a'){
      for(int i = 0; i < 1000; i++){
        moveMotor(motor2Pins, currentStep2, CLOCKWISE);
      }
    }
    else if (currentBasket == 'c'){
      for(int i = 0; i < 1000; i++){
        moveMotor(motor2Pins, currentStep2, COUNTERCLOCKWISE);
      }
    }
    
    stopAllMotors();

    currentBasket = 'b';
    command = '\0'; // set command to null again
  }

  // if command c: basket a -> cw for 2 seconds, basket b -> cw for 1 second
  else if (command == 'c') {
    
    if (currentBasket == 'a'){
      for(int i = 0; i < 2000; i++){
        moveMotor(motor2Pins, currentStep2, CLOCKWISE);
      }
    }
    else if (currentBasket == 'b'){
      for(int i = 0; i < 1000; i++){
        moveMotor(motor2Pins, currentStep2, CLOCKWISE);
      }
    }
    
    stopAllMotors();

    currentBasket = 'c';
    command = '\0'; // set command to null again
  }
}

// =============================
// GENERIC MOTOR FUNCTION
// =============================
void moveMotor(int motorPins[], int &currentStep, int direction) {

  // =============================
  // OUTPUT STEP SEQUENCE
  // =============================
  for (int i = 0; i < 4; i++) {

    digitalWrite(motorPins[i], stepSequence[currentStep][i]);
  }

  // =============================
  // UPDATE STEP INDEX
  // =============================
  if (direction == CLOCKWISE) {
    currentStep = (currentStep + 1) % 4;
  }

  else {
    currentStep = (currentStep - 1 + 4) % 4;
  }

  delayMicroseconds(2000);
}

// =============================
// STOP BOTH MOTORS
// =============================
void stopAllMotors() {

  for (int i = 0; i < 4; i++) {

    digitalWrite(motor1Pins[i], LOW);
    digitalWrite(motor2Pins[i], LOW);
  }
}
