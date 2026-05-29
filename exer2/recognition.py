import cv2
import numpy as np
import json
import time
import serial
import mysql.connector
from tensorflow.keras.models import load_model

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="fruitinventory"
)
cursor = db.cursor()

machine_status = {}
def parse_status(line):
    # line format: "key=value"
    if '=' in line:
        key, _, value = line.partition('=')
        machine_status[key.strip()] = value.strip()
    # Once all 4 keys are collected, save and clear
    if len(machine_status) == 4:
        save_machine_status(dict(machine_status))
        machine_status.clear()

# save machine status that was read from arduino into the database
def save_machine_status(status):
    sql = """
        INSERT INTO machine_status
            (conveyor1_status, conveyor2_status, current_box_position, arduino_status, last_updated)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        status.get("conveyor1_status", "stopped"),
        status.get("conveyor2_status", "stopped"),
        status.get("current_box_position", "b"),
        status.get("arduino_status", "online")
    )
    cursor.execute(sql, values)
    db.commit()
    print("Saved to MySQL:", status)


# Load the trained model
model = load_model('fruit_recognition_model.h5')

# Load class names from JSON
with open('class_indices.json', 'r') as f:
    fruit_classes = json.load(f)

# Initialize webcam
cap = cv2.VideoCapture(0)
arduino = serial.Serial('COM4', 9600)
time.sleep(2)

confidence_thresh = 0.75 
required_frames = 10           # consecutive frames needed to send the command
stable_confidence_count = 0    # current stable frames with >= confidence thresh
last_sent_fruit = ""
last_sent_time = 0.0           # timestamp of last command sent
cooldown_seconds = 3.0         # seconds to wait before the same fruit can re-trigger

fruit_to_command = {
    "apple": "a",
    "calamansi": "b",
    "lemon": "c"
}

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocess frame
    resized = cv2.resize(frame, (100, 100))
    normalized = resized / 255.0
    input_tensor = np.expand_dims(normalized, axis=0)
    
    # Predict
    predictions = model.predict(input_tensor, verbose=0)
    print("Raw Predictions:", predictions)  # Debug: Print raw predictions
    
    class_idx = np.argmax(predictions)
    confidence = np.max(predictions)

    fruit_name = fruit_classes[class_idx]
    label = f"{fruit_name} ({confidence:.2f})"

    if confidence >= confidence_thresh:
        stable_confidence_count +=1
    else:
        stable_confidence_count = 0

    # send fruit command if confidence stays stable for at least 10 frames
    if stable_confidence_count >= required_frames:
        stable_confidence_count = 0  # reset counter regardless of outcome

        # get current time and check how much time has passed since then
        now = time.time()
        time_since_last = now - last_sent_time
        # prevent spamming arduino with the same command if its still on the same fruit
        same_fruit_on_cooldown = (fruit_name == last_sent_fruit) and (time_since_last < cooldown_seconds)
 
        if fruit_name in fruit_to_command and not same_fruit_on_cooldown:
            command = fruit_to_command[fruit_name]
            arduino.write(command.encode())
            print(f"Sent to Arduino: '{command}' ({fruit_name}, confidence: {confidence:.2f})")
            last_sent_fruit = fruit_name
            last_sent_time = now

    # update display based on confidence
    if confidence >= confidence_thresh:
        display_label = f"{fruit_name} ({confidence:.2f})"
        color = (0, 255, 0)
    else:
        display_label = f"No fruit detected ({confidence:.2f})"
        color = (255, 0, 0)

    cv2.putText(frame, display_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow('Fruit Recognition', frame)

    if arduino.in_waiting > 0:
        line = arduino.readline().decode("utf-8").strip()
        if line.startswith("conveyor1_status"):		
            status = parse_status(line)		
            save_machine_status(status)
    
    if cv2.waitKey(1) == ord('q'):
        break
        

cap.release()
arduino.close()
cv2.destroyAllWindows()
