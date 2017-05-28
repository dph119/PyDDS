.PHONY: lint
lint:
	pylint --rcfile=.pylintrc PyDDS/*py && echo "LINT PASSED" || echo "LINT FAILED."

.PHONY: test
test:
	python -m unittest discover

.PHONY: doc
doc:
	epydoc PyDDS/*py --graph all -o doc --name PyDDS
