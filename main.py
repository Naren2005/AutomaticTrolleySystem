import cv2
from pyzbar.pyzbar import decode
import serial
from collections import Counter
import pandas as pd
import warnings
from Database import send_sms

warnings.filterwarnings('ignore')



SerialComm = serial.Serial('COM6', baudrate=9600, timeout=0.5)
total_price = 0
Item_list = []

def BarCodeDetector():
    global total_price
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,280)
    cap.set(cv2.CAP_PROP_FPS,120)


    Temp_list = []

    while True:
        ret, frame = cap.read() # frame is a numpy array
        decoded_objects = decode(frame)  # List of decoded obj, deletes after detected instantly

        for obj in decoded_objects:
            objectData = obj.data.decode('utf-8')
            Temp_list.append(objectData)
            if objectData not in Item_list:
                if check_frequency(objectData,Temp_list) == True:
                    send_data_to_arduino("2")
                    send_data_to_arduino("1")
                    Item_list.append(objectData)
                    serial_checker(objectData)
                    Temp_list.clear()
            else:
                if check_frequency(objectData,Temp_list) == True:
                    send_data_to_arduino("3")
                    Item_list.remove(objectData)
                    Temp_list.clear()

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

def check_frequency(item_to_check, input_list):
    # Use Counter to count the frequency of each item in the list
    frequency_counter = Counter(input_list)

    # Check if the frequency of the specified item is above 20
    if frequency_counter[item_to_check] > 50:
        return True

def serial_checker(serialcode):
    # Replace 'your_excel_file.xlsx' with the actual path to your Excel file
    excel_file_path = 'Lists.xlsx'
    # Read the data from the Excel sheet into a DataFrame
    df = pd.read_excel(excel_file_path)

    # Your 6-digit number
    barcode = serialcode

    # Check if the number exists in the 'Number' column
    if barcode in df['S.No'].values:
        # Retrieve the corresponding Name and Date
        row = df[df['S.No'] == barcode]
        price = row['MRP'].values[0]
        item_name = row['product'].values[0]  # Replace 'Date' with the actual column name

        global total_price
        total_price += price

        print(f"{item_name} : {price} Rs         Total: {total_price}")
        print("")
    else:
        print(f"This code: {barcode} does not exist in our Datasheet.")

main()
for i in Item_list:
    serial_checker(i)
