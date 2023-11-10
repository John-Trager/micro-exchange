from dataclasses import dataclass
from enum import Enum
from functools import total_ordering

@dataclass()
class Trade:
    # a class to keep track of order matches or "trades"
    fill_price: float
    quantity: float  # amount of shares traded (bought or sold)
    bid_order_id: int  # order that is being filled
    bid_client_id: int
    ask_order_id: int
    ask_client_id: int
    symbol: str


class OrderType(Enum):
    BID = 0
    ASK = 2
    NULL = -1


@total_ordering
@dataclass()
class Order:
    price: float = -1
    quantity: float = -1
    order_id: int = -1
    client_id: int = -1
    side: OrderType = OrderType.NULL
    symbol: str = None

    def __lt__(self, other):
        if self.side == OrderType.BID:
            return self.price > other.price
        else:
            return self.price < other.price

    def __repr__(self) -> str:
        return f"Order(price={self.price}, quantity={self.quantity}, order_id={self.order_id}, side={self.side})"
