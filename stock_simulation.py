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

def animate(i):
    x = np.linspace(0, 1, 100)
    y = fermi(x, 0.5, T[i])
    f_d.set_data(x, y)
    f_d.set_color(colors(i))
    temp.set_text(str(int(T[i])) + ' K')
    temp.set_color(colors(i))

### MAIN FLOW ###
## Configure main window
root = tk.Tk()

window = (1300, 800) # window dimension
screen = (root.winfo_screenwidth(), root.winfo_screenheight()) # get the screen dimension
center= (int(screen[0]/2 - window[0] / 2), int(screen[1]/2 - window[1] / 2)) # find the center point
root.geometry(f'{window[0]}x{window[1]}+{center[0]}+{center[1]}') # set position of window to center of screen

# root.resizable(False, False)
root.title('Stock Simulation')

## Stock entry textbox
stock = tk.StringVar() # store stock name
date = tk.StringVar() # store date

# # Stock entry frame
# root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=2)
# root.rowconfigure(0, weight=1)
# root.rowconfigure(1, weight=2)
# enter_stock = ttk.Frame(root)
#
#
# # stock label
# stock_label = ttk.Label(enter_stock, text="Stock:")
# stock_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
#
# stock_entry = ttk.Entry(enter_stock, textvariable=stock)
# stock_entry.focus()
# stock_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)


# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(2, weight=20)


# stock label
stock_label = ttk.Label(root, text="Stock:")
stock_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

stock_entry = ttk.Entry(root, textvariable=stock)
stock_entry.focus()
stock_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

# date label
date_label = ttk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

date_entry = ttk.Entry(root,  textvariable=date)
date_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

# login button
login_button = ttk.Button(root, text="Login")
login_button.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)


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

data['Datetime'] = [x.strftime("%H:%M") for x in data['Datetime']]

g = sns.lineplot(x='Datetime', y='Close', data=data)
g.set_xticks(range(0, 400, 30), labels=[x for x in data['Datetime'] if x[-2:] == '00' or x[-2:] == '30'])
plt.show()

f_d, = ax.plot([], [], linewidth=2.5)
temp = ax.text(1, 1, '', ha='right', va='top', fontsize=24)
ani = FuncAnimation(fig=fig, func=animate, frames=range(len(T)), interval=500, repeat=True)
fig.tight_layout()

## Run GUI
root.mainloop()
