# Kotlin Inference Study Analysis & Replication Package

This replication package contains all data and scripts needed to
reproduce results from the paper.

**TL;DR**: Download `data-cache.zip` and run `make` to regenerate
tables/figures.

Raw data is very large, however, cached Parquet files are smaller.
You are likely able to skip downloading `data.zip` and can instead use
`data-cache.zip`.  This should be sufficient to run `make`.

----------------------------------------------------------------------

### Required Packages

The scripts require Python 3, and were tested on 3.9.  Earlier
versions likely work.

The following packages are required:

 - `boa-api>=0.1.13`
 - `jsonschema>=3.2.0`
 - `pandas>=1.4.2`
 - `pyarrow>=7.0.0`
 - `seaborn>=0.11.2`
 - `jinja2>=3.1.2`
 - `tqdm>=4.64.0`
 - `scipy>=1.8.1`
 - `lifelines>=0.27.1`

These may be installed by running:

```sh
pip install -r requirements.txt
```

If you need to download Boa jobs, the Boa API does require
authentication.  You may, however, view the jobs online: they are
public.

----------------------------------------------------------------------

### File Organization

Files are organized in the following layout:

 - `data` data files are kept here.  This includes unprocessed boa
   output (`.txt`), and processed versions (`.parquet`, `.txt`)
 - `boa` contains Boa queries and snippets used.  A description of the
   output and the snippets is available in CODEBOOK.md
 - `analyses` contains code used to produce figures, tables and other
   analyses.  This is organized in a `common` directory which contains
   common utilities, and directories for both `java` and `kotlin`.
 - `figures` and `tables` contains generated tables/figures.
 

----------------------------------------------------------------------

### Building figures/tables

The following `make` targets are available:

 - `kotlin/table-counts` or `java/table-counts`: These produce Tables
   Ia and Ib, respectively.
 - `kotlin/rq-usage-2` or `java/rq-usage-2`: These produce Figures 4a
   and 4b, respectively
 - `kotlin/rq-usage` or `java/rq-usage`: These produce Figures 5 and
   6, respectively
 - `kotlin/rq-mutability`: This produces Figure 8.
 - `kotlin/rq-rhs-types` or `java/rq-rhs-types`: These produce Figures
   7a and 7b, respectively.
 - `kotlin/rq-rhs-methodcalls` or `java/rq-rhs-methodcalls`: These
   produce Tables IIa and IIb, respectively
 - `kotlin/rq-survival` or `java/rq-survival`: These produce Figures
   9a and 9b, respectively
