# Tripos PDF

A command-line utility for downloading PDFs for CUED Tripos Papers.

## Installation

```bash
pip install .
```

## Usage

`tripos-pdf` takes paper names and years (`<Paper Name>_<Year>`) as positional arguments and downloads PDFs for each paper and merges them into one file.

Specific page numbers of each paper may also be specified.
e.g. 2P7_2017:1,3-5

Optionally, each page can also be watermarked with its paper and year.

Consult `tripos-pdf --help` for the full set of options.

```bash
tripos-pdf 1P1_2000 3A1_2021
```

### Without Console Script

```bash
python -m tripos_pdf 1P1_2000 3A1_2021
```
