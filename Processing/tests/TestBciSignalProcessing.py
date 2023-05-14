import logging
logging.basicConfig(
	level=logging.INFO)
import numpy as np
import random

class BciSignalProcessing(BciGenericSignalProcessing):	
	
	
	
	def Construct(self):
		parameters = [
			
		]
		states = [
			#"TargetClass  3 0 0 0"
		]
		self.cache = np.zeros((16,0))
		return (parameters, states)
		
	
	
	def Preflight(self, sigprops):
		pass
		
	
	
	def Initialize(self, indim, outdim):
		pass
		
	
	
	def Process(self, sig):
		#self.states['TargetClass2'] = random.randint(0,5)
		self.cache = np.hstack([self.cache,sig])
		
	def StopRun(self):
		np.save('np_save', self.cache)
