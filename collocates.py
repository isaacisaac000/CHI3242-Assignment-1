from pathlib import Path

import pandas as pd
from qhchina import load_stopwords
from qhchina.analytics.collocations import find_collocates


def load_sentences(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.split() for line in f if line.strip()]


def main():
    sentences = load_sentences("sentences.txt")
    stopwords = load_stopwords()

    filters = {"min_word_length": 2, "max_p": 0.05, "stopwords": stopwords}

    runs = [
        ("window_h5", {"method": "window", "horizon": 5}),
        ("window_h10", {"method": "window", "horizon": 10}),
        ("sentence", {"method": "sentence", "horizon": None}),
    ]

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    for name, kwargs in runs:
        df = find_collocates(sentences, "我", filters=filters, **kwargs)
        df = df.sort_values("obs_local", ascending=False).reset_index(drop=True)
        csv_path = out_dir / f"collocates_我_{name}.csv"
        df.to_csv(csv_path, index=False)
        print(f"\n=== {name} -> {csv_path} ({len(df)} collocates) ===")
        print(df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
