.PHONY: raws
raws: data-raw/kotlin/basic-usage.txt

data-raw/%:
	python3 scripts/download-or-run-job.py $@

data-csv/kotlin/basic-usage.csv: data-raw/kotlin/basic-usage.txt
	python3 scripts/boa-to-csv.py -t '2,.(kt|kts|java)' --header 'type,project,file,location,isinferred,count' $< > $@

rq1: data-csv/kotlin/basic-usage.csv
	python3 analysis/rq1.py
