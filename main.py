import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import serial
from collections import Counter
import pandas as pd
import warnings
import colorama


warnings.filterwarnings("ignore",category=UserWarning)

mydict = {}

SerialComm = serial.Serial('COM5', baudrate=9600, timeout=0.5)
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
            pts = np.array([obj.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame,[pts],True,(255,0,255),5)
            pts2 = obj.rect
            cv2.putText(frame,objectData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
            Temp_list.append(objectData)
            if objectData not in Item_list:
                if check_frequency(objectData,Temp_list) == True:
                    send_data_to_arduino("2")
                    send_data_to_arduino("1")
                    Item_list.append(objectData)
                    serial_checker(objectData,True)
                    Temp_list.clear()
            else:
                if check_frequency(objectData,Temp_list) == True:
                    send_data_to_arduino("3")
                    send_data_to_arduino("4")
                    Item_list.remove(objectData)
                    serial_checker(objectData,False)
                    Temp_list.clear()

        cv2.imshow("Bar Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break


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
    if frequency_counter[item_to_check] > 40:
        return True

def serial_checker(serialcode,condition):
    # Replace 'your_excel_file.xlsx' with the actual path to your Excel file
    excel_file_path = 'Lists.xlsx'
    # Read the data from the Excel sheet into a DataFrame
    df = pd.read_excel(excel_file_path)

    # Your 6-digit number
    barcode = serialcode
    barcode = barcode.strip()
    barcode = str(barcode)

    # Check if the number exists in the 'Number' column
    if barcode in df['S.No'].values:
        # Retrieve the corresponding Name and Date
        row = df[df['S.No'] == barcode]
        price = row['MRP'].values[0]
        item_name = row['product'].values[0]  # Replace 'Date' with the actual column name


        global mydict
        global total_price

        if condition == True:
            mydict[item_name] = price
            total_price += price
            k = f"+Added {item_name} : {price} Rs         Total: {total_price}"
            print(colorama.Fore.GREEN + k)
            print("")
        elif condition == False:
            mydict.pop(item_name)
            total_price -= price
            t = f"-Removed {item_name} : {price} Rs         Total: {total_price}"
            print(colorama.Fore.RED + t)
            print("")

    else:
        print(f"{colorama.Fore.LIGHTMAGENTA_EX}This code: {barcode} does not exist in our Datasheet.")
        print(barcode)

from twilio.rest import Client
account_sid = "ACa28af891c27eceb77f6c9305511d42eb"
auth_token = "43784ce5d4ee616ecd5684545d4b547f"

client = Client(account_sid,auth_token)

def send_sms(smz):
    client.messages.create(
            to="+919490932710",
            from_="+14439633415",
            body=smz
        )


main()
print(colorama.Fore.BLACK + "------Bill------" +  '\n')
p = " "
for key , values in mydict.items():
    print(f"{colorama.Fore.RESET} {key} : Rs {values} \n")
    p += f"{key} : Rs {values}"
send_sms(p)
