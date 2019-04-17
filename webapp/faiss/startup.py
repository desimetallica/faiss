import faiss
import time
import numpy as np
import os 
import tensorflow as tf

from pymongo import MongoClient
from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input 
from keras.models import Model 
from keras.models import load_model

abspath = '/opt/faiss/webapp/media/'

class Startup:
	
	client = None
	graph = None
	index = None
	model = None	

	@staticmethod 
	def loadIndex():
		
		defaultShape = 4096
		savedIndex = abspath + 'faiss.index'
		#load index in memory
		if os.path.isfile(savedIndex):
			print "Loading index in memory..", savedIndex
			Startup.index = faiss.read_index(savedIndex) 
			print "..done"			
		#..or load a new empty index if cant found 
		else:
			print "No index saved found: loading new empty index in memory"
			Startup.index = faiss.IndexFlatL2(defaultShape)

	@staticmethod
	def loadVgg19():
			
		with tf.device('/gpu:1'):
			#base_model = VGG19(weights='imagenet')
			savedModel = abspath + 'VGG19.h5'
			base_model = load_model(savedModel)
			Startup.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)
			Startup.graph = tf.get_default_graph()
	
	@staticmethod
	def connMongo():
		print "Connecting to MongoDB.."
		Startup.client = MongoClient('mongorai', 27017)
