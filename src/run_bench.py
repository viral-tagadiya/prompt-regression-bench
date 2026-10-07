from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .models import generate
from .scoring import score_output

ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((ROOT / "data" / name).read_text())


def render_prompt(template: str, product: dict) -> str:
    size = product.get("dimensions") or product.get("capacity_ml") or product.get("capacity_l")
    return template.format(
        name=product["name"],
        category=product["category"],
        material=product["material"],
        size=size,
        color=product["color"],
        warranty_years=product["warranty_years"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run prompt regression bench")
    parser.add_argument("--prompt-version", default="v1")
    parser.add_argument("--model", default="mock-a")
    args = parser.parse_args()

    products = load_json("products.json")
    prompts = load_json("prompts.json")
    checks = load_json("gold_checks.json")

    if args.prompt_version not in prompts:
        raise SystemExit(f"Unknown prompt version: {args.prompt_version}")

    rows = []
    for product in products:
        prompt = render_prompt(prompts[args.prompt_version], product)
        output = generate(args.model, prompt, product)
        scores = score_output(output, product, checks)
        rows.append(
            {
                "sku": product["sku"],
                "prompt_version": args.prompt_version,
                "model": args.model,
                "output": output,
                **scores,
            }
        )

    df = pd.DataFrame(rows)
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    csv_path = reports / "runs.csv"
    if csv_path.exists():
        prev = pd.read_csv(csv_path)
        df = pd.concat([prev, df], ignore_index=True)
    df.to_csv(csv_path, index=False)

    summary = {
        "prompt_version": args.prompt_version,
        "model": args.model,
        "n": len(rows),
        "mean_overall": round(float(df.tail(len(rows))["overall"].mean()), 3),
        "mean_accuracy": round(float(df.tail(len(rows))["accuracy"].mean()), 3),
        "invented_total": int(sum(len(r["invented_phrases"]) for r in rows)),
    }
    (reports / "latest.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
