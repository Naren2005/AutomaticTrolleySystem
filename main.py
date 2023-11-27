import cv2
from pyzbar.pyzbar import decode
import serial
import time

SerialComm = serial.Serial('COM6', baudrate=9600, timeout=0.5)

def BarCodeDetector():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,280)
    cap.set(cv2.CAP_PROP_FPS, 120)

    Item_list = []

    while True:
        ret, frame = cap.read()
        decoded_objects = decode(frame)  # list of decoded obj, deletes after detected instantly
        for obj in decoded_objects:
            print(f"Type: {obj.type}, Data: {obj.data.decode('utf-8')}")
            if obj.data.decode('utf-8') in Item_list:
                send_data_to_arduino("3")
            else:
                print(f"Type: {obj.type}, Data: {obj.data.decode('utf-8')}")
                Item_list.append(obj.data.decode('utf-8'))
                send_data_to_arduino("1")
                send_data_to_arduino("2")

        cv2.imshow("Bar Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    print(Item_list)


    cap.release()
    cv2.destroyAllWindows()

def main():
    BarCodeDetector()


def send_data_to_arduino(data):
    SerialComm.write(data.encode())

def read_data_from_arduino():
    print(SerialComm.readline().decode('ascii'))
main()
