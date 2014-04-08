KARMA=$(CURDIR)/node_modules/karma/bin/karma
BOWER=$(CURDIR)/node_modules/.bin/bower

.PHONY : test clean test-py test-js coverage coverage-py coverage-js coverage-py-html default

default: coverage

test-py:
	coverage run test/runtests.py

test-js: node_modules
	$(KARMA) start test/karma.conf.js --single-run \
		--reporters dots --browsers PhantomJS

test: test-js test-py

node_modules: package.json test/bower.json
	npm install
	cd test && \
		$(BOWER) install --config.interactive=false

coverage: coverage-js coverage-py

coverage-py:
	coverage run test/runtests.py --with-xunit && \
		coverage xml --omit="admin.py,*.virtualenvs/*,./test/*"

coverage-js: node_modules
	$(PHANTOMJS) -R xunit test/tests.html > mochatests.xml

coverage-py-html:
	[ -d htmlcov ] || rm -rf htmlcov
	coverage run test/runtests.py && \
		coverage html --omit="admin.py,*.virtualenvs/*,./test/*"

clean:
	find . -name '*.pyc' | xargs rm -f

upload-package: test
	python setup.py sdist upload
