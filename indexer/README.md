# Using Keras via Docker

This directory contains `Dockerfile` to make it easy to get up and running with
Keras via [Docker](http://www.docker.com/).

## Installing Docker

General installation instructions are
[on the Docker site](https://docs.docker.com/installation/), but we give some
quick links here:

* [OSX](https://docs.docker.com/installation/mac/): [docker toolbox](https://www.docker.com/toolbox)
* [ubuntu](https://docs.docker.com/installation/ubuntulinux/)

## Running the container

We are using `Makefile` to simplify docker commands within make commands.

Build the container and start a bash

    $ make bash

For example:

    $ make bash GPU=1 BACKEND=tensorflow INPUT=/home/teche/docker_workspace/indexer/input OUTPUT=/home/teche/docker_workspace/indexer/output

For GPU support install NVIDIA drivers (ideally latest) and
[nvidia-docker](https://github.com/NVIDIA/nvidia-docker). Run using

    $ make notebook GPU=0 # or [ipython, bash]

Mount a volume for external data sets:

    $ INPUT=/home/teche/docker_workspace/indexer/input

    $ OUTPUT=/home/teche/docker_workspace/indexer/output

    $ make INPUT=~/Input

Prints all make tasks

    $ make help

