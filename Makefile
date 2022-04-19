.PHONY: raws
raws: data-raw/kotlin/basic-usage.txt

Makefile.jobs: job-config.json
	python3 scripts/build-makefile.py > $@

data-raw/%: Makefile.jobs
	make -f $^ $@
