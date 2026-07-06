#!/usr/bin/env python3
"""
Provider-agnostic price/momentum helper for the Serenity bottleneck-hunter skill.

按优先级回退抓历史价,**严禁靠网页猜价格**——SKILL Step 6 的 stage 判定必须基于真实数据:
  1) Tushare         (A 股优先;默认前复权 qfq;需 TUSHARE_TOKEN;可用 TUSHARE_ADJ=raw 切未复权)
  2) EODHD            (若环境变量 EODHD_API_KEY 已设;**全球覆盖最广,海外股优先**)
  3) yfinance         (无需 key,**美股覆盖好,海外股常有 gap**)
  4) 失败 → 报错退出 (do NOT silently guess)

返回每只票的 JSON:last、6 月区间位置、距高点、1/3 月动量、stage 标签。

CLI:
    python scripts/price.py AEHR NVTS VICR IPWR POWI            # 默认走 yfinance(无 EODHD/Tushare key)
    TUSHARE_TOKEN=xxx python scripts/price.py 000001.SZ         # A 股优先 Tushare(默认前复权)
    TUSHARE_ADJ=raw TUSHARE_TOKEN=xxx python scripts/price.py 000001.SZ  # 未复权
    EODHD_API_KEY=xxx python scripts/price.py XFAB.STU AEHR     # 海外股请用 EODHD

可作为模块导入:
    from price import analyze, fetch_history
"""
import json, os, sys, urllib.request, datetime

EODHD_KEY = os.environ.get("EODHD_API_KEY", "").strip()
TUSHARE_TOKEN = os.environ.get("TUSHARE_TOKEN", "").strip()
TUSHARE_ADJ = os.environ.get("TUSHARE_ADJ", "qfq").strip().lower()  # qfq|hfq|raw


def _to_float(v):
    """把 pandas/numpy/字符串标量转成 float;无效值返回 None。"""
    if v is None:
        return None
    try:
        import pandas as pd
        if pd.isna(v):
            return None
    except Exception:
        pass
    try:
        f = float(v)
        return f if f == f else None  # 过滤 NaN
    except Exception:
        return None


def _to_ts_code(symbol):
    """把 skill 内部的 A 股代码映射成 Tushare 的 ts_code。"""
    su = (symbol or "").upper().strip()
    for old, new in ((".SS", ".SH"), (".SHG", ".SH"), (".SH", ".SH"),
                     (".SHE", ".SZ"), (".SZ", ".SZ"), (".BJ", ".BJ")):
        if su.endswith(old):
            return su[:-len(old)] + new
    # 纯数字 6 位代码,按首位推断交易所
    if su.isdigit() and len(su) >= 6:
        code = su[:6]
        if code.startswith("6") or code.startswith("9") or code.startswith("688"):
            return f"{code}.SH"
        if code.startswith("0") or code.startswith("3"):
            return f"{code}.SZ"
        if code.startswith("4") or code.startswith("8"):
            return f"{code}.BJ"
    return None


def _is_a_share(symbol):
    """判断 symbol 是否为 A 股(含北交所)。"""
    su = (symbol or "").upper()
    return _to_ts_code(su) is not None


def _fetch_tushare(symbol, days=400):
    """用 Tushare 拉 A 股日线。默认前复权(qfq),可通过 TUSHARE_ADJ=raw/hfq 切换。返回 list[dict] 或 None。"""
    if not TUSHARE_TOKEN:
        return None
    ts_code = _to_ts_code(symbol)
    if not ts_code:
        return None
    try:
        import tushare as ts
        pro = ts.pro_api(TUSHARE_TOKEN)
    except Exception:
        return None
    end = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")
    try:
        adj = TUSHARE_ADJ if TUSHARE_ADJ in ("qfq", "hfq") else None
        if adj:
            df = ts.pro_bar(ts_code=ts_code, start_date=start_str, end_date=end_str,
                            freq="D", adj=adj)
        else:
            df = pro.daily(ts_code=ts_code, start_date=start_str, end_date=end_str)
        if df is None or df.empty:
            return None
        df = df.sort_values("trade_date", ascending=True)
        out = []
        for _, row in df.iterrows():
            try:
                d = datetime.datetime.strptime(str(row["trade_date"]), "%Y%m%d").date().isoformat()
            except Exception:
                d = str(row["trade_date"])
            out.append({
                "date": d,
                "open": _to_float(row["open"]),
                "high": _to_float(row["high"]),
                "low": _to_float(row["low"]),
                "close": _to_float(row["close"])
            })
        return out
    except Exception:
        return None


