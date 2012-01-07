NAME=classicmenu-indicator
VERSION=0.07
DEBVERSION=${VERSION}
PPA=diesch/test2

DEBUILD=debuild -sa  -v${DEBVERSION} -kB57F5641 -i'icon|.bzr'

.PHONY: clean deb sdist ppa deb


clean:
	rm -rf *.pyc build dist  ../${NAME}_${DEBVERSION}* classicmenu_indicator.egg-info


sdist:
	python setup.py sdist

egg:
	python setup.py bdist_egg

sdeb: sdist
	cp dist/${NAME}-${VERSION}.tar.gz ../${NAME}_${VERSION}.orig.tar.gz
	rm -r dist
	${DEBUILD} -S

deb: sdeb
	${DEBUILD} -b

pypi:
	python setup.py register

ppa: sdeb
	dput ppa:${PPA} ../${NAME}_${DEBVERSION}_source.changes


install: deb
	sudo dpkg -i ..//classicmenu-indicator_${DEBVERSION}_all.deb
