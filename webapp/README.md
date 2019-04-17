## Faiss project for Image search 

Similarity search based on FAISS index.

Features extraction with VGG-19 DCNN and indexing in FAISS index. Default shape have dimensionality of 4096.
You need a makeindex.py script also. 

Search page and add page based on django framework. 

#### Notes

- In ordere to use this project you need [FAISS](https://github.com/facebookresearch/faiss)
- Also [keras](https://keras.io/) and [tensorFlow](https://www.tensorflow.org/install/) are needed
- A MongoDB instance to store images paths 
