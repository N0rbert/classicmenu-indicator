PYTHONNAME=classicmenu_indicator
PYTHON_VERSION=$(subst ~pre,pr,${VERSION})

GARBAGE:=${GARBAGE} *.pyc ./${PYTHONNAME}.egg-info
PRE_BUILD_TARGETS:=${PRE_BUILD_TARGETS} potfiles update_meta