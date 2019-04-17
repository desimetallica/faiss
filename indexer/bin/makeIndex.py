
import tensorflow as tf
from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.models import Model
from keras.layers import Reshape
from keras.layers import Flatten
from keras.models import load_model
from shutil import copytree
from shutil import copy
import datetime

#import pymongo
from pymongo import MongoClient

import os
import h5py
import time
import numpy as np
import requests 
import mmap

t0 = time.time()

d = datetime.datetime.today()
print(d, end=" Starting indexer")


#parameters debugMode = 1 for more info and test imagePath;
#in debugMode scanPath is ignored and script run into debugScanPath
#scanPath is recursive inside all folders

faissPostUrl = 'http://faissrai:8000/faiss/add/'
debugMode = 0 
storePath = '../store'
scanPath = '../input'
debugScanPath = '../input'
imagesPathFile = '../output/pathFile.txt'
imagesPathFile2 = '../output/pathFile2.txt'
dbFile = '../output/TestFile.hdf5'
mongoIp = 'mongorai'
mongoPort = 27017

date = datetime.datetime.today()
print(date, end=" Trying to connect on mongoDB")

client = MongoClient(mongoIp,mongoPort)
db = client.faissdb
debugColl = db.test

date = datetime.datetime.today()
print(date, end=" Try to loading model with keras")
with tf.device('/gpu:0'):
	base_model = load_model("VGG19.h5")
	#base_model.load_weights("vgg19_weights_tf_dim_ordering_tf_kernels.h5")
	#model = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_pool').output)
	#model = Model(inputs=base_model.input, outputs=base_model.get_layer('flatten').output)
	#selectedLayerModel = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)
	model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)

#model = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_pool').output)
#model = Model(inputs=base_model.input, outputs=base_model.get_layer('flatten').output)
#selectedLayerModel = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)

if debugMode:
	date = datetime.datetime.today()
	print(date, end=" print model configuration summary:")
	model.summary()

#selectedLayerModel.summary()
#config = model.get_config()
#like a new NN we get output of base_model as input of new layer Reshape 
#x = selectedLayerModel.output
#reshape = Reshape((49, 512))(x)
#flatten = Flatten()(x)
#than we create new model with this reshape
#model = Model(inputs=base_model.input, outputs=flatten)



#print "[%.3f s] print keras shape:" % (time.time() - t0)
#for layer in model.layers:
#    print(layer.get_output_at(0).get_shape().as_list())
while True:
	date = datetime.datetime.today()
	print(date," loading files from filesystem: ")
	fileList = []
	#fileList2 = []
	pathfile2 = open(imagesPathFile2, 'w')

	if debugMode:
		scanPath = debugScanPath

	for root, dirs, files in os.walk(scanPath):
		for file in files:
			if file.endswith('.jpg'):
				#absStorePath = os.path.abspath(storePath)
				structure = os.path.join(storePath, root[len(scanPath)+1:])
				destFile = os.path.join(structure, file)
				mongoPath = os.path.join(structure[len(storePath):], file)
				srcFile = os.path.join(root, file)
				#fileList2.append(destFile)
				if not debugColl.find_one({"path": mongoPath}):		
					#append file if only is not already in db so it will be processed
					fileList.append(destFile)
					if not os.path.isdir(structure):
						os.mkdir(structure)
						copy(srcFile, structure)
					else:
						copy(srcFile, structure)
				pathfile2.write('%s\n' % mongoPath)
	pathfile2.close()

	if debugMode:	
		print(fileList)

	fileNum = len(fileList)

	if fileNum != 0:
		
		print('%4i images will be processed \n' % (fileNum))
		#create a tensor from very first image 
		img = image.load_img(fileList[0], target_size=(224, 224))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		x = preprocess_input(x)
		block4_pool_features = model.predict(x)

		if debugMode:
			date = datetime.datetime.today()
			print(date," print Shape of tensor:")
			print(block4_pool_features.shape)
			date = datetime.datetime.today()
			print(date," print Example tensor:")
			print(block4_pool_features)

		#get dimension of vector (e.g. 4096 for fc-layer in vgg-19)
		d = block4_pool_features.shape[1]
		date = datetime.datetime.today()
		print(date," Running features extraction and writing .hdf5 database file")
		f = h5py.File(dbFile, 'a')
		dset = f.create_dataset('testdata', (fileNum, d), maxshape=(None, d), dtype='f')
		i=0
		for path in fileList:
			img = image.load_img(path, target_size=(224, 224))
			x = image.img_to_array(img)
			x = np.expand_dims(x, axis=0)
			x = preprocess_input(x)
			block4_pool_features = model.predict(x)	
			dset[i] = block4_pool_features
			i=i+1
		date = datetime.datetime.today()		
		print(date," Closing hdf5 file")
		f.close()

		date = datetime.datetime.today()
		print(date," Posting to Faiss application")
		multifile = {'mytxt' :  open(imagesPathFile2, 'rb'), 'myfile' : open(dbFile, 'rb')}
		r = requests.post(faissPostUrl, files=multifile)		
		os.remove(dbFile)
	else:
		date = datetime.datetime.today()
		print(date," All files are already stored. Nothing to do.")
	print(date," Removing temp files")
	os.remove(imagesPathFile2)
	date = datetime.datetime.today()
	print(date," Sleeping 1 minute")
	time.sleep(60) 
