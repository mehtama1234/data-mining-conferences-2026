"""Merge one-paper deep outputs into existing rich_out/batch JSON files."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BATCH_DIR = os.path.join(HERE, "data", "batches")
ITEM_DIR = os.path.join(HERE, "data", "rich_paper_out")
OUT_DIR = os.path.join(HERE, "data", "rich_out")

FIELDS = ("bp", "wh", "naive", "ap", "mech", "math", "dots", "ww", "po", "limits")


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_existing_rich():
    path = os.path.join(HERE, "data", "rich.json")
    if not os.path.exists(path):
        return {}
    try:
        data = load_json(path)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): v for k, v in data.items() if isinstance(v, dict)}


def complete(rec):
    return isinstance(rec, dict) and all(str(rec.get(field, "")).strip() for field in FIELDS)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    existing_rich = load_existing_rich()
    merged = 0
    complete_items = 0
    for name in sorted(os.listdir(BATCH_DIR)):
        if not name.endswith(".json"):
            continue
        batch = name[:-5]
        papers = load_json(os.path.join(BATCH_DIR, name))
        out_path = os.path.join(OUT_DIR, name)
        batch_out = {}
        if os.path.exists(out_path):
            try:
                existing = load_json(out_path)
                if isinstance(existing, dict):
                    batch_out.update({str(k): v for k, v in existing.items()})
            except Exception:
                batch_out = {}
        for paper in papers:
            gid = str(paper["gid"])
            if gid not in batch_out and gid in existing_rich:
                batch_out[gid] = existing_rich[gid]
        changed = False
        for paper in papers:
            gid = str(paper["gid"])
            item_path = os.path.join(ITEM_DIR, f"{gid}.json")
            if not os.path.exists(item_path):
                continue
            item = load_json(item_path)
            if not complete(item):
                raise SystemExit(f"incomplete item output: {item_path}")
            batch_out[gid] = {field: item[field] for field in FIELDS}
            changed = True
            complete_items += 1
        if changed:
            with open(out_path, "w") as f:
                json.dump(batch_out, f, indent=1)
                f.write("\n")
            merged += 1
    print(f"merged {complete_items} one-paper outputs into {merged} rich_out batches")


if __name__ == "__main__":
    main()
