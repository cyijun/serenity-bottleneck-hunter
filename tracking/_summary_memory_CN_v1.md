# Serenity Bottleneck-Hunter Scan Summary — A股存储芯片 (memory)

**Scan date:** 2026-07-06  
**Scope:** DRAM、NAND Flash、NOR Flash、存储模组（SSD/eMMC/UFS）、存储主控/MCU、HBM相关先进封装，以及存储晶圆厂专用的上游材料/设备（前驱体、光刻胶、靶材、CMP、清洗/刻蚀/沉积）。

---

## Theme-scope + capital-expenditure certainty

AI服务器、AI手机/PC与国产算力三重需求叠加，全球HBM与DDR5进入结构性短缺；国内长鑫存储（CXMT）拟科创板IPO并持续扩产，长江存储（YMTC）NAND产能爬坡，**存储晶圆厂与先进封装环节的资本开支在未来2–3年具有高度确定性**[网络检索:富途牛牛2026-07-01][网络检索:与非网2026-01-21]。无论终端品牌如何竞争，前驱体/CMP耗材/光刻胶/刻蚀沉积设备/先进封装的订单都会被强制拉动——这是“必须花的钱”。

---

## Key bottleneck layers identified

1. **L5 上游材料与化学品** — 前驱体、CMP抛光液/垫、光刻胶认证周期长（2–3年）、客户粘性极强，是存储/HBM扩产中供给弹性最小的环节。代表：雅克科技、安集科技、鼎龙股份、南大光电。
2. **L3 先进封装** — HBM/2.5D/3D堆叠依赖TSV、CoWoS类封装，产能紧张且扩产周期长，是当前产业链最硬瓶颈之一[网络检索:雪球2026-02-15][网络检索:东方财富2025-10-27]。代表：通富微电、长电科技、深科技、华天科技、晶方科技。

---

## Top 3 🟢 candidates

| Ticker | Name | Bottleneck logic | Last price / Stage | Target range | Invalidation |
|--------|------|------------------|--------------------|--------------|--------------|
| **603005.SH** | 晶方科技 | 晶圆级封装/TSV小盘龙头，受益存储/CIS/WLCSP国产替代；市值小、机构覆盖低，股价相对板块滞涨。 | 42.59 / early-uptrend (1m -7.0%, off 6mo high -22.9%) | 51–58 | 收盘价跌破39元或Q2营收环比下滑 |
| **688019.SH** | 安集科技 | 国产CMP抛光液龙头，长鑫/长江存储扩产核心耗材；认证壁垒高、复购属性强，股价尚未进入板块主升浪。 | 289.35 / early-uptrend (3m +50.6%, fwd PE 82.8x) | 350–400 | 长鑫/长江存储扩产延期，或丢失关键制程验证 |
| **688008.SH** | 澜起科技 | 全球DDR5/HBM内存接口芯片核心供应商，HBM4E接口已送样[网络检索:雪球2025-10-31]；服务器内存升级+国产算力替代双重驱动。 | 268.68 / early-uptrend (off high -19.3%, fwd PE 145.95x) | 320–370 | 核心客户平台延期或市场份额被Renesas/Inphi侵蚀 |

---

## 3 🟡 watchlist + re-evaluation triggers

| Ticker | Name | Why watch | Re-evaluation trigger |
|--------|------|-----------|----------------------|
| **002185.SZ** | 华天科技 | 三线封测中估值最低、PEG仅0.14，先进封装产能持续爬坡。 | 2.5D/HBM产线投产+毛利率环比提升；跌破17元则剔除 |
| **002156.SZ** | 通富微电 | AMD核心封测伙伴，国内HBM/2.5D技术领先；近1月横盘整理，未进入最癫狂阶段。 | HBM样品量产或国产算力客户导入；跌破60元支撑则降级 |
| **688110.SH** | 东芯股份 | 利基型存储（SLC NAND/NOR/DRAM）小盘设计商，利润刚扭亏，机构覆盖低。 | Q2净利润环比继续上行+毛利率维持30%以上；业绩miss则剔除 |

---

## Biggest theme-level risk / bear case

**存储价格周期逆转与国产HBM进度不及预期。** 当前板块已充分定价“存储超级周期”与“国产HBM突破”两大叙事，多数龙头3个月涨幅超过100%。若AI服务器需求放缓、DRAM/NAND合约价回落，或长鑫HBM量产/良率爬坡显著慢于预期，估值与业绩双杀将首先冲击高PE、高弹性的设备与材料龙头。此外，美国对华半导体设备/材料限制升级可能打断国产替代节奏，使“必须花的钱”被迫延迟。

---

## Methodology note

- 所有价格/动量字段来自 `python scripts/price.py <TICKER>`（默认前复权 qfq，未覆盖 TUSHARE_ADJ）。
- 估值字段来自 `python -c "from scripts.price import valuation; valuation('<TICKER>')"`（优先 Tushare，来源标注为 `tushare`）。
- 目标区间基于瓶颈稀缺性与技术验证节奏[推断]，非精确DCF；请在触发invalidation时果断止损。
