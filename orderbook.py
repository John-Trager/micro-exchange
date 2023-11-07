'''
Orderbook class
'''
import heapq
from dataclasses import dataclass
from functools import total_ordering

@total_ordering
@dataclass()
class Order():
    price: float = -1
    quantity: float = -1
    order_id: int = -1
    client_id: int = -1
    side: str = None # ("bid" or "ask")
    symbol: str = None

    def __lt__(self, other):
        if self.side == 'bid':
            return self.price > other.price
        else:
            return self.price < other.price
        
    def __repr__(self) -> str:
        return f"Order(price={self.price}, quantity={self.quantity}, order_id={self.order_id}, side={self.side})"

class Orderbook:

    def __init__(self, symbol: str):
        self.symbol = symbol

        # bids and asks should be stored as priority queues
        self.bids = []
        self.asks = []

    def add_bid(self, order: Order) -> None:
        assert order.side == 'bid'
        assert order.quantity > 0

        heapq.heappush(self.bids, order)
        self.match_orders()

    def add_ask(self, order: Order) -> None:
        assert order.side == 'ask'
        assert order.quantity > 0
        heapq.heappush(self.asks, order)
        self.match_orders()

    def cancel_order(self, order_id: int) -> bool:
        if not self.cancel_bid(order_id):
            return self.cancel_ask(order_id)
        return True

    def cancel_bid(self, order_id: int) -> bool:
        for i, order in enumerate(self.bids):
            if order.order_id == order_id:
                self.bids.pop(i)
                heapq.heapify(self.bids)
                return True
        return False
    
    def cancel_ask(self, order_id: int) -> bool:
        for i, order in enumerate(self.asks):
            if order.order_id == order_id:
                self.bids.pop(i)
                heapq.heapify(self.asks)
                return True
        return False

    def get_bid(self) -> Order:
        return heapq.heappop(self.bids)
    
    def get_ask(self) -> Order:
        return heapq.heappop(self.asks)
    
    def match_orders(self):
        # match orders
        # while lowest bid is >= highest ask
        while len(self.bids) > 0 and len(self.asks) > 0 and self.bids[0].price >= self.asks[0].price:
            bid = self.get_bid()
            ask = self.get_ask()
            if bid.quantity > ask.quantity:
                bid.quantity -= ask.quantity
                self.add_bid(bid)
            elif bid.quantity < ask.quantity:
                ask.quantity -= bid.quantity
                self.add_ask(ask)
            else:
                # both orders are filled
                # TODO: add to trade history
                ...

    def __repr__(self):
        return f"Orderbook: symbol={self.symbol},\nbids={self.bids},\nasks={self.asks}"
    

if __name__ == '__main__':
    orderbook = Orderbook('AAPL')
    
    # test case1
    orderbook.add_bid(Order(100, 10, 1, 'bid'))
    orderbook.add_bid(Order(99, 10, 2, 'bid'))
    orderbook.add_bid(Order(98, 10, 3, 'bid'))
    print(orderbook,'\n')

    orderbook.add_ask(Order(101, 10, 4, 'ask'))
    orderbook.add_ask(Order(102, 10, 5, 'ask'))
    orderbook.add_ask(Order(103, 10, 6, 'ask'))
    print(orderbook,"\n")

    orderbook.add_ask(Order(100, 9, 6, 'ask'))
    print(orderbook)
