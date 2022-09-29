import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import stocks


def get_time(driver):
    ori_time = driver.find_element(By.ID, "label-1066").text
    print('ori_time', ori_time)
    hour = int(ori_time[0:2])
    minute = int(ori_time[3:5])
    format_time = hour * 100 + minute
    print(format_time)
    # return time as integer Eg: 11:03 = 1103
    return format_time


# trading hr: 9.15-12.15 14.45-16.30

# Time selector: #label-1066 - id name
# currentTime = "12:24:51"  # Get time by get element

def format_qty(qty):
    if qty[-1].isalpha():
        if qty[-1].upper() == 'M':
            new_qty = qty[0:-1]
            new_qty = float(new_qty) * 1000000
            # print(new_qty)
            return new_qty
        elif qty[-1].upper == 'K':
            new_qty = qty[0:-1]
            new_qty = float(new_qty) * 1000
            # print(new_qty)
            return new_qty
    else:
        new_qty = qty.replace(",", "")
        new_qty = float(new_qty)
        # print(new_qty)
        return new_qty

# Get value from stocklist table:
def get_stock_name(driver, column_id):
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[1]/div'
    value = driver.find_element(By.XPATH, path).text
    return value


def get_stock_bid_qty(driver, column_id):
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[5]/div'
    bid_qty = driver.find_element(By.XPATH, path).text
    bid_qty = format_qty(bid_qty)
    return bid_qty


def get_stock_bid_price(driver, column_id):
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[6]/div'
    bid_price = driver.find_element(By.XPATH, path).text
    bid_price = format_qty(bid_price)
    return bid_price


def get_stock_ask_price(driver, column_id):
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[7]/div'
    ask_price = driver.find_element(By.XPATH, path).text
    ask_price = format_qty(ask_price)
    return ask_price


def get_stock_ask_qty(driver, column_id):
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[8]/div'
    ask_qty = driver.find_element(By.XPATH, path).text
    ask_qty = format_qty(ask_qty)
    return ask_qty

# ----------------------------------------------------------------------

# Portfolio table values:
def get_qty_hand(driver, column_id):
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[3]/div'
    qty_hand = driver.find_element(By.XPATH, path).text
    qty_hand = format_qty(qty_hand)
    return qty_hand


def get_qty_available(driver, column_id):
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[4]/div'
    qty_available = driver.find_element(By.XPATH, path).text
    qty_available = format_qty(qty_available)
    return qty_available


def get_avg_buy_prc(driver, column_id):
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[6]/div'
    avg_buy_prc = driver.find_element(By.XPATH, path).text
    avg_buy_prc = format_qty(avg_buy_prc)
    return avg_buy_prc


# Get stock name in portfolio table
def get_pf_stock_name(driver, col_id):
    path = '//*[@id="' + col_id + '"]/tbody/tr/td[1]/div'
    name = driver.find_element(By.XPATH, path).text
    return name


# ---------------------------------------------------------------------


# Get value from order book table
def get_order_status(driver, col_id):
    if col_id:
        path = '//*[@id="' + col_id + '"]/tbody/tr/td[8]'
        if driver.find_element(By.XPATH, path):
            status = driver.find_element(By.XPATH, path).text
            print('order status:', status)
            return status
    else:
        print('Return Filled')
        return 'Filled'


def get_match_qty(driver, col_id):
    path = '//*[@id="' + col_id + '"]/tbody/tr/td[11]'
    qty = driver.find_element(By.XPATH, path).text
    qty = format_qty(qty)
    print('match qty:', qty)
    return qty


def get_avg_price(driver, col_id):
    path = '//*[@id="' + col_id + '"]/tbody/tr/td[12]'
    price = driver.find_element(By.XPATH, path).text
    price = format_qty(price)
    print('avg price:', price)
    return price


# ---------------------------------------------------------------------

