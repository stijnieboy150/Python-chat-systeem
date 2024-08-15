import socket
from tkinter import *
from threading import Thread
from datetime import datetime

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
separator_token = ""

s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))

def send_message():
    message = message_entry.get()
    receiver = to_entry.get()
    if message.lower() == 'q':
        s.close()
        root.quit()
    else:
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name = name_entry.get()
        if receiver:
            to_send = f"[{date_now}] {name} (Naar {receiver}): {message}"
        else:
            to_send = f"[{date_now}] {name}: {message}"
        s.send(to_send.encode())

def listen_for_messages():
    while True:
        try:
            message = s.recv(1024).decode()
            chat_display.insert(END, f"{message}\n")
        except ConnectionResetError:
            break

root = Tk()
root.title("Chat Client")

name_label = Label(root, text="Gebruikersnaam:")
name_label.pack()

name_entry = Entry(root, width=50)
name_entry.pack()

to_label = Label(root, text="Naar: (let op iedereen kan zien naar wie jij dat stuurt)")
to_label.pack()

to_entry = Entry(root, width=50)
to_entry.pack()

message_label = Label(root, text="Bericht:")
message_label.pack()

message_entry = Entry(root, width=50)
message_entry.pack()

send_button = Button(root, text="Stuur bericht", command=send_message)
send_button.pack()

chat_display = Text(root, height=20, width=50)
chat_display.pack()

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

root.mainloop()