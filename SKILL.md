---
name: serenity-bottleneck-hunter
description: 给定一个投资主题/趋势,复用交易者 Serenity(@aleabitoreddit)的"供应链瓶颈逆向映射"方法论,独立挖出被市场忽视的上游瓶颈股(而非分析他已喊过的标的)。当用户给出一个主题(如"AI 数据中心电力""人形机器人""HBM 内存")并想要候选标的+论证时使用。仅供研究教育,非投资建议。
---

# Serenity Bottleneck Hunter

把一个**投资主题**转成一份**被忽视的上游瓶颈候选股名单 + 论证 + 目标价/时间框架**。核心不是抄 Serenity 的票,而是**复用他的逻辑去选新股**。

## 何时用
- 用户给出一个主题/趋势,想要"沿这个方向能买什么"。
- 用户给一个上游环节/材料,想找对应的瓶颈公司。
- ❌ 不要用于:已知标的的纯财务分析、抄作业式"他买了啥"。

## 核心理念
> 逆向拆解供应链,在机构与分析师发现之前,埋伏那个**无人察觉的上游瓶颈**,用催化剂兑现。
> alpha 来自"**早于机构发现主题**",不是抄到最低点。

---

## 工作流(7 步)

**Step 1 · 确认资本开支确定性**
这个主题的钱为什么"一定"会花?规模、周期多长?需求确定性 > 个股故事性。先归类:这是 **Bottleneck(瓶颈)/ Disruption(颠覆)/ Evolution(演进)**?(本 skill 主攻 Bottleneck)
- **标明需求来源**:政府/国防(NASA、SDA、NRO…节奏慢、看订单与预算周期)还是商业(超大规模厂商 capex…节奏快)?二者的估值锚与择时节奏不同,后面 Step 6/7 要据此调整。

**Step 2 · 逆向拆链 + 广扫纪律(5 层产业链 + 跨主题 root + 可选第 6 层独有 IP)**
列出 **5 层** 从下游到上游:**下游对照 → 中游系统 → 中游器件 → 上游设备 → 上游材料/代工**。**跳过人人都盯的下游龙头**。
- **必做"广扫供应商"**:除最上游材料层外,**单独再搜一轮**该主题的"子系统/器件/卖铲子供应商"(如航天的太阳能阵/星敏感器厂)。否则会漏掉④原型的标的——教训:首跑商业航天就漏了 Redwire(ROSA 太阳能阵/星敏感器)。
- **广扫颗粒度纪律**:必须覆盖**5 层产业链**——上游材料/代工 → 上游设备 → 中游器件 → 中游系统 → 下游对照,**每层至少 2-3 个标的**。避免"上游只看到 1 个就停"。**广扫不到位 ≠ 板块没机会**——800VDC v1 只扫 6 只就判"全 extended",v2 扩到 15 只立刻挖出 STM。
- **跨主题 root 节点纪律(2026-06-02 用户反馈驱动 — IP/EDA 分层冗余暴露)**:**ARM / CDNS / SNPS 不再画在每个主题的产业链层里**,而是放在 chain-viz 上方独立的**"跨主题 root"小 section**,显示一次。理由:这三家是**所有芯片设计驱动主题共用的根**(EDA 双寡头 + ARM IP 单源),在 7 份历史报告里 100% 重复 = 信息熵 = 0。
  - **报告 chain-viz 上方加 cross-theme root 卡片**(独立 section,跨主题节点,标 ⭐⭐):
    ```
    <div class="cross-theme-root">
      <span class="label">跨主题 root(芯片设计驱动主题共用)</span>
      ARM ⭐⭐ + CDNS ⭐⭐ + SNPS ⭐⭐
    </div>
    ```
  - **链接到** `tracking/cross_theme_index_snapshot.csv` — 它们的 ⭐⭐ 状态是 cross-theme 计算结果,不再每个主题重画。
