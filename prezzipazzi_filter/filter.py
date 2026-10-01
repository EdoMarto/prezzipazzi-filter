"""Similarity filter for Amazon offers.

An offer is considered *not interesting* when its text is similar enough to one
already in the "not interesting" list. Similarity is the Jaccard index between
the two sets of word tokens; above `threshold` (0.70 by default) the offer is
rejected. Rejected offers are added back to the list, so the filter keeps
growing from what it sees — a simple instance-based (k-nearest-neighbour) model.

Keep a human in the loop: review what gets auto-added now and then, so the list
stays true to your taste instead of drifting.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from .text import tokenize

log = logging.getLogger(__name__)

DEFAULT_THRESHOLD = 0.70


def jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard index: |A ∩ B| / |A ∪ B|, in [0, 1]."""
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    return intersection / (len(a) + len(b) - intersection)


class OfferFilter:
    def __init__(self, not_interesting_path: str | Path, threshold: float = DEFAULT_THRESHOLD) -> None:
        self.path = Path(not_interesting_path)
        self.threshold = threshold
        self._items: list[str] = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else []
        self._sets: list[set[str]] = [tokenize(text) for text in self._items]

    # -- scoring --------------------------------------------------------------

    def similarity(self, text: str) -> float:
        """Highest Jaccard similarity between `text` and the not-interesting list."""
        tokens = tokenize(text)
        return max((jaccard(tokens, s) for s in self._sets), default=0.0)

    def is_interesting(self, text: str) -> tuple[bool, float]:
        """Return (keep?, similarity). Not interesting when similarity >= threshold."""
        score = self.similarity(text)
        return score < self.threshold, score

    # -- learning -------------------------------------------------------------

    def learn(self, text: str) -> None:
        """Add a rejected offer to the list and persist it."""
        self._items.append(text)
        self._sets.append(tokenize(text))
        self.path.write_text(json.dumps(self._items, ensure_ascii=False, indent=2), encoding="utf-8")

    def select(self, offers: list[str]) -> list[str]:
        """Return the interesting offers; reject the rest and learn from them."""
        kept: list[str] = []
        for offer in offers:
            keep, score = self.is_interesting(offer)
            if keep:
                kept.append(offer)
            else:
                log.info("Rejected (%.0f%% similar): %s", score * 100, offer[:70])
                self.learn(offer)
        return kept
