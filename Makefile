
.PHONY: help clean install uninstall

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  clean      to remove build artifacts."
	@echo "  install    pip install the crossplane-update command."
	@echo "  uninstall  pip uninstall the crossplane-update command."

clean:
	@rm -fr 'dist/'
	@rm -fr 'build/'
	@rm -fr '.cache/'
	@rm -fr '.pytest_cache/'
	@find . -path '*/.*' -prune -o -name '__pycache__' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.egg-info' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.py[co]' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.build' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.so' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.c' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*~' -exec rm -fr {} +

install:
	@make clean
	pip install -e .

uninstall:
	pip uninstall -y crossplane-update
	@make clean
