import os
import pickle
import socket
import unittest


class Peer:
    files = {}
    name = ""

    def __init__(self, addr) -> None:
        self.addr = addr[0]
        self.port = addr[1]

    def connect(self, addr, port):
        peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return peer.connect(addr, port)
    
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
    
    def __eq__(self, o: object) -> bool:
        return self.addr, self.port == (o.addr, o.port)


class TestPeer(unittest.TestCase):
    def setUp(self) -> None:
        addr = ("127.0.0.1", 75000)
        addr2 = ("127.0.0.1", 75001)
        self.peer1 = Peer(addr)
        self.peer2 = Peer(addr2)

        self.file = "/home/mokolo/Documents/Torrens/Year2Term1/DDE/Assessments/p2p_file_sharing_service/server.py"
        return super().setUp()

    def test_add_file(self):
        self.peer1.add_file(self.file)
        self.assertEqual(len(self.peer1.files.keys()), 1)
        self.assertEqual(self.peer1.files["server.py"], self.file)
    
    def test_remove_file(self):
        self.peer1.add_file(self.file)
        remove = self.peer1.remove_file("server.py")
        self.assertTrue(remove)
        self.assertEqual(len(self.peer1.files.keys()), 0)
    
    def test_search_files(self):
        self.peer1.add_file(self.file)
        self.assertEqual(self.peer1.search_file("server.py"), self.file)
        self.assertEqual(self.peer1.search_file("server2.py"), None)
        self.peer1.remove_file("server.py")
    
    def test_show_files(self):
        print(self.peer2.show_files())
        print(self.peer1.name)
        self.assertFalse(bool(self.peer2.show_files()))
        self.peer2.add_file(self.file)
        self.assertEqual(self.peer2.show_files(), ["server.py"])
        


if __name__ == "__main__":
    unittest.main()