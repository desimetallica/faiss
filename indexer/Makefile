help:
	@cat Makefile

OUTPUT?="${HOME}/Output"
INPUT?="${HOME}/Input"
GPU?=0
DOCKER_FILE=Dockerfile
DOCKER=GPU=$(GPU) nvidia-docker
BACKEND=tensorflow

build:
	docker build -t indexer --build-arg python_version=3.5 -f $(DOCKER_FILE) .

bash: build
	$(DOCKER) run --name indexer -it -v $(OUTPUT):/home/keras/indexer/output -v $(INPUT):/home/keras/indexer/input --env KERAS_BACKEND=$(BACKEND) indexer bash

