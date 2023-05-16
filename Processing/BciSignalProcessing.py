import logging
from pathlib import Path
import os
import pickle
import sys
sys.path.append(os.path.join(Path().resolve(), "MLA_Processing"))
logging.basicConfig(
	level=logging.INFO)
import numpy as np
import random
from SignalManager import PredictHistory, SignalManager

class BciSignalProcessing(BciGenericSignalProcessing):
	def Construct(self):
		parameters = [
			
		]
		states = [
			"predictClass  3 0 0 0"
		]
		return (parameters, states)
		
	def Preflight(self, sigprops):
		pass
	
	def Initialize(self, indim, outdim): #indim[0] = ch
		self.signals = SignalManager(indim[0])
		self.history = PredictHistory()
		pass
		
	def Process(self, stream_sig):
		trial_num = self.states['sender_trialNum']
		fb = self.states["sender_feedback"] # fb is 0 == true_class is 0
		true_class = self.states['sender_trueClass'] # 0(wait) or 1 or 2 
		self.signals.add_signal(trial_num,stream_sig,true_class)
		data = self.signals.get_last_samples()
		if data is None:
			return
		sig = data[:-2,:]
		#TODO: LDA
		if fb == 1:
			predict = random.randint(1,2)
		else:
			predict = 0
		self.states['predictClass'] = predict
		self.history.add_data(trial_num,data,predict)
	
	def StopRun(self):
		with open("history.pkl", "wb") as file:
			pickle.dump(self.history.history, file)
		np.save('data', self.signals.combined_data)
		
