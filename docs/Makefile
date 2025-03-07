# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

UVR = uv run --group docs

#### Variable for building man page ###

MAN_DIR = source/_static/man
MAN_FILE = $(MAN_DIR)/rouge-scroll.1

AP_CMD = argparse-manpage
# These tell argparse-manpage where to find the argparser object
AP_MODULE = rogue_scroll.__main__
AP_OBJECT = parser

default: man html

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

.PHONY: man

man: $(MAN_FILE)

$(MAN_FILE): FORCE
	mkdir -p $(MAN_DIR)
	$(UVR) $(AP_CMD) --module $(AP_MODULE) --object $(AP_OBJECT) --output $@

FORCE: ;

html:
	$(UVR) $(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	$(UVR) $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
