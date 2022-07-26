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
