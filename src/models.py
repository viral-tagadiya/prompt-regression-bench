"""Model adapters. Default mocks need no API keys."""

from __future__ import annotations

from typing import Callable, Dict


def _facts_line(product: dict) -> str:
    size = product.get("dimensions") or product.get("capacity_ml") or product.get("capacity_l")
    return (
        f"{product['name']} is made of {product['material']}. "
        f"Size: {size}. Color: {product['color']}. "
        f"Warranty: {product['warranty_years']} years."
    )


def mock_a(prompt: str, product: dict) -> str:
    # Older prompt style: sometimes invents specs
    base = _facts_line(product)
    if "Do not invent" in prompt and product["sku"].endswith("2"):
        return base + " It is waterproof and has bluetooth tracking."
    return base + " A practical everyday choice."


def mock_b(prompt: str, product: dict) -> str:
    # Stricter model: sticks to facts
    size = product.get("dimensions") or (
        f"{product['capacity_ml']}ml" if "capacity_ml" in product else f"{product['capacity_l']}L"
    )
    return (
        f"{product['name']} ({product['category']}) features {product['material']}, "
        f"size {size}, color {product['color']}. "
        f"It includes a {product['warranty_years']}-year warranty. Designed for daily use."
    )


ADAPTERS: Dict[str, Callable[[str, dict], str]] = {
    "mock-a": mock_a,
    "mock-b": mock_b,
}


def generate(model: str, prompt: str, product: dict) -> str:
    if model not in ADAPTERS:
        raise KeyError(f"Unknown model '{model}'. Known: {', '.join(ADAPTERS)}")
    return ADAPTERS[model](prompt, product)
