"""
Exchange class
"""
from orderbook import Orderbook
from utils import Order, OrderType, Trade
from dataclasses import dataclass, field


@dataclass()
class Client:
    client_id: int
    cash: float
    assets: dict[str, int] = field(default_factory=dict)
    trades: list[Trade] = field(default_factory=list)


class Exchange:
    def __init__(self) -> None:
        # symbol -> Orderbook
        self.orderbooks = {}
        # client id -> Client
        self.clients = {}

    def create_client(self, client: Client) -> None:
        if client.client_id in self.clients:
            raise ValueError(f"Client with id {client.client_id} already exists")
        self.clients[client.client_id] = client

    def create_orderbook(self, symbol: str) -> None:
        if symbol in self.orderbooks:
            raise ValueError(f"Orderbook for {symbol} already exists")

        self.orderbooks[symbol] = Orderbook(symbol)

    def run() -> None:
        # TODO make routine that listens for incoming requests from clients and places their orders
        # and sends back their trades as well as market 
        ...

    def add_order(self, order: Order) -> bool:
        # TODO: handle where client doesn't have enough cash or assets to place order
        # do we want to allow short selling? - if not then need to add counter to track number of sell quantity vs number of held shares

        if order.symbol not in self.orderbooks:
            print("Warning: attempted to place order on non-existent symbol")
            return False

        if order.client_id not in self.clients:
            print("Warning: invalid client tried to place order")
            return False

        trades = []
        if order.side == OrderType.BID:
            trades = self.orderbooks[order.symbol].add_bid(order)
        else:
            trades = self.orderbooks[order.symbol].add_ask(order)

        for trade in trades:
            if trade.bid_client_id != trade.ask_client_id:
                self.clients[trade.bid_client_id].trades.append(trade)
                self.clients[trade.bid_client_id].assets[trade.symbol] += trade.quantity
                self.clients[trade.bid_client_id].cash -= trade.quantity*trade.fill_price
                
                self.clients[trade.ask_client_id].trades.append(trade)
                self.clients[trade.ask_client_id].assets[trade.symbol] -= trade.quantity
                self.clients[trade.bid_client_id].cash += trade.quantity*trade.fill_price
            else:
                # client is both buyer and seller so only save trade once
                # so cash and asset quantity doesn't change?
                self.clients[trade.bid_client_id].trades.append(trade)

    def cancel_order(self, symbol: str, order_id: int) -> bool:
        if symbol not in self.orderbooks:
            return False
        return self.orderbooks[symbol].cancel_order(order_id)

    def __repr__(self):
        return f"--- Exchange: \nOrderbooks: {self.orderbooks} \nClient States: {self.clients} \n---"


if __name__ == "__main__":
    exchange = Exchange()
    exchange.create_orderbook("AAPL")
    exchange.create_orderbook("MSFT")

    exchange.create_client(Client(125, 1000))
    exchange.create_client(Client(124, 1000))

    order1 = Order(119, 10, 1, 125, OrderType.BID, "AAPL")
    order2 = Order(105, 10, 2, 125, OrderType.BID, "AAPL")
    order3 = Order(110, 10, 3, 125, OrderType.BID, "AAPL")
    order4 = Order(115, 10, 4, 125, OrderType.BID, "AAPL")

    order5 = Order(120, 10, 5, 124, OrderType.ASK, "AAPL")
    order6 = Order(125, 10, 6, 124, OrderType.ASK, "AAPL")
    order7 = Order(130, 10, 7, 124, OrderType.ASK, "AAPL")
    order8 = Order(135, 10, 8, 124, OrderType.ASK, "AAPL")

    exchange.add_order(order1)
    exchange.add_order(order2)
    exchange.add_order(order3)
    exchange.add_order(order4)
    exchange.add_order(order5)
    exchange.add_order(order6)
    exchange.add_order(order7)
    exchange.add_order(order8)

    print(exchange)

    exchange.cancel_order("AAPL", 1)
    print("cancelled order 1")
    print(exchange)

    # test matching order
    order9 = Order(120, 10, 9, 125, OrderType.BID, "AAPL")
    exchange.add_order(order9)
    print("made trade with order 5, full fill")
    print(exchange)
