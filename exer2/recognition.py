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
last_conveyor_state = None
last_logged_fruit = ""
last_logged_confidence = 0.0

# =============================
# PARSE ARDUINO STATUS LINE
# =============================
def parse_status(line):
    # declare as global here to correctly update these variables outside the function
    global last_conveyor_state, last_logged_fruit, last_logged_confidence
    
    # ["conveyor1_status=running", "conveyor2_status=stopped", ...]
    parts = line.split(",")
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            # machine_status = {"conveyor1_status": "running", "conveyor2_status": "stopped", ...}
            machine_status[key.strip()] = value.strip()

    # only proceeds once all 4 keys are collected
    if len(machine_status) == 4:
        save_machine_status(machine_status) 

        # grab current conveyor state
        conv1 = machine_status.get("conveyor1_status")
        conv2 = machine_status.get("conveyor2_status")
        current_state = (conv1, conv2)

        # only runs if a fruit was detected AND the conveyor state actually changed
        if last_logged_fruit and current_state != last_conveyor_state:
            # step 2/3: conveyor1 stopped, conveyor2 moving = shifting basket position
            if conv1 == "stopped" and conv2 == "running":
                log_sort_event(last_logged_fruit, last_logged_confidence, f"move_to_{last_logged_fruit}_box")
            # step 3/3: conveyor1 running again after both were stopped = fruit dropped
            elif conv1 == "running" and conv2 == "stopped" and last_conveyor_state == ("stopped", "stopped"):
                log_sort_event(last_logged_fruit, last_logged_confidence, "drop_fruit")

        # remember last state for next comparison and clear dict for next arduino message
        last_conveyor_state = current_state
        machine_status.clear()

# =============================
# DEDICATED ARDUINO READ FUNCTION
# =============================
def read_arduino_status():
    # only reads if arduino has actually sent something
    if arduino.in_waiting > 0:
        line = arduino.readline().decode("utf-8", errors="ignore").strip()
        # if it's a status update, parse it
        if line.startswith("conveyor1_status"):
            parse_status(line)
        else:
            print("[Arduino]", line)

# =============================
# SAVE SORTING LOGS
    ### called 3 times per fruit cycle
    # "fruit_detected": when AI first confirms the fruit
    # "move_to_fruit_box": when conveyor2 starts moving
    # "drop_fruit": when conveyor1 resumes after basket is in position
# =============================
def log_sort_event(fruit_name, confidence, action):
    fruit_ids = {"apple": 1, "calamansi": 2, "lemon": 3}
    if fruit_name not in fruit_ids:
        return
        
    sql = """
        INSERT INTO sorting_logs
            (fruit_id, detected_label, confidence_score, detection_datetime, conveyor_action)
        VALUES (%s, %s, %s, NOW(), %s)
    """
    # timestamp is handled by sql, no need to include it here
    values = (fruit_ids[fruit_name], fruit_name, confidence, action)
    cursor.execute(sql, values)
    db.commit()
    print(f"Logged: {fruit_name} -> {action} ({confidence:.2f})")

# =============================
# SAVE MACHINE STATUS TO MySQL
# =============================
def save_machine_status(status):
    sql = """
        INSERT INTO machine_status
            (conveyor1_status, conveyor2_status, current_box_position, arduino_status)
        VALUES (%s, %s, %s, %s)
    """
    # .get() with a default means if the key is missing, use the default instead of crashing
    values = (
        status.get("conveyor1_status", "stopped"),
        status.get("conveyor2_status", "stopped"),
        status.get("current_box_position", "b"),
        status.get("arduino_status", "online")
    )
    # save to the db
    cursor.execute(sql, values)
    db.commit()
    print("Saved to MySQL:", status)

# =============================
# LOAD MODEL AND SETUP
# =============================
model = load_model('fruit_recognition_model.h5')

with open('class_indices.json', 'r') as f:
    fruit_classes = json.load(f)

cap = cv2.VideoCapture(0)
arduino = serial.Serial('COM4', 9600)
time.sleep(2)

confidence_thresh = 0.80
required_frames = 15
stable_confidence_count = 0
last_sent_fruit = ""
last_sent_time = 0.0
cooldown_seconds = 3.0

fruit_to_command = {
    "apple": "a",
    "calamansi": "b",
    "lemon": "c"
}

# =============================
# MAIN LOOP
# =============================
try:
    while True:
        # reads one frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # preprocess and normalize frame
        resized = cv2.resize(frame, (100, 100))
        normalized = resized / 255.0
        input_tensor = np.expand_dims(normalized, axis=0)

        # passes the image through the AI model and returns probs
        predictions = model.predict(input_tensor, verbose=0)
        # gets the index of the highest probability and the actual highest probablity value
        class_idx = np.argmax(predictions)
        confidence = np.max(predictions)
        # maps the index to the fruit name using class_indices.json
        fruit_name = fruit_classes[class_idx]

        # resets to 0 if confidence drops, prevents false positives
        if confidence >= confidence_thresh:
            stable_confidence_count += 1
        else:
            stable_confidence_count = 0

        if stable_confidence_count >= required_frames:
            stable_confidence_count = 0

            # checks how many seconds since last command was sent
            now = time.time()
            time_since_last = now - last_sent_time

            # True if same fruit AND less than 3 seconds have passed
            # prevents spamming arduino with the same command repeatedly
            same_fruit_on_cooldown = (fruit_name == last_sent_fruit) and (time_since_last < cooldown_seconds)

            # only sends command if fruit is recognized AND not on cooldown
            if fruit_name in fruit_to_command and not same_fruit_on_cooldown:
                command = fruit_to_command[fruit_name]
                # converts "a"/"b"/"c" string to bytes and sends to Arduino via serial
                arduino.write(command.encode())
                print(f"Sent to Arduino: '{command}' ({fruit_name}, confidence: {confidence:.2f})")

                # updates cooldown tracking variables
                last_sent_fruit = fruit_name
                last_sent_time = now

                # stores for use in parse_status() steps 2 and 3
                last_logged_fruit = fruit_name
                last_logged_confidence = float(confidence)

                # step 1/3: fruit detected by AI
                # steps 2 and 3 are triggered later by arduino status changes
                log_sort_event(fruit_name, float(confidence), f"{fruit_name}_detected")

        # update webcam display
        if confidence >= confidence_thresh:
            display_label = f"{fruit_name} ({confidence:.2f})"
            color = (0, 255, 0)
        else:
            display_label = f"No fruit detected ({confidence:.2f})"
            color = (255, 0, 0)

        cv2.putText(frame, display_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow('Fruit Recognition', frame)

        # read conveyor status sent by arduino
        read_arduino_status()

        if cv2.waitKey(1) == ord('q'):
            break

finally:
    cap.release()
    arduino.close()
    cv2.destroyAllWindows()
