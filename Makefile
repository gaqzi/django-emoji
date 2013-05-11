PHANTOMJS=$(CURDIR)/node_modules/.bin/mocha-phantomjs

.PHONY : test clean test-py test-js

default: test

test-py:
	python test/runtests.py

test-js:
	$(PHANTOMJS) test/tests.html

test: test-py test-js

clean:
	find . -name '*.pyc' | xargs rm -f