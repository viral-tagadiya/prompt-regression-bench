Offline harness for e-commerce product-description prompts. Runs each prompt version against the same product list, scores outputs for invented specs, length, and tone, and writes a comparison spreadsheet.

## Stack

- Python 3.10+
- Pandas / NumPy
- Pluggable model adapters (deterministic mock by default; OpenAI / Gemini hooks ready)

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_bench
python -m src.run_bench --prompt-version v2 --model mock-b
```

## Inputs

- `data/products.json` — ground-truth product facts
- `data/prompts.json` — prompt templates by version
- `data/gold_checks.json` — forbidden invented claims / required phrases

## Outputs

- `reports/latest.json` — aggregate scores
- `reports/runs.csv` — one row per product × prompt × model

## Scoring

- **accuracy**: fraction of output facts that match product fields; inventing missing fields lowers score
- **length**: soft target band (chars)
- **tone**: keyword cues for professional vs hype language
def run_regression_matrix(variants: list, dataset_path: str):
    # Compare prompt string versions across variants
    pass
