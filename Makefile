dist:
	@rm -rf dist
	@mkdir -p dist
	@bower install
	@gulp
	@python setup.py sdist bdist_wheel
.PHONY: dist
