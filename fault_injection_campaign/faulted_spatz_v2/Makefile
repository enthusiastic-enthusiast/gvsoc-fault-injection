GVSOC_WORKDIR ?= $(CURDIR)/build
ifdef BUILDDIR
FULL_BUILDDIR ?= $(GVSOC_WORKDIR)/$(BUILDDIR)
else
FULL_BUILDDIR ?= $(GVSOC_WORKDIR)
endif

TARGET = spatz_v2

clean:
	rm -rf $(FULL_BUILDDIR)/test
	make -C ../.. TARGETS=${TARGET} MODULES=$(CURDIR) BUILDDIR=$(FULL_BUILDDIR)/build INSTALLDIR=$(FULL_BUILDDIR)/install $(OPTIONS) clean

gvsoc:
	make -C ../.. TARGETS=${TARGET} MODULES=$(CURDIR) BUILDDIR=$(FULL_BUILDDIR)/build INSTALLDIR=$(FULL_BUILDDIR)/install $(OPTIONS) build

run:
	$(FULL_BUILDDIR)/install/bin/gvrun --target ${TARGET} --work-dir=$(FULL_BUILDDIR)/work --param chip/soc/binary=$(FULL_BUILDDIR)/test/test run $(runner_args)
