import socket
import os


class Slave:
    master_addr = ("192.168.1.113", 7000)
    slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    file = dict()

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
        pass

    def start(self):
        try:
            self.connect()
            self.connected = True
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
        filename = file.split("/")[-1:][0]
        self.file[filename] = file
        # self.send(str(self.file))
        msg = "This is a good day"
        self.send(msg)

    
    def commands(self):
        print("")
        print("Available Commands")
        print("_" *50)
        print("")

        commands = {"add": "You will be able to add files for download",
                    "remove": "You will be able to remove your files from the download list",
                    "search": "You will be able to search for files",
                    "menu": "You will see this command list again",
                    "exit": "You will leave the peer network"
            }
        for k, v in commands.items():
            print(f"{k:<7}| {v}".ljust(50))
        
        print("")
    
    def route(self):
        while True:
            command = input(">>> ").lower()
            if command == "exit":
                self.stop()
                break
            elif command == "add":
                self.add()
            elif command == "remove":
                pass
            elif command == "search":
                pass
            elif command == "menu":
                self.commands()
            else:
                print("Unrecognised Command")



slave = Slave()
slave.start()