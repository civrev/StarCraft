"""
Scripted agents.
From the pysc2 module, but with small changes to build
a training set for my neural network

python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.scripted.CollectMineralShards

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy
numpy.set_printoptions(threshold=numpy.nan)

from ungsc2.agents import base
from pysc2.lib import actions
from pysc2.lib import features

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_NOT_QUEUED = [0]
_SELECT_ALL = [0]


class MoveToBeacon(base.BaseAgent):
	"""An agent specifically for solving the MoveToBeacon map."""

	def step(self, obs):
		super(MoveToBeacon, self).step(obs)
		if _MOVE_SCREEN in obs.observation["available_actions"]:
			player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
			neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
			if not neutral_y.any():
				return actions.FunctionCall(_NO_OP, [])
			target = [int(neutral_x.mean()), int(neutral_y.mean())]
			return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, target])
		else:
			return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])


class CollectMineralShards(base.BaseAgent):
	"""An agent specifically for solving the CollectMineralShards map."""

	def step(self, obs):
		super(CollectMineralShards, self).step(obs)
		player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
		obs_string = ' '.join(player_relative.astype(str).flatten().tolist())
		if _MOVE_SCREEN in obs.observation["available_actions"]:
			neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
			player_y, player_x = (player_relative == _PLAYER_FRIENDLY).nonzero()
			if not neutral_y.any() or not player_y.any():
				out_file = open(str(_NO_OP)+"_NO_OP_df.txt", 'a')
				out_file.write(obs_string + "|"+str([]) + "\n")
				return actions.FunctionCall(_NO_OP, [])
			player = [int(player_x.mean()), int(player_y.mean())]
			closest, min_dist = None, None
			for p in zip(neutral_x, neutral_y):
				dist = numpy.linalg.norm(numpy.array(player) - numpy.array(p))
				if not min_dist or dist < min_dist:
					closest, min_dist = p, dist
			out_file = open(str(_MOVE_SCREEN)+"_MOVE_SCREEN_df.txt", 'a')
			out_file.write(obs_string +"|"+str([_NOT_QUEUED, closest]) + "\n")
			return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, closest])
		else:
			out_file = open(str(_SELECT_ARMY)+"_SELECT_ARMY_df.txt", 'a')
			out_file.write(obs_string+ "|" + str([_SELECT_ALL]) + "\n")
			return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])


class DefeatRoaches(base.BaseAgent):
	"""An agent specifically for solving the DefeatRoaches map."""

	def step(self, obs):
		super(DefeatRoaches, self).step(obs)
		if _ATTACK_SCREEN in obs.observation["available_actions"]:
			player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
			roach_y, roach_x = (player_relative == _PLAYER_HOSTILE).nonzero()
			if not roach_y.any():
				return actions.FunctionCall(_NO_OP, [])
			index = numpy.argmax(roach_y)
			target = [roach_x[index], roach_y[index]]
			return actions.FunctionCall(_ATTACK_SCREEN, [_NOT_QUEUED, target])
		elif _SELECT_ARMY in obs.observation["available_actions"]:
			return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
		else:
			return actions.FunctionCall(_NO_OP, [])
