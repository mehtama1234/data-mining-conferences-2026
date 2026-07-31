"""Validate selected deep per-paper batch outputs.

This is a scoped gate for incremental generation waves. The full
validate_deep_content.py gate remains intentionally strict for the whole site.
"""
import argparse
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = ("bp", "wh", "naive", "ap", "mech", "math", "dots", "ww", "po", "limits")
RANGES = {
    "bp": (120, 180),
    "wh": (120, 180),
    "naive": (90, 140),
    "ap": (120, 180),
    "mech": (180, 260),
    "math": (180, 260),
    "dots": (120, 180),
    "ww": (140, 220),
    "po": (80, 130),
    "limits": (80, 130),
}
MARKDOWN = re.compile(r"(^|[^\\])(\*\*|\*)")


def words(text):
    return len(str(text).split())


def load_batch(batch):
    path = os.path.join(HERE, "data", "rich_out", f"{batch}.json")
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{batch}: root is not an object")
    return data


def check_batch(batch):
    data = load_batch(batch)
    errors = []
    for gid, item in data.items():
        if not isinstance(item, dict):
            errors.append(f"{batch}:{gid}: item is not an object")
            continue
        for field in FIELDS:
            text = str(item.get(field, "")).strip()
            if not text:
                errors.append(f"{batch}:{gid}.{field}: missing")
                continue
            lo, hi = RANGES[field]
            count = words(text)
            if count < lo or count > hi:
                errors.append(f"{batch}:{gid}.{field}: {count} words, expected {lo}-{hi}")
            if MARKDOWN.search(text):
                errors.append(f"{batch}:{gid}.{field}: markdown marker")

    for field in FIELDS:
        counts = collections.Counter(str(item.get(field, "")).strip() for item in data.values())
        for text, count in counts.items():
            if text and count > 1:
                errors.append(f"{batch}:{field}: duplicated exact text across {count} papers")
                break

    print(f"{batch}: {len(data)} papers")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("batches", nargs="+", help="batch ids such as b013 b015")
    args = parser.parse_args()
    errors = []
    for batch in args.batches:
        errors.extend(check_batch(batch))
    if errors:
        print("FAIL")
        for error in errors:
            print(error)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
