"""
Orderbook class
"""
import heapq
from utils import Order, OrderType, Trade

class Orderbook:
    def __init__(self, symbol: str):
        self.symbol = symbol

        # bids and asks should be stored as priority queues
        self.bids = []
        self.asks = []

    def add_bid(self, order: Order) -> list[Trade]:
        assert order.side == OrderType.BID
        assert order.quantity > 0
        assert order.price > 0
        assert order.symbol == self.symbol

        heapq.heappush(self.bids, order)
        return self.match_orders()

    def add_ask(self, order: Order) -> list[Trade]:
        assert order.side == OrderType.ASK
        assert order.quantity > 0
        assert order.price > 0
        assert order.symbol == self.symbol

        heapq.heappush(self.asks, order)
        return self.match_orders()

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

    def match_orders(self) -> list[Trade]:
        trades = []
        # match orders
        # while lowest bid is >= highest ask
        while (
            len(self.bids) > 0
            and len(self.asks) > 0
            and self.bids[0].price >= self.asks[0].price
        ):
            bid = self.get_bid()
            ask = self.get_ask()

            fill_quantity = min(bid.quantity, ask.quantity)
            bid.quantity -= fill_quantity
            ask.quantity -= fill_quantity
            # fill price will always be the bid price since it should be >= ask price
            trades.append(
                Trade(
                    bid.price,
                    fill_quantity,
                    bid.order_id,
                    bid.client_id,
                    ask.order_id,
                    ask.client_id,
                    bid.symbol,
                )
            )

            if bid.quantity > 0:
                self.add_bid(bid)
            elif ask.quantity > 0:
                self.add_ask(ask)

        return trades

    def __repr__(self):
        return (
            f"\nOrderbook: symbol={self.symbol},\nbids={self.bids},\nasks={self.asks}"
        )


if __name__ == "__main__":
    orderbook = Orderbook("AAPL")

    orderbook.add_bid(Order(100, 10, 1, OrderType.BID))
    orderbook.add_bid(Order(99, 10, 2, OrderType.BID))
    orderbook.add_bid(Order(98, 10, 3, OrderType.BID))
    print(orderbook, "\n")

    orderbook.add_ask(Order(101, 10, 4, OrderType.ASK))
    orderbook.add_ask(Order(102, 10, 5, OrderType.ASK))
    orderbook.add_ask(Order(103, 10, 6, OrderType.ASK))
    print(orderbook, "\n")

    orderbook.add_ask(Order(100, 9, 6, OrderType.ASK))
    print(orderbook)
