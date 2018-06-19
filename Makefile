all: build install

NPM = npm
BOWER = $(abspath ./node_modules/bower-installer/bower-installer.js)

bootstrap:
	@if [ ! -x $(NPM) ]; then $(NPM) install bower-installer; $(NPM) install bower-npm-resolver; fi

build: bootstrap # build
	cd src/anomalydetection/dashboard && nodejs $(BOWER) --remove

install: # install
	pip3 install .

clean:
	rm -rf anomalydetection/dashboard/static/vendor
