import os
import socket
import time

IP = "10.30.201.56"
PORT = 4456
SIZE = 1024
FORMAT = "utf"
CLIENT_FOLDER = "client_folder"

def main():
    """ Starting a tcp socket """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    """ Folder path """
    path = os.path.join(CLIENT_FOLDER, "files")
    folder_name = path.split("/")[-1]

    """ Sending the folder name """
    msg = f"{folder_name}"
    print(f"[CLIENT] Sending folder name: {folder_name}")
    client.send(msg.encode(FORMAT))

    """ Receiving the reply from the server """
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER] {msg}\n")

    """ Sending files """
    files = sorted(os.listdir(path))

    for file_name in files:
        """ Send the file name """
        msg = f"FILENAME:{file_name}"
        print(f"[CLIENT] Sending file name: {file_name}")
        client.send(msg.encode(FORMAT))

        """ Recv the reply from the server """
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        """ Send the data """
        file = open(os.path.join(path, file_name), "r")
        file_data = file.read()

        start_time = time.time()  # Record the time before sending the file data

        #FOR HIGH SPEED TESTING
        msg = f"DATA:{file_data}"
        client.send(msg.encode(FORMAT))


        #FOR LOW SPEED TESTING
        '''for chunk in file_data:
            msg = f"DATA:{chunk}"
            client.send(msg.encode(FORMAT))
            time.sleep(0.01)
        ''' 
        end_time = time.time()  # Record the time after the file data is sent

        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        # Calculate the speed of the file transfer
        elapsed_time = end_time - start_time
        file_size = len(file_data)
        # Calculate the speed of the file transfer
        if elapsed_time > 0:
            speed = file_size / elapsed_time
            print(f"[CLIENT] File transfer speed: {speed:.2f} bytes/sec\n")
        else:
            print("[CLIENT] File transferred instantaneously.\n")


        """ Sending the close command """
        msg = f"FINISH:Complete data send"
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

    """ Closing the connection from the server """
    msg = f"CLOSE:File transfer is completed"
    client.send(msg.encode(FORMAT))
    client.close()

if __name__ == "__main__":
    main()
