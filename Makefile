-include proto.mk

.PHONY: help
.DEFAULT_GOAL := help
SHELL         := /bin/bash

help: ## Show this help message.
	@echo 'usage: make [target]'
	@echo
	@echo 'targets:'
	@egrep '^(.+)\:\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'
