import cv2
import os

# Define fruit classes and directories
fruit_classes = ['apple', 'lemon', 'calamansi']
dataset_dir = 'dataset'

# Create dataset directory
os.makedirs(dataset_dir, exist_ok=True)

# Capture images for each class
for fruit in fruit_classes:
    class_dir = os.path.join(dataset_dir, fruit)
    os.makedirs(class_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    print(f"Press 's' to capture images for {fruit}. Press 'q' to quit.")
    
    count = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow('Webcam', frame)
        key = cv2.waitKey(1)
        
        if key == ord('s'):
            img_path = os.path.join(class_dir, f'{fruit}_{count}.jpg')
            cv2.imwrite(img_path, frame)
            print(f"Saved {img_path}")
            count += 1
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()