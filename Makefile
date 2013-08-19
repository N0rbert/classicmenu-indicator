GARBAGE:=build dist

PRE_BUILD_TARGETS:=clean

include make/*.inc
include make/*.make


clean:
	rm -rf ${GARBAGE}


