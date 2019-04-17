# -*- coding: utf-8 -*-
import time
import faiss 
import h5py
import numpy as np
import json
import pymongo
import atexit
from startup import Startup

from keras.models import Model
from keras.layers import Reshape
from keras.layers import Flatten
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input 
from keras import backend as K

from pymongo import MongoClient

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

abspath = '/opt/faiss/webapp/media/'

#loading index and DCNN here 
Startup.loadIndex()
Startup.loadVgg19()
Startup.connMongo()

print "Get debugColl collection.."
db = Startup.client.faissdb
debugColl = db.test

def clearKeras():
	print '...Clearing Keras session'
	K.clear_session()
	print 'Done.'

def quitHandler():
	print '...Saving index'
	faiss.write_index(Startup.index, abspath + 'faiss.index')
	print 'Done.'
#register the exit function
atexit.register(quitHandler)
atexit.register(clearKeras)

def index(request):
	return render(request, 'index.html')

def mongodRequest(request):
	result = debugColl.find_one()	
    	return HttpResponse(json.dumps(result))

def simple_upload(request):
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		return render(request, 'blog/simple_upload.html', {
			'uploaded_file_url': uploaded_file_url
		})
	return render(request, 'simple_upload.html')

def search(request):
	if request.method == 'POST' and request.FILES['file']:
					
		t0 = time.time()
		myimg = request.FILES['file']
		fs = FileSystemStorage()
		imgname = fs.save(myimg.name, myimg)
		uploaded_img = fs.url(imgname)

		queryFile = abspath + imgname

		print "[%.3f s] Preprocess input image.." % (time.time() - t0)
		img = image.load_img(queryFile, target_size=(224, 224))
		fs.delete(queryFile)	
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		x = preprocess_input(x)

		print "[%.3f s] Extracting features with DCNN.." % (time.time() - t0)
		with Startup.graph.as_default():
			tensor = Startup.model.predict(x)
		
		print "[%.3f s] Searching in index.." % (time.time() - t0)
		k = 10
		D, I = Startup.index.search(tensor, k)     # actual search
		
		#prepare response json
		print "[%.3f s] Get paths from MongoDB.." % (time.time() - t0)
		ids = np.array(I[0,])

		dists = D[0,].tolist()
		response = []
		it = 0

		for _id, _dist in zip(ids, dists):			
			res = debugColl.find_one({"_id": _id})		
			#element = {"path": res['path'], "id": res['_id'], "distance": D[0,it]}
			element = {"path": res.get('path'), "id": res.get('_id'), "distance": _dist}
			response.append(element)
			it = it + 1			
		#return JsonResponse(element)
		print "[%.3f s] Done" % (time.time() - t0)
		return HttpResponse(json.dumps(response), content_type="application/json")
	return HttpResponseBadRequest()
	#else: return HttpResponse('Error')	

@csrf_exempt
def add(request):
	t0 = time.time()
	result = None
	if request.method == 'POST' and request.FILES['mytxt'] and request.FILES['myfile']:
		
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		print uploaded_file_url
			
		mytxt = request.FILES['mytxt']
		txtname = fs.save(mytxt.name, mytxt)
		uploaded_txt_url = fs.url(txtname)
		print uploaded_txt_url
		
		print "[%.3f s] Reading uploaded file... " % (time.time() - t0)
		with h5py.File(abspath + filename, 'r') as f:
        		data = f['.']['testdata'].value
				
		fs.delete(abspath + filename)	

		print "[%.3f s] Print an element: " % (time.time() - t0)
		first = np.array(data[1])
		print first
		print "[%.3f s] Print shape: " % (time.time() - t0)
		print first.shape
		
		print "[%.3f s] Loading paths file.. " % (time.time() - t0)
		with open(abspath + txtname) as f2:
    			paths = f2.readlines()
		# remove whitespace characters like `\n` at the end of each line
		paths = [x.strip() for x in paths] 

		print len(paths)
		fs.delete(abspath + txtname)
		collSize = db.test.count()
		docList = []
		it = 0
		if collSize == 0:
			for x in paths:
				element = {'_id': it, 'path': x}
				docList.append(element)
				it = it + 1
			#print docList
			print "[%.3f s] Empty index: creating a new one.. " % (time.time() - t0)
			Startup.index.add(data)
			db.test.insert_many(docList)	
			result = db.test.find_one()
    			return HttpResponse(json.dumps(result))
		else:
			print collSize
			it = collSize
			for x in paths:
				element = {'_id': it, 'path': x}
				docList.append(element)
				it = it + 1
			#print docList
			print "[%.3f s] Loading in existing index" % (time.time() - t0)
			Startup.index.add(data)
			db.test.insert_many(docList)	
			result = db.test.find_one()
    			return HttpResponse(json.dumps(result))
	return render(request, 'simple_upload.html')