- **可选第 6 层 · "主题独有 IP/EDA 玩家"(仅当主题真有独立玩家)**:
  - **自动驾驶 L4** → 真有独立 IP:**MBLY**(Mobileye,IP 授权给 BMW/Audi/Geely)— 必须画
  - **个人 AI PC** → ARM 在 PC 是**真单源**(Apple M + Qualcomm Snapdragon X + AMD AI300)— 保留画在产业链顶层 + 标本主题真单源(不仅是 cross-theme)
  - **AI Agent / 物理 AI / AMR** → 无独立 IP 玩家 → **chain-viz 不画第 6 层**,在 root section 提一次即可
  - **MLCC / 800VDC / 商业航天** → 不依赖芯片设计,**完全跳过** IP/EDA(已有先例,继续保持)
  - **凑数禁令**:**没有真独立玩家的主题不强制画第 6 层** — IP/EDA 是 optional,不是 mandatory。**只有真存在主题独有玩家 + 该玩家在产业链有真瓶颈角色** 才画。
- **穷尽性纪律(A 项,2026-06-01 用户反馈驱动,候选数集中 20+ 是隐性 stopping rule 而非穷尽广扫)**:每个主题开扫前,**必须先列"已知玩家全集"**(全球+全市场,涵盖上市/私有/被并购),然后**逐一显式标记**:`covered`(已纳入候选)/ `private`(私有公司,跳过 + 原因)/ `acquired`(已被收购,标合并实体)/ `delisted`(已退市)/ `untracked`(EODHD/yfinance 都无数据)。**不允许"默认遗漏"**——例:自动驾驶 L4 LiDAR 玩家全集 = Hesai/Luminar/Innoviz/Aeva/Ouster/Velodyne(已合并 OUST)/Cepton(被 KOEL 收)/Innovusion(被尼欧买)/Quanergy(破产)/RoboSense(港股)/Hesai 速腾 = **必须显式列全 + 标记**,不允许"我扫了 5 家就够了"。这个清单写在报告底部的"私有公司诚实跳过"区块或独立"已知玩家全集 audit"块。
- **A+ 工具化兜底 · ETF 持仓 audit(2026-06-02,Dogfood #10 漏 PANW/CRWD/RBRK 教训驱动)**:**A 项"凭记忆列全集"不够**——会漏 PANW、CRWD、FTNT、RBRK 这种主仓玩家(Dogfood #10 美股 AI Agent 真实漏标:34 只里漏 34 只,covered 率只有 50%)。**修复机制(强制)**:每个新主题开 forward_picks 扫描前,**必须先跑** `python scripts/theme_etf_coverage.py --etfs <ETF1>,<ETF2>,... --theme "<主题名>"`,工具会:
  1. 从 stockanalysis.com 拉每个主题 ETF 的 top 25 持仓
  2. 合并 dedupe → 主题已知玩家全集
  3. 跟 forward_picks 已覆盖清单做 diff
  4. 输出 `tracking/_etf_audit_<theme>.json` audit log
  → LLM 对每只 new candidate **必须人工判定** 产业链层 + Serenity 原型 + 是否纳入。**top 25 持仓 100% 必须 audit**(主仓占总权重 >70%,小权重是 me-too 通常 ok 跳过)。
  - **主题 ETF 映射(2026-06-02 维护)**:
    - AI Agent / SaaS / Software → `IGV` (iShares Software) + `WCLD` (WisdomTree Cloud) + `AIQ` (Global X AI)
    - 网络安全 → `CIBR` (First Trust Cyber) + `BUG` (Global X Cyber) + `HACK` (ETFMG)
    - 半导体 → `SOXX` (iShares Semi) + `SMH` (VanEck Semi) + `PSI`
    - AI 算力/GPU → `AIQ` + `BOTZ` (Global X Robotics&AI)
    - 网络/算力基础设施 → `WCLD` + `CLOU` + `SKYY`
    - 物理 AI 机器人 → `BOTZ` + `ROBO` (RoboGlobal) + `IRBO`
    - 自动驾驶 → `DRIV` (Global X AV) + `IDRV` (iShares AV)
    - 电网/能源 → `GRID` (First Trust SmartGrid) + `XLU` + `URNM`
    - 清洁能源/电气化 → `ICLN` + `LIT` + `KARS`
    - 国防/航天 → `ITA` (iShares Aerospace) + `XAR` + `UFO`
    - 5G / 通信 → `FIVG` + `NXTG`
    - 数据中心 / 算力 → `DTCR` + `CLOU` + `SRVR`
  - **报告 audit section 必须列**:① 用到的 ETF 清单 + ② ETF top 持仓全集数量 + ③ covered / private / 跳过原因的逐一分类 + ④ ETF coverage 百分比(covered / ETF 全集)。**< 80% 必须诚实标"穷尽性纪律未达标"**。
  - **教训档案 — Dogfood #10 漏标 case**:原仅扫 ZS,漏 PANW(IGV 主仓 7.38% / CIBR 主仓 10.23%)、CRWD(IGV 6.07% / CIBR 10.66%)、FTNT(CIBR 8.83%)、RBRK(CIBR 1.88%)等 34 只。其中 **CHKP**(rng31/off-30%/1m+21%) 和 **FICO**(rng42/off-31%/1m+24%) 是真正漏掉的 Mode A 候选,其余 32 只都已抛物线 ext 不变结论。**纪律失败的代价是隐性的:这次只漏 2 个 Mode A 候选,下次可能漏的就是该主题的整个 thesis**。
- **A++ ticker 双向验证纪律(2026-06-05,Dogfood #12 绿的谐波错标 教训驱动)**:**广扫前必须用 EODHD search 反查"代码 → 公司名"双向验证**——A 项穷尽 + A+ ETF audit 都不防"错标"(标对了公司名但 ticker 错对应另一家公司)。**修复机制(强制)**:每个新主题广扫前,对每只候选必须做 ticker 验证:
  ```bash
  curl "https://eodhd.com/api/search/<COMPANY_NAME>?api_token=$KEY&fmt=json"
  curl "https://eodhd.com/api/search/<TICKER>?api_token=$KEY&fmt=json"
  ```
  → 比对两次返回的 `Name` 字段必须一致。**禁止凭记忆写 ticker** — 哪怕"我很确定是这个代码"也必须 search 一遍。**A 股容易踩坑**:6 开头(沪市主板)/ 0 开头(深市)/ 3 开头(创业板)/ 688 开头(科创板)/ 002 开头(中小板)的代码段交叉,同 5 位数字可能出现在不同板块对应不同公司。
  - **教训档案 — Dogfood #12 绿的谐波错标 case**:v3 物理 AI 报告里 4 处用 **603297.SHG** 当成"绿的谐波"(谐波减速器),但 603297 实际是 **永新光学(宁波永新)**。真绿的谐波(Leader Harmonious Drive)代码是 **688017.SHG**(科创板)。错位影响:
    - 价格:误用 ¥123.74(永新)代替 ¥327.50(真绿的)
    - stage:误判"rng49 早期 mid"(永新真状态)代替"rng77 已抛物线"(真绿的)
    - 推荐反向:原报告说"等回 rng<30 再看"(基于永新数据),真实 688017 已 1m+42%/3m+55% 抛物线 — Mode A 窗口早已过,**完全 reverse 判定**
    - **核心错误成因**:中文公司名"绿的谐波"凭记忆写代码时 → 与永新光学的代码 603297 同样是 6 开头沪市主板 → LLM 训练数据混淆
  - **强制流程**:任何 A 股新候选,广扫前必须 EODHD search 验证一次,验证通过才写入 _scan_*.py。**只要一次错标可能让整个主题的 thesis 反向**。
- **私有公司检查 + 诚实跳过纪律(2026-06-01 加,物理 AI dogfood 教训)**:每个主题都会有"真单源/真瓶颈但是私有公司或子部门"的标的(如物理 AI 的六维力传感器:坤维/字节灵犀/宇立 — 全私;鼎智科技:北交所 EODHD 不支持)。**禁止为了"凑标的"硬塞一个不纯/不可投的公司当候选**;**应在报告里显式列出"已识别但跳过"的瓶颈+原因**,这本身就是高密度信号(让读者知道"这层是真瓶颈但没法投")。例:物理 AI 报告底部列了"六维力 / 触觉皮肤:都是私有 → 跳过;鼎智:北交所 EODHD 不支持 → 跳过"。**坦诚标"无干净纯 play"比硬凑标的更有价值**。
- **主题边界声明纪律(2026-06-01 加,物理 AI scope 教训)**:跑大类主题(如"物理 AI" / "AI 算力" / "能源转型")时,**报告顶部必须明确界定本期主题边界**——这些大类下通常有 3+ 个供应链特征差异显著的子领域(物理 AI 含人形机器人/自动驾驶/AMR/无人机/手术等),**不要默认覆盖全部**,而是显式说"本期聚焦 X 子领域,其他子领域(Y / Z)作为独立专题分批跑"。否则用户期待与实际产出 mismatch。物理 AI 主题 v1 已踩坑:默认"物理 AI = 人形机器人",未声明边界。**报告命名格式**:`<大类>_<子领域>_完整分析报告.html`(如 `物理AI_人形机器人专题_完整分析报告.html`)。
- **公司状态检查纪律(2026-06-12 加,Dogfood #16 SKYT+SPCX 双教训;原"被收购检查",06-13 扩为双向)**:写入判定前,每只候选(含链路图里的非候选节点)**查一次当前公司状态**:收购/被收购/私有化/**IPO/上市**/退市/破产重组(新闻搜 "<公司名> acquisition/IPO/merger" 即可)。两个方向的真实翻车:
  - **上市→被收走**:SkyWater(美国唯一上市受信 rad-hard 代工,教科书级 ①②⑦)2026-01 被 IonQ 宣布 $35/股收购,瓶颈逻辑瞬间不可投。收购中标的一律 🔴 剔除并注明——被收购反向验证选股方向(战略买家与本框架看上同一个瓶颈),记进报告当佐证;小盘纯 play(FEIM/KRMN 级别)天然是并购标的,持仓者应把"被收购溢价/折价"列入情景。
  - **私有→已上市**:SpaceX 2026-06-12 NASDAQ IPO(SPCX,$1.75T,史上最大)——而 Dogfood #16 报告当天仍标它"私有不可投"。**LLM 对"某某是私有公司"的先验是训练数据的快照,极易过期**;凡在报告里写"私有 / 不可投 / 无纯 play"这类**状态性断言,必须当场搜一次验证**,并在 company_desc 里把状态写进带日期的 status 字段(不是静态 business 字段——这正是 business/status 拆分纪律存在的原因)。

**Step 3 · 对每层套「9 大瓶颈原型」**(详见 `reference/supply-chain-and-archetypes.md` Part D):
①上游材料/衬底垄断 ②单一来源卡脖子 ③产能售罄/已锁定=去风险 ④进每个设计的BOM/普适 ⑤估值对标套利 ⑥测试/设备瓶颈 ⑦冷门/前机构 ⑧巨头依赖护城河 ⑨宏观二阶/错杀。
命中原型越多的环节,越是猎区。

**Step 4 · 产出候选(偏上游、冷门、小市值)**
每个环节挑 1-3 家最纯正的公司。优先:小市值、卖方覆盖少、散户没听过(原型⑦)。用 `search` 校验代码与上市地(含海外)。
- **别只押"最上游材料咽喉(①②)"**:也要纳入"普适器件/卖铲子供应商(④)"——两档都列,避免选股偏科。
- **最纯的瓶颈常在海外/OTC**(如 5N Plus 在 TSX、Umicore 在布鲁塞尔)→ 主动去海外交易所找,并注明流动性/准入限制。
- **若瓶颈落在私有公司、或大公司的一个部门**(如 AZUR 在 5N+ 内、SolAero 在 RKLB 内、Spectrolab 在 Boeing 内、rad-hard 纯 play VORAGO 私有)→ 必须给"暴露路径":买含该业务的母公司(说明稀释/纯度),或如实标注"无干净纯 play、跳过"。**不要硬凑一个不纯的标的来充数。**
- **跨主题节点检查(强制,2026-06-01 加,对应 Serenity ⑤跨 capex cycle 原型)**:产出候选后立即跑 `python tracking/cross_theme_scan.py`,把当前候选名单与历史 `forward_picks.csv` 对照 ——
  - 同一只 symbol 同时出现在 ≥2 个主题 = **⭐**;≥3 个 = **⭐⭐**(罕见,真"非线性定价权")。
  - **档位过滤防止巨头摊薄误标**:中游系统/下游对照/反面参照不计入;中游卖铲子档必须有 ④ 普适才计入(避免 STM/NVDA/Vertiv 因业务摊薄被假高亮)。
  - ⭐ 节点在 Step 5"前机构"闸门**自动加分**(被多个 capex cycle 同时驱动 = 即使有机构覆盖,产能压力是叠加的、仍可能 mispriced)。
  - 已验证案例(2026-06-01 首测):**AEHR.US 跨光子学 + 800VDC 双主题** = ⭐(都是上游设备 ⑥⑤,跨 capex cycle 真实存在)。
  - **eodhd_symbol 规范**:美股一律带 `.US` 后缀(`AEHR.US` 而非 `AEHR`),否则脚本无法匹配同一只。

**Step 5 · 三道闸门逐一检验**
- 🔒 真瓶颈:产能受限/有定价权/短期无法绕过("别人能 1-2 年内绕过吗?")
- 👁️ 前机构:卖方研报少、机构持仓低、市值小;**⭐ 跨主题节点自动加分**(被多个 capex 同时锁定 = 即使有机构覆盖也仍可能 mispriced)
- 💰 便宜+已去风险:估值压抑 + 产能/订单锁定或现金充足

**Step 6 · 入场时机(★ 见下方两套模式,别搞错)**

**Step 7 · 出报告**(生成**单文件 HTML 报告**,用下方"输出模板(HTML)" + `reference/report_template.html`,含目标价+时间框架+风险+免责声明)

---

## 入场时机:两套模式(经价格回测校准,勿混用)

| 模式 | 适用 | 触发 |
|---|---|---|
| **A 主题瓶颈长线**(本 skill 默认) | 主题里的上游瓶颈股 | **主题刚点燃 + 早期上行/突破 + 仍前机构就进,主动放弃抄底。等回调=踏空。** |
| **B 波段超跌反弹** | 成熟大票的非实质性错杀 | 买恐慌回调(增发/稀释类实质利空则回避) |

回测依据(11 只光子学标的):首call时多在前6月区间 **86%-237% 高位**入场,之后 **2-6 个月 +150%~+1100%**(中位 ~+277%)。→ **早于主题、容忍不抄底**才是 alpha 来源。

**强制**用 `scripts/price.py` 拉真实价格数据(provider 自动回退:**EODHD(`EODHD_API_KEY`)优先 → yfinance 兜底**),输出 6 月区间位置、距高点、近 1/3 月动量、stage 标签。**严禁用 WebSearch 抓价格、严禁凭印象猜"差不多 early/extended"**——猜测视为流程错误。海外股(欧股/台股等)若 yfinance 拿不到,**让用户提供 EODHD key 或换可解析代码后重跑,不要降级为定性**。
- **广扫批量拉价格必须走 price.py 接口(2026-06-01 加,用户挑战驱动)**:不允许用 PowerShell 直接 `Invoke-RestMethod` 调 EODHD API,**会绕过 yfinance fallback**——这是真实犯过的错(物理 AI 主题 v1 报告漏 4 只日股,因为 EODHD 不支持 .T 后缀,我用 inline EODHD 调用没触发 fallback)。**正确方式**:`python -c "from scripts.price import analyze; print(analyze('6324.T'))"`(走 EODHD→yfinance 完整链)或在脚本里 `from scripts.price import fetch_history`。批量场景写小 wrapper 脚本,**禁止 inline API**。
- **报告内所有数字必须 100% 来自 price.py 输出,严禁手填/猜数(2026-06-02 加,用户抓错驱动)**:`price.py analyze()` 返回 6 个字段(`last / range_pos_6mo_pct / pct_off_6mo_high / ret_1m_pct / ret_3m_pct / above_sma50 / stage`),报告显示**任一数字**必须从这里来。**真实犯过的错(2026-06-02 dogfood #7+#8)**:9 个标的的 `off_6mo_high` 数字被手填错(HSAI 写 -89%、真实 -35.6%;海康写 -77%、真实 -19% 等),根本原因是 PowerShell 输出里我只复制了 `rng/1m/3m`,**off% 没记录就手填了"看着合理的大数字"**。修复机制:批量 scan 脚本输出**必须包含 off_high**,并保留完整 PowerShell 输出 log;forward_picks 写入前对 9 个字段做完整 verify。**手填任何数字都是流程错误**。

---

## 输出模板(HTML)

> **交付物 = 一个自包含的 HTML 文件**(单文件、样式内联,仅 Google Fonts 可外链 CDN;**不再交付 .md 报告**)。写到项目的 `reports/<主题>_分析报告.html`。**骨架与配色直接复用 `reference/report_template.html`**(机构研究简报风格:可读性优先、语义化三档配色、动量条)。生成后用 `Start-Process <file>.html`(Win)/ `open`(mac)打开供用户查看。

**报告必含区块(对应 7 步,所有项都是 hard rule 不允许跳过):**
1. **页眉 + 一句话结论**:主题 | 资本开支确定性 | 类别(Bottleneck/Disruption/Evolution) | 数据截止日 | 价格源 | 免责。
2. **Step1 资本开支确定性**:为什么钱一定花 + 需求来源(政府/商业)。
3. **核心发现 callout**:最该被先看到的那句(瓶颈在哪层、有没有干净纯 play)。
4. **⚠ Step2 逆向拆链(网状视图)— 强制必含,不允许跳过(C 项,2026-06-01 用户挑战驱动)**:历史教训 — 自动驾驶 L4 / AMR 两份报告漏了这一区块,导致报告残缺。**禁止以"前面已经画过类似的"为由跳过**,每个子主题供应链都不同。**用 `.chain-viz` 容器,6 层 `.chain-layer`:IP/EDA → 上游材料/代工 → 上游设备 → 中游器件 → 中游系统 → 下游对照(D 项升级到 6 层)**。每层用 `.cnode[data-id=...]`(data-id 与 `forward_picks` 一致的 eodhd_symbol;美股带 `.US`)。供货关系写在 `.edge-list` 里(`data-from / data-to / data-weight` 三档),JS 自动画 SVG 曲线 + 判定瓶颈点。跨主题节点加 `<span class="star-inline">⭐</span>`(跨 3 加 ⭐⭐,跨 5+ 加 ⭐⭐⁵)。骨架照搬 `reference/report_template.html`。
5. **候选 leaderboard(B 项:与 forward_picks 入库解耦,2026-06-01 用户反馈驱动)**:
   - **leaderboard 显示 top 15-20**(按"决策相关性"排序:🟢 优先、跨主题 ⭐ 节点优先、stage 健康优先,**不需要完整列全**;超过的折叠成"其他 N 只 → 见 forward_picks.csv")
   - **forward_picks 入库无上限**:广扫到的所有候选(含 🟢🟡🔴 三档)都必须入库,**不允许"为了 leaderboard 视觉舒服而漏入库"**
   - **上游咽喉(①②③)** 与 **中游卖铲子(④⑧)** 分两档;**按 stage 排序**(early/basing-momentum 在前、extended 在后)。每只必含字段:
     - 代码+现价 · 档位/是什么 · 瓶颈逻辑(命中原型#) · 估值/增长 + **稀释红旗**(亏损+ATM/增发+现金跑道短=标红) · **动量条**(6 月区间位置 + 1m/3m,颜色=stage) · **三档判定 🟢/🟡/🔴** · **目标价/时间框架** · **重估触发条件(🟡 必填)** · 风险 · **`.why` 块**(20-40 字人话:它实际做什么、为什么是瓶颈)。
6. **Step5 三道闸门**:🔒真瓶颈 / 👁️前机构 / 💰便宜去风险,逐关诚实打分(过/半过/不过)。
7. **跨主题信号区块**:把当前主题命中的 ⭐ 节点列出(来自 `tracking/cross_theme_index_snapshot.csv`)。
8. **已知玩家全集 audit 块(A 项,穷尽性,2026-06-01)**:列出该主题全球+全市场已知玩家,**显式标 covered / private / acquired / delisted / untracked**。不允许默认遗漏。
9. **落地结论 + 数据备注 + 免责页脚**。
10. **底部 glossary 折叠速查表**(JS 自动从 abbr 抽取)。

- **目标价/时间框架**写法:给**情景区间 + 时间框**。⚠️ **基准率随主题而变,切勿套用光子学的数字**:高 beta、快速点燃的主题(如光子学,历史约 2-6 个月 +150~1000%)与慢周期、政府/国防驱动、低 beta 的主题(如商业航天、电网,可能是 1-3 年 +30~150%)完全不同。按**当前主题的 beta 与催化剂节奏**自行设定,并显式标注"情景非承诺、有幸存者偏差"。
- **三档判定 + trigger 条件**(替代老的"排除清单"):每只候选必标 🟢/🟡/🔴;🟡 必须配可量化的重估触发条件。详见 methodology.md §7。
- **三档分级表(代替老的"排除清单",见 methodology.md §7)**:把所有评估过的标的分到 🟢 候选 / 🟡 暂时观望 / 🔴 永久排除 三档。
  - 🟡 **必填"重估触发条件"**——写清楚价格点 / 财报指标 / 公司动作 / 政策事件,什么时候会重新评估。
  - 🔴 **极度克制**:只用于商业模式作假 / 欺诈 / 业务死亡 / 个人原则(中国军技)。**严禁"历史事件式硬排除"**——如"曾经重组"、"曾经增发过"、"1m 涨太多"都不算永久排除理由,前两个是过期信息,第三个是 stage 问题(降 🟡 等回调)。
  - 例:`$WOLF` 不应因"重组后旧股东归零"被永久排除——重组后是 NewCo,业务/瓶颈逻辑可独立评估;**正确处理**:🟡 观望,trigger 条件 = "回到 $X 以下 + 下季度营收/产能数据"。
- **可读性纪律(用户明确要求)**:语义化三档配色(🟢green / 🟡amber / 🔴red)、动量条让"谁已抛物线"一眼可见、表格/卡片清爽、留白充足。
- **术语友好度纪律(2026-06-01 加,用户反馈"很多专业缩写读得一知半解")**:报告必须做 3 件事:
  1. **顶部加"30 秒看懂这个主题"区块**(150-220 字大白话,对完全不熟主题的读者解释"这个主题在解决什么问题、关键瓶颈在哪")。位置:hero verdict 之后、Step 1 之前。class 用 `.thirty-sec`。
  2. **每个 🟢/🟡 候选行加"为什么重要"一行**(20-40 字人话,讲它实际做什么、为什么是瓶颈)。位置:`.nmcell .d` 之下加 `.why` 块。例:`AMKR(它就像 SoC 的"组装工厂":TSMC 做完芯片晶圆,AMKR 把芯片裸片切下贴到基板上)`。
  3. **专业缩写第一次出现用 `<abbr title="{中文解释}">{缩写}</abbr>` 包裹**;术语来源是 `reference/glossary.md`(预填 120+ 条);**若 glossary 没有的新术语**,**LLM 必须先 append 到 glossary.md 对应分类,再回报告使用**(策略 C 改良:宁滥勿缺,允许膨胀)。
  4. **报告底部加 `<details class="glossary-section">` 折叠速查表**(默认折叠);JS 自动从本报告所有 `<abbr title>` 抽取条目生成,无需 LLM 手动维护两份。

**页脚必带**:⚠️ 仅供研究教育,非投资建议;估值为网页研究近似值需复核;微盘/诉讼/海外标的风险极高。

---

## 数据来源与边界

- **价格/动量(择时)**:统一走 `scripts/price.py`,provider 自动回退:**① EODHD**(若 `EODHD_API_KEY` 已设,全球覆盖最佳、海外股推荐)→ **② yfinance**(无 key,美股 OK、海外股常 gap)→ **③ 两者都失败 = 报错退出**。Key 从环境变量读、不硬编码。**WebSearch 仅用于公司基本面/定性研究,不用于抓价格**。
- **EODHD 取不到**:❌ fundamentals(估值/增长/毛利率/市值)、❌ screener、❌ 财报日历 → 这些用 **网页研究**逐只补(财报、财经站、IR)。
- **瓶颈/单源/产能/客户**等定性判断:靠财报+行业资料+新闻研究。

## 参考文件
- `reference/methodology.md` —— 完整方法论(理念、筛选清单、两套择时、回避清单、风险)
- `reference/supply-chain-and-archetypes.md` —— 元框架、CPO/硅光产业链速查表、**Part D 9 大瓶颈原型库**、EODHD 数据映射
- `reference/report_template.html` —— **HTML 报告骨架 + 配色模板**(交付物按此生成,见"输出模板(HTML)")
- `reference/example_commercial_space.md` —— worked example(商业航天),**示范分析内容与颗粒度**(报告格式以 HTML 模板为准)
- `reference/glossary.md` —— **术语库**(120+ 条预填,LLM 自动 enrich);所有报告的 `<abbr>` 注释来源,新术语必须先 append 再用
- `reference/company_desc.md` —— **公司业务描述库**(2026-06-02 加,用户挑战 driven 3 次迭代):**只存 business**(主营/产业链位置/技术/客户)— **严禁包含 price/stage/跨主题数/市值/估值** 等动态数据。
  - **格式**:`- **SYM.EX** [YYYY-MM-DD] = 业务描述...`(每条 entry 必带 last_updated 时间戳)
  - **拆分纪律 v2(2026-06-02 第 2 次重构)**:
    - 🟢 **business(本文件 + `.cnode[data-desc=]`)**:相对稳定但**非永久** — 加 last_updated 时间戳
    - 🔴 **status(`.cnode[data-status=]`)**:price/stage/跨主题/估值 — 每次重写,带 `[YYYY-MM-DD]`
  - **Cache invalidation 纪律 v3(2026-06-02 第 3 次重构,用户反馈"业务重点也会变化")**:LLM 用 data-desc 前**必查 last_updated**:
    - **≤ 90 天** → 直接复用(信任 business 描述未漂移)
    - **> 90 天** → **必须重新评估**(查最新公司战略 / 财报 / 业务调整),若有重大变化则 update business 描述 + bump 时间戳;若无变化则只 bump 时间戳到当前日期
    - 工具:`tracking/check_desc_freshness.py` 跑一遍输出过期 entry 列表
  - **HTML hover tooltip 2 段**:business(上,无日期)+ status(下,带日期)。
  - 维护:每跑新主题 → 检查 freshness → 必要时 update business → append 新标的 business → 报告里写 status。
- `tracking/forward_picks.csv` + `tracking/score_tracker.py` —— 向前(样本外)跟踪表 + EODHD 打分脚本
- `tracking/cross_theme_scan.py` + `tracking/cross_theme_index_snapshot.csv` —— **跨主题节点扫描**(Step 4 末尾强制跑)+ 最近一次快照

## 验证状态(诚实说明)
- **逻辑自洽性(已做,非业绩回测)**:套到他研究过的"AI 光子学"能重建其名单(AXTI/SIVE/LITE/TSEM/SOI/IQE/AEHR…);套到他没碰过的"AI 电力散热"能独立挖出 $CLF(GOES 电工钢独家)、$CC(浸没冷却液单源);套到"商业航天"能挖出 $VNP/5N+(西方锗/镓/铟 + AZUR 空间太阳能,China 出口管制)、$MTRN(铍近垄断)。→ 说明"拆链 + 原型"逻辑能指向真实瓶颈公司。
- **⚠️ 这不是业绩回测**:此前"光子学首 call 后 +X%"的数字存在**选股循环论证(用已知赢家倒推)、幸存者偏差、峰值未来函数(假设卖在事后最高点)**,**不能当作收益预期**。
- **唯一可信的是向前(样本外)验证**:对本 skill 当下产出的候选,记录"建议日 + 当时价 + 事先定死的进出场规则",日后用 EODHD 客观打分。结论出来前,输出只当**研究线索**,不是业绩。
  → 已落地:`tracking/forward_picks.csv`(种子=商业航天+A股半导体候选,带记录日/入场价/stage/判定)+ `tracking/score_tracker.py`(日后 `EODHD_API_KEY=… python score_tracker.py` 重拉价、算入场以来涨跌、并检验"别追"纪律是否有效)。**每次用 skill 出新候选,都应追加进这张表。**
