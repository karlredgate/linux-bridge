
PWD := $(shell pwd)
KERNEL := $(shell uname -r)
EXTRA = exports/lib/modules/$(KERNEL)/extra

INSTALL = install
INSTALL_PROGRAM = $(INSTALL) --mode=755
INSTALL_DATA = $(INSTALL) --mode=644
INSTALL_DIR = $(INSTALL) -d --mode=755
INSTALL_KO = $(INSTALL) --mode=744

default: rpm

rpm: dist
	rm -rf rpm
	mkdir -p rpm/BUILD rpm/RPMS rpm/BUILDROOT
	rpmbuild -bb --buildroot=$(PWD)/rpm/BUILDROOT bridge.spec

dist: build
	$(RM) -rf exports
	mkdir -p $(EXTRA)
	$(INSTALL_KO) bridge/bridge.ko $(EXTRA)

build:
	make -C /lib/modules/$(KERNEL)/build M=$(PWD)/bridge

clean:
	make -C /lib/modules/$(KERNEL)/build M=$(PWD)/bridge clean
	$(RM) -rf rpm exports

distclean: clean
