import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import value
import stocks


def update(driver, current_time, my_stock):
    new_current_time = value.get_time(driver)
    new_my_stock = value.update_stock_list(driver, my_stock)
    return new_current_time, new_my_stock


driver = uc.Chrome()
driver.maximize_window()

# try:
# Get to trading portal
value.setup(driver)
# Start Algorithm
current_time = value.get_time(driver)
try:
    my_stock = value.setup_stock_list(driver)
except Exception as e:
    print('error', e)
print('Current time', current_time)

exit_signal = 0

# try:


while exit_signal == 0:
    # ori time 910 time 1210 or 1435 time 1630
    if 910 <= current_time <= 1215 or 1435 <= current_time <= 1630:
        my_stock = value.update_stock_list(driver, my_stock)
        # Loop through every stock
        for s in my_stock:
            if s.qty_available == 0:
                if s.order is None:  # No order
                    buy_qty = s.get_buy_qty() * 100
                    if s.ask_qty / s.bid_qty <= 10 and s.bid_qty / buy_qty:
                        value.buy_stock(driver, s)
                        # Update
                        # current_time = value.get_time(driver)
                        # my_stock = value.update_stock_list(driver, my_stock)
                else:
                    pass
            else:
                if s.order is None:
                    if s.ask_qty / s.bid_qty >= 10:
                        print('Fulfill condition: s.ask_qty / s.bid_qty >= 10:')
                        value.sell_stock(driver, s, s.bid_price)
                    else:
                        print('Not Fulfill condition: s.ask_qty / s.bid_qty >= 10:')
                        value.sell_stock(driver, s, s.ask_price)

                else:   # Order exist:
                    if s.ask_qty / s.bid_qty >= 10:
                        # Order type is Buy Order
                        if s.order.get_order_type() == 'Buy':

                            if s.order.get_order_status() == 'Queued':
                                # Cancel order
                                value.cancel_order(driver, s)

                            elif s.order.get_order_status() == 'Partially Filled':
                                if s.bid_qty / s.order.get_unmatch_qty() >= 3:
                                    pass
                                else:
                                    value.cancel_order(driver, s)
                                    print('Sell stock because s.bid_qty / s.order.get_unmatch_qty() >= 3 ')
                                    value.sell_stock(driver, s, s.bid_price)

                        # Order type is Sell Order
                        elif s.order.get_order_type() == 'Sell':
                            if s.order.get_order_status() == 'Queued':
                                # Cancel order
                                value.cancel_order(driver, s)
                                # Sell at bid price
                                print('Order queue')
                                print('Cancel order, sell stock at bid price')
                                value.sell_stock(driver, s, s.bid_price)
                            elif s.order.get_order_status() == 'Partially Filled':
                                if s.ask_qty / s.order.get_unmatch_qty() >= 3:
                                    pass
                                else:
                                    value.cancel_order(driver, s)
                                    print('Order partially fill')
                                    print('Cancel order, sell stock at bid price')
                                    value.sell_stock(driver, s, s.bid_price)

                    else:
                        pass
        current_time = value.get_time(driver)
        my_stock = value.update_stock_list(driver, my_stock)
        print('Time is right')
    elif 1216 <= current_time <= 1230 or 1631 <= current_time <= 1644:
        print('sell everything at bid price')
        # Loop through every stock
        for s in my_stock:
            if s.order is not None:
                if s.order.order_type == 'Sell':
                    if s.order.order_price > s.bid_price:
                        value.cancel_order(driver, s)
                        value.sell_stock(driver, s, s.bid_price)
                else:   # Order type = Buy
                    value.cancel_order(driver, s)
                    value.sell_stock(driver, s, s.bid_price)
            else:
                pass
        my_stock = value.update_stock_list(driver, my_stock)
        time.sleep(30)
    elif 1231 <= current_time <= 1429 or 1645 <= current_time <= 1700:
        print('Do nothing')
        time.sleep(30)

    elif 1701 <= current_time <= 1710:
        for s in my_stock:
            s.report_principal()
        # End program
        exit_signal = 1

    else:
        # Dont do anything
        print('Do nothing')
        time.sleep(30)
    current_time = value.get_time(driver)

# except Exception as e:
#     print('Error', e)