def _fetch_eodhd(symbol, days=400):
    end = datetime.date.today().isoformat()
    start = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    url = f"https://eodhd.com/api/eod/{symbol}?api_token={EODHD_KEY}&from={start}&to={end}&period=d&fmt=json"
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                d = json.load(r)
                if isinstance(d, list) and d:
                    return [{"date": x["date"], "open": x["open"], "high": x["high"],
                             "low": x["low"], "close": x["close"]} for x in d]
        except Exception:
            pass
    return None


def _fetch_yf(symbol, days=400):
    try:
        import yfinance as yf
    except ImportError:
        return None
    try:
        t = yf.Ticker(symbol)
        h = t.history(period=f"{max(days, 400)}d", auto_adjust=False)
        if h is None or len(h) == 0:
            return None
        return [{"date": idx.strftime("%Y-%m-%d"),
                 "open": float(row["Open"]), "high": float(row["High"]),
                 "low": float(row["Low"]),   "close": float(row["Close"])}
                for idx, row in h.iterrows()]
    except Exception:
        return None


def fetch_history(symbol, days=400):
    """按 Tushare(A股) → EODHD → yfinance 顺序抓;返回 (data, provider) 或 (None, None)。"""
    if _is_a_share(symbol) and TUSHARE_TOKEN:
        data = _fetch_tushare(symbol, days)
        if data:
            return data, "tushare"
    if EODHD_KEY:
        data = _fetch_eodhd(symbol, days)
        if data:
            return data, "eodhd"
    data = _fetch_yf(symbol, days)
    if data:
        return data, "yfinance"
    return None, None


def analyze(symbol, days=400):
    data, prov = fetch_history(symbol, days)
    if data is None:
        return {"ticker": symbol,
                "error": "no data from Tushare/EODHD/yfinance (A股请设 TUSHARE_TOKEN,海外股请设 EODHD_API_KEY,或校验代码/交易所后缀)"}
    closes = [x["close"] for x in data]
    last = closes[-1]
    last_date = data[-1]["date"]
    w6 = data[-126:] if len(data) >= 126 else data
    lo6 = min(x["low"] for x in w6)
    hi6 = max(x["high"] for x in w6)
    rng_pos = round((last - lo6) / (hi6 - lo6) * 100) if hi6 > lo6 else 50
    off_high = round((last / hi6 - 1) * 100, 1)
    sma50 = sum(closes[-50:]) / min(50, len(closes))
    r1m = round((last / closes[-21] - 1) * 100, 1) if len(closes) > 21 else None
    r3m = round((last / closes[-63] - 1) * 100, 1) if len(closes) > 63 else None
    up = last > sma50
    # stage heuristic — 同时看 1 月动量(避免把刚暴拉的标判成 early)
    hot_1m = (r1m is not None and r1m > 40)
    at_top = (rng_pos >= 95 and (r3m or 0) > 30)
    if (r3m is not None and r3m > 120) or hot_1m or at_top:
        stage = "extended/parabolic (already ran hot -> late for Mode A; DON'T chase, wait for pullback)"
    elif up and r3m is not None and 5 < r3m <= 120 and not hot_1m:
        stage = "early-uptrend (reasonable Mode-A entry: theme igniting, not yet overextended)"
    elif not up and r3m is not None and r3m < -10:
        stage = "downtrend/basing (only Mode B 'buy the dip' if catalyst is non-material)"
    else:
        stage = "range/neutral"
    return {
        "ticker": symbol,
        "provider": prov,
        "last": round(last, 2),
        "last_date": last_date,
        "range_pos_6mo_pct": rng_pos,
        "pct_off_6mo_high": off_high,
        "ret_1m_pct": r1m,
        "ret_3m_pct": r3m,
        "above_sma50": up,
        "stage": stage,
    }


# ── 估值/速度字段(二轴判定的「基本面跟不跟得上」轴)= 多源 ──
# A股→akshare(中国源:百度 PE-TTM + 东财券商一致预期 forward + 东财财务增速);美股/海外→yfinance。
# 实测:yfinance 的 A股 trailing PE / 盈利增速 基本准,但 forward 系统性偏低(乐观)→ A股 forward 用 akshare 更可信;
# 且两源对 trailing 可交叉验证。每个 akshare 接口独立 try(本机代理会拦部分 endpoint),缺字段由 yfinance 兜底。
_AK_FC = None  # 东财全市场一致预期表,缓存一次(~2700 只,拉一次 ~35s)

def _ak_forecast():
    global _AK_FC
    if _AK_FC is None:
        import akshare as ak
        _AK_FC = ak.stock_profit_forecast_em()
    return _AK_FC

def _ak_valuation(code, last=None):
    out = {"forward_pe": None, "trailing_pe": None, "peg": None, "eps_growth": None, "rev_growth": None, "src": "akshare"}
    import akshare as ak
    try:  # ① PE-TTM(百度,序列尾 = 最新)
        df = ak.stock_zh_valuation_baidu(symbol=code, indicator="市盈率(TTM)", period="近一年")
        out["trailing_pe"] = round(float(df["value"].iloc[-1]), 2)
    except Exception:
        pass
    try:  # ② forward = 现价 ÷ 次年券商一致预期 EPS(真 forward,非 yfinance 乐观值)
        fc = _ak_forecast(); row = fc[fc["代码"] == code]
        col = next((c for c in fc.columns if "2026" in str(c) and "每股收益" in str(c)), None)
        if not row.empty and col and last:
            eps = float(row[col].iloc[0])
            if eps > 0:
                out["forward_pe"] = round(last / eps, 2)
    except Exception:
        pass
    try:  # ③ 增速:财务摘要 归母净利润 / 营业总收入 最新 vs 4 季前 YoY
        fa = ak.stock_financial_abstract(symbol=code)
        dc = [c for c in fa.columns if str(c).isdigit() and len(str(c)) == 8]
        def yoy(metric):
            r = fa[fa["指标"].astype(str) == metric]
            if r.empty or len(dc) < 5:
                return None
            try:
                cur, pri = float(r[dc[0]].iloc[0]), float(r[dc[4]].iloc[0])
                return round((cur - pri) / abs(pri) * 100, 1) if pri else None
            except Exception:
                return None
        out["eps_growth"] = yoy("归母净利润")
        out["rev_growth"] = yoy("营业总收入")
    except Exception:
        pass
    if out["trailing_pe"] and out["eps_growth"] and out["eps_growth"] > 0:  # 粗略 PEG
        out["peg"] = round(out["trailing_pe"] / out["eps_growth"], 2)
    return out

def _yf_valuation(yf_symbol, info=None):
    out = {"forward_pe": None, "trailing_pe": None, "peg": None, "eps_growth": None, "rev_growth": None, "src": "yfinance"}
    if info is None:
        try:
            import yfinance as yf
            info = yf.Ticker(yf_symbol).info or {}
        except Exception:
            return out
    def g(k):
        v = info.get(k)
        return round(float(v), 2) if isinstance(v, (int, float)) and v == v else None
    out["forward_pe"] = g("forwardPE"); out["trailing_pe"] = g("trailingPE")
    out["peg"] = g("pegRatio") or g("trailingPegRatio")
    eg = g("earningsGrowth")
    if eg is None:
        eg = g("earningsQuarterlyGrowth")
    out["eps_growth"] = round(eg * 100, 1) if eg is not None else None
    rg = g("revenueGrowth")
    out["rev_growth"] = round(rg * 100, 1) if rg is not None else None
    return out

