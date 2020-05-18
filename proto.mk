IMAGE_NAME := protoc
TAG        := python

proto-docker-image:
	docker build -t $(IMAGE_NAME):$(TAG) -f protos/docker/Dockerfile .

proto-gen:
	docker run -ti --rm -v $(shell pwd)/:/usr/src $(IMAGE_NAME):$(TAG_SBT) bash -c "python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/*.proto "

proto: |proto-docker-image proto-gen