def setup_stock_list(driver):
    # Create a list of chosen stock
    print('setup stock list is called')
    chosen_stocks = [
        # stocks.TheChosen("ARMADA", 1000, 0),
        # stocks.TheChosen("BJCORP", 1000, 1),
        # stocks.TheChosen("DNEX", 1000, 2),
        # stocks.TheChosen("FFB", 1000, 3),
        stocks.TheChosen("HARTA", 5000, 4),
        stocks.TheChosen("HIBISCS", 5000, 5),
        # stocks.TheChosen("MYEG", 1000, 6),
        stocks.TheChosen("TOPGLOV", 15000, 7),
    ]
    stocks_list = []  # Create stock object list
    # stock list table
    # try:
    # table = driver.find_element(By.CSS_SELECTOR, "#gridview-1481 > div.x-grid-item-container")
    # table = driver.find_element(By.XPATH, '//*[@id="gridview-1481"]/div[2]')
    table = driver.find_element(By.XPATH,
                                '/html/body/div[2]/div[1]/div/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]')
    # print('table')
    # columns of the table
    columns = table.find_elements(By.TAG_NAME, "table")
    # print('columns:', columns)
    # except:
    #     print('cant find table 2')
    column_id_list = []
    for column in columns:
        column_id_list.append(column.get_attribute("id"))
    for stock in chosen_stocks:
        for i in range(len(column_id_list)):
            # get value by xpath
            col_id = column_id_list[i]
            # print("col_id:" +col_id)
            # try:
            stock_name = get_stock_name(driver, col_id)
            # except:
            # print('err line 99')
            try:
                if stock_name == stock.get_name():
                    # Create Stock object and add to an object list
                    stocks_list.append(stocks.Stock(
                        get_stock_name(driver, col_id),
                        stock.get_starting_principal(),
                        stock.get_stock_queue(),
                        get_stock_bid_price(driver, col_id),
                        get_stock_ask_price(driver, col_id),
                        get_stock_bid_qty(driver, col_id),
                        get_stock_ask_qty(driver, col_id)
                    )
                    )
                else:
                    pass
            except:
                print('err here')
    print('stocks_list: ')
    for s in stocks_list:
        print(s.get_name())
    return stocks_list


