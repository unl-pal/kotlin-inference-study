.PHONY: raws
raws: data-raw/kotlin/basic-usage.txt

data-raw/%:
	python3 scripts/download-or-run-job.py $@
