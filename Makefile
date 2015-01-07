dist:
	@rm -rf dist
	@mkdir -p dist
	@gulp
	@python setup.py sdist bdist_wheel
.PHONY: dist
