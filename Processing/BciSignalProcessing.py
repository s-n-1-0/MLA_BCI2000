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
import time
from SignalManager import PredictHistory, SignalManager
import threading

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
		self.predict_history = PredictHistory()
		self.is_run = False
	
	def StartRun(self):
		self.is_run = True
		self.predict_class = self.states['predictClass']
		thread = threading.Thread(target=processing,args=[self])
		thread.start()

	def Process(self, stream_sig):
		trial_num = self.states['sender_trialNum']
		true_class = self.states['sender_trueClass'] # 0(wait) or 1 or 2 
		self.signals.add_signal(trial_num,stream_sig,true_class)
		self.states['predictClass'] = self.predict_class
		
	
	def StopRun(self):
		self.is_run = False
		with open("history.pkl", "wb") as file:
			pickle.dump(self.predict_history.history, file)
		np.save('data', self.signals.combined_data)
		
def processing(module:BciSignalProcessing):
	while module.is_run:
		data = module.signals.get_last_samples()
		if data is None:
			continue
		sig = data[:-2,:]
		fb = module.states["sender_feedback"] # fb is 0 == true_class is 0
		trial_num = module.states['sender_trialNum']
		#TODO: LDA
		if fb == 1:
			predict = random.randint(1,2)
		else:
			predict = 0
		module.predict_class = predict
		module.predict_history.add_data(trial_num,data,predict)
		time.sleep(0.2)