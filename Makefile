dist:
	@rm -rf dist
	@mkdir -p dist
	@bower install
	@gulp
	@cd ark && pybabel compile -d translations
	@python setup.py sdist bdist_wheel
.PHONY: dist
