'''
Exchange class
'''
from orderbook import Orderbook, Order

class Exchange:

    def __init__(self) -> None:
        self.orderbooks = {}
        self.trades = [] # list of trades TODO

    def create_orderbook(self, symbol: str) -> None:
        if symbol in self.orderbooks:
            raise ValueError(f"Orderbook for {symbol} already exists")
        
        self.orderbooks[symbol] = Orderbook(symbol)

    def add_order(self, order: Order) -> bool:
        if order.symbol not in self.orderbooks:
            return False
        if order.side == 'bid':
            self.orderbooks[order.symbol].add_bid(order)
        else:
            self.orderbooks[order.symbol].add_ask(order)

    def cancel_order(self, symbol: str, order_id: int) -> bool:
        if symbol not in self.orderbooks:
            return False
        return self.orderbooks[symbol].cancel_order(order_id)

if __name__ == '__main__':
    exchange = Exchange()
    exchange.create_orderbook('AAPL')
    exchange.create_orderbook('MSFT')

    Order(100,10,1,0,'bid','AAPL')

    order1 = Order(119,10,1,0,'bid','AAPL')
    order2 = Order(105,10,2,0,'bid','AAPL')
    order3 = Order(110,10,3,0,'bid','AAPL')
    order4 = Order(115,10,4,0,'bid','AAPL')
    order5 = Order(120,10,5,0,'ask','AAPL')
    order6 = Order(125,10,6,0,'ask','AAPL')
    order7 = Order(130,10,7,0,'ask','AAPL')
    order8 = Order(135,10,8,0,'ask','AAPL')

    exchange.add_order(order1)
    exchange.add_order(order2)
    exchange.add_order(order3)
    exchange.add_order(order4)
    exchange.add_order(order5)
    exchange.add_order(order6)
    exchange.add_order(order7)
    exchange.add_order(order8)

    print(exchange.orderbooks['AAPL'])
    
    exchange.cancel_order('AAPL', 1)

    print(exchange.orderbooks['AAPL'])



    