def update_stock_list(driver, my_stock):
    print('Start update stock list')
    for s in my_stock:
        # stock list table
        table = driver.find_element(By.CSS_SELECTOR, "#gridview-1481 > div.x-grid-item-container")
        # columns of the table
        print('189')
        columns = table.find_elements(By.TAG_NAME, "table")
        column_id_list = []
        for column in columns:
            column_id_list.append(column.get_attribute("id"))
        for i in range(len(column_id_list)):
            # get value by xpath
            col_id = column_id_list[i]
            # print("col_id:" +col_id)
            # try:
            stock_name = get_stock_name(driver, col_id)
            # except:
            #     print('err')
            try:
                if stock_name == s.get_name():
                    # Update Stock object detail
                    s.set_bid_price(get_stock_bid_price(driver, col_id))
                    s.set_ask_price(get_stock_ask_price(driver, col_id))
                    s.set_bid_qty(get_stock_bid_qty(driver, col_id))
                    s.set_ask_qty(get_stock_ask_qty(driver, col_id))
                else:
                    pass
            except:
                print('err here')

        try:
            # Refresh portfolio table
            driver.find_element(By.XPATH, '//*[@id="button-1345-btnIconEl"]').click()
            time.sleep(1)
            # portfolio table
            pf_table = driver.find_element(By.CSS_SELECTOR, "#gridview-1385 > div.x-grid-item-container")
            print('219')
            pf_columns = pf_table.find_elements(By.TAG_NAME, "table")
            pf_column_id_list = []
            for column in pf_columns:
                pf_column_id_list.append(column.get_attribute("id"))
            for i in range(len(pf_column_id_list)):
                # get value by xpath
                col_id = pf_column_id_list[i]
                # print("col_id:" + col_id)
                # try:
                stock_name = get_pf_stock_name(driver, col_id)
                # print('stock_name', stock_name)
                # print('s.get_name', s.get_name)
                if stock_name == s.get_name():
                    # Update Stock qty.hand, avg buy price
                    s.set_qty_on_hand(get_qty_hand(driver, col_id))
                    s.set_qty_available(get_qty_available(driver, col_id))
                    s.set_avg_buy_price(get_avg_buy_prc(driver, col_id))
                else:
                    pass
        except Exception as e:
            print('264', e)

        try:
            # Click refresh button
            driver.find_element(By.XPATH, '//*[@id="button-1192-btnIconEl"]').click()
            time.sleep(1)
            if s.order is not None:
                # Get order status
                print(s.get_name(), 's.order.get_order_no()', s.order.get_order_no())
                col_id = get_order_book_col_id(driver, s.order.get_order_no())
                print('col_id 264', col_id)
                text = get_order_status(driver, col_id)
                print('Order status=', text)
                if text == 'Filled':
                    print('After filled, current principal', s.current_principal)
                    if s.order.get_order_type() == 'Sell':
                        # Switch to Filled
                        set_ob_filled(driver)
                        # Update order
                        col_id2 = get_order_book_col_id(driver, s.order.get_order_no())
                        refresh_portfolio(driver)
                        s.order.set_order_status(text)
                        s.order.set_match_qty(get_match_qty(driver, col_id2))
                        s.order.set_avg_price(get_avg_price(driver, col_id2))
                        # Switch back to Open
                        set_ob_open(driver)
                        # New current principal / Refund
                        print('Start refund')
                        print(s.order.get_avg_price(), s.order.get_match_qty(), s.current_principal)
                        value1 = s.order.get_avg_price() * s.order.get_match_qty()
                        value1 = round(value1, 2)
                        value2 = value1 + s.current_principal
                        new_cur_principal = round(value2, 2)
                        print('After round', new_cur_principal)
                        s.set_current_principal(new_cur_principal)
                        print('New current principal:', s.current_principal)

                        s.set_qty_on_hand(0)
                        s.set_qty_available(0)
                        print(s.qty_on_hand, s.qty_available)

                    else:  # When Buy order is filled
                        pf_col_id = get_pf_col_id(driver, s)
                        s.set_qty_on_hand(get_qty_hand(driver, pf_col_id))
                        s.set_qty_available(get_qty_available(driver, pf_col_id))
                        s.set_avg_buy_price(get_avg_buy_prc(driver, pf_col_id))
                        pass
                    s.set_order(None)  # Del order
                    print('Order', s.order)
                    print('Done close order')

                else:  # Order not filled

                    s.order.set_order_status(text)
                    s.order.set_match_qty(get_match_qty(driver, col_id))
                    s.order.set_avg_price(get_avg_price(driver, col_id))

                    refresh_portfolio(driver)
                    pf_col_id = get_pf_col_id(driver, s)
                    if pf_col_id:   # If stock exist in portfolio
                        s.set_qty_on_hand(get_qty_hand(driver, pf_col_id))
                        s.set_qty_available(get_qty_available(driver, pf_col_id))
                        s.set_avg_buy_price(get_avg_buy_prc(driver, pf_col_id))
                    else:
                        pass

            else:
                pass
        except Exception as e:
            print(e)
            # Switch back to Open
            set_ob_open(driver)

    print('Success update')
    return my_stock


def get_ticket_no(driver):
    # ticket_detail = driver.find_element(By.XPATH, '//*[@id="component-1560"]/div').text
    time.sleep(1)
    e1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-1563"]/div'))
    )
    ticket_detail = e1.text
    ticket_no = ticket_detail[11:27]
    print('ticket_detail', ticket_detail)
    print('ticket no', ticket_no)
    return ticket_no


def buy_stock(driver, stock):
    print('Try buy', stock.name)
    column_id = get_column_id(driver, stock.stock_queue)
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[7]/div'
    ask_price_box = driver.find_element(By.XPATH, path)
    ActionChains(driver) \
        .double_click(ask_price_box) \
        .perform()
    time.sleep(1)
    # Calculate buy qty
    buy_qty = str(int(stock.get_buy_qty()))
    print('Buy qty:', buy_qty)
    # Input qty
    e1 = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="customspinner-1514-inputEl"]'))
    )
    e1.click()
    e1.send_keys(buy_qty)
    time.sleep(3)
    # Input price
    price_box = driver.find_element(By.XPATH, '//*[@id="combobox-1512-inputEl"]')
    print('clear box')
    price_box.clear()
    buy_price = stock.bid_price
    price_box.send_keys(buy_price)
    time.sleep(1)
    # Click Buy Button
    driver.find_element(By.XPATH, '//*[@id="button-1574-btnInnerEl"]').click()
    # Click Ok Button
    e2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="messagebox-1001-displayfield-inputEl"]/div/span/button[1]'))
    )
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".reply-button"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(e2)).click()
    e2.click()
    time.sleep(0.5)
    # Print ticket no.
    tkt_no = get_ticket_no(driver)
    buy_qty = stock.get_buy_qty() * 100
    new_order = stocks.Order(tkt_no, 'Buy', buy_qty, buy_price)

    print('buy tkt no', tkt_no)
    # Close
    driver.find_element(By.XPATH, '//*[@id="tool-1631-toolEl"]').click()
    # Reset current_principal
    print(stock.current_principal, stock.bid_price, buy_qty)
    value1 = stock.current_principal - stock.bid_price * buy_qty
    value1 = round(value1, 2)
    stock.set_current_principal(value1)
    print('current principal', stock.current_principal)
    # Create new order
    stock.set_order(new_order)
    print('done buy stock')


