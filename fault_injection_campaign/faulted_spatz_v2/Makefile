GVSOC_WORKDIR ?= $(CURDIR)/build
ifdef BUILDDIR
FULL_BUILDDIR ?= $(GVSOC_WORKDIR)/$(BUILDDIR)
else
FULL_BUILDDIR ?= $(GVSOC_WORKDIR)
endif

TARGET = spatz

clean:
	rm -rf $(FULL_BUILDDIR)/test
	make -C ../.. TARGETS=${TARGET} MODULES=$(CURDIR) BUILDDIR=$(FULL_BUILDDIR)/build INSTALLDIR=$(FULL_BUILDDIR)/install $(OPTIONS) clean

gvsoc:
	make -C ../.. TARGETS=${TARGET} MODULES=$(CURDIR) BUILDDIR=$(FULL_BUILDDIR)/build INSTALLDIR=$(FULL_BUILDDIR)/install $(OPTIONS) build

test:
	$(FULL_BUILDDIR)/install/bin/gvsoc --target=${TARGET} --work-dir=$(FULL_BUILDDIR)/work --binary=$(FULL_BUILDDIR)/test/test run $(runner_args)
