"""
A learning agent for starcraft, with comments!
Using the optimistic initial values strategy,
get the agent to choose profitable actions
python3 -m pysc2.bin.agent --map CollectMineralShards --agent ungsc2.agents.crystal_learner_nn.CrystalLearnerAgent
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from pysc2.lib import actions

class CrystalLearnerAgent(object):
	"""Learning agent for solving crystal shards"""
	def __init__(self):
		self.episodes = 0
		self.obs_spec = None
		self.action_spec = None
		self.old_act = -1
		self.actions = [Action(0)]
		self.old_score=0

	def setup(self, obs_spec, action_spec):
		self.obs_spec = obs_spec
		self.action_spec = action_spec

	def reset(self):
		self.episodes += 1

	def build_model(self, function_id):
		model_name = str(function_id)+'.h5'
		try:
			model = load_model(model_name)
		except:
			return "zero"
		return model
		

	def step(self, obs):
		#everything happens here
		act_ids = [act.a_id for act in self.actions]

		for act in obs.observation["available_actions"]:
			if act not in act_ids:
				self.actions.append(Action(act))


		reward = obs.observation["score_cumulative"][0] - self.old_score
		self.old_score = obs.observation["score_cumulative"][0]

		if self.old_act!=-1:
			self.actions[self.old_act].update(reward)
			if reward>0 and type(self.actions[self.old_act].model)==int:
				#if score was good, and no model exist, build model
				self.actions[self.old_act].model = self.build_model(self.actions[self.old_act].a_id)	

		j = np.argmax([act.mean for act in self.actions])

		if self.actions[j].a_id not in obs.observation["available_actions"]:
			function_id = np.random.choice(obs.observation["available_actions"])
			args = [[np.random.randint(0, size) for size in arg.sizes]
				for arg in self.action_spec.functions[function_id].args]
		else:
			function_id = self.actions[j].a_id
			if self.actions[j].model==2:
				#get args from model
				print("shouldn't be here")
			else:
				#no model present, random gen
				args = [[np.random.randint(0, size) for size in arg.sizes]
					for arg in self.action_spec.functions[function_id].args]

		

		self.old_act=j

		return actions.FunctionCall(function_id, args)

class Action:
	def __init__(self, a_id):
		self.a_id = a_id
		self.mean = 1 #mean of reward (optimistic)
		self.N = 1 #steps
		self.model = 0 #NN model

	def update(self, x):
		self.N +=1
		old = self.mean
		self.mean = (1 - 1/self.N)*self.mean + (1/self.N)*x
