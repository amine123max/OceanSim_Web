.PHONY: html clean

html:
	python scripts/build_docs.py

clean:
	rm -rf _build .doctrees _sources _static guide api developer css js img *.html searchindex.js objects.inv .buildinfo
