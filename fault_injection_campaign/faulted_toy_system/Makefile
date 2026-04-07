include ./utils/rt.mk

GVSOC_WORKDIR ?= $(CURDIR)/build
ifdef BUILDDIR
FULL_BUILDDIR ?= $(GVSOC_WORKDIR)/$(BUILDDIR)
else
FULL_BUILDDIR ?= $(GVSOC_WORKDIR)
endif

clean:
	rm -rf $(FULL_BUILDDIR)/test
	make -C ../.. TARGETS=faulted_toy_system MODULES=$(CURDIR) BUILDDIR=$(FULL_BUILDDIR)/build INSTALLDIR=$(FULL_BUILDDIR)/install $(OPTIONS) clean

all:
	mkdir -p $(FULL_BUILDDIR)/test
	riscv64-unknown-elf-gcc -std=gnu89 -g -o $(FULL_BUILDDIR)/test/test prog_simple.c $(RT_SRCS) $(RT_FLAGS)

gvsoc:
	make -C ../.. TARGETS=faulted_toy_system MODULES=$(CURDIR) BUILDDIR=$(FULL_BUILDDIR)/build INSTALLDIR=$(FULL_BUILDDIR)/install $(OPTIONS) build

run:
	$(FULL_BUILDDIR)/install/bin/gvsoc --target-dir=$(CURDIR) --target=faulted_toy_system --work-dir=$(FULL_BUILDDIR)/work --binary=$(FULL_BUILDDIR)/test/test run $(runner_args)

campaign:
	cd .. && ./faulted_toy_system/simple.py
