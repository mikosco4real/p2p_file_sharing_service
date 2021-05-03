import os
import socket
import unittest
from threading import Thread


class Peer:
    files = {}
    name = ""

    def __init__(self, addr) -> None:
        self.addr = addr[0]
        self.port = addr[1]

    def connect(self, addr, port):
        peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return peer.connect((addr, port))
    
    def add_file(self, file):
        name = file.split("/")[-1:][0]
        self.files[name] = file
    
    def remove_file(self, filename):
        if filename in self.files.keys():
            self.files.pop(filename)
            return True
        else:
            return False
    
    def search_file(self, filename):
        file = None
        if filename in self.files.keys():
            file = self.files[filename]
        return file
    
    def show_files(self):
        return list(self.files.keys())
    
    def send_file(self, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.addr, self.port))
            server.listen()
            conn, addr = server.accept()
            file = self.search_file(filename)
            filesize = os.path.getsize(file)
            if file:
                with open(file, "rb") as c:
                    while len(c) > 0:
                        data = c.read(1024)
                        conn.send(data)
    
    def receive_file(self, filename, addr, port):
        conn = self.connect(addr, port)
        msg = conn.recv(1024)
        with open(filename, "wb") as file:
            file.write(msg)

    def __eq__(self, o: object) -> bool:
        return self.addr, self.port == (o.addr, o.port)


class TestPeer(unittest.TestCase):
    def setUp(self) -> None:
        addr = ("127.0.0.1", 65000)
        addr2 = ("127.0.0.1", 65001)
        self.peer1 = Peer(addr)
        self.peer2 = Peer(addr2)

        self.file = "/home/mokolo/Documents/Torrens/Year2Term1/DDE/Assessments/p2p_file_sharing_service/sample.txt"
        self.filename = "sample.txt"
        return super().setUp()

    def test_add_file(self):
        self.peer1.add_file(self.file)
        self.assertEqual(len(self.peer1.files.keys()), 1)
        self.assertEqual(self.peer1.files[self.filename], self.file)
    
    def test_remove_file(self):
        self.peer1.add_file(self.file)
        remove = self.peer1.remove_file(self.filename)
        self.assertTrue(remove)
        self.assertEqual(len(self.peer1.files.keys()), 0)
    
    def test_search_files(self):
        self.peer1.add_file(self.file)
        self.assertEqual(self.peer1.search_file(self.filename), self.file)
        self.assertEqual(self.peer1.search_file("server2.py"), None)
        self.peer1.remove_file(self.filename)
    
    def test_show_files(self):
        self.peer2.add_file(self.file)
        self.assertEqual(self.peer2.show_files(), [self.filename])

    def test_send_file(self):
        self.peer1.add_file(self.file)
        # thread = Thread(target = self.peer1.send_file, args=(self.filename))
        # thread.start()
        # self.peer2.receive_file("sample2.txt", self.peer1.addr, self.peer1.port)
        # self.assertTrue(open("sample2.txt", "r"))


if __name__ == "__main__":
    unittest.main()