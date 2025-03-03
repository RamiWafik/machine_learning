# Recurrent Neural Networks

# Importing Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Data preprocessing
dataset_train = pd.read_csv('Google_stock_Price_Train.csv')
training_set = dataset_train.iloc[:, 1:2].values

# Feature Scaling (Normalisation)
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()
training_set_scaled = sc.fit_transform(training_set)

# Creating Datastructure With 60 Timesteps
X_train = []
y_train = []
for i in range(60, 1258):
    X_train.append(training_set_scaled[i - 60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping And Adding New Dimension
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Building The RNN
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising The RNN
regressor = Sequential()

# Adding First LSTM Layer And Dropout Regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding Three More LSTM Layers With Dropout Regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# Adding Output Layer
regressor.add(Dense(units = 1))

# Compiling The RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting The Rnn To The Training Set
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

# Import Real Prices And Preparing Inputs For Prediction
dataset_test = pd.read_csv('Google_stock_Price_Test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1, 1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 80):
    X_test.append(inputs[i - 60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Predicting The Results
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Visualising The Results
plt.plot(real_stock_price, color = 'red', label = 'Real Google Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()
