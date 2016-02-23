# -*- makefile -*-

PYTHON_DIR=${PYTHONNAME}



update_meta:
	echo update_meta:${PYTHON_DIR}/_meta.py 
	( \
	  echo "#-*- coding: utf-8 -*-" ;\
	  echo "# This file is generated. All changes will be lost" ;\
	  echo ;\
	  echo 'VERSION="${PYTHON_VERSION}"' ;\
	  echo 'TITLE="${TITLE}"' ;\
	  echo 'NAME="${NAME}"' ;\
	  echo 'AUTHOR_NAME="${AUTHOR_NAME}"' ;\
	  echo 'AUTHOR_EMAIL="${AUTHOR_EMAIL}"' ;\
	  echo 'WEB_URL="${WEB_URL}"' ;\
	  echo 'TIMESTAMP="${TIMESTAMP}"' ;\
	) > ${PYTHON_DIR}/_meta.py 

pypi:
	twine upload dist/${NAME}-${VERSION}.*	

sdist: ${PRE_BUILD_TARGETS}
	python setup.py sdist bdist_wheel
	mv dist/${NAME}-${PYTHON_VERSION}.tar.gz dist/${NAME}-${VERSION}.tar.gz || true


potfiles:
	mkdir -p po
	find ${PYTHON_DIR} -type f -name \*.py > po/POTFILES.in
	find data -type f -name \*.desktop.in >> po/POTFILES.in
	find data -type f -name \*.ui -printf '[type: gettext/glade]%p\n' >> po/POTFILES.in
