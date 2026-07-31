"""Split paper batches into one-paper inputs for safer deep generation."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BATCH_DIR = os.path.join(HERE, "data", "batches")
OUT_DIR = os.path.join(HERE, "data", "paper_in")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    count = 0
    for name in sorted(os.listdir(BATCH_DIR)):
        if not name.endswith(".json"):
            continue
        batch = name[:-5]
        papers = json.load(open(os.path.join(BATCH_DIR, name)))
        for paper in papers:
            gid = str(paper["gid"])
            payload = {"batch": batch, "paper": paper}
            with open(os.path.join(OUT_DIR, f"{gid}.json"), "w") as f:
                json.dump(payload, f, indent=1)
                f.write("\n")
            count += 1
    print(f"wrote {count} one-paper inputs -> data/paper_in")


if __name__ == "__main__":
    main()
