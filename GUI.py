import tkinter
import tkinter as tk
from tkinter import *
import serial

comPort = 'COM20'
arduino = serial.Serial(comPort, baudrate=9600, timeout=1)


def delete_person():
    arduino.write(b'd')


def add_person():
    arduino.write(b'a')
    send_textbox_data()


def send_textbox_data():
    name = entry_name.get()
    surname = entry_lastname.get()
    code = entry_code.get()
    password = entry_password.get()
    data_to_send = name + '-' + surname + '-' + code + '-' + password
    arduino.write(data_to_send.encode())


def checkSerialPort():
    if arduino.isOpen() and arduino.in_waiting:
        recent_packet = arduino.readline()
        recent_packet_string = recent_packet.decode('utf-8').rstrip('\n\r')
        print(recent_packet_string)
        if recent_packet_string.startswith("Access"):
            packet_string = recent_packet_string.split()
            print(packet_string)
            update_access_label(packet_string[1])

        if recent_packet_string.startswith("RFID UID"):
            recent_packet_string = recent_packet_string[10:].replace(" ", "")
            update_code_label(recent_packet_string)

        if recent_packet_string.startswith("Name: "):
            recent_packet_string = recent_packet_string.split()
            print(recent_packet_string)
            name = recent_packet_string[1]
            lastname = recent_packet_string[2]
            password = recent_packet_string[3]
            update_name_label(name)
            update_last_name_label(lastname)
            update_password_label(password)


def update_code_label(content):
    code.set(content)


def update_name_label(content):
    name.set(content)


def update_last_name_label(content):
    lastname.set(content)


def update_password_label(content):
    password.set(content)


def update_access_label(content):
    access.set(content)


root = Tk()
root.title('Project GUI')

btn_on = tk.Button(root, text="Delete person", command=delete_person)
btn_on.grid(row=0, column=0)

btn_off = tk.Button(root, text="Add person", command=add_person)
btn_off.grid(row=0, column=1)

name = StringVar()
entry_name = Entry(root, textvariable=name, width=10)
entry_name.insert(0, "...")
entry_name_label = tk.Label(root, text="Name")
entry_name_label.grid(row=2, column=0)
entry_name.grid(row=2, column=1)

lastname = StringVar()
entry_lastname = Entry(root, textvariable=lastname, width=10)
entry_lastname.insert(0, "...")
entry_lastname_label = tk.Label(root, text="Lastname")
entry_lastname_label.grid(row=2, column=3)
entry_lastname.grid(row=2, column=6)

code = StringVar()
entry_code = Entry(root, textvariable=code, width=10, state='disabled')
entry_code.insert(0, "########")
entry_code_label = tk.Label(root, text="UID: ")
entry_code_label.grid(row=3, column=0)
entry_code.grid(row=3, column=1)

password = StringVar()
entry_password = Entry(root, textvariable=password, width=5)
entry_password.insert(0, "####")
entry_password_label = tk.Label(root, text="Password: ")
entry_password_label.grid(row=4, column=0)
entry_password.grid(row=4, column=1)

access = StringVar()
entry_access = Entry(root, textvariable=access, width=7)
entry_access.insert(0, "...")
entry_access_label = tk.Label(root, text="Access: ")
entry_access_label.grid(row=5, column=0)
entry_access.grid(row=5, column=1)

root.geometry("300x150")

while True:
    root.update()
    checkSerialPort()
