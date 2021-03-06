INSTALL ?= install
RM ?= rm
MSGFMT ?= msgfmt
MSGMERGE ?= msgmerge
XGETTEXT ?= xgettext
FIND ?= find

PREFIX = /usr/local
# This is for debian
REAL_PREFIX = $(PREFIX)

LIBDIR = $(PREFIX)/lib/itaka
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share/itaka
IMAGESDIR = $(DATADIR)/images
LOCALEDIR = $(DATADIR)/locale
APPLICATIONSDIR = $(PREFIX)/share/applications
ICONDIR = $(PREFIX)/share/pixmaps
MANDIR = $(PREFIX)/share/man/man1

# For debian compatibility, these are hardcoded
REPLACEIMAGESDIR = $(REAL_PREFIX)/share/itaka/images/
REPLACELOCALEDIR = $(REAL_PREFIX)/share/itaka/locale/


PYFILES := $(shell $(FIND) . -name "*.py" -print)

install: 
	# Replace images and locales directory
	mv config.py config.py.old
	mv itaka.py itaka.py.old
	sed "s|/usr/local/share/itaka/images/|$(REPLACEIMAGESDIR)|g" config.py.old > config.py
	sed "s|/usr/share/locale/|$(REPLACELOCALEDIR)|g" itaka.py.old > itaka.py
	
	$(INSTALL) -m 755 -d $(BINDIR) $(DATADIR) $(LIBDIR) $(IMAGESDIR) $(APPLICATIONSDIR) $(ICONDIR) $(MANDIR)
	$(INSTALL) -m 755 *.py $(LIBDIR)

	# We only need a few images
	$(INSTALL) -m 644 share/images/itaka.png $(IMAGESDIR)
	$(INSTALL) -m 644 share/images/itaka-take.png $(IMAGESDIR)
	$(INSTALL) -m 644 share/images/itaka-secure.png $(IMAGESDIR)
	$(INSTALL) -m 644 share/images/itaka-secure-take.png $(IMAGESDIR)
	$(INSTALL) -m 644 share/images/itaka16x16-take.png $(IMAGESDIR)
	$(INSTALL) -m 644 share/images/itaka16x16-secure-take.png $(IMAGESDIR)
	$(INSTALL) -m 644 share/images/itaka64x64.png $(IMAGESDIR)

	# Would symlink but it fails
	cp $(IMAGESDIR)/itaka.png $(ICONDIR)/itaka.png
	#ln -sf share/itaka/images/itaka.png $(ICONDIR)/itaka.png

	$(INSTALL) -m 644 share/itaka.desktop $(APPLICATIONSDIR)
	gzip -9 -c share/itaka.1 > share/itaka.1.gz
	$(INSTALL) -m 644 share/itaka.1.gz $(MANDIR)
	if test -f $(BINDIR)/itaka; then rm $(BINDIR)/itaka; fi	

	# Create our binary directory for the symlink
	if test ! -d $(BINDIR); then mkdir $(BINDIR); fi
	ln -sf  $(LIBDIR)/itaka.py $(BINDIR)/itaka

	#echo $( ls $(BINDIR)/itaka )
	chmod +x $(BINDIR)/itaka
	
	for lang in locale/*; do 
	    if [[ -e $lang/LC_MESSAGES/itaka.po ]]; then 
		for pofile in $lang/LC_MESSAGES/itaka.po; do
		    msgfmt $pofile -o $lang/LC_MESSAGES/itaka.mo && $(INSTALL) -m 644 $pofile $(LOCALEDIR)/${lang#locale/}/LC_MESSAGES/itaka.mo; 
		done;
	    fi;
	done

	# Clean up
	mv config.py.old config.py
	mv itaka.py.old itaka.py

uninstall:
	rm -r $(BINDIR)/itaka $(DATADIR) $(LIBDIR) $(ICONDIR)/itaka.png $(APPLICATIONSDIR)/itaka.desktop $(MANDIR)/itaka.1.gz

clean:
	find . -type f  \( -regex '.+\.py[co]' -o -name 'itaka.1.gz' \) -exec rm -f {} \;
	rm locale/*/LC_MESSAGES/*.mo

help:
	@echo Usage:
	@echo make clean                - delete built modules and object files
	@echo make install              - install binaries into the official directories
	@echo make uninstall            - uninstall binaries from the official directories
	@echo make help                 - prints this help
	@echo

