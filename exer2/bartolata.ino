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
char detectedFruit;

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

    detectedFruit = Serial.read();
  }
    
  // ignore repeated commands
  if (detectedFruit == currentBasket) {
    detectedFruit = '\0';
  }

  //// motor 2 control for shifting basket position
  // if detectedFruit a: basket b -> ccw for 1 second, basket c -> ccw for 2 seconds
  if (detectedFruit == 'a') {

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

    stopMotor(motor2Pins);
    // motor 1 control moves a bit to drop fruit into basket below if confident enough
    for(int i = 0; i < 500; i++){
      moveMotor(motor1Pins, currentStep1, CLOCKWISE);
    }
    
    currentBasket = 'a';
    detectedFruit = '\0'; // set command to null again
  }

  // if command b: basket a -> cw for 1 second, basket c -> ccw for 1 second
  else if (detectedFruit == 'b') {
    
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

    stopMotor(motor2Pins);
    // motor 1 control moves a bit to drop fruit into basket below if confident enough
    for(int i = 0; i < 500; i++){
      moveMotor(motor1Pins, currentStep1, CLOCKWISE);
    }

    currentBasket = 'b';
    detectedFruit = '\0'; // set command to null again
  }

  // if command c: basket a -> cw for 2 seconds, basket b -> cw for 1 second
  else if (detectedFruit == 'c') {
    
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

    stopMotor(motor2Pins);
    // motor 1 control moves a bit to drop fruit into basket below if confident enough
    for(int i = 0; i < 500; i++){
      moveMotor(motor1Pins, currentStep1, CLOCKWISE);
    }

    currentBasket = 'c';
    detectedFruit = '\0'; // set command to null again
  }
  else {
    // move continuously until a new fruit is spotted
    moveMotor(motor1Pins, currentStep1, CLOCKWISE);
  }
}

// communicate status to python
void sendMachineStatus() {
  Serial.print("conveyor1_status=");
  Serial.print(conveyor1_status);
  
  Serial.print("conveyor2_status=");
  Serial.print(conveyor2_status);
  
  Serial.print("current_box_position=");
  Serial.print(current_box_position);
  
  Serial.print("arduino_status=");
  Serial.println(arduino_status);
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

void stopMotor(int motorPins[]) {
  for(int i = 0; i < 4; i++){
    digitalWrite(motorPins[i], LOW);
  }
}


void stopAllMotors() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(motor1Pins[i], LOW);
    digitalWrite(motor2Pins[i], LOW);
  }
}
