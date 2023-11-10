'''
a gui for the client

supports placing trades and viewing the order book
and personal account info (like assets held and cash balance)

for now the data values will be dummy values, we will connect it to the orderbook API later
'''

import dearpygui.dearpygui as dpg
import random

def place_trade():
    print(f"Placing trade: {dpg.get_value('asset')} {dpg.get_value('quantity')}")

def generate_data():
    data_x, data_y = [], []
    for x in range(30, 45):
        data_x.append(x)
        data_y.append(random.randint(1, 20))
    return data_x, data_y

def update_plot():
    if random.random() < 0.01:
        print("updating plot")
        data_x, data_y = generate_data()
        dpg.configure_item('bid_line', x=data_x, y=data_y)
        dpg.configure_item('ask_line', x=data_x, y=data_y)

        dpg.fit_axis_data("xaxis_bids")
        dpg.fit_axis_data("yaxis_bids")

        dpg.fit_axis_data("xaxis_asks")
        dpg.fit_axis_data("yaxis_asks")



def setup_gui():
    # window setup?
    with dpg.window(tag="main window", pos=[0,0], width=600, height=600, no_collapse=True, no_resize=True, 
                    no_close=True, no_move=True, no_title_bar=True, ):
        dpg.add_text("Place a trade:")
        dpg.add_input_text(label="Symbol", tag="asset")
        dpg.add_input_text(label="Quantity", tag="quantity")
        dpg.add_button(label="Place trade", callback=place_trade)

        dpg.add_text("Order book:")
        dpg.add_text("NONE:", indent=20)


        dpg.add_text("Account info:")
        dpg.add_text("Assets held:", indent=20)
        dpg.add_text("Cash balance:", indent=20)

        dpg.add_text("Order book:")
        with dpg.group(horizontal=True):
            with dpg.plot(label="bids", height=200, width=300):
                    dpg.add_plot_axis(dpg.mvXAxis, label="price", tag="xaxis_bids")
                    dpg.add_plot_axis(dpg.mvYAxis, label="volume", tag="yaxis_bids")
                    dpg.add_line_series(x=[], y=[], tag='bid_line', parent="yaxis_bids")

            with dpg.plot(label="asks", height=200, width=300):
                    dpg.add_plot_axis(dpg.mvXAxis, label="price", tag="xaxis_asks")
                    dpg.add_plot_axis(dpg.mvYAxis, label="volume", tag="yaxis_asks")
                    dpg.add_line_series(x=[], y=[], tag='ask_line', parent="yaxis_asks")

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