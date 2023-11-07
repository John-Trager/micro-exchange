import pytest
from exchange import Exchange
from orderbook import Orderbook, Order

# write out test cases for the exchange and orderbook classes using pytest

## ORDERBOOK TESTS ##
def test_orderbook_init():
    orderbook = Orderbook("AAPL")
    assert isinstance(orderbook, Orderbook), "Object should be an instance of Orderbook"

def test_place_bid_order():
    orderbook = Orderbook("AAPL")
    order = Order(150.0, 100, 0, 0, "bid", "AAPL")
    orderbook.add_bid(order)
    assert len(orderbook.bids) == 1 and len(orderbook.asks) == 0, "Order should be placed in bids"

def test_place_ask_order():
    orderbook = Orderbook("AAPL")
    order = Order(150.0, 100, 0, 0, "ask", "AAPL")
    orderbook.add_ask(order)
    assert len(orderbook.asks) == 1 and len(orderbook.bids) == 0, "Order should be placed in asks"

def test_match_orders():
    orderbook = Orderbook("AAPL")
    buy_order = Order(150.0, 100, 0, 0, "bid", "AAPL")
    sell_order = Order(150.0, 100, 0, 0, "ask", "AAPL")
    orderbook.add_bid(buy_order)
    orderbook.add_ask(sell_order)
    assert len(orderbook.bids) == 0, "Buy orders should be empty after matching"
    assert len(orderbook.asks) == 0, "Sell orders should be empty after matching"

def test_orderbook_no_orders():
    orderbook = Orderbook("AAPL")
    assert len(orderbook.bids) == 0 and len(orderbook.asks) == 0, "Orderbook should be empty on initialization"

def test_orderbook_unmatched_orders():
    orderbook = Orderbook("AAPL")
    buy_order = Order(150.0, 100, 0, 0, "bid", "AAPL")
    sell_order = Order(160.0, 100, 0, 0, "ask", "AAPL")  # Price too high to match
    orderbook.add_bid(buy_order)
    orderbook.add_ask(sell_order)
    assert len(orderbook.bids) == 1, "Buy order should remain unmatched"
    assert len(orderbook.asks) == 1, "Sell order should remain unmatched"

## EXCHANGE TESTS ##
def test_exchange_init():
    exchange = Exchange()
    assert isinstance(exchange, Exchange), "Object should be an instance of Exchange"

def test_exchange_multiple_orderbooks():
    exchange = Exchange()
    exchange.create_orderbook("AAPL")
    exchange.create_orderbook("MSFT")
    assert len(exchange.orderbooks) == 2, "Exchange should have two orderbooks"

def test_exchange_duplicate_orderbook():
    exchange = Exchange()
    exchange.create_orderbook("AAPL")
    with pytest.raises(ValueError):
        exchange.create_orderbook("AAPL")

def test_exchange_add_order():
    exchange = Exchange()
    exchange.create_orderbook("AAPL")
    order = Order(150.0, 100, 0, 0, "bid", "AAPL")
    exchange.add_order(order)
    assert len(exchange.orderbooks["AAPL"].bids) == 1, "Order should be added to orderbook"

def test_exchange_cancel_order():
    exchange = Exchange()
    exchange.create_orderbook("AAPL")
    order = Order(150.0, 100, 0, 0, "bid", "AAPL")
    exchange.add_order(order)
    exchange.cancel_order("AAPL", 0)
    assert len(exchange.orderbooks["AAPL"].bids) == 0, "Order should be removed from orderbook"

def test_exchange_cancel_order_invalid_orderbook():
    exchange = Exchange()
    exchange.create_orderbook("AAPL")
    order = Order(150.0, 100, 0, 0, "bid", "AAPL")
    exchange.add_order(order)
    assert not exchange.cancel_order("MSFT", 0), "Cancel order should return False if orderbook doesn't exist"

def test_exchange_cancel_order_invalid_order():
    exchange = Exchange()
    exchange.create_orderbook("AAPL")
    order = Order(150.0, 100, 0, 0, "bid", "AAPL")
    exchange.add_order(order)
    assert not exchange.cancel_order("AAPL", 1), "Cancel order should return False if order doesn't exist"

def test_exchange_cancel_order_invalid_order_id():
    exchange = Exchange()
    exchange.create_orderbook("AAPL")
    order = Order(150.0, 100, 0, 0, "bid", "AAPL")
    exchange.add_order(order)
    assert not exchange.cancel_order("AAPL", 1), "Cancel order should return False if order doesn't exist"
