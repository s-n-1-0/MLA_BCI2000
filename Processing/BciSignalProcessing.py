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
from SignalManager import SignalManager

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
		self.count = 0
		pass
		
	def Process(self, stream_sig):
		self.signals.add_signal(stream_sig)
		self.count += 1
		sig = self.signals.get_last_samples(self.count)
		#TODO: LDA
		predict = random.randint(1,2)
		self.states['predictClass'] = predict
	
	def StopRun(self):
		saved_samples = self.signals.get_saved_samples()
		with open("saved_samples.pkl", "wb") as file:
			pickle.dump(saved_samples, file)
