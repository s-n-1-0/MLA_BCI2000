import logging
from pathlib import Path
import os
import pickle
import sys
import datetime

sys.path.append(os.path.join(Path().resolve(), "MLA_Processing"))
logging.basicConfig(filename="test.log",
	level=logging.INFO)
import numpy as np
import random
import time
from SignalManager import PredictHistory, SignalManager
import threading
import keras
import json
with open("./MLA_Processing/settings.json") as f:
	settings = json.load(f)
loaded = keras.models.load_model(settings["model_path"])
ch_list = []
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
		self.ch = indim[0]
		self.is_run = False
	
	def StartRun(self):
		self.is_run = True
		self.signals = SignalManager(self.ch)
		self.predict_history = PredictHistory()
		self.predict_class = self.states['predictClass'] + 1
		thread = threading.Thread(target=processing,args=[self])
		thread.start()

	def Process(self, stream_sig):
		trial_num = self.states['sender_trialNum']
		true_class = self.states['sender_trueClass'] # 0(wait) or 1 or 2 
		self.signals.add_signal(trial_num,stream_sig,true_class)
		self.states['predictClass'] = self.predict_class
		
	
	def StopRun(self):
		self.is_run = False
		now = datetime.datetime.now()
		dir_name = f"{settings['save_path']}/{settings['subject_id']}/history_{now.strftime('%Y_%m_%d_%H_%M_%S')}"
		os.makedirs(dir_name)
		with open(f"{dir_name}/history.pkl", "wb") as file:
			pickle.dump(self.predict_history.history, file)
		np.save(f"{dir_name}/data", self.signals.combined_data)
		
def processing(module:BciSignalProcessing):
	while module.is_run:
		data = module.signals.get_last_samples()
		if data is None:
			continue
		sig = data.astype('float32')
		sig = np.array([sig[ch_list,:]])[:,:,:,None]
		fb = module.states["sender_feedback"] # fb is 0 == true_class is 0
		trial_num = module.states['sender_trialNum']
		#feedback
		predict = loaded.predict(sig)#,batch_size=1)
		module.predict_class = predict[0]
		module.predict_history.add_data(trial_num,data,predict)
		time.sleep(0.1)