SPHINXOPTS    ?=
SPHINXBUILD   ?= pipenv run sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
DOCSDIR = docs/

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

docs: Makefile
	pipenv run sphinx-apidoc -o source constructorio_python
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp -a $(BUILDDIR)/html/. $(DOCSDIR)
	rm -r $(BUILDDIR)

install: Makefile
	pipenv install
	pipenv run pre-commit install --hook-type pre-commit --hook-type pre-push

