#!/usr/bin/env python3
"""Batch price + valuation scan for A-share semiconductors theme."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from price import analyze, fetch_history, valuation

TICKERS = [
    "688126.SH","605358.SH","688233.SH","300655.SZ","300346.SZ","300666.SZ",
    "300706.SZ","002409.SZ","300054.SZ","688019.SH","002371.SZ","688012.SH",
    "688072.SH","688120.SH","688082.SH","688037.SH","688147.SH","300567.SZ",
    "301269.SZ","688521.SH","688206.SH","688981.SH","688347.SH","600460.SH",
    "688396.SH","300661.SZ","688536.SH","688798.SH","688052.SH","300782.SZ",
    "002049.SZ","688385.SH","603501.SH","603986.SH","688008.SH","688608.SH",
    "603688.SH","688268.SH","603650.SH","688106.SH","688200.SH","688630.SH",
    "603005.SH","002156.SZ","688519.SH","605111.SH","603290.SH","688172.SH",
    "688596.SH","300623.SZ","600584.SH"
]

results = []
for sym in TICKERS:
    print(f"scanning {sym} ...", file=sys.stderr)
    r = analyze(sym)
    if r.get("error"):
        results.append({"ticker": sym, "error": r["error"]})
        continue
    data, _ = fetch_history(sym, days=400)
    if data:
        w6 = data[-126:] if len(data) >= 126 else data
        hi6 = max(x["high"] for x in w6)
        lo6 = min(x["low"] for x in w6)
        r["high_6mo"] = round(hi6, 2)
        r["low_6mo"] = round(lo6, 2)
        r["cur_div_high_pct"] = round(r["last"] / hi6 * 100, 1)
    try:
        v = valuation(sym, last=r["last"])
    except Exception as e:
        v = {"error": str(e)}
    r["valuation"] = v
    results.append(r)
    time.sleep(0.15)

out_path = os.path.join(HERE, "_scan_semiconductors_CN_raw.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"wrote {out_path}", file=sys.stderr)
