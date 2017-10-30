'''
building and training neural networks from
scripted agents

python3 create_nn.py

'''

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


from pysc2.lib import actions
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from keras.models import load_model

feat1 = "7_SELECT_ARMY_features.txt"
targ1 = "7_SELECT_ARMY_targets.txt"
feat2 = "331_MOVE_SCREEN_features.txt"
targ2 = "331_MOVE_SCREEN_targets.txt"

#alright, load all these in to a dataframe
f1 = pd.read_csv(feat1, header=None)
t1 = pd.read_csv(targ1, header=None)
f2 = pd.read_csv(feat2, header=None)
t2 = pd.read_csv(targ2, header=None)

#since f1/t1 are particularly useless, we will focus on improving
#our good moves with neural networks

#our features are workable as is, we just need to do our targets
#take a look at our targets from "331_MOVE_SCREEN_targets.txt"
print("targets from 331_MOVE_SCREEN_targets.txt\n",t2.head())

#I will try and sum these 3 outputs into the two x,y coordinates
#the X,Y coordinate
t2.drop([0], axis = 1, inplace = True)

def strip_paren(word):
	word = word.replace("(", "")
	word = word.replace(")", "")
	word = word.replace("]", "")
	return int(word)/2


#change them to int values
t2.iloc[:,0] = t2.iloc[:,0].apply(strip_paren, convert_dtype=int)
t2.iloc[:,1] = t2.iloc[:,1].apply(strip_paren, convert_dtype=int)
print(t2.head())


#all our data is what it needs to be, now we can begin using the neural networks on it
#split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(f2.as_matrix(),t2.as_matrix(), test_size=0.25, random_state=21)

#build the NN

#early stopping monitor, after 50 epochs of no improvement, quit
monitor = EarlyStopping(patience=5)

n_cols = X_train.shape[1] #the size of the player_relative feature layer
print(X_train.shape,y_train.shape)
print("Building NN:","331_MOVE_SCREEN","STATE_SIZE",n_cols)
model = Sequential()
model.add(Dense(48, activation='relu', input_shape=(n_cols,)))
model.add(Dense(36, activation='relu'))
model.add(Dense(24, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(2, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
print(model.summary())
#train the NN
model.fit(X_train, y_train, epochs=500, callbacks=[monitor])
model.save('331.h5')

#model = load_model('331.h5')

#test the NN
#single = np.array([X_test[0]])
#pred=model.predict([single])
pred = model.predict(X_test)
print(np.mean((y_test-pred)/y_test))

