import json

from prezzipazzi_filter.filter import OfferFilter, jaccard
from prezzipazzi_filter.text import tokenize


def test_jaccard_bounds():
    assert jaccard(set(), {"a"}) == 0.0
    assert jaccard({"a", "b"}, {"a", "b"}) == 1.0
    assert jaccard({"a", "b"}, {"b", "c"}) == 1 / 3


def _filter(tmp_path, items, threshold=0.70):
    path = tmp_path / "list.json"
    path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    return OfferFilter(path, threshold=threshold), path


def test_similar_offer_is_rejected(tmp_path):
    of, _ = _filter(tmp_path, ["Orecchini a cerchio placcati oro, gioielli moda donna"])
    keep, score = of.is_interesting("Orecchini a cerchio placcati oro rosa, gioielli moda donna")
    assert keep is False
    assert score >= 0.70


def test_different_offer_is_kept(tmp_path):
    of, _ = _filter(tmp_path, ["Collana donna acciaio bigiotteria regalo"])
    keep, _ = of.is_interesting("SSD interno NVMe 1TB Gen4 per PC e PS5")
    assert keep is True


def test_select_learns_from_rejected(tmp_path):
    of, path = _filter(tmp_path, ["Rossetto liquido mat lunga tenuta make-up donna"])
    before = len(json.loads(path.read_text(encoding="utf-8")))
    kept = of.select(["Rossetto liquido mat lunga tenuta make-up donna offerta"])
    assert kept == []  # rejected
    after = len(json.loads(path.read_text(encoding="utf-8")))
    assert after == before + 1  # the rejected offer was added to the list


def test_tokenize_drops_stopwords():
    assert "donna" in tokenize("Borsa per la donna") and "per" not in tokenize("Borsa per la donna")
