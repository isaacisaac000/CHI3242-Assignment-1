import json
from pathlib import Path

import pandas as pd


OUT_DIR = Path("output")

RUNS = [
    ("collocates_我_window_h5.csv", "Window (horizon=5)"),
    ("collocates_我_window_h10.csv", "Window (horizon=10)"),
    ("collocates_我_sentence.csv", "Sentence"),
]


def format_p(p):
    if p < 1e-4:
        return f"{p:.2e}"
    return f"{p:.4f}"


def main():
    data = {}
    for filename, label in RUNS:
        df = pd.read_csv(OUT_DIR / filename)
        df["p_value"] = df["p_value"].map(format_p)
        for col in ("exp_local", "ratio_local"):
            df[col] = df[col].map(lambda v: f"{v:.3f}")
        data[label] = df.to_dict(orient="records")

    report = OUT_DIR / "results.html"
    report.write_text(
        TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False)),
        encoding="utf-8",
    )
    print(f"Wrote {report}")


TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>Collocates of 我 — 呼兰河传</title>
<style>
  body { font-family: sans-serif; margin: 2rem; background: #fafafa; color: #222; }
  h1 { font-size: 1.4rem; }
  select { font-size: 1rem; padding: 0.4rem 0.8rem; margin-bottom: 1rem; }
  table { border-collapse: collapse; width: 100%; max-width: 60rem; background: #fff; }
  th, td { border: 1px solid #ccc; padding: 0.35rem 0.7rem; text-align: right; }
  th { background: #eee; }
  th:first-child, td:first-child { text-align: center; }
  td:nth-child(2) { text-align: left; font-weight: 600; }
  tr:nth-child(even) { background: #f5f5f5; }
  .meta { color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
</style>
</head>
<body>
<h1>Collocates of 我 — filters: min_word_length=2, max_p=0.05, stopwords removed</h1>
<select id="picker"></select>
<div class="meta" id="meta"></div>
<table id="tbl"></table>
<script>
const DATA = __DATA__;
const picker = document.getElementById('picker');
const meta = document.getElementById('meta');
const tbl = document.getElementById('tbl');

Object.keys(DATA).forEach(label => {
  const opt = document.createElement('option');
  opt.value = label;
  opt.textContent = label;
  picker.appendChild(opt);
});

function show(label) {
  const rows = DATA[label];
  meta.textContent = rows.length + ' collocates';
  const cols = Object.keys(rows[0]);
  tbl.innerHTML = '<tr>' + cols.map(c => '<th>' + c + '</th>').join('') + '</tr>' +
    rows.map(r => '<tr>' + cols.map(c => '<td>' + r[c] + '</td>').join('') + '</tr>').join('');
}

picker.addEventListener('change', () => show(picker.value));
show(picker.value);
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
