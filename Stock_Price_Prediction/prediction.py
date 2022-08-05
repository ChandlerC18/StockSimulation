#---------Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from keras.models import Sequential # deep learning
from keras.layers import LSTM, Dropout, Dense
from sklearn.preprocessing import MinMaxScaler
#---------End of imports

### FUNCTIONS ###
def get_data(path):
    ''' returns the pandas dataframe at the specificed path '''

    df = pd.read_csv(path) # read data

    df["Date"] = pd.to_datetime(df.Date, format="%Y-%m-%d") # format date
    df.index = df['Date']

    data = df.sort_index(ascending=True, axis=0)

    return data

def filter_data(df, columns):
    ''' returns a copy of data with the specified columns '''

    new_dataset = pd.DataFrame(index = range(0, len(df)), columns=columns)

    for i in range(0,len(data)):
        for col in columns:
            new_dataset[col][i] = data[col][i]

    new_dataset.index = new_dataset.Date
    new_dataset.drop("Date", axis=1, inplace=True)

    return new_dataset

def normalize(data):
    ''' normalize the data '''

    final_dataset = data.values

    train_data = final_dataset[0:987, :]
    valid_data = final_dataset[987:, :]

    scaler = MinMaxScaler(feature_range = (0,1))
    scaled_data = scaler.fit_transform(final_dataset)

    x_train_data, y_train_data=[], []

    for i in range(60, len(train_data)):
        x_train_data.append(scaled_data[i - 60:i, 0])
        y_train_data.append(scaled_data[i, 0])

    x_train_data, y_train_data = np.array(x_train_data), np.array(y_train_data)

    x_train_data = np.reshape(x_train_data, (x_train_data.shape[0], x_train_data.shape[1], 1))

    return (scaler, x_train_data, y_train_data, train_data, valid_data)

def create_model(scaler, x_train_data, y_train_data, train_data, valid_data, save=False):
    ''' create and train the LSTM model; returns the list of predicted prices '''

    lstm_model=Sequential()
    lstm_model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train_data.shape[1], 1)))
    lstm_model.add(LSTM(units=50))
    lstm_model.add(Dense(1))

    lstm_model.compile(loss='mean_squared_error', optimizer='adam')
    lstm_model.fit(x_train_data,y_train_data, epochs=1, batch_size=1, verbose=2)

    inputs_data = new_dataset[len(new_dataset) - len(valid_data) - 60:].values
    inputs_data = inputs_data.reshape(-1, 1)
    inputs_data = scaler.transform(inputs_data)

    # sample of dataset to make prediction
    X_test=[]

    for i in range(60, inputs_data.shape[0]):
        X_test.append(inputs_data[i - 60:i, 0])

    X_test=np.array(X_test)

    X_test=np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_closing_price = lstm_model.predict(X_test)
    predicted_closing_price = scaler.inverse_transform(predicted_closing_price)

    if save:
        lstm_model.save("saved_lstm_model.h5") # save model

    return predicted_closing_price

def plot(data, prediction, save=False):
    ''' create the plot of predicted data '''

    train_data = data[:987]
    valid_data = data[987:]
    valid_data['Predictions'] = prediction
    plt.plot(train_data["Close"])
    plt.plot(valid_data[['Close',"Predictions"]])

    plt.show()

    if save:
        plt.savefig('predicted_prices_graph.png')

### MAIN FLOW ###
if __name__ == '__main__':
    rcParams['figure.figsize'] = (20, 10) # set up figure

    data = get_data("data/NSE-Tata-Global-Beverages-Limited.csv") # get data
    new_dataset = filter_data(data, ['Date', 'Close']) # filter data
    normalized = normalize(new_dataset) # normalize filtered dataset
    predicted_closing_price = create_model(*normalized) # build and train LSTM model
    plot(new_dataset, predicted_closing_price)# visualize performace
