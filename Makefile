SPHINXOPTS    ?=
SPHINXBUILD   ?= pipenv run sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
DOCSDIR = docs/
PACKAGE_VERSION = $(shell pipenv run python -c "from constructor_io import __version__;print(__version__);")

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

docs: Makefile
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp -a $(BUILDDIR)/html/. "$(DOCSDIR)$(PACKAGE_VERSION)/"
	# Find the url='./x.x.x' pattern in docs/index.html file and replace it with the current package version
	sed -i "" "s/url=\'\.\/[^']*\'/url=\'\.\/$(PACKAGE_VERSION)\'/" docs/index.html  
	rm -r $(BUILDDIR)

install: Makefile
	pipenv install --dev
	pipenv run pre-commit install --hook-type pre-commit --hook-type pre-push

build: Makefile
	pipenv run python setup.py sdist

publish: Makefile
	twine upload dist/*
