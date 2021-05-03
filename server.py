# Add Peers to the network and broadcast the peer details to all peers
import os, pickle
import socket
from threading import Thread
import unittest
from peer import Peer


class Master:
    port = 7000
    host = socket.gethostbyname(socket.gethostname())
    addr = (host, port)
    peers = []
    active = False

    def __init__(self) -> None:
        pass

    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(self.addr)
            server.listen()
            self.active = True
            print(f"[LISTENING . . . ")
            print(f"[Server::: ({self.addr}")
            while self.active:
                conn, addr = server.accept()
                thread = Thread(target=self.slave_handler, args=(conn, addr))
                thread.start()

    def stop(self) -> None:
        self.active = False
    
    def slave_handler(self, conn, addr):
        # request for files the peer is offering for download
        # keep checking that the peer is active
        # create a broadcast message to all peers updating the list of files they have for download
        peer = self.register_peers(conn, addr)
        print(conn)
        print(f"[NEW CONNECTION] ip: {addr[0]}, port: {addr[1]}")
        conn.send(f"Connected to {self.addr} successfully!".encode())

        # Send the Peer details to the Client
        encode_peer = pickle.dumps(peer)
        conn.send(encode_peer)
        
        while True:
            msg = self.receive(conn)
            if msg == "add":
                self.register_files(conn, peer)

    def register_peers(self, conn, addr):
        peer = Peer(addr)
        self.peers.append(peer)
        conn.send("Connected to the Peer Network Successfully!".encode())
        return peer
        # Send Message to the peer confirming the connection.
        # Ask the peer to advertise the files they have available for download

    def register_files(self, conn, peer):
        files = conn.recv(1024).decode()
        peer.files = dict(files)
        print(peer.files)
        return True

    def send_broadcast(self, msg):
        pass

    def receive(self, conn):
        msg = conn.recv(1024)
        return msg.decode()


class TestMaster(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_slave_can_connect_to_master(self):
        pass


server = Master()
server.start()

if __name__ == "__main__":
    unittest.main()