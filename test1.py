import pytest
import os
import socket
import threading
from serv import main as server_main
from cli import main as client_main
import time

IP = "10.30.201.56"
PORT = 4456
SIZE = 1024
FORMAT = "utf"
SERVER_FOLDER = "server_folder"
CLIENT_FOLDER = "client_folder"
FILES_DIRECTORY = "files"

def test_file_transfer():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=server_main)
    server_thread.start()

    # Give the server a second to start
    time.sleep(1)

    # Run the client
    client_main()

    # Check if the files have been transferred correctly
    client_files_directory = os.path.join(CLIENT_FOLDER, FILES_DIRECTORY)
    server_files_directory = os.path.join(SERVER_FOLDER, CLIENT_FOLDER, FILES_DIRECTORY)
    
    # Test for connection
    assert server_thread.is_alive(), "Server is not running."
    print("Passed: Server is running.")

    # Test for file upload name consistency and contents of the file
    for filename in os.listdir(client_files_directory):
        client_file_path = os.path.join(client_files_directory, filename)
        server_file_path = os.path.join(server_files_directory, filename)
        
        # Test if the file is uploaded to the server
        assert os.path.exists(server_file_path), f"File {filename} does not exist on the server."
        print(f"Passed: File {filename} exists on the server.")
        
        # Test if the contents of the file are correct
        with open(client_file_path, 'r') as client_file:
            with open(server_file_path, 'r') as server_file:
                assert client_file.read() == server_file.read(), f"Contents of the file {filename} are not correct."
                print(f"Passed: Contents of the file {filename} are correct.")

    # Close the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((IP, PORT))
    server_socket.send("CLOSE:Test completed".encode(FORMAT))
    server_socket.close()

    # Wait for the server thread to finish
    server_thread.join()
