import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np

import numpy as np

X = np.random.rand(1000, 5)  # 1000 samples, 5 features (random values for demo)
y = np.random.randint(2, size=1000)


# Reshape data for LSTM: (samples, time steps, features)
X_lstm = np.reshape(X, (X.shape[0], 1, X.shape[1]))

# Define LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(1, X.shape[1])),
    LSTM(50, return_sequences=False),
    Dense(25),
    Dense(1, activation='sigmoid')  # Binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_lstm, y, epochs=10, batch_size=32)
