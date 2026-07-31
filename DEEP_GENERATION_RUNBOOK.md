# Deep Generation Runbook

This repo is ready for the deeper first-principles pass described in
[FIRST_PRINCIPLES_GOAL.md](FIRST_PRINCIPLES_GOAL.md). The current checked-in generated text is mostly the
older shallow schema; this runbook is for replacing it safely.

## Order

1. Prepare family inputs:

   ```bash
   python3 prep_families.py
   ```

2. Run Haiku workflows in the workflow runner:

   ```text
   rich_workflow.js
   kdd_workflow.js
   concepts_workflow.js
   family_workflow.js
   synth_workflow.js
   ```

3. Merge outputs and rebuild:

   ```bash
   python3 merge_rich.py
   python3 merge_concepts.py
   python3 merge_families.py
   python3 prep_synth.py
   # rerun synth_workflow.js after prep_synth.py if concepts were regenerated
   python3 build_explorer.py
   python3 build_deep.py
   python3 build_math.py
   cp site/*.html .
   ```

4. Check progress:

   ```bash
   python3 deep_status.py
   python3 validate_deep_content.py
   ```

## Resume Logic

Use `deep_todo.py` to see what is still legacy or missing:

```bash
python3 deep_todo.py
```

On the current legacy content, this should list all standard batches `b000` through `b099`, all KDD
batches `b000` through `b003`, all 11 concept keys, and all 22 family keys. As each workflow completes
and is merged, the lists should shrink.

The generation workflow files have two edit-in-place controls near the top:

```javascript
const ONLY = []
const WAVE_SIZE = 8
```

Leave `ONLY` empty to run the whole workflow. To rerun only failed or missing jobs, paste values from
`deep_todo.py`, for example:

```javascript
const ONLY = ['b000', 'b017', 'b042']
```

For `concepts_workflow.js` and `family_workflow.js`, `ONLY` takes concept or family keys instead of
batch names. `WAVE_SIZE` controls how many agents run concurrently.

If the JS workflow runner is not available, run one job at a time through Codex CLI:

```bash
python3 run_deep_job.py paper b000
python3 run_deep_job.py kdd b000
python3 run_deep_job.py concept attention
python3 run_deep_job.py family information-retrieval-search
python3 run_deep_job.py synth
```

This is slower than the workflow runner but fully resumable and uses the same workflow prompts as the
source of truth.

The final gate is strict: `validate_deep_content.py` should fail until every analyzed paper has the ten
deep fields, every concept has the new `math` and `family` fields, every theme has a family essay, and
the synthesis has been rerun after the richer concept inputs.

## Expected Final State

- papers: `1537/1537`
- concepts: `11/11`
- families: `22/22`
- synthesis: deep/family-aware
