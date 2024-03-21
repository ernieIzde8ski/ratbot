format:
	@echo Formatting files!
	isort .
	black .

.PHONY: format
