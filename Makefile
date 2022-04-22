# What raw files/csvs?
RAWS:=data-raw/kotlin/basic-usage.txt
CSVS:=$(patsubst %.txt,%.csv,$(subst raw,csv,$(RAWS)))

# What analyses are wanted?
.PHONY: wanted
wanted: rq-usage results.tbz2

# Analysis for RQ for usage
.PHONY: rq-usage
rq-usage: figures/rq-usage-summary.pdf

figures/rq-usage-summary.pdf: data-csv/kotlin/basic-usage.csv
	python3 analysis/rq-usage.py

# Package results
results.tbz2:
	tar cjvf $@ figures/ tables/

# Build raws/csvs
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

# Clean things up
.PHONY: real-clean
real-clean: clean clean-raws

.PHONY: clean
clean: clean-csvs clean-tables clean-figures
	$(rm) results.tbz2

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
