#---------Imports
import tkinter as tk
from tkinter import ttk
from calendar import month_name
from tkcalendar import Calendar
import datetime
import numpy as np
import pandas as pd
import requests
import os
import yfinance as yf
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import pytz
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
#---------End of imports

### FUNCTIONS ###
def run_clicked():
    """ callback to validate stock ticker and date in correct format when run button is clicked
    """

    global valid_entries
    global ticker

    msg = ''
    ticker = yf.Ticker(stock.get())

    # check if stock ticker exists
    if (ticker.info['regularMarketPrice'] == None):
         msg += f"No information for '{stock.get()}'. \nPlease enter a valid stock ticker.\n\n\n"

    # check format of date
    try:
        datetime.datetime.strptime(date.get(), "%Y-%m-%d")
    except:
        msg += f'Invalid date format. Please \nenter a valid date \nwith the following \nformat YYYY-mm-dd.'

    if msg: # there's an error
        tk.messagebox.showerror(title='Error', message=msg)
    else: # valid entries
        valid_entries = True
        prepare_data()

def prepare_data():
    """ retrieves the data for the plot and sets up axes for the graph
    """

    global ax
    global fig
    global data

    date_end = datetime.datetime.strptime(date.get(), "%Y-%m-%d") + datetime.timedelta(days=1)
    data = ticker.history(start=date.get(), end=date_end.strftime("%Y-%m-%d"), interval="1m").reset_index() # stock ticker data

    data.loc[len(data) - 1, 'Datetime'] = data.iloc[len(data)-1]['Datetime'].replace(year=int(date.get()[:4]), month=int(date.get()[5:7]), day=int(date.get()[8:])) # change date of last entry

    ax.set_ylim(data.iloc[0]['Close'] - 0.5, data.iloc[0]['Close'] + 0.5) # set up y axis
    ax.set_xlim(data.iloc[0]['Datetime'].to_pydatetime(), data.iloc[len(data) - 1]['Datetime'].to_pydatetime()) # set up x axis
    canvas.draw()

def agreement_changed():
    """ callback to display the plot toolbar or not
    """

    global toolbar

    if agreement.get() == 'agree': # want to display toolbar
        toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=6, column=0)
    else: # no toolbar
        toolbar.grid_remove()


def plot_point():
    """ sets up animation to display the points of transactions on the plot
    """

    if info[-1][0] == 'up': # long/buy transaction
        point_up.set_data([info[-1][1]], [info[-1][2]])
        anim_point_up = FuncAnimation(fig, animate_point_up, frames=len(data) - len(x_val) + 1, interval=20, repeat=False, blit=True)
    elif info[-1][0] == 'down': # short/sell transaction
        point_down.set_data([info[-1][1]], [info[-1][2]])
        anim_point_down = FuncAnimation(fig, animate_point_down, frames=len(data) - len(x_val) + 1, interval=20, repeat=False, blit=True)

def resume():
    """ callback to resume animated plot of the stock price
    """

    global anim
    global started

    if started: # check if animation has started already
        anim.event_source.start()
    elif data != None: # start animation if it wasn't started yet and valid stock ticker and date
        started = True
        anim = FuncAnimation(fig, animate, init_func=init, frames=len(data) - 1, interval=20, repeat=False, blit=True)

def pause():
    """ callback to pause animated plot of the stock price
    """

    if started: # check if the plot has been started, then stop all 3 animations; otherwise, nothing needs to be done
        anim.event_source.stop()
        anim_point_up.event_source.stop()
        anim_point_down.event_source.stop()

def trade(guess):
    """ save data of transaction
    """

    global mode

    if (mode == 'Begin'): # no transactions have been completed
        mode = guess
        time = x_val[-1]
        amount = y_val[-1]
        info.append((mode, time, amount))
        plot_point()
    elif (mode == 'complete'): # only up to 2 transactions are allowed
        pass
    elif (mode == 'up' and guess == 'down') or (mode == 'down' and guess == 'up'): # has to be 2 different transactions
        mode = 'complete'
        time = x_val[-1]
        amount = y_val[-1]
        info.append((guess, time, amount))
        plot_point()

def down():
    """ wrapper function to call the sell/short transaction
    """

    trade('down')

def up():
    """ wrapper function to call the buy/long transaction
    """

    trade('up')

