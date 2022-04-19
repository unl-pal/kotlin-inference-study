.PHONY: rq1
rq1: data-csv/kotlin/basic-usage.csv
	python3 analysis/rq1.py

.PHONY: raws
raws: data-raw/kotlin/basic-usage.txt

Makefile.jobs: job-config.json
	python3 scripts/build-makefile.py > $@

data-raw/%: Makefile.jobs
	make -f $^ $@

data-csv/%: Makefile.jobs
	make -f $^ $@