def _ts_valuation(symbol, last=None):
    """用 Tushare 拉 A 股估值/增速。返回 dict 或 None。"""
    if not TUSHARE_TOKEN:
        return None
    ts_code = _to_ts_code(symbol)
    if not ts_code:
        return None
    try:
        import tushare as ts
        pro = ts.pro_api(TUSHARE_TOKEN)
    except Exception:
        return None

    out = {"forward_pe": None, "trailing_pe": None, "peg": None,
           "eps_growth": None, "rev_growth": None, "src": "tushare"}
    latest_mv = None

    try:  # ① trailing PE + 总市值
        db = pro.daily_basic(ts_code=ts_code, fields="trade_date,pe_ttm,pe,total_mv")
        if db is not None and not db.empty:
            db = db.sort_values("trade_date", ascending=True).iloc[-1]
            latest_mv = _to_float(db.get("total_mv"))
            out["trailing_pe"] = _to_float(db.get("pe_ttm")) or _to_float(db.get("pe"))
    except Exception:
        pass

    try:  # ② 增速
        fi = pro.fina_indicator(ts_code=ts_code,
                                fields="end_date,netprofit_yoy,or_yoy,grossprofit_margin")
        if fi is not None and not fi.empty:
            fi = fi.sort_values("end_date", ascending=True).iloc[-1]
            out["eps_growth"] = _to_float(fi.get("netprofit_yoy"))
            out["rev_growth"] = _to_float(fi.get("or_yoy"))
    except Exception:
        pass

    try:  # ③ forward PE:用业绩预告净利润中值 / 总市值(不用券商一致预期)
        if latest_mv:
            fc = pro.forecast(ts_code=ts_code,
                              fields="end_date,net_profit_min,net_profit_max")
            if fc is not None and not fc.empty:
                fc = fc.sort_values("end_date", ascending=True).iloc[-1]
                np_min = _to_float(fc.get("net_profit_min"))
                np_max = _to_float(fc.get("net_profit_max"))
                if np_min and np_max and np_max > 0:
                    np_mid = (np_min + np_max) / 2.0  # 单位都是万元,可直接相除
                    forward_pe = latest_mv / np_mid
                    if forward_pe > 0:
                        out["forward_pe"] = round(forward_pe, 2)
    except Exception:
        pass

    if out["trailing_pe"] and out["eps_growth"] and out["eps_growth"] > 0:
        out["peg"] = round(out["trailing_pe"] / out["eps_growth"], 2)
    return out


def valuation(symbol, info=None, last=None):
    """多源估值:A股优先 Tushare,缺字段 akshare → yfinance 兜底;美股/海外 → yfinance。
    传 last(现价)供 A股算 forward。返回含 src 标来源,便于报告标注与交叉验证。"""
    su = (symbol or "").upper()
    if not _is_a_share(su):
        return _yf_valuation(symbol, info)
    code = su.split(".")[0][:6]

    # 1) 优先 Tushare
    if TUSHARE_TOKEN:
        try:
            out = _ts_valuation(symbol, last)
            if out and any(out.get(k) is not None for k in ("trailing_pe", "forward_pe", "eps_growth", "rev_growth")):
                return out
        except Exception:
            pass

    # 2) Tushare 拿不到再用 akshare
    try:
        out = _ak_valuation(code, last)
    except Exception:
        out = None
    if not out or all(out.get(k) is None for k in ("trailing_pe", "forward_pe", "eps_growth")):
        v = _yf_valuation(symbol, info); v["src"] = "yfinance(ak不可用)"; return v
    if any(out.get(k) is None for k in ("trailing_pe", "forward_pe", "eps_growth", "rev_growth")):  # 缺字段兜底
        yv = _yf_valuation(symbol, info); filled = False
        for k in ("forward_pe", "trailing_pe", "peg", "eps_growth", "rev_growth"):
            if out.get(k) is None and yv.get(k) is not None:
                out[k] = yv[k]; filled = True
        if filled:
            out["src"] = "akshare+yf兜底"
    return out


if __name__ == "__main__":
    syms = sys.argv[1:]
    if not syms:
        print("usage: python scripts/price.py TICKER [TICKER ...]", file=sys.stderr)
        print("notes: A股优先 Tushare (set TUSHARE_TOKEN,默认前复权 qfq;TUSHARE_ADJ=raw 切未复权),其次 EODHD,最后 yfinance。海外股必须 EODHD。", file=sys.stderr)
        sys.exit(1)
    for s in syms:
        print(json.dumps(analyze(s), ensure_ascii=False))