def done():
    """ display transaction information when trading is done
    """

    msg = 'Below is a list of your transactions: \n\n'

    # loop through all transactions
    for i in range(len(info)):
        if i == 0 and info[i][0] == 'up':
            msg += 'Long'
        elif i == 0 and info[i][0] == 'down':
            msg += 'Short'
        elif i == 1 and info[i][0] == 'up':
            msg += 'Bought'
        elif i == 1 and info[i][0] == 'down':
            msg += 'Sold'

        msg += f" {stock.get().upper()} at the price of {info[i][2]:0.2f} at {info[i][1]:%H:%M} \n\n"

    if len(info) == 2: # if 2 transactions, calculate profit
        msg += "~~~~~~~~~~~~~~~~\n\n"
        profit = info[0][2] if info[0][0] == 'down' else -info[0][2]
        profit += info[1][2] if info[1][0] == 'down' else -info[1][2]
        msg += f"Your profit is {profit:0.2f}"

    tk.messagebox.showinfo(title='Information', message=msg)


def animate(i):
    """ animation function to display the line graph of the stock price
    """

    global canvas

    if i == len(data) - 2:
        done() # plot is done
    elif started:
        x_val.append(data.iloc[i]['Datetime'].to_pydatetime()) # add new time
        y_val.append(data.iloc[i]['Close']) # add new stock price
        ax.set_ylim(min(y_val) - 0.5, max(y_val) + 0.5) # change y axis limits if necessary

        line.set_data(x_val, y_val) # change data of graph
        canvas.draw() # draw
    else:
        anim.event_source.stop()

    return line,

def animate_point_up(i):
    """ animation function to display up triangle to indicate long/buy transaction point
    """

    global canvas

    if i == len(data) - 2:
        done()
    elif started:
        canvas.draw()
    else:
        anim_point_up.event_source.stop()

    return point_up,

def animate_point_down(i):
    """ animation function to display down triangle to indicate short/sell transaction point
    """

    global canvas

    if i == len(data) - 2:
        done()
    elif started:
        canvas.draw()
    else:
        anim_point_down.event_source.stop()

    return point_down,

def init():
    """ initialize line plot data to empty to begin animation
    """

    line.set_data([], [])
    return line,

#
# def animate(i):
#     time.append(i)
#     close.append(random.randint(0, 5))
#     f_d.set_data(time, close)
    # f_d.set_color(colors(i))
    # temp.set_text(str(int(T[i])) + ' K')
    # temp.set_color(colors(i))

### MAIN FLOW ###
mode = 'Begin' # last transaction
amount = 0 # profit
ticker = None # yfinance stock ticker
valid_entries = False # boolean for whether data entered is valid

# Configure main window
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

# Run button
run_button = ttk.Button(root, text="Run", command=run_clicked)
run_button.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

# Checkbox to display graph toolbar
agreement = tk.StringVar()
checkbox = ttk.Checkbutton(root, text='Show Graph Toolbar', command=agreement_changed,
                variable=agreement, onvalue='agree', offvalue='disagree')
checkbox.grid(column=2, row=3, sticky=tk.E, padx=5, pady=5)

# Canvas element for plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=5, column=0, ipadx=40, ipady=20, columnspan=3)

# Quit button
button = tk.Button(master=root, text="Quit", command=root.quit)
button.grid(row=7, column=2)

# Start button
button = tk.Button(master=root, text="Start", command=resume)
button.grid(row=7, column=0)

# Pause button
button = tk.Button(master=root, text="Pause", command=pause)
button.grid(row=7, column=1)

# Long/Buy button
button = tk.Button(master=root, text="Long/Buy", command=up)
button.grid(row=8, column=0)

# Sell/Short button

button = tk.Button(master=root, text="Sell/Short", command=down)
button.grid(row=8, column=1)

### Create figure
## Init Plot Variables
data = None # pandas dataframe of stock information
x_val = [] # time
y_val = [] # stock price
info = [] # transaction list

toolbar = None # plot toolbar

anim = None # line plot animation
anim_point_up = None # up triangle animation
anim_point_down = None # down triangle animation
started = False # boolean for whether animation has started
## End Variables

# Plot parameters
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

fig = plt.Figure(dpi=100)
ax = fig.add_subplot(xlim=(datetime.datetime(2021, 6, 10, hour=8, minute=30, tzinfo=pytz.timezone('America/New_York')),
                           datetime.datetime(2021, 6, 10, hour=15, minute=0, tzinfo=pytz.timezone('America/New_York'))), ylim=(0, 2)) # default plot axis limits
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz=pytz.timezone('America/New_York'))) # change format of time on x axis

# initialize empty plot data
line, = ax.plot([], [], lw=2, color='lightblue')
point_up, = ax.plot([], [], 'k^')
point_down, = ax.plot([], [], 'kv')

# Run GUI
root.mainloop()
