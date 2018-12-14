bin/pip:
	virtualenv .

bin/buildout: bin/pip
	bin/pip install -r requirements.txt
	touch bin/buildout

bootstrap: bin/buildout

bin/instance: bin/buildout setup.py *.cfg
	bin/buildout -Nv
	touch bin/instance

buildout: bin/instance

fg: bin/instance
	bin/instance fg

bin/test: bin/buildout setup.py *.cfg
	bin/buildout -Nv
	touch bin/test

test: bin/test
	bin/test
