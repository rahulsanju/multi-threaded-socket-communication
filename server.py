import socket
from _thread import *
import threading

PORT = 7999
HOST = "localhost"
FORMAT = "utf-8"

lock = threading.Lock()


def process_client_request(s, conn, thread_name):

    try:
        while True:
            print("connection started in thread : "+thread_name)
            command = conn.recv(1024).decode(FORMAT)
            conn.send((thread_name + " acknowledgement").encode(FORMAT))
            print("command received (" + thread_name + "): " + command)
            if "get" in command and (conn.recv(1024) == b'start sending'):
                print(thread_name+"get command Received")
                lock.acquire()
                filename = command.split(" ")[1].strip()
                fileToSend = open(filename, "rb")

                data = fileToSend.read(1024)
                while data:
                    # print(thread_name+"Sending...")
                    conn.send(data)
                    if b'ack' != conn.recv(1024):
                        break
                    data = fileToSend.read(1024)
                conn.send(b'END')
                fileToSend.close()
                if conn.recv(1024) != b'writing finished':
                    break
                lock.release()
                print(thread_name+"file sending completed...\n\n\n")

            elif "upload" in command:
                print(thread_name+"upload command received")
                lock.acquire()
                filename = command.split(" ")[1].strip()
                fileToWrite = open("new_" + filename, "wb")

                data = conn.recv(1024)
                while data != b'' and data != b'END':
                    # print(thread_name+"Receiving...")
                    conn.send(b'ack')
                    fileToWrite.write(data)
                    data = conn.recv(1024)

                fileToWrite.close()
                lock.release()
                print(thread_name+"File recevied and saved\n\n")

            conn.send(b'--END--')

    except:
        s.close()


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print("started server on port : ", PORT)

    # put the socket into listening mode
    s.listen(2)
    counter = 1
    while True:
        conn, address = s.accept()

        start_new_thread(process_client_request, (s, conn, "Thread-" + str(counter)))
        counter = counter + 1


if __name__ == "__main__":
    start_server()
