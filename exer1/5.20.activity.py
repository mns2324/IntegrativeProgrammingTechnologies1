import serial
import time

arduino = serial.Serial('COM4', 9600)
time.sleep(2)

while True:
    print("Enter A, B, or C to shift basket")
    cmd = input("").lower()
    print("command entered: " +cmd)

    if cmd == "a":
        arduino.write(b'a')
        print("Sent a")

    elif cmd == "b":
        arduino.write(b'b')
        print("Sent b")

    elif cmd == "c":
        arduino.write(b'c')
        print("Sent c")
        
    else:
        print("Invalid input")


