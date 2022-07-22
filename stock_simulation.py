import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from calendar import month_name
from tkcalendar import Calendar
from datetime import datetime
import numpy as np
import pandas as pd
import requests
import os
import yfinance as yf
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

### FUNCTIONS ###
def login_clicked():
    """ callback when the login button clicked
    """
    msg = f'You entered stock: {stock.get()}'
    showinfo(
        title='Information',
        message=msg
    )
#
# def animate(i):
#     time.append(i)
#     close.append(random.randint(0, 5))
#     f_d.set_data(time, close)
    # f_d.set_color(colors(i))
    # temp.set_text(str(int(T[i])) + ' K')
    # temp.set_color(colors(i))

### MAIN FLOW ###
# # Configure main window
# root = tk.Tk()
#
# window = (1300, 800) # window dimension
# screen = (root.winfo_screenwidth(), root.winfo_screenheight()) # get the screen dimension
# center= (int(screen[0]/2 - window[0] / 2), int(screen[1]/2 - window[1] / 2)) # find the center point
# root.geometry(f'{window[0]}x{window[1]}+{center[0]}+{center[1]}') # set position of window to center of screen
#
# # root.resizable(False, False)
# root.title('Stock Simulation')
#
# ## Stock entry textbox
# stock = tk.StringVar() # store stock name
# date = tk.StringVar() # store date
#
# # # Stock entry frame
# # root.columnconfigure(0, weight=1)
# # root.columnconfigure(1, weight=2)
# # root.rowconfigure(0, weight=1)
# # root.rowconfigure(1, weight=2)
# # enter_stock = ttk.Frame(root)
# #
# #
# # # stock label
# # stock_label = ttk.Label(enter_stock, text="Stock:")
# # stock_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
# #
# # stock_entry = ttk.Entry(enter_stock, textvariable=stock)
# # stock_entry.focus()
# # stock_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
#
#
# # configure the grid
# root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=3)
# root.columnconfigure(2, weight=20)
#
#
# # stock label
# stock_label = ttk.Label(root, text="Stock:")
# stock_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
#
# stock_entry = ttk.Entry(root, textvariable=stock)
# stock_entry.focus()
# stock_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
#
# # date label
# date_label = ttk.Label(root, text="Date (YYYY-MM-DD):")
# date_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
#
# date_entry = ttk.Entry(root,  textvariable=date)
# date_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
#
# # login button
# login_button = ttk.Button(root, text="Login")
# login_button.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)


# ## Select date
# enter_date = ttk.Frame(root)
# date_label = ttk.Label(enter_date, text="Please select a month:")
# date_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
#
# # create a combobox
# selected_month = tk.StringVar()
# month_cb = ttk.Combobox(enter_date, textvariable=selected_month)
#
# # get first 3 letters of every month name
# month_cb['values'] = [month_name[m][0:3] for m in range(1, 13)]
#
# # prevent typing a value
# month_cb['state'] = 'normal'
#
# # place the widget
# month_cb.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
#
#
# # bind the selected value changes
# def month_changed(event):
#     """ handle the month changed event """
#     showinfo(
#         title='Result',
#         message=f'You selected {selected_month.get()}!'
#     )
#
#
# month_cb.bind('<<ComboboxSelected>>', month_changed)
#
# # set the current month
# current_month = datetime.now().strftime('%b')
# month_cb.set(current_month)

## Get stock data ##
tick = 'AAPL'
date_start = "2022-07-07"
date_end = "2022-07-08"
data = yf.Ticker(tick).history(start=date_start, end=date_end, interval="1m").reset_index()

# data['Datetime'] = [x.strftime("%H:%M") for x in data['Datetime']]

# g = sns.lineplot(x='Datetime', y='Close', data=data)
# g.set_xticks(range(0, 400, 30), labels=[x for x in data['Datetime'] if x[-2:] == '00' or x[-2:] == '30'])
# plt.show()

# time = []
# close = []
#
# fig = plt.figure(figsize=(6, 4))
# ax = fig.add_subplot(111)
# f_d, = ax.plot([], [], linewidth=2.5)
# temp = ax.text(1, 1, '', ha='right', va='top', fontsize=24)
# ani = FuncAnimation(fig=fig, func=animate, frames=range(len(data)), interval=500, repeat=False)
# fig.tight_layout()
# plt.show()

from itertools import count
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

plt.style.use('fivethirtyeight')

x_values = []
y_values = []

index = count()

def animate(i):
    haha = next(index)
    x_values.append(data.iloc[haha]['Datetime'])
    y_values.append(data.iloc[haha]['Close'])
    plt.cla()
    plt.plot(x_values, y_values)

# ani = FuncAnimation(fig=plt.gcf(), func=animate, frames = len(data), interval=300, repeat=False)

# plt.tight_layout()
# plt.show()
## Run GUI
# root.mainloop()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter Matplotlib Demo')

        # prepare data
        data = {
            'Python': 11.27,
            'C': 11.16,
            'Java': 10.46,
            'C++': 7.5,
            'C#': 5.26
        }
        languages = data.keys()
        popularity = data.values()

        # create a figure
        figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        # axes.bar(languages, popularity)
        # axes.set_title('Top 5 Programming Languages')
        # axes.set_ylabel('Popularity')
        ani = FuncAnimation(fig=figure, func=animate, frames = len(data), interval=300, repeat=False)

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        plt.show()


if __name__ == '__main__':
    app = App()
    app.mainloop()
