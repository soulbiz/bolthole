IMAGE_NAME := protoc
TAG        := python

.GRPCUI    := $(shell command -v grpcui 2> /dev/null)

proto-docker-image:
	docker build -t $(IMAGE_NAME):$(TAG) -f proto/Dockerfile .

proto-gen:
  #TODOO

proto: |proto-docker-image proto-gen
