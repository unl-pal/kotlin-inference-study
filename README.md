# Kotlin Inference Study Analysis & Replication Package

This replication package contains all data and scripts needed to reproduce
results from the paper.

**TL;DR**: Download `data-cache.zip` and run `make` to regenerate
tables/figures.

Raw data is very large, however, cached Parquet files are smaller.  You are
likely able to skip downloading `data.zip` and can instead use
`data-cache.zip`.  This should be sufficient to run `make`.

### Required Packages

The scripts require Python 3, and were tested on 3.9.  Earlier versions likely
work.

See the `requirements.txt` file for a list of required packages.  These may be
installed by running:

```sh
pip install -r requirements.txt
```

If you need to download Boa jobs, the Boa API does require authentication.  You
may, however, view the jobs online: they are public.

### File Organization

Files are organized in the following layout:

 - `data` data files are kept here.  This includes unprocessed boa output
   (`.txt`), and processed versions (`.parquet`, `.txt`)
 - `boa` contains Boa queries and snippets used.  A description of the output
   and the snippets is available in CODEBOOK.md
 - `analyses` contains code used to produce figures, tables and other analyses.
   This is organized in a `common` directory which contains common utilities,
   and a directory for `kotlin`.
 - `figures` and `tables` contains generated tables/figures.
 
### Building figures/tables

The following `make` targets are available:

 - `kotlin/table-counts`: This produces Table 1.
 - `project-size`: This produces Table 2.
 - `kotlin/rq-usage`: This produces Table 3 and Figure 2a.
 - `kotlin/rq-usage-2`: This produces Figure 2b.
 - `kotlin/rq-correlation`: This produces Table 4.
 - `kotlin/rq-rhs-types`: This produces Figure 3.
 - `kotlin/rq-rhs-methodcalls`: This produces Table 5.
 - `kotlin/rq-mutability`: This produces Table 6 and Figures 4a and 4b.
 - `kotlin/rq-tests`: This produces Table 7 and Figure 5a.
 - `kotlin/rq-mixed-projects`: This produces Table 8 and Figure 5b.
 - `kotlin/rq-survival`: This produces Figure 6.
