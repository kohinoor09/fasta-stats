#!/usr/bin/env python3
"""fasta_stats.py - report length, GC content and base composition
for every sequence in a FASTA file."""

import argparse
import csv
import sys
from collections import Counter


def read_fasta(path):
    """Yield (header, sequence) for each record in a FASTA file."""
    header = None
    chunks = []
    with open(path, "r") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(chunks)
                header = line[1:].strip()
                chunks = []
            else:
                if header is None:
                    raise ValueError(
                        f"line {line_number\}: sequence found before any '>' header"
                    )
                chunks.append(line)
    if header is not None:
        yield header, "".join(chunks)


def sequence_stats(seq):
    """Return length, base counts and GC% for one sequence."""
    seq = seq.upper()
    counts = Counter(seq)
    length = len(seq)
    a, c, g, t, n = (counts[b] for b in "ACGTN")
    other = length - (a + c + g + t + n)
    acgt = a + c + g + t
    gc = (g + c) / acgt * 100 if acgt else 0.0
    return {
        "length": length,
        "A": a, "C": c, "G": g, "T": t, "N": n, "other": other,
        "GC%": round(gc, 2),
    \}


def main():
    parser = argparse.ArgumentParser(
        description="Length, GC content and composition for each FASTA sequence."
    )
    parser.add_argument("fasta", help="path to a FASTA file")
    parser.add_argument("--csv", help="also write the results to this CSV file")
    args = parser.parse_args()

    try:
        rows = []
        for header, seq in read_fasta(args.fasta):
            stats = sequence_stats(seq)
            stats["id"] = header.split()[0]
            rows.append(stats)
    except (OSError, ValueError) as err:
        sys.exit(f"Error: {err\}")

    if not rows:
        sys.exit("Error: no FASTA records found in the file.")

    columns = ["id", "length", "A", "C", "G", "T", "N", "other", "GC%"]
    print("\\t".join(columns))
    for row in rows:
        print("\\t".join(str(row[col]) for col in columns))

    total = sum(r["length"] for r in rows)
    print(f"\\nSequences: {len(rows)\} | Total length: {total\}")

    if args.csv:
        with open(args.csv, "w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()