def sell_stock(driver, stock, sell_price):
    print('Try sell', stock.name)
    # sell stock
    column_id = get_column_id(driver, stock.stock_queue)
    path = '//*[@id="' + column_id + '"]/tbody/tr/td[6]/div'
    bid_price_box = driver.find_element(By.XPATH, path)
    ActionChains(driver) \
        .double_click(bid_price_box) \
        .perform()
    time.sleep(1)
    # Calculate Sell qty
    sell_qty = str(int(stock.set_sell_qty()))
    print('sell qty', sell_qty)
    # Input qty
    e1 = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="customspinner-1514-inputEl"]'))
    )
    e1.click()
    e1.send_keys(sell_qty)
    time.sleep(3)
    # Input price
    price_box = driver.find_element(By.XPATH, '//*[@id="combobox-1512-inputEl"]')
    print('clear box')
    price_box.clear()
    price_box.send_keys(sell_price)  # Need change
    time.sleep(1)
    # Click Sell Button
    driver.find_element(By.XPATH, '//*[@id="button-1574-btnInnerEl"]').click()
    # Click Ok Button
    e2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="messagebox-1001-displayfield-inputEl"]/div/span/button[1]'))
    )
    e2.click()
    time.sleep(0.5)
    # Print ticket no.
    tkt_no = get_ticket_no(driver)
    new_order = stocks.Order(tkt_no, 'Sell', stock.get_sell_qty(), sell_price)
    print('sell tkt no:', tkt_no)
    # Close
    driver.find_element(By.XPATH, '//*[@id="tool-1631-toolEl"]').click()
    # Create new order
    stock.set_order(new_order)
    print('done sell stock')


def revise_order(driver, stock):
    print('Start revise order')

    print('Done revise order')


# Get stock list table column id
def get_column_id(driver, queue_no):
    # stock list table
    table = driver.find_element(By.CSS_SELECTOR, "#gridview-1481 > div.x-grid-item-container")
    # columns of the table
    print('353')
    first_column = table.find_element(By.TAG_NAME, "table")
    col_id = first_column.get_attribute("id")
    # Get the last 2 or 3 no.
    col_code = col_id[21:]  # Get the number start from index 21
    col_code = int(col_code) + queue_no
    new_col_id = col_id[:21] + str(col_code)  # Get col id needed
    # Function done in 0.015619277954101562 sec
    # print('col_code', col_code)
    # print('new col id', new_col_id)
    return new_col_id


# Get order book column id
def get_order_book_col_id(driver, order_no):
    order_table = driver.find_element(By.CSS_SELECTOR, '#gridview-1259 > div.x-grid-item-container')
    # columns of the table
    print('370')
    columns = order_table.find_elements(By.TAG_NAME, "table")
    order_column_id_list = []
    for column in columns:
        order_column_id_list.append(column.get_attribute("id"))
    # for i in range(len(order_column_id_list)):
    final_id = None
    for col_id in order_column_id_list:
        path = '//*[@id="' + col_id + '"]/tbody/tr/td[5]'
        print('path=', path)
        text1 = driver.find_element(By.XPATH, path).text
        print('order no', order_no, text1 )
        time.sleep(1)
        if order_no == text1 :
            print('done return new_col_id')
            final_id = col_id
            break
        else:
            pass
    # if final_id is None:

    print('final_id', final_id)
    return final_id


