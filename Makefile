test:
	@PYTHONPATH=`pwd`/src nosetests -vs

.PHONY: test
