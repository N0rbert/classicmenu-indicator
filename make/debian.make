# -*- makefile -*-


DEBUILD=debuild -sa -v${DEBVERSION} -k${GPG_KEY} -i'.bzr|.patternbook'

GARBAGE:=${GARBAGE} ../*.deb ../*.changes ../*.build ../${NAME}_${DEBVERSION}* debian/${NAME}

PRE_BUILD_TARGETS:=update_version ${PRE_BUILD_TARGETS}


update_version:
	version="$$(awk -F'[()]' '/^${NAME}/{print $$2}' debian/changelog| head -n1)" ;\
	patternbook set version -o -v "$$version"
	patternbook update  --yes

sdeb: update_version sdist
	cp dist/${NAME}-${VERSION}.tar.gz ../${NAME}_${VERSION}.orig.tar.gz
	rm -r dist
	python3 setup.py build_i18n
	${DEBUILD} -S

deb: ${PRE_BUILD_TARGETS}
	${DEBUILD} -b


ppa: sdeb
	dput ppa:${PPA} ../${NAME}_${DEBVERSION}_source.changes


install:
	sudo dpkg -i ../${NAME}_${DEBVERSION}_all.deb

