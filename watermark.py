"""
Generate GPT-2 text with a keyed statistical watermark and test for that
watermark.

This only detects text produced by a generator using this same algorithm and
key. A missing watermark is not evidence that text was written by a person.

Set AI201_WATERMARK_KEY to a private random value of at least 16 characters:

    export AI201_WATERMARK_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
    python watermark.py generate "A short story about a lighthouse" --max-new-tokens 120
    python watermark.py detect "paste the generated continuation here"

Keep the key secret and stable. Anyone with the key can create text that
passes this detector.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from dataclasses import asdict, dataclass
from typing import Sequence

import detector

DEFAULT_GAMMA = 0.25
DEFAULT_STRENGTH = 2.0
DEFAULT_THRESHOLD = 4.0
DEFAULT_MIN_TOKENS = 50
CONTEXT_WIDTH = 4
KEY_ENV_VAR = "AI201_WATERMARK_KEY"


@dataclass(frozen=True)
class DetectionResult:
    """Statistical evidence for a watermark, not proof of authorship."""

    status: str
    detected: bool | None
    token_count: int
    green_tokens: int
    green_fraction: float | None
    z_score: float | None
    threshold: float

    def to_dict(self) -> dict[str, bool | float | int | str | None]:
        """Return a JSON-serializable representation."""
        return asdict(self)


def _key_bytes(key: str | None) -> bytes:
    value = key if key is not None else os.getenv(KEY_ENV_VAR)
    if not value:
        raise ValueError(
            f"Set {KEY_ENV_VAR} to the same private key for generation and detection."
        )
    encoded = value.encode("utf-8")
    if len(encoded) < 16:
        raise ValueError(f"{KEY_ENV_VAR} must be at least 16 bytes long.")
    return hashlib.sha256(encoded).digest()


def _seed(context: Sequence[int], key: bytes) -> int:
    context_bytes = b",".join(str(token_id).encode("ascii") for token_id in context)
    digest = hashlib.blake2b(context_bytes, key=key, digest_size=8).digest()
    return int.from_bytes(digest, "big") & ((1 << 63) - 1)


def _green_token_ids(
    context: Sequence[int], key: bytes, vocab_size: int, gamma: float
) -> list[int]:
    import torch

    generator = torch.Generator(device="cpu")
    generator.manual_seed(_seed(context[-CONTEXT_WIDTH:], key))
    permutation = torch.randperm(vocab_size, generator=generator)
    green_count = max(1, min(vocab_size - 1, round(vocab_size * gamma)))
    return permutation[:green_count].tolist()


def _validate_gamma(gamma: float) -> None:
    if not 0.0 < gamma < 1.0:
        raise ValueError("gamma must be greater than 0 and less than 1.")


class _WatermarkLogitsProcessor:
    def __init__(self, key: bytes, gamma: float, strength: float):
        self.key = key
        self.gamma = gamma
        self.strength = strength

    def __call__(self, input_ids, scores):
        import torch

        vocab_size = scores.shape[-1]
        for row_index in range(input_ids.shape[0]):
            context = input_ids[row_index].tolist()
            green_ids = _green_token_ids(
                context, self.key, vocab_size, self.gamma
            )
            indices = torch.tensor(green_ids, dtype=torch.long, device=scores.device)
            scores[row_index, indices] += self.strength
        return scores


def generate(
    prompt: str,
    *,
    max_new_tokens: int = 120,
    strength: float = DEFAULT_STRENGTH,
    gamma: float = DEFAULT_GAMMA,
    key: str | None = None,
) -> str:
    """Generate and return only the watermarked continuation of ``prompt``."""
    _validate_gamma(gamma)
    if not prompt.strip():
        raise ValueError("prompt must not be empty.")
    if not 1 <= max_new_tokens <= 1024:
        raise ValueError("max_new_tokens must be between 1 and 1024.")
    if not math.isfinite(strength) or strength <= 0.0:
        raise ValueError("strength must be a finite positive number.")

    import torch

    model, tokenizer = detector._load()
    key_material = _key_bytes(key)
    model_device = next(model.parameters()).device
    encoded = tokenizer(prompt, return_tensors="pt")
    input_ids = encoded["input_ids"].to(model_device)
    attention_mask = encoded.get("attention_mask")
    if attention_mask is not None:
        attention_mask = attention_mask.to(model_device)

    generated = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        logits_processor=[
            _WatermarkLogitsProcessor(key_material, gamma, strength)
        ],
        pad_token_id=tokenizer.eos_token_id,
    )
    continuation = generated[0, input_ids.shape[1]:]
    with torch.no_grad():
        return tokenizer.decode(continuation, skip_special_tokens=True).strip()


def detect_watermark(
    text: str,
    *,
    key: str | None = None,
    gamma: float = DEFAULT_GAMMA,
    threshold: float = DEFAULT_THRESHOLD,
    min_tokens: int = DEFAULT_MIN_TOKENS,
) -> DetectionResult:
    """
    Detect this watermark with a one-sided binomial z-score.

    Text shorter than ``min_tokens`` yields ``status="insufficient_text"``
    and ``detected=None`` rather than a false negative.
    """
    _validate_gamma(gamma)
    if not math.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("threshold must be a finite positive number.")
    if min_tokens < 1:
        raise ValueError("min_tokens must be at least 1.")

    _, tokenizer = detector._load()
    key_material = _key_bytes(key)
    token_ids = tokenizer.encode(text, add_special_tokens=False)
    observed_tokens = max(0, len(token_ids) - 1)
    green_tokens = 0

    for token_index in range(1, len(token_ids)):
        context = token_ids[max(0, token_index - CONTEXT_WIDTH):token_index]
        green_ids = set(_green_token_ids(
            context, key_material, len(tokenizer), gamma
        ))
        if token_ids[token_index] in green_ids:
            green_tokens += 1

    green_fraction = green_tokens / observed_tokens if observed_tokens else None
    if observed_tokens < min_tokens:
        return DetectionResult(
            status="insufficient_text",
            detected=None,
            token_count=observed_tokens,
            green_tokens=green_tokens,
            green_fraction=green_fraction,
            z_score=None,
            threshold=threshold,
        )

    standard_deviation = math.sqrt(observed_tokens * gamma * (1.0 - gamma))
    z_score = (green_tokens - observed_tokens * gamma) / standard_deviation
    detected = z_score >= threshold
    return DetectionResult(
        status="detected" if detected else "not_detected",
        detected=detected,
        token_count=observed_tokens,
        green_tokens=green_tokens,
        green_fraction=green_fraction,
        z_score=round(z_score, 4),
        threshold=threshold,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or test a keyed GPT-2 watermark.")
    commands = parser.add_subparsers(dest="command", required=True)

    generate_parser = commands.add_parser("generate", help="generate watermarked text")
    generate_parser.add_argument("prompt")
    generate_parser.add_argument("--max-new-tokens", type=int, default=120)
    generate_parser.add_argument("--strength", type=float, default=DEFAULT_STRENGTH)
    generate_parser.add_argument("--gamma", type=float, default=DEFAULT_GAMMA)

    detect_parser = commands.add_parser("detect", help="test text for this watermark")
    detect_parser.add_argument("text")
    detect_parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    detect_parser.add_argument("--min-tokens", type=int, default=DEFAULT_MIN_TOKENS)
    detect_parser.add_argument("--gamma", type=float, default=DEFAULT_GAMMA)

    args = parser.parse_args()
    if args.command == "generate":
        print(generate(
            args.prompt,
            max_new_tokens=args.max_new_tokens,
            strength=args.strength,
            gamma=args.gamma,
        ))
        return

    result = detect_watermark(
        args.text,
        threshold=args.threshold,
        min_tokens=args.min_tokens,
        gamma=args.gamma,
    )
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
