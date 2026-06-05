#!/usr/bin/env python3
"""verify_tickers.py — L3 pre-commit hook 拦截:扫描 staged 文件里所有
ticker 模式 (\d+\.SHG/HK/US/T/PA/...),对每个查 ticker_truth.csv 验证旁边的中文名是否匹配。
不匹配 → 阻止 commit,要求人工修复。

用法:
  # 手动: 扫描某个文件
  python scripts/verify_tickers.py path/to/file.html

  # 装 git pre-commit hook:
  ln -sf ../../scripts/verify_tickers.py .git/hooks/pre-commit
  (Windows: copy 文件到 .git/hooks/pre-commit;或建 .bat wrapper)

退出码:
  0 = 全 pass / 没找到 ticker
  1 = 有 mismatch / 阻止 commit
  2 = 工具内部错(EODHD 不可用 etc)
"""
import os, re, sys, csv, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ticker_truth import lookup_by_ticker, verify_pair

# 匹配 ticker:数字.SHG / .SHE / .HK / .US / .T / .PA / .LSE / .TO 等
TICKER_RE = re.compile(r"\b(\d{4,6}(?:\.[A-Z]{1,4})?|[A-Z]{1,5}\.(?:US|HK|T|PA|LSE|TO|OL|L))\b")

# 中文公司名匹配 — 在 ticker ±60 字符窗口找
ZH_NAME_RE = re.compile(r"[一-鿿]{2,12}")  # 2-12 个中文字


def scan_file(path):
    """扫单个文件,返回 (mismatches, warnings) lists
    SKIP 机制:文件首 500 字符内含 'ticker-verify: skip' → 跳过(文档/示例文件用)"""
    if not os.path.exists(path): return ([], [])
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        return ([], [f"can't read {path}: {e}"])
    # SKIP magic comment(允许文档文件含错例示意)
    if "ticker-verify: skip" in text[:500]:
        return ([], [])

    mismatches = []
    warnings = []
    STOPWORDS = {"上游", "中游", "下游", "系统", "对照", "扩列", "排除", "观望", "候选",
                 "深度", "回调", "启动", "等止跌", "等启动", "已涨", "未启动", "本主题",
                 "等回调", "无独立", "持续跌", "持平", "极深", "中位", "边缘", "测试",
                 "代码", "现价", "数据", "区间", "动量", "目标", "情景", "风险"}
    # 找所有 ticker 出现位置
    seen = set()
    for m in TICKER_RE.finditer(text):
        ticker = m.group(1)
        if not (ticker.endswith(".SHG") or ticker.endswith(".SHE") or ticker.endswith(".HK")
                or ticker.endswith(".US") or "." in ticker):
            continue
        # 取 ticker 后 60 字符为主(典型报告里 ticker 后跟公司名)+ 前 30 字符 fallback
        after = text[m.end(): min(len(text), m.end() + 60)]
        before = text[max(0, m.start() - 30): m.start()]
        # 抓最近的中文名(after 优先 → before 兜底)
        zh = None
        for ctx in (after, before):
            for z in ZH_NAME_RE.findall(ctx):
                if z not in STOPWORDS and not any(s in z for s in ("rng", "off", "ext")):
                    zh = z; break
            if zh: break
        if not zh:
            continue
        key = (ticker, zh)
        if key in seen: continue
        seen.add(key)
        # 查 ground truth
        info = lookup_by_ticker(ticker)
        if not info:
            warnings.append(f"{path}:{ticker} 旁注'{zh}' — NOT IN TICKER_TRUTH DB(请跑 init/resolve)")
            continue
        truth_zh = (info.get("name_zh", "") or "").strip()
        truth_en = (info.get("name_en", "") or "").strip()
        # 双向 contains 检查
        if zh in truth_zh or truth_zh in zh:
            continue  # ok
        # 写英文情况(rare)
        if any(c.lower() in truth_en.lower() for c in [zh]) or any(p.lower() in truth_en.lower() for p in zh.split()):
            continue
        mismatches.append({
            "file": path, "ticker": ticker, "claimed_zh": zh,
            "truth_zh": truth_zh, "truth_en": truth_en,
        })

    return mismatches, warnings


def get_staged_files():
    """git diff --cached --name-only"""
    try:
        r = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                           capture_output=True, text=True, cwd=os.path.join(HERE, "..", ".."))
        files = [f.strip() for f in r.stdout.splitlines() if f.strip()]
        return files
    except Exception as e:
        return []


def main():
    if "--staged" in sys.argv:
        files = get_staged_files()
        if not files:
            print("verify_tickers: no staged files")
            return 0
        targets = files
    elif len(sys.argv) > 1:
        targets = [a for a in sys.argv[1:] if not a.startswith("--")]
    else:
        print(__doc__); return 0

    # 只扫文本类
    OK_EXT = (".py", ".html", ".csv", ".md", ".json", ".txt")
    targets = [t for t in targets if t.endswith(OK_EXT)]

    if not targets:
        print("verify_tickers: no scannable files (.py/.html/.csv/.md/.json)")
        return 0

    all_mis = []
    all_warn = []
    for t in targets:
        # 用绝对路径
        if not os.path.isabs(t):
            root = os.path.join(HERE, "..", "..")
            t_abs = os.path.normpath(os.path.join(root, t))
        else:
            t_abs = t
        m, w = scan_file(t_abs)
        all_mis.extend(m)
        all_warn.extend(w)

    print(f"verify_tickers · scanned {len(targets)} files")
    if all_warn:
        print(f"\n[WARN] {len(all_warn)} ticker not in truth DB (跑 init/resolve 先):")
        for w in all_warn[:15]:
            print(f"  - {w}")

    if all_mis:
        print(f"\n[FAIL] {len(all_mis)} MISMATCH(ES) — 阻止 commit:")
        for m in all_mis:
            print(f"  [FAIL]{m['file']}: {m['ticker']} 旁注 '{m['claimed_zh']}'")
            print(f"     truth name_zh: '{m['truth_zh']}'")
            print(f"     truth name_en: '{m['truth_en']}'")
        print(f"\n修复建议:")
        print(f"  1. 用 EODHD search 重核公司名 + ticker")
        print(f"  2. 如果 ticker 错 → 改 ticker;如果文件里中文名错 → 改中文名")
        print(f"  3. 重 commit")
        print(f"  4. 或者 bypass(不推荐):git commit --no-verify")
        return 1

    print("[PASS] all ticker/name pairs match ground truth")
    return 0


if __name__ == "__main__":
    sys.exit(main())
