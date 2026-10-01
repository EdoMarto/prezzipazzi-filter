"""CLI: read offers from a JSON file, print the ones worth posting.

The input is a JSON array of strings (each the title + description of an offer),
or of objects with a "title" and optional "description".
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from .filter import DEFAULT_THRESHOLD, OfferFilter


def _as_text(offer) -> str:
    if isinstance(offer, str):
        return offer
    if isinstance(offer, dict):
        return " ".join(str(offer.get(k, "")) for k in ("title", "description")).strip()
    return str(offer)


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Filter Amazon offers before posting them.")
    parser.add_argument("offers", help="JSON file with the offers to filter")
    parser.add_argument("--list", default="data/not_interesting.json", help="not-interesting list (JSON)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="reject at or above this similarity")
    parser.add_argument("--no-learn", action="store_true", help="do not add rejected offers to the list")
    args = parser.parse_args(argv)

    offers = [_as_text(o) for o in json.loads(open(args.offers, encoding="utf-8").read())]
    offer_filter = OfferFilter(args.list, threshold=args.threshold)

    if args.no_learn:
        kept = [o for o in offers if offer_filter.is_interesting(o)[0]]
    else:
        kept = offer_filter.select(offers)

    print(f"\n{len(kept)}/{len(offers)} offers worth posting:")
    for offer in kept:
        print(f"  • {offer}")


if __name__ == "__main__":
    main()
