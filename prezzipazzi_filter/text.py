"""Turn a product title/description into a set of meaningful word tokens."""

from __future__ import annotations

import re

# A small Italian stop-word list: common words that carry no signal for the filter.
_STOPWORDS = {
    "a", "ad", "al", "allo", "ai", "agli", "alla", "alle", "con", "col", "coi",
    "da", "di", "del", "dello", "dei", "degli", "della", "delle", "in", "nel",
    "nello", "nei", "negli", "nella", "nelle", "su", "sul", "per", "tra", "fra",
    "e", "ed", "o", "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
    "the", "and", "set", "pezzi", "pz", "confezione", "paia", "pack",
}

_TOKEN_RE = re.compile(r"[a-zàèéìòù0-9]+")


def tokenize(text: str) -> set[str]:
    """Lowercase, split on non-letters, drop stop-words and 1-char tokens."""
    words = _TOKEN_RE.findall(text.lower())
    return {w for w in words if len(w) > 1 and w not in _STOPWORDS}
