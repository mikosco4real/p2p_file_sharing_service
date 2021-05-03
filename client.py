import pickle
import socket
import os
from peer import Peer
from time import sleep


class Slave:
    master_addr = ("192.168.1.103", 7000)
    slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    file = dict()
    peer = Peer

    def __init__(self) -> None:
        pass

    def connect(self):
        self.slave.connect(self.master_addr)
    
    def send(self, msg, dtype="text", addr=None, filename=None):
        if addr == None:
            self.slave.send(msg.encode())
        elif addr and dtype == "text":
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer:
                    peer.connect(addr)
                    peer.send(msg.encode())
            except Exception as e:
                print("Error Occurred: ", e)
        elif addr and dtype == "file" and filename != None:
            try:
                file_size = os.path.getsize(self.file[filename])
                with open(self.file[filename], 'rb') as file:
                    pass
            except Exception as e:
                print("Error Occured: ", e)
        else:
            pass

    def receive(self, type="text"):
        self.slave.recv(1024)

    def start(self):
        try:
            self.connect()
            self.connected = True
            msg = self.slave.recv(1024).decode()
            print(" ")
            print(msg)
            msg = self.slave.recv(1024).decode()
            print(msg)
            peer = self.slave.recv(1024)
            self.peer = pickle.loads(peer)
        except Exception as e:
            print(e)
        while self.connected:
            self.commands()
            self.route()
    
    def stop(self):
        self.connected = False
        self.slave.close()
    
    def add(self):
        file = input(">>> File path >>> ")
        self.peer.add_file(file)
    
    def remove(self):
        file = input(">>> filename >>> ")
        remove = self.peer.remove_file(file)
        if remove:
            print("File removed successfully")

    def search(self):
        filename = input(">>> filename >>> ")
        item = self.peer.search_file(filename)
        if item:
            print("Hurray! This item is available for download")
        else:
            print("Item not Found!")
    
    def show(self):
        print()
        print("All files")
        all_files = self.peer.show_files()
        print(all_files)
    
    def download(self):
        filename = input(">>> Filename >>> ")
        if self.peer.search_file(filename):
            print("File Found! ")
            print("Preparing to Download ... ")
            sleep(0.3)
            print("Downloading . . .")
            sleep(2)
            print("Download Completed")
        else:
            print("Sorry, File is not Found on the Network")
    
    def commands(self):
        print("")
        print("Available Commands")
        print("_" *50)
        print("")

        commands = {"add": "You will be able to add files for download",
                    "remove": "You will be able to remove your files from the download list",
                    "search": "You will be able to search for files",
                    "show": "Shows all files in the peer Network",
                    "download": "Downloads a given file from the peer Network",
                    "menu": "You will see this command list again",
                    "exit": "You will leave the peer network"
            }
        for k, v in commands.items():
            print(f"{k:<7}| {v}".ljust(50))
        
        print("")
    
    def route(self):
        while True:
            command = input(">>> ").lower().strip(" ")
            if command == "exit":
                self.stop()
                break
            elif command == "add":
                self.add()
            elif command == "remove":
                self.remove()
            elif command == "search":
                self.search()
            elif command == "show":
                self.show()
            elif command == "download":
                self.download()
            elif command == "menu":
                self.commands()
            else:
                print("Unrecognised Command")



slave = Slave()
slave.start()