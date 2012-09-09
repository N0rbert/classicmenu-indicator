NAME=classicmenu-indicator
PYNAME=classicmenu_indicator

DEBVERSION=$(shell awk -F '[()]' '/^${NAME}/ {print $$2}'  debian/changelog|head -1)

VERSION=$(shell echo '${DEBVERSION}' | egrep -o '[0-9.-]{3,}')

WEBDIR=/home/diesch/florian-diesch.de/sphinx/neu/source/software/${NAME}/dist

PREFIX_FILE=.install_prefix

PPA=diesch/testing

DEBUILD=debuild -sa -v${DEBVERSION} -kB57F5641 -i'icon|.bzr'

.PHONY: clean deb sdist ppa deb clear_prefix app_prefix


clean:
	rm -rf *.pyc build dist ../*.deb ../*.changes ../*.build ../${NAME}_${DEBVERSION}* ${PYNAME}.egg-info debian/${NAME}

potfiles:
	find ${PYNAME} -type f -name \*.py > po/POTFILES.in
	find data -type f -name \*.desktop.in >> po/POTFILES.in
	find data -type f -name \*.ui -printf '[type: gettext/glade]%p\n'  >> po/POTFILES.in


clear_prefix:
	rm "${PREFIX_FILE}"

app_prefix:
	echo '/opt/extras.ubuntu.com/${NAME}' > "${PREFIX_FILE}"

sdist:
	python setup.py sdist

egg:
	python setup.py bdist_egg

sdeb: sdist
	cp dist/${NAME}-${VERSION}.tar.gz ../${NAME}_${VERSION}.orig.tar.gz
	rm -r dist
	python setup.py build_i18n
	${DEBUILD} -S

deb: 
	${DEBUILD} -b

pypi:
	python setup.py register

ppa: sdeb
	dput ppa:${PPA} ../${NAME}_${DEBVERSION}_source.changes


install: deb
	sudo dpkg -i ../${NAME}_${DEBVERSION}_all.deb


unpackpo:
	tar xzvf launchpad-export.tar.gz && \
	cd po && \
	mmv '${NAME}-*.po' '#1.po' && \
	cd .. && \
	rm launchpad-export.tar.gz

share: deb
	cp ../${NAME}_${DEBVERSION}_all.deb ~/Shared/

web: deb sdist
	mkdir -p ${WEBDIR}
	cp ../${NAME}_${DEBVERSION}_all.deb dist/${NAME}-${VERSION}.tar.gz ${WEBDIR}


pbuilder-natty: sdeb
	 sudo pbuilder --create  --distribution natty
	 sudo pbuilder --build ../${NAME}_${DEBVERSION}.dsc

pbuilder-oneiric: sdeb
	 sudo pbuilder --create  --distribution oneiric
	 sudo pbuilder --build ../${NAME}_${DEBVERSION}.dsc

pbuilder-precise: sdeb
	 sudo pbuilder --create  --distribution precise
	 sudo pbuilder --build ../${NAME}_${DEBVERSION}.dsc

pbuilder-quantal: sdeb
	 sudo pbuilder --create  --distribution quantal
	 sudo pbuilder --build ../${NAME}_${DEBVERSION}.dsc


pbuilder: pbuilder-natty  pbuilder-oneiric pbuilder-precise pbuilder-quantal
