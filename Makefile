PHANTOMJS=$(CURDIR)/node_modules/.bin/mocha-phantomjs

.PHONY : test clean test-py test-js

default: coverage

test-py:
	python test/runtests.py

test-js: node_modules
	$(PHANTOMJS) -R tap test/tests.html

test: test-js test-py

node_modules: package.json
	npm install

coverage: coverage-js coverage-py

coverage-py:
	coverage run test/runtests.py --with-xunit && \
		coverage xml --omit="admin.py,*.virtualenvs/*,./test/*"

coverage-js:
	$(PHANTOMJS) -R xunit test/tests.html > mochatests.xml

coverage-py-html:
	[ -d htmlcov ] || rm -rf htmlcov
	coverage run test/runtests.py && \
		coverage html --omit="admin.py,*.virtualenvs/*,./test/*"

clean:
	find . -name '*.pyc' | xargs rm -f
