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
import time
from SignalManager import SignalManager
from Preprocessing import preprocess
import threading
import keras
import json
with open("./MLA_Processing/settings.json") as f:
	settings = json.load(f)
loaded = keras.models.load_model(settings["model_path"])
ch_list = [0,1,2,3,4,5,6,7,8,9,10,11,12]
fs = 500
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
		self.predict_class = 0
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
		dir_name = f"{settings['save_path']}/{settings['subject_id']}"
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
		np.save(f"{dir_name}/data_{now.strftime('%Y_%m_%d_%H_%M_%S')}", self.signals.total_combined_data)
		
def processing(module:BciSignalProcessing):
	predict_list = []
	true_class = 0
	prev_true_class = 0
	while module.is_run:
		prev_true_class = true_class
		true_class = module.states['sender_trueClass']
		data = module.signals.get_last_samples()
		if data is None or true_class == 0:
			module.predict_class = 0
			time.sleep(0.01)
			continue
		if prev_true_class == 0 and true_class != 0:
			module.signals.reset()
			predict_list = []
			module.predict_class = 0
			time.sleep(0.01)
			continue
		sig = np.asarray(data).astype('float32')
		sig = preprocess(sig[ch_list,:],fs)
		sig = np.array([sig])[:,:,:,None]
		fb = module.states["sender_feedback"] # fb is 0 == true_class is 0
		#feedback
		prediction = loaded.predict(sig)[0]
		prediction = 1 if prediction > 0.5 else 0
		predict_list.append(prediction)
		module.predict_class = round(np.mean(predict_list[-10:])) + 1
		time.sleep(0.5)