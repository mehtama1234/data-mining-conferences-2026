"""Run one deep-generation job through `codex exec`.

This is a fallback when the JS workflow runner is not available. It runs one
paper batch, KDD batch, concept key, family key, or synthesis job at a time.
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

JOBS = {
    "paper": ("rich_workflow.js", "data/batches/{id}.json", "data/rich_out/{id}.json"),
    "paper-item": ("rich_workflow.js", "data/paper_in/{id}.json", "data/rich_paper_out/{id}.json"),
    "kdd": ("kdd_workflow.js", "data/kdd_batches/{id}.json", "data/kdd_out/{id}.json"),
    "concept": ("concepts_workflow.js", "data/concept_in/{id}.json", "data/concept_out/{id}.json"),
    "family": ("family_workflow.js", "data/family_in/{id}.json", "data/family_out/{id}.json"),
    "synth": ("synth_workflow.js", "data/synth_in.json", "data/synth_out.json"),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=JOBS)
    ap.add_argument("id", nargs="?", help="batch/key, e.g. b000 or geometry-processing-meshes")
    args = ap.parse_args()

    workflow, input_t, output_t = JOBS[args.kind]
    job_id = args.id or "synth"
    input_path = input_t.format(id=job_id)
    output_path = output_t.format(id=job_id)
    if not os.path.exists(os.path.join(HERE, input_path)):
        sys.exit(f"missing input: {input_path}")

    out_dir = os.path.dirname(os.path.join(HERE, output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    if args.kind == "paper-item":
        prompt = f"""Read FIRST_PRINCIPLES_GOAL.md, {workflow}, and {input_path}.
Run exactly one per-paper deep generation job for gid {job_id}. Write only {output_path}.
The input file contains one object with "batch" and "paper"; generate only that one paper.
Follow the per-paper schema and word ranges in {workflow}: bp, wh, naive, ap, mech, math, dots, ww, po, limits.
Write a single JSON object with exactly those ten fields, not an object keyed by gid.
Use only evidence from the input file and the repo's current JSON data. Do not modify any other files.
The output JSON is large enough that shell argument limits can matter: write with apply_patch or another file-safe edit path, not by passing the whole JSON through node -e, python -c, or a shell here-doc.
After writing, validate that {output_path} is parseable JSON and report the word counts for each generated field."""
    else:
        prompt = f"""Read FIRST_PRINCIPLES_GOAL.md, {workflow}, and {input_path}.
Run exactly one {args.kind} generation job for {job_id}. Write only {output_path}.
Follow the schema, word ranges, no-jargon/plain-language style, grounding rules, and JSON escaping rules in {workflow}.
Use only evidence from the input file and the repo's current JSON data. Do not modify any other files.
After writing, validate that {output_path} is parseable JSON and report the word counts for each generated field."""

    cmd = [
        "codex", "exec",
        "-C", HERE,
        "--dangerously-bypass-approvals-and-sandbox",
        prompt,
    ]
    raise SystemExit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
