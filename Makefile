all: build

NPM = npm
BOWER = $(abspath ./node_modules/bower-installer/bower-installer.js)
SPARK_VERSION = "2.2.1"
HADOOP_VERSION = "2.7"
SPARK_PKGNAME = "spark-$(SPARK_VERSION)-bin-hadoop$(HADOOP_VERSION)"
SPARK_MIRROR = "http://www-eu.apache.org/dist/spark/"
SPARK_MIRROR = "http://apache.uvigo.es/spark/"
SPARK_URL = "$(SPARK_MIRROR)spark-$(SPARK_VERSION)/$(SPARK_PKGNAME).tgz"

bootstrap:
	@if [ ! -x $(NPM) ]; then $(NPM) install bower-installer; $(NPM) install bower-npm-resolver; fi

install-spark:
	cd /opt/spark && wget $(SPARK_URL) && tar vxzf $(SPARK_PKGNAME).tgz && ln -s $(SPARK_PKGNAME) spark

build: bootstrap # build
	cd src/anomalydetection/dashboard && nodejs $(BOWER) --remove

install: # install
	pip3 install .

clean:
	rm -rf anomalydetection/dashboard/static/vendor
