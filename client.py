import socket

IP = socket.gethostbyname(socket.gethostname())
UTF_FORMAT = "utf-8"
SIZE = 1024


def execute_client(client, address):
    client.connect(address)

    print("Connected to the Server")

    while True:

        command = input("enter get or upload command along with file name:\n")

        client.send(command.encode(UTF_FORMAT))

        message = client.recv(SIZE).decode(UTF_FORMAT)
        if message == "ack":
            print("Server received the command")

        if "get" in command:
            print("get command received")
            filename = command.split(" ")[1].strip()
            fileToWrite = open("new_" + filename, "wb")
            client.send(b'start sending')
            data = client.recv(SIZE)
            while data != b'' and data != b'END':
                print("Downloading...")
                client.send(b'ack')
                fileToWrite.write(data)
                data = client.recv(SIZE)
            client.send(b'writing finished')
            fileToWrite.close()
            print("File received and saved\n\n")

        elif "upload" in command:
            print("upload command")
            filename = command.split(" ")[1].strip()
            fileToSend = open(filename, "rb")

            data = fileToSend.read(SIZE)
            while data:
                print("Sending...")
                client.send(data)
                if b'ack' != client.recv(SIZE):
                    break
                data = fileToSend.read(SIZE)
            client.send(b'END')
            fileToSend.close()
            print("file sending completed...\n\n\n")

        else:
            print("Please enter a valid command")

        endMessage = client.recv(SIZE)
        if endMessage != b'--END--':
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        connectCommand = input("Please enter the command to connect to the server:\n")

        if connectCommand.split(" ")[0] == "ftpclient":
            serverPort = connectCommand.split(" ")[1].strip()
            try:
                server_address = ("localhost", int(serverPort))
                execute_client(client, server_address)
            except:
                print("Error connecting to the Server => " + IP + ":" + str(serverPort))

        else:
            print("Enter valid command")

if __name__ == "__main__":
    main()