# Get portfolio column id
def get_pf_col_id(driver, stock):
    # port folio table
    table = driver.find_element(By.CSS_SELECTOR, "#gridview-1385 > div.x-grid-item-container")
    # columns of the table
    print('475')
    columns = table.find_elements(By.TAG_NAME, "table")
    pf_column_id_list = []
    for column in columns:
        pf_column_id_list.append(column.get_attribute("id"))

    final_id = None
    for col_id in pf_column_id_list:
        path = '//*[@id="' + col_id + '"]/tbody/tr/td[1]/div'
        print('path=', path)
        time.sleep(1)
        if stock.name == driver.find_element(By.XPATH, path).text:
            print('done return new_col_id')
            final_id = col_id
            break
        else:
            pass

    print('final_pf_id', final_id)
    return final_id


# Cancel order
def cancel_order(driver, stock):
    print('Cancel order called')
    order_no = stock.order.get_order_no()
    col_id = get_order_book_col_id(driver, order_no)
    print('col_id 444', col_id)
    if col_id:  # if order exist
        path = '//*[@id="' + col_id + '"]/tbody/tr/td[5]'
        # if order_no == driver.find_element(By.XPATH, path).text:
        clickable = driver.find_element(By.XPATH, path)
        ActionChains(driver) \
            .context_click(clickable) \
            .perform()
        time.sleep(1)

        e1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ext-453-textEl"]'))
        )
        e1.click()  # Click cancel in dropdown menu
        # driver.find_element(By.XPATH, '//*[@id="ext-453-textEl"]').click()  # Click cancel in dropdown menu
        time.sleep(1)
        e2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="button-1574-btnInnerEl"]'))
        )
        e2.click()  # Click cancel in order menu
        e3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="button-1005-btnInnerEl"]'))
        )
        e3.click()  # Click ok button to confirm cancel
        e4 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tool-1631-toolEl"]'))
        )
        e4.click()  # Click close button to close order menu

        # Switch to Filled
        set_ob_filled(driver)
        # # Update order
        col_id2 = get_order_book_col_id(driver, stock.order.get_order_no())
        stock.order.set_order_status('Filled')
        stock.order.set_match_qty(get_match_qty(driver, col_id2))
        stock.order.set_avg_price(get_avg_price(driver, col_id2))
        stock.order.set_unmatch_qty()
        # Refund principal
        if stock.order.get_order_type() == 'Buy':
            refund = stock.order.get_unmatch_qty() * stock.order.avg_price
            new_principal = stock.current_principal + refund
            new_principal = round(new_principal, 2)
            stock.set_current_principal(new_principal)
        else:   # when sell order
            refund = stock.order.get_match_qty() * stock.order.avg_price
            new_principal = stock.current_principal + refund
            new_principal = round(new_principal, 2)
            stock.set_current_principal(new_principal)
        # Switch back to Open
        set_ob_open(driver)
        print('Done cancel order', order_no)

    else:  # col_id not exist(order had been filled)
        # Switch to Filled
        set_ob_filled(driver)
        # # Update order
        col_id2 = get_order_book_col_id(driver, stock.order.get_order_no())
        # stock.order.set_order_status(get_order_status(col_id2))
        stock.order.set_order_status('Filled')
        stock.order.set_match_qty(get_match_qty(driver, col_id2))
        stock.order.set_avg_price(get_avg_price(driver, col_id2))
        stock.order.set_unmatch_qty()
        # Switch back to Open
        set_ob_open(driver)

        if stock.order.get_order_type() == 'Sell':
            # New current principal
            print('avg_price', stock.order.get_avg_price())
            print('match_qty', stock.order.get_match_qty())
            print('current_principal', stock.current_principal)
            # new_cur_principal = (stock.order.get_avg_price() * stock.order.get_match_qty()) + stock.current_principal
            # stock.set_current_principal(new_cur_principal)
            print('New current principal:', stock.current_principal)
            refund = stock.order.get_match_qty() * stock.order.get_avg_price()
            value1 = stock.current_principal + refund
            new_principal = round(value1, 2)
            print('new principal after round', new_principal)
            stock.set_current_principal(new_principal)

        else:  # if order = buy
            pass  # No need do anything
        print('Order Filled')

        # New code:
        # if s.order.get_order_type() == 'Sell':
        #     # Switch to Filled
        #     set_ob_filled(driver)
        #     # Update order
        #     col_id2 = get_order_book_col_id(driver, s.order.get_order_no())
        #     refresh_portfolio(driver)
        #     s.order.set_order_status(text)
        #     s.order.set_match_qty(get_match_qty(driver, col_id2))
        #     s.order.set_avg_price(get_avg_price(driver, col_id2))
        #     # Switch back to Open
        #     set_ob_open(driver)
        #     # New current principal / Refund
        #     print('Start refund')
        #     print(s.order.get_avg_price(), s.order.get_match_qty(), s.current_principal)
        #     value1 = s.order.get_avg_price() * s.order.get_match_qty()
        #     value1 = round(value1, 2)
        #     value2 = value1 + s.current_principal
        #     new_cur_principal = round(value2, 2)
        #     print('After round', new_cur_principal)
        #     s.set_current_principal(new_cur_principal)
        #     print('New current principal:', s.current_principal)
        #
        #     s.set_qty_on_hand(0)
        #     s.set_qty_available(0)
        #     print(s.qty_on_hand, s.qty_available)
        #
        # else:  # When Buy order is filled
        #     pf_col_id = get_pf_col_id(driver, s)
        #     s.set_qty_on_hand(get_qty_hand(driver, pf_col_id))
        #     s.set_qty_available(get_qty_available(driver, pf_col_id))
        #     s.set_avg_buy_price(get_avg_buy_prc(driver, pf_col_id))
        #     pass
        print('Done close order')
    stock.set_order(None)  # Del order
    print('Order', stock.order)




