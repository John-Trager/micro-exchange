'''
client API to the exchange
connects to the exchange via sockets
'''
import socket
import asyncio # TODO: use async functions for sending / receiving data
import json
import time

from utils import Order, OrderType, Trade

class Client:
    def __init__(self, client_id: int) -> None:
        self.client_id = client_id

        # these data will be updated by the exchange
        self.cash = None 
        self.assets = {}
        self.trades = []
        self.socket = None

    def __repr__(self) -> str:
        return f"Client(client_id={self.client_id}, cash={self.cash}, assets={self.assets}, trades={self.trades})"

    def connect_to_exchange(self, host: str, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port)) # todo is this correct?

    def start(self):
        # waits for the exchange to start, and starts streaming
        # exchange updates once it starts
        ...
    
    def place_order(self, order: Order) -> bool:
        ...

    def cancel_order(self, order_id: int) -> bool:
        ...

