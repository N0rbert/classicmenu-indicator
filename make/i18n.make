
unpackpo:
	tar xzvf launchpad-export.tar.gz && \
	cd po && \
	mmv '${NAME}-*.po' '#1.po' && \
	cd .. && \
	rm launchpad-export.tar.gz
