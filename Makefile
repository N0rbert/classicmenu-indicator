NAME=classicmenu-indicator
VERSION=0.03
DEBVERSION=0.03
PPA=diesch/testing

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
	debuild -S -sa  -v${DEBVERSION} -kB57F5641

deb: sdeb
	debuild -b -sa -v${DEBVERSION} -kB57F5641

ppa: sdeb
	dput ppa:${PPA} ../${NAME}_${DEBVERSION}_source.changes

