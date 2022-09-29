# Python code to demonstrate how parent constructors
# are called.
import time


# parent class
class TheChosen(object):

    def __init__(self, name, starting_principal, stock_queue):
        self.name = name
        self.starting_principal = starting_principal
        self.stock_queue = stock_queue

    def get_name(self):
        return self.name

    def get_starting_principal(self):
        return self.starting_principal

    def get_stock_queue(self):
        return self.stock_queue


# child class
class Stock(TheChosen):

    # __init__ is known as the constructor
    def __init__(
            self, name, starting_principal, stock_queue, bid_price, ask_price, bid_qty, ask_qty):
        self.bid_price = bid_price
        self.ask_price = ask_price
        self.bid_qty = bid_qty
        self.ask_qty = ask_qty
        self.qty_on_hand = 0  # Might need upgrade
        self.qty_available = 0
        self.current_principal = starting_principal
        self.ordered_qty = None
        self.avg_buy_price = None
        self.order = None  # The order object
        # self.ordered_qty = ordered_qty
        # self.current_principal = current_principal
        # invoking the __init__ of the parent class
        TheChosen.__init__(self, name, starting_principal, stock_queue)

    def set_name(self, newname):
        self.name = newname

    def set_bid_price(self, new_bid_price):
        self.bid_price = new_bid_price
        print('set bid price')

    def set_ask_price(self, new_ask_price):
        self.ask_price = new_ask_price

    def set_bid_qty(self, new_bid_qty):
        self.bid_qty = new_bid_qty

    def set_ask_qty(self, new_ask_qty):
        self.ask_qty = new_ask_qty

    def set_qty_on_hand(self, new_qty_on_hand):
        self.qty_on_hand = new_qty_on_hand

    def set_qty_available(self, new_qty_available):
        self.qty_available = new_qty_available

    def set_current_principal(self, new_current_principal):
        self.current_principal = new_current_principal

    def set_avg_buy_price(self, new_avg_buy_price):
        self.avg_buy_price = new_avg_buy_price

    def get_buy_qty(self):
        qty = self.current_principal / self.ask_price
        qty = int(qty / 100) * 100
        no_of_lots = qty / 100
        return no_of_lots

    def get_sell_qty(self):
        no_of_lots = self.qty_on_hand / 100
        return no_of_lots

    # Sell Price is determined when the function is called
    # def set_sell_qty(self, sell_price):
    #     qty = sell_price * self.qty_on_hand / 100
    #     return qty
    def set_sell_qty(self):
        qty = self.qty_on_hand / 100
        return qty


    def set_order(self, new_order):
        self.order = new_order

    def get_ordered_qty(self, new_ordered_qty):
        self.ordered_qty = new_ordered_qty

    def display(self):
        if self.order is None:
            print(
                self.name,
                'Bid Qty: ', self.bid_qty,
                'Ask Qty: ', self.ask_qty,
                'Qty on hand: ', self.qty_on_hand,
                'Avg Buy Price: ', self.avg_buy_price,
            )
        else:
            print(
                self.name,
                ' Bid Qty:', self.bid_qty,
                ' Ask Qty:', self.ask_qty,
                ' Qty on hand:', self.qty_on_hand,
                ' Avg Buy Price:', self.avg_buy_price,
                ' Order:', self.order.get_order_no()
            )

    def report_principal(self):
        print(self.name,
              'Starting Principal:', self.starting_principal,
              'Current Principal:', self.current_principal)

    # Order Class


class Order(object):

    def __init__(self, order_no, order_type, order_qty, order_price):
        self.order_no = order_no
        self.order_type = order_type
        self.order_status = 'Pending Release'
        self.order_qty = order_qty
        self.order_price = order_price
        self.match_qty = 0
        self.avg_price = None
        self.unmatch_qty = None

    def __del__(self):
        print('Order deleted')

    def get_order_no(self):
        return self.order_no

    def get_order_type(self):
        return self.order_type

    def get_order_status(self):
        return self.order_status

    def get_order_qty(self):
        return self.order_qty

    def get_match_qty(self):
        return self.match_qty

    def get_avg_price(self):
        return self.avg_price

    def get_unmatch_qty(self):
        return self.unmatch_qty

    def set_order_status(self, new_order_status):
        self.order_status = new_order_status

    def set_match_qty(self, new_match_qty):
        self.match_qty = new_match_qty

    def set_avg_price(self, new_avg_price):
        self.avg_price = new_avg_price

    def set_unmatch_qty(self):
        qty = self.order_qty - self.unmatch_qty
        self.unmatch_qty = qty


order1 = Order('ABCDE', 'Sell', 'Queued', '0.700')
# print('order1', order1.get_order_no())

stock1 = Stock('TOPGLOV', 10000, 7, 0.705, 0.710, 100000, 100000)

# Stock portfolio planning
# Topglov 30000
# Armada 20000
#
