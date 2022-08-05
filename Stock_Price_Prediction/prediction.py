#---------Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from keras.models import Sequential # deep learning
from keras.layers import LSTM, Dropout, Dense
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf # stock data
#---------End of imports

### CLASSES ###

### FUNCTIONS ###

### MAIN FLOW ###
if __name__ == '__main__':
    rcParams['figure.figsize'] = (20, 10)

    data = yf.Ticker('AAPL').history(period='max').reset_index() # get stock data
    df = data[['Date', 'Close']]

    # normalize dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = df.values

    train_data = dataset[0:987, :]
    valid_data = dataset[987:, :]

    df.index = df.Date
    df.drop("Date", axis=1, inplace=True)
    scaled_data = scaler.fit_transform(dataset)

    x_train_data, y_train_data = [], []

    for i in range(60, len(train_data)):
        x_train_data.append(scaled_data[i - 60:i, 0])
        y_train_data.append(scaled_data[i, 0])

x_train_data, y_train_data = np.array(x_train_data), np.array(y_train_data)
x_train_data = np.reshape(x_train_data, (x_train_data.shape[0], x_train_data.shape[1], 1))