def setup(driver):
    driver.get("https://bursaacademy.bursamarketplace.com/en/login")
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl13_btnLogin"]'))  # Make sure submit button presence
    )
    # print('login page: ', driver.title)
    driver.find_element(By.XPATH, '//*[@id="ctl13_txtEmail"]').send_keys('xushengchin@gmail.com')
    driver.find_element(By.XPATH, '//*[@id="ctl13_txtPassword"]').send_keys('5Qn5CLl#')
    time.sleep(8)
    driver.find_element(By.XPATH, '//*[@id="ctl13_btnLogin"]').click()
    # time.sleep(3)
    # driver.quit()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="newnav"]/div[2]/div[1]/div[1]/div[6]/div[1]/a'))
        # Remember to have double bracket
    )
    # print('dashboard: ', driver.title)
    # Click stimulator, open trading portal tab
    driver.find_element(By.XPATH, '//*[@id="newnav"]/div[2]/div[1]/div[1]/div[6]/div[1]/a').click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])  # Switch back to dashboard tab
    time.sleep(1.5)
    driver.close()  # Close dashboard tab
    driver.switch_to.window(driver.window_handles[0])  # Switch to trading portal tab
    time.sleep(3)
    # Make sure trading portal is ready
    print('trading portal: ', driver.title)
    time.sleep(5)
    driver.switch_to.frame('tclitewin')  # Switch to the targeted iframe

    # Set order book - All order to Open:
    set_ob_open(driver)
    # e1 = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="combobox-1186-trigger-picker"]'))
    # )
    # e1.click()  # Click down arrow
    # e2 = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="boundlist-1187-listEl"]/li[3]'))
    # )
    # e2.click()  # Select Open # Done


# Set order book to open
def set_ob_open(driver):
    print('Try switch to open')
    try:
        # Set order book - All order to Open:
        e1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="combobox-1186-trigger-picker"]'))
        )
        e1.click()  # Click down arrow
        e2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="boundlist-1187-listEl"]/li[3]'))
        )
        e2.click()  # Select Open # Done
        print('Done switch to Open')
    except Exception as e:
        print(e)
        print('Failed switch to open')


# Set order book to filled
def set_ob_filled(driver):
    print('Try switch to filled')
    try:
        # Set order book - All order to Open:
        e1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="combobox-1186-trigger-picker"]'))
        )
        e1.click()  # Click down arrow
        e2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="boundlist-1187-listEl"]/li[4]'))
        )
        e2.click()  # Select Filled # Done
        print('Done switch to Filled')
    except Exception as e:
        print(e)
        print('Fail switch to filled')

def refresh_portfolio(driver):
    e1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="button-1345-btnIconEl"]'))
    )
    e1.click()
    print('Done refresh portfolio')
