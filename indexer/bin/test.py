import tensorflow as tf
import os
import h5py
import time
import numpy as np


from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.models import Model
from keras.layers import Reshape
from keras.layers import Flatten
from keras.models import load_model

t0 = time.time()

#parameters debugMode = 1 for more info and test imagePath;
#in debugMode scanPath is ignored and script run into debugScanPath
#scanPath is recursive inside all folders

print('[%.3f s] Try to loading VGG-19 model with keras \n' % (time.time() - t0))

with tf.device('/gpu:0'):

	base_model = load_model("VGG19.h5")
	#base_model.load_weights("vgg19_weights_tf_dim_ordering_tf_kernels.h5")
	#model = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_pool').output)
	#model = Model(inputs=base_model.input, outputs=base_model.get_layer('flatten').output)
	#selectedLayerModel = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)

	model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)

	print('\n[%.3f s] print test VGG-19 model configuration summary:' % (time.time() - t0))
	model.summary()
