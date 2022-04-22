RAWS:=data-raw/kotlin/basic-usage.txt
CSVS:=$(patsubst %.txt,%.csv,$(subst raw,csv,$(RAWS)))

.PHONY: rq-usage
rq-usage: data-csv/kotlin/basic-usage.csv

figures/rq-usage-summary.pdf: data-csv/kotlin/basic-usage.csv
	python3 analysis/rq-usage.py

.PHONY: raws
raws: $(RAWS)

.PHONY: csvs
csvs: $(CSVS)

Makefile.jobs: job-config.json
	python3 scripts/build-makefile.py > $@

data-raw/%: Makefile.jobs
	make -f $^ $@

data-csv/%: Makefile.jobs
	make -f $^ $@

.PHONY: real-clean
real-clean: clean clean-raws

.PHONY: clean
clean: clean-csvs clean-tables clean-figures

.PHONY: clean-raws
clean-raws:
	$(RM) $(RAWS)

.PHONY: clean-csvs
clean-csvs:
	$(RM) $(CSVS)

.PHONY: clean-tables
clean-tables:
	$(RM) tables/*
	touch tables/.gitkeep

.PHONY: clean-figures
clean-figures:
	$(RM) figures/*
	touch figures/.gitkeep
