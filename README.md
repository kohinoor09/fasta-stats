# FASTA Stats

Python script that reads any FASTA file and reports, for each sequence:
length, counts of A/C/G/T/N/other, and GC content (%).

## How to run
Requires Python 3 (no extra libraries).

```bash
python3 fasta_stats.py example.fasta
python3 fasta_stats.py example.fasta --csv stats.csv
```

## Example data
`example.fasta` has three public NCBI genomes: phiX174 (NC_001422.1),
lambda phage (NC_001416.1) and SARS-CoV-2 (NC_045512.2).
The output is in `output.txt` and `stats.csv`.

## Decisions
- Own small FASTA parser: handles multi-line sequences, blank lines and many records.
- Sequences are uppercased so lowercase bases are counted.
- GC% = (G + C) / (A + C + G + T); N and other characters are not in the denominator.
- Any character other than A, C, G, T, N goes into "other".
- Bad or empty files give a clear error message instead of a crash.
