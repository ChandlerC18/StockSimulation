#---------Imports
from numpy import arange, sin, pi
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yfinance as yf
from itertools import count
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import matplotlib.dates as mdates
import pandas as pd
#---------End of imports
index = count()

tick = 'AAPL'
date_start = "2022-07-20"
date_end = "2022-07-21"
data = yf.Ticker(tick).history(start=date_start, end=date_end, interval="1m").reset_index()

x_values = []
y_values = []

data.loc[len(data) - 1, 'Datetime'] = data.iloc[len(data)-1]['Datetime'].replace(year=int(date_start[:4]), month=int(date_start[5:7]), day=int(date_start[8:]))

# fig = plt.Figure()
#
# x = np.arange(0, 2*np.pi, 0.01)        # x-array
#
# def animate(i):
#     print(i)
#     line.set_xdata(x+i/10.0)
#     line.set_ydata(np.sin(x+i/10.0))  # update the data
#     # x_values.append(i)
#     # y_values.append(np.sin(i))
#     # line.set_ydata(y_values)
#     # line.set_xdata(x_values)
#     return line,
#
# root = Tk.Tk()
#
# label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)
#
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.get_tk_widget().grid(column=0,row=1)
#
# ax = fig.add_subplot(111)
# line, = ax.plot(x, np.sin(x))
# ani = animation.FuncAnimation(fig, animate, frames=200, interval=25, repeat=False)
#
# Tk.mainloop()

######------Aunimated plot of stock data------######

def create_plot():
    plt.style.use('fivethirtyeight')

    x_values = []
    y_values = []

    index = count()

    def animate(i):
        counter = next(index)

        x_values.append(data.iloc[counter]['Datetime'].to_pydatetime())
        y_values.append(data.iloc[counter]['Close'])
        plt.cla()
        plt.axis([data.iloc[0]['Datetime'].to_pydatetime(), data.iloc[len(data) - 1]['Datetime'].to_pydatetime(), min(y_values) - 0.75, max(y_values) + 0.75])
        fig = plt.plot(x_values, y_values)
        plt.xlabel("Time")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz= data.iloc[0]['Datetime'].tz))
        # plt.gcf().autofmt_xdate()


    ani = animation.FuncAnimation(fig=plt.gcf(), func=animate, frames = len(data) - 1, interval=300, repeat=False)

    plt.tight_layout()
    plt.show()

#####-----Embed plot in tkinter-----#####
#
# plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True
#
# root = Tk.Tk()
# root.wm_title("Embedding in Tk")
#
# fig = plt.Figure(dpi=100)
# ax = fig.add_subplot(xlim=(data.iloc[0]['Datetime'].to_pydatetime(), data.iloc[len(data) - 1]['Datetime'].to_pydatetime()), ylim=(data.iloc[0]['Close'] - 0.5, data.iloc[0]['Close'] + 0.5))
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz= data.iloc[0]['Datetime'].tz))
# line, = ax.plot([], [], lw=2)
#
# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.draw()
#
# toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
# toolbar.update()
#
# button = Tk.Button(master=root, text="Quit", command=root.quit)
# button.pack(side=Tk.BOTTOM)
#
# toolbar.pack(side=Tk.BOTTOM, fill=Tk.X)
# canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
#
# index = count()
#
# def animate(i):
#     print(i)
#     if begin:
#         counter = next(index)
#         x_values.append(data.iloc[counter]['Datetime'].to_pydatetime())
#         y_values.append(data.iloc[counter]['Close'])
#         ax.set_ylim(min(y_values) - 0.5, max(y_values) + 0.5)
#         line.set_data(x_values, y_values)
#     else:
#         anim.event_source.stop()
#
# anim = animation.FuncAnimation(fig, animate,
#                                 frames=len(data) - 1, interval=100, repeat=False)
#
# begin = False
#
# def start():
#     global begin
#     begin = True
#     anim.event_source.start()
#
# def stop():
#     anim.event_source.stop()
#
# button = Tk.Button(master=root, text="Start", command=start)
# button.pack(side=Tk.BOTTOM)
#
# button = Tk.Button(master=root, text="Stop", command=stop)
# button.pack(side=Tk.BOTTOM)
#
# Tk.mainloop()

### BROKEN DIFFERENT COLORS GRAPH ###

def animate(i):

    global canvas

    if started:
        x_val.append(data.iloc[i]['Datetime'].to_pydatetime())
        y_val.append(data.iloc[i]['Close'])
        ax.set_ylim(min(y_val) - 0.5, max(y_val) + 0.5)

        # for start, stop in zip(range(0, len(x_val) - 1), range(1, len(x_val))):
        #     first, second = zip((x_val[start], y_val[start]), (x_val[stop], y_val[stop]))
        #     ax.plot(first, second, color=color(second))
        #     print(color(second))
        #
        # line.set_data(x_val, y_val)
        print(i)
        if (i < len(data) - 1):
            first, second = zip((data.iloc[i]['Datetime'].to_pydatetime(), data.iloc[i]['Close']),
                                (data.iloc[i + 1]['Datetime'].to_pydatetime(), data.iloc[i + 1]['Close']))
            # line.set_data(first, second)
            line, = ax.plot(first, second, lw=2, color=color(second))
            # canvas.draw()
        # plt.show()
    else:
        anim.event_source.stop()

    return line,

#### --- Different Colors --- ####
def color(y):
    return 'green' if y[1] > y[0] else 'red'

for i in range(len(data) - 1):
    first, second = zip((data.iloc[i]['Datetime'].to_pydatetime(), data.iloc[i]['Close']),
                        (data.iloc[i + 1]['Datetime'].to_pydatetime(), data.iloc[i + 1]['Close']))
    # line.set_data(first, second)
    line, = plt.plot(first, second, lw=2, color=color(second))

    # pos = computeNewPos(pos, vel, force)
    #
    #
    # plt.scatter(pos[0, 0], pos[0, 1], label = '1', color = 'r')
    # plt.scatter(pos[1, 0], pos[1, 1], label = '2', color = 'b')
    #
    # plt.xlabel('X')
    # plt.ylabel('Y')

    plt.pause(0.05)

plt.show()

#### OTHER CODE ####
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

## Combo box for selecting date
# enter_date = ttk.Frame(root)
# date_label = ttk.Label(enter_date, text="Please select a month:")
# date_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

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
# date_end = datetime.strptime(date.get(), "%Y-%m-%d") + datetime.timedelta(days=1)
# data = ticker.history(start=date.get(), end=date_end.strftime("%Y-%m-%d"), interval="1m").reset_index()
#
# data.loc[len(data) - 1, 'Datetime'] = data.iloc[len(data)-1]['Datetime'].replace(year=int(date_start[:4]), month=int(date_start[5:7]), day=int(date_start[8:]))
