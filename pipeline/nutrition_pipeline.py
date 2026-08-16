#!/usr/bin/env python3
"""Build/update one master nutrition CSV from Fuel Tap daily exports.

Usage:
    python3 nutrition_pipeline.py --input /path/to/exports --output nutrition_master.csv

The script scans fuel-tap_YYYY-MM-DD.csv files, keeps the newest export for each
local_date, and writes one clean row per date. It uses only Python's standard library.
"""
from __future__ import annotations
import argparse
import csv
import re
from pathlib import Path

DATE_FILE = re.compile(r"^fuel-tap_(\d{4}-\d{2}-\d{2})\.csv$")


def read_one(path: Path) -> dict | None:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        row = next(reader, None)
    if not row or not row.get("local_date"):
        return None
    row["_source_file"] = path.name
    row["_source_mtime"] = str(path.stat().st_mtime)
    return row


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path, help="Folder containing Fuel Tap daily CSV exports")
    p.add_argument("--output", required=True, type=Path, help="Master CSV to create/update")
    args = p.parse_args()

    newest: dict[str, dict] = {}
    for path in args.input.glob("fuel-tap_*.csv"):
        if not DATE_FILE.match(path.name):
            continue
        row = read_one(path)
        if not row:
            continue
        date = row["local_date"]
        if date not in newest or float(row["_source_mtime"]) > float(newest[date]["_source_mtime"]):
            newest[date] = row

    if not newest:
        raise SystemExit(f"No daily Fuel Tap CSVs found in {args.input}")

    fieldnames = [k for k in next(iter(newest.values())).keys() if not k.startswith("_source_")]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for date in sorted(newest):
            writer.writerow({k: newest[date].get(k, "") for k in fieldnames})

    print(f"Wrote {len(newest)} daily rows to {args.output}")


if __name__ == "__main__":
    main()
