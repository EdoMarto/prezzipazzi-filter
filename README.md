# prezzipazzi-filter

A small tool that filters Amazon offers before they are posted to a Telegram deals channel, dropping the
ones that look uninteresting (fashion, beauty, jewellery, gadgets…).

It is a simple **instance-based (k-nearest-neighbour) filter**: each offer's text is compared to a list
of known not-interesting products with the **Jaccard similarity** of their words. If an offer is at
least 70% similar to something in the list, it is rejected — and added to the list, so the filter keeps
growing from what it sees.

![How it works](docs/how-it-works.svg)

## Use

```bash
# print the offers worth posting (input: a JSON array of strings or {title, description})
python -m prezzipazzi_filter data/sample_offers.json

# try it without modifying the list
python -m prezzipazzi_filter data/sample_offers.json --no-learn
```

In code:

```python
from prezzipazzi_filter import OfferFilter

f = OfferFilter("data/not_interesting.json")      # threshold defaults to 0.70
keep, score = f.is_interesting("Echo Dot con Alexa, sconto 45%")
good = f.select(offers)                            # returns the keepers, learns from the rest
```

Plug `is_interesting()` into your bot right before sending an offer.

On the sample offers it keeps the tech deals and filters out fashion, beauty and jewellery — each bar is
an offer's similarity to the not-interesting list, and anything past the 0.70 line is dropped:

![Similarity of sample offers](docs/similarity.png)

## Files

- `data/not_interesting.json` — the seed list of uninteresting products (edit it freely).
- `prezzipazzi_filter/filter.py` — Jaccard similarity and the `OfferFilter`.
- `prezzipazzi_filter/text.py` — tokeniser (lowercase, Italian stop-words removed).

## Tune it

- `--threshold 0.6` rejects more aggressively; `0.8` is stricter about what counts as "similar".
- **Review what it learns.** Rejected offers are added automatically, so the list can drift over time.
  Open `data/not_interesting.json` now and then and remove anything that slipped in wrongly.

## Tests

No runtime dependencies (standard library only).

```bash
pip install pytest
pytest
```

## License

[MIT](LICENSE)
