from __future__ import annotations

import re
from typing import Any, Dict, List


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def product_fact_values(product: dict) -> List[str]:
    values: List[str] = []
    for key in ("material", "color", "dimensions", "wattage"):
        if key in product:
            values.append(str(product[key]))
    if "capacity_ml" in product:
        values.append(str(product["capacity_ml"]))
    if "capacity_l" in product:
        values.append(str(product["capacity_l"]))
    values.append(str(product["warranty_years"]))
    return values


def score_output(output: str, product: dict, checks: dict) -> Dict[str, Any]:
    text = _normalize(output)
    facts = product_fact_values(product)
    present = sum(1 for fact in facts if _normalize(str(fact)) in text)
    accuracy = present / max(len(facts), 1)

    invented = [p for p in checks["forbidden_phrases"] if p in text]
    if invented:
        accuracy = max(0.0, accuracy - 0.35 * len(invented))

    length = len(output)
    if checks["length_min"] <= length <= checks["length_max"]:
        length_score = 1.0
    else:
        length_score = 0.5

    bad = sum(1 for w in checks["tone_bad"] if w in text)
    good = sum(1 for w in checks["tone_good"] if w in text)
    tone_score = max(0.0, min(1.0, 0.55 + 0.15 * good - 0.25 * bad))

    overall = round(0.6 * accuracy + 0.2 * length_score + 0.2 * tone_score, 3)
    return {
        "accuracy": round(accuracy, 3),
        "length_score": length_score,
        "tone_score": round(tone_score, 3),
        "overall": overall,
        "invented_phrases": invented,
        "char_len": length,
    }
