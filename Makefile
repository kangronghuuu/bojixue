PY ?= python3

.PHONY: build audit pdf clean

build:
	$(PY) build/build.py --out index.html

pdf: dist/薄肌学.pdf

dist/薄肌学.pdf:
	mkdir -p dist
	$(PY) build/build.py --out index.html --pdf "dist/薄肌学.pdf"

audit:
	mkdir -p build
	$(PY) build/build.py --out build/audit.html --audit

clean:
	rm -f index.html build/*.html build/_op.*
	rm -rf build/preview
