from src.scoring import score_output


CHECKS = {
    "forbidden_phrases": ["waterproof", "bluetooth"],
    "tone_bad": ["amazing"],
    "tone_good": ["durable", "practical"],
    "length_min": 40,
    "length_max": 400,
}


def test_penalizes_invented_specs():
    product = {
        "name": "Bottle",
        "material": "steel",
        "color": "black",
        "dimensions": "20cm",
        "warranty_years": 1,
    }
    clean = score_output(
        "Bottle uses steel, size 20cm, color black. Warranty: 1 years. practical durable.",
        product,
        CHECKS,
    )
    dirty = score_output(
        "Bottle uses steel and is waterproof with bluetooth. amazing!",
        product,
        CHECKS,
    )
    assert clean["overall"] > dirty["overall"]
    assert dirty["invented_phrases"]
