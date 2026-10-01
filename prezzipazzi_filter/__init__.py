"""prezzipazzi-filter: drop uninteresting Amazon offers by Jaccard similarity."""

from .filter import OfferFilter, jaccard

__all__ = ["OfferFilter", "jaccard"]
__version__ = "1.0.0"
