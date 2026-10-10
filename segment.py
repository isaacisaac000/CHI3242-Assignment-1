import re

import jieba
from opencc import OpenCC


def main():
    with open("data/novel.txt", "r", encoding="utf-8-sig") as f:
        text = f.read()

    cc = OpenCC("t2s")
    text = cc.convert(text)

    # Split into sentences on Chinese sentence-ending punctuation
    sentences = [s for s in re.split(r"[。！？]+", text) if s.strip()]

    # Tokens consisting solely of punctuation/whitespace are dropped
    punct_re = re.compile(r"^[\W_]+$", re.UNICODE)

    lines = []
    for sentence in sentences:
        words = [w for w in jieba.cut(sentence) if w.strip() and not punct_re.match(w)]
        if len(words) >= 5:
            lines.append(" ".join(words))

    with open("sentences.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"{len(sentences)} sentences, {len(lines)} kept (>= 5 words)")


if __name__ == "__main__":
    main()
