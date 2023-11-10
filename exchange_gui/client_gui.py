'''
a gui for the client

supports placing trades and viewing the order book
and personal account info (like assets held and cash balance)

for now the data values will be dummy values, we will connect it to the orderbook API later
'''

import dearpygui.dearpygui as dpg
import random
import time

def place_trade():
    print(f"Placing trade: {dpg.get_value('asset')} {dpg.get_value('quantity')}")

def connect_to_exchange():
    print("connecting to exchange")
    print(f"info: {dpg.get_value('server_ip')} {dpg.get_value('server_port')} {dpg.get_value('client_id')} {dpg.get_value('client_key')}")

    # disable connect button, and text inputs
    dpg.configure_item("connect", enabled=False)
    dpg.configure_item("server_ip", enabled=False)
    dpg.configure_item("server_port", enabled=False)
    dpg.configure_item("client_id", enabled=False)
    dpg.configure_item("client_key", enabled=False)

    time.sleep(1) # simulate connection time
    # ... after connecting to exchange
    
    dpg.hide_item("connect_window")

def generate_dummy_orderbook_data():
    data_x_bids, data_y_bids, data_x_asks, data_y_asks = [], [], [], []
    for x in range(30, 45):
        data_x_bids.append(x)
        data_y_bids.append(random.randint(1, 20))

    for x in range(47,47+15):
        data_x_asks.append(x)
        data_y_asks.append(random.randint(1, 20))
    
    return data_x_bids, data_y_bids, data_x_asks, data_y_asks

def update_plot():
    # TODO this should check a separate process/thread to see if their are new messages

    # if so then process them, otherwise do nothing

    if random.random() < 0.01:
        print("updating plot")
        data_x_bids, data_y_bids, data_x_asks, data_y_asks = generate_dummy_orderbook_data()
        dpg.configure_item('bid_line', x=data_x_bids, y=data_y_bids)
        dpg.configure_item('ask_line', x=data_x_asks, y=data_y_asks)

        dpg.fit_axis_data("xaxis")
        dpg.fit_axis_data("yaxis")

def setup_gui():
    with dpg.window(tag="main window", pos=[0,0], width=600, height=600, no_collapse=True, no_resize=True, 
                    no_close=True, no_move=True, no_title_bar=True, ):
        
        ## Define Themes ##
        with dpg.theme(tag="bids_theme"):
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 0), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 255, 0, 64), category=dpg.mvThemeCat_Plots)


        with dpg.theme(tag="asks_theme"):
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 0, 0), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 0, 0, 64), category=dpg.mvThemeCat_Plots)
        
        ## Define Widgets ##

        dpg.add_text("Place a trade:")
        dpg.add_input_text(label="Symbol", tag="asset")
        dpg.add_input_text(label="Quantity", tag="quantity")
        dpg.add_button(label="Place trade", callback=place_trade)

        dpg.add_text("Account info:")
        dpg.add_text("Assets held:", indent=20)
        dpg.add_text("Cash balance:", indent=20)

        dpg.add_text("Order book:")
        with dpg.plot(label="Orderbook", height=250, width=400):
            dpg.add_plot_legend(outside=True)
            xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Prices", tag="xaxis")
            with dpg.plot_axis(dpg.mvYAxis, label="Volume", tag="yaxis"):
                dpg.add_line_series(x=[], y=[], tag='bid_line', label="bids", parent=xaxis)
                dpg.bind_item_theme(dpg.last_item(), "bids_theme")

                dpg.add_line_series(x=[], y=[], tag='ask_line', label="asks", parent=xaxis)
                dpg.bind_item_theme(dpg.last_item(), "asks_theme")

    # connect to exchange window (closes after connecting)
    with dpg.window(tag="connect_window", label="Connect to Exchange", autosize=True, no_collapse=True, no_close=True):
        dpg.add_input_text(label="Server IP", tag="server_ip")
        dpg.add_input_text(label="Server port", tag="server_port")
        dpg.add_input_text(label="Client ID", tag="client_id")
        dpg.add_input_text(label="Client Key", tag="client_key")

        dpg.add_button(label="connect", tag="connect", callback=connect_to_exchange)

def main():
    dpg.create_context()

    dpg.create_viewport(title='Micro Trading Client')
    dpg.configure_viewport(0, x_pos=0, y_pos=0, width=600, height=600)
    dpg.setup_dearpygui()

    setup_gui()

    dpg.set_primary_window("main window", True)
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        update_plot()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

if __name__ == "__main__":
    main()