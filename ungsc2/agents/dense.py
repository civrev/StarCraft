"""
An agent that uses a dense neural network
for the Collect Mineral Shards Map
Work in progress
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#it isn't imported, but you'll need h5py installed too
import numpy as np
np.random.seed(16)
from keras.layers import Dense
from keras.models import Sequential
from keras.models import load_model

from ungsc2.agents import base
from pysc2.lib import actions
from pysc2.lib import features

_PLAYER_RELATIVE = features.MINIMAP_FEATURES.player_relative.index
_PLAYER_FRIENDLY = 1 #player
_PLAYER_NEUTRAL = 3 #beacon/minerals
_NO_OP = 0 #the action for no action
_SELECT_ARMY = actions.FUNCTIONS.select_army.id


#always just extend base agent
class DenseAgent(base.BaseAgent):
	def step(self, obs):
		#just run the step in base agent first
		super(DenseAgent, self).step(obs)
		#everything that happens, should happen here
		
		#so for collecting minerals, we don't need many observations
		#print(_PLAYER_RELATIVE)
		player_relative = obs.observation["minimap"][_PLAYER_RELATIVE]

		#if you only want the cordinates of the stuff, add .nonzero() to the end
		neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()

		player_y, player_x = (player_relative == _PLAYER_FRIENDLY).nonzero()


		print(neutral_y)
		#print(neutral_a.shape, player_a.shape)

		try:
			model = load_model("dense_agent_model.h5")
		except:
			model = Sequencial()
			model.add(Dense(100, activation='relu', input_shape=(44,)))
			model.add(Dense(100, activation='relu'))
			model.add(Dense(20, activation='softmax'))
			model.compile(optimizer='adam', loss='categorical_crossentropy',
			metrics=['accuracy'])

		#the categories sorting into are zip(neutral_x, neutral_y)?
		classes = zip(neutral_x, neutral_y)

		if not neutral_y.any() or not player_y.any():
			return actions.FunctionCall(_NO_OP, [])

		#return actions.FunctionCall(function_id, args)
		return actions.FunctionCall(0, [])
