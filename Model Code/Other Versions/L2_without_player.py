import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.src.layers import Input, Dense, Dropout
from keras.src.models import Model
from keras.src.regularizers import L2
from sklearn.metrics import accuracy_score

# Load dataset
current_dir = os.getcwd()
csv_file_path = os.path.join(current_dir, 'Cleanned Data', 'processed_data.csv')
data = pd.read_csv(csv_file_path)

# Separate features and target
X = data.drop('Tries', axis=1)
y = data['Tries']

# One-hot encode categorical features except for 'Player'
categorical_features = ['Home_Team', 'Away_Team', 'Position', 'isHomePlayer']
onehot_encoder = OneHotEncoder(sparse_output=False, drop='first')
X_encoded = onehot_encoder.fit_transform(X[categorical_features])

# Normalize numerical features
numerical_features = ['Prev_Round_Tries', 'Prev_Round_MinsPlayed', 'Prev_Round_All_RunMeters', 'Prev_OpponentTotalTackles', 'Prev_OpponentTeamTackleEfficiency']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X[numerical_features])

# Combine all processed features
X_combined = np.hstack([X_encoded, X_scaled])

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.1, random_state=42)

# Define the input layers
input_layer = Input(shape=(X_encoded.shape[1] + X_scaled.shape[1],), name='Input_Layer')


# Add dense layers with L2 regularization
x = Dense(64, activation='relu', kernel_regularizer=L2(0.001))(input_layer)
x = Dropout(0.5)(x)
x = Dense(32, activation='relu', kernel_regularizer=L2(0.001))(x)
x = Dropout(0.5)(x)
output = Dense(1, activation='linear')(x)

# Define the model
model = Model(inputs=input_layer, outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train,
                    validation_data=(X_test, y_test),
                    epochs=400, batch_size=256)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Accuracy on Test Set: {accuracy}')
