#!/usr/bin/env python3
"""Build final _scan_semiconductors_CN_v1.json + _forward_picks_semiconductors_CN_v1.csv."""
import json, os, sys, csv, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "_scan_semiconductors_CN_raw.json")
OUT_JSON = os.path.join(HERE, "_scan_semiconductors_CN_v1.json")
OUT_CSV = os.path.join(HERE, "_forward_picks_semiconductors_CN_v1.csv")

SCAN_DATE = "2026-07-06"
THEME = "A股半导体"
TAG = "semiconductors"

NAMES = {
    "688126.SH": "沪硅产业", "605358.SH": "立昂微", "688233.SH": "神工股份",
    "300655.SZ": "晶瑞电材", "300346.SZ": "南大光电", "300666.SZ": "江丰电子",
    "300706.SZ": "阿石创", "002409.SZ": "雅克科技", "300054.SZ": "鼎龙股份",
    "688019.SH": "安集科技", "002371.SZ": "北方华创", "688012.SH": "中微公司",
    "688072.SH": "拓荆科技", "688120.SH": "华海清科", "688082.SH": "盛美上海",
    "688037.SH": "芯源微", "688147.SH": "微导纳米", "300567.SZ": "精测电子",
    "301269.SZ": "华大九天", "688521.SH": "芯原股份", "688206.SH": "概伦电子",
    "688981.SH": "中芯国际", "688347.SH": "华虹公司", "600460.SH": "士兰微",
    "688396.SH": "华润微", "300661.SZ": "圣邦股份", "688536.SH": "思瑞浦",
    "688798.SH": "艾为电子", "688052.SH": "纳芯微", "300782.SZ": "卓胜微",
    "002049.SZ": "紫光国微", "688385.SH": "复旦微电", "603501.SH": "豪威集团",
    "603986.SH": "兆易创新", "688008.SH": "澜起科技", "688608.SH": "恒玄科技",
    "603688.SH": "石英股份", "688268.SH": "华特气体", "603650.SH": "彤程新材",
    "688106.SH": "金宏气体", "688200.SH": "华峰测控", "688630.SH": "芯碁微装",
    "603005.SH": "晶方科技", "002156.SZ": "通富微电", "688519.SH": "南亚新材",
    "605111.SH": "新洁能", "603290.SH": "斯达半导", "688172.SH": "燕东微",
    "688596.SH": "正帆科技", "300623.SZ": "捷捷微电", "600584.SH": "长电科技"
}

LAYER = {
    # L1 upstream materials
    "688126.SH": "L1 上游材料", "605358.SH": "L1 上游材料", "688233.SH": "L1 上游材料",
    "300655.SZ": "L1 上游材料", "300346.SZ": "L1 上游材料", "300666.SZ": "L1 上游材料",
    "300706.SZ": "L1 上游材料", "002409.SZ": "L1 上游材料", "300054.SZ": "L1 上游材料",
    "688019.SH": "L1 上游材料", "603688.SH": "L1 上游材料", "688268.SH": "L1 上游材料",
    "603650.SH": "L1 上游材料", "688106.SH": "L1 上游材料", "688519.SH": "L1 上游材料",
    # L2 equipment/EDA/IP
    "002371.SZ": "L2 上游设备/EDA/IP", "688012.SH": "L2 上游设备/EDA/IP",
    "688072.SH": "L2 上游设备/EDA/IP", "688120.SH": "L2 上游设备/EDA/IP",
    "688082.SH": "L2 上游设备/EDA/IP", "688037.SH": "L2 上游设备/EDA/IP",
    "688147.SH": "L2 上游设备/EDA/IP", "300567.SZ": "L2 上游设备/EDA/IP",
    "688200.SH": "L2 上游设备/EDA/IP", "688630.SH": "L2 上游设备/EDA/IP",
    "688596.SH": "L2 上游设备/EDA/IP", "301269.SZ": "L2 上游设备/EDA/IP",
    "688521.SH": "L2 上游设备/EDA/IP", "688206.SH": "L2 上游设备/EDA/IP",
    # L3 foundry/IDM/OSAT
    "688981.SH": "L3 中游制造/Foundry-IDM", "688347.SH": "L3 中游制造/Foundry-IDM",
    "600460.SH": "L3 中游制造/Foundry-IDM", "688396.SH": "L3 中游制造/Foundry-IDM",
    "688172.SH": "L3 中游制造/Foundry-IDM", "603005.SH": "L3 中游制造/Foundry-IDM",
    "002156.SZ": "L3 中游制造/Foundry-IDM", "600584.SH": "L3 中游制造/Foundry-IDM",
    # L4 devices
    "300661.SZ": "L4 中游器件/芯片", "688536.SH": "L4 中游器件/芯片",
    "688798.SH": "L4 中游器件/芯片", "688052.SH": "L4 中游器件/芯片",
    "300782.SZ": "L4 中游器件/芯片", "002049.SZ": "L4 中游器件/芯片",
    "688385.SH": "L4 中游器件/芯片", "603290.SH": "L4 中游器件/芯片",
    "605111.SH": "L4 中游器件/芯片", "300623.SZ": "L4 中游器件/芯片",
    "603986.SH": "L4 中游器件/芯片",
    # L5 downstream reference
    "603501.SH": "L5 下游模块/参考", "688008.SH": "L5 下游模块/参考",
    "688608.SH": "L5 下游模块/参考"
}

ARCH = {
    "① 上游材料/衬底垄断": "materials/substrate monopoly",
    "② 单一来源卡脖子": "single-source choke",
    "③ 产能售罄/已锁定": "sold-out capacity",
    "④ 进每个设计的BOM/普适": "BOM-ubiquitous",
    "⑤ 估值对标套利": "valuation arbitrage",
    "⑥ 测试/设备瓶颈": "test/equipment bottleneck",
    "⑦ 冷门/前机构": "off-radar/pre-institutional",
    "⑧ 巨头依赖护城河": "giant-dependent moat",
    "⑨ 宏观错杀/二阶": "macro dislocation"
}

ARCH_BY_TICKER = {
    "688126.SH": ["① 上游材料/衬底垄断", "⑦ 冷门/前机构", "③ 产能售罄/已锁定"],
    "605358.SH": ["① 上游材料/衬底垄断", "④ 进每个设计的BOM/普适", "⑦ 冷门/前机构"],
    "688233.SH": ["① 上游材料/衬底垄断", "⑦ 冷门/前机构"],
    "300655.SZ": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "300346.SZ": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "300666.SZ": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "300706.SZ": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "002409.SZ": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑧ 巨头依赖护城河"],
    "300054.SZ": ["① 上游材料/衬底垄断", "④ 进每个设计的BOM/普适", "⑦ 冷门/前机构"],
    "688019.SH": ["① 上游材料/衬底垄断", "⑥ 测试/设备瓶颈", "⑦ 冷门/前机构"],
    "603688.SH": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "688268.SH": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "603650.SH": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "688106.SH": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "688519.SH": ["① 上游材料/衬底垄断", "④ 进每个设计的BOM/普适", "⑦ 冷门/前机构"],
    "002371.SZ": ["④ 进每个设计的BOM/普适", "⑥ 测试/设备瓶颈", "⑧ 巨头依赖护城河"],
    "688012.SH": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑧ 巨头依赖护城河"],
    "688072.SH": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑧ 巨头依赖护城河"],
    "688120.SH": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑧ 巨头依赖护城河"],
    "688082.SH": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑧ 巨头依赖护城河"],
    "688037.SH": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "688147.SH": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "300567.SZ": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "688200.SH": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "688630.SH": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "688596.SH": ["⑥ 测试/设备瓶颈", "④ 进每个设计的BOM/普适", "⑦ 冷门/前机构"],
    "301269.SZ": ["② 单一来源卡脖子", "⑦ 冷门/前机构", "① 上游材料/衬底垄断"],
    "688521.SH": ["② 单一来源卡脖子", "⑦ 冷门/前机构", "① 上游材料/衬底垄断"],
    "688206.SH": ["② 单一来源卡脖子", "⑦ 冷门/前机构", "① 上游材料/衬底垄断"],
    "688981.SH": ["⑧ 巨头依赖护城河", "③ 产能售罄/已锁定", "④ 进每个设计的BOM/普适"],
    "688347.SH": ["⑧ 巨头依赖护城河", "③ 产能售罄/已锁定", "④ 进每个设计的BOM/普适"],
    "600460.SH": ["④ 进每个设计的BOM/普适", "⑧ 巨头依赖护城河"],
    "688396.SH": ["④ 进每个设计的BOM/普适", "⑧ 巨头依赖护城河"],
    "688172.SH": ["④ 进每个设计的BOM/普适", "⑦ 冷门/前机构"],
    "603005.SH": ["⑥ 测试/设备瓶颈", "③ 产能售罄/已锁定", "⑦ 冷门/前机构"],
    "002156.SZ": ["⑥ 测试/设备瓶颈", "⑧ 巨头依赖护城河"],
    "600584.SH": ["⑥ 测试/设备瓶颈", "⑧ 巨头依赖护城河"],
    "300661.SZ": ["④ 进每个设计的BOM/普适", "⑧ 巨头依赖护城河"],
    "688536.SH": ["④ 进每个设计的BOM/普适", "⑧ 巨头依赖护城河"],
    "688798.SH": ["④ 进每个设计的BOM/普适", "⑦ 冷门/前机构"],
    "688052.SH": ["④ 进每个设计的BOM/普适", "⑧ 巨头依赖护城河"],
    "300782.SZ": ["④ 进每个设计的BOM/普适", "⑨ 宏观错杀/二阶"],
    "002049.SZ": ["② 单一来源卡脖子", "⑧ 巨头依赖护城河"],
    "688385.SH": ["② 单一来源卡脖子", "⑦ 冷门/前机构"],
    "603290.SH": ["④ 进每个设计的BOM/普适", "⑧ 巨头依赖护城河"],
    "605111.SH": ["④ 进每个设计的BOM/普适", "⑦ 冷门/前机构"],
    "300623.SZ": ["④ 进每个设计的BOM/普适", "⑦ 冷门/前机构"],
    "603986.SH": ["④ 进每个设计的BOM/普适", "⑧ 巨头依赖护城河"],
    "603501.SH": ["⑧ 巨头依赖护城河", "⑨ 宏观错杀/二阶"],
    "688008.SH": ["⑧ 巨头依赖护城河", "⑨ 宏观错杀/二阶"],
    "688608.SH": ["⑧ 巨头依赖护城河", "⑨ 宏观错杀/二阶"]
}

RATING_OVERRIDE = {
    "603501.SH": "🔴",   # 韦尔/CIS 下游参照
    "603986.SH": "🔴",   # 兆易 NOR/MCU，记忆体主题单独覆盖
    "688008.SH": "🔴",   # 澜起 内存接口，记忆体主题单独覆盖
    "688608.SH": "🔴",   # 恒玄 智能音频SoC 下游参照
    "688126.SH": "🟢",
    "605358.SH": "🟢",
    "300655.SZ": "🟢",
    "300346.SZ": "🟢",
    "688019.SH": "🟢",
    "300706.SZ": "🟢",
    "688106.SH": "🟢",
    "688521.SH": "🟢",
    "603005.SH": "🟢",
    "300623.SZ": "🟢",
    "603290.SH": "🟢",
    "688385.SH": "🟢"
}

def rating(sym, p):
    if sym in RATING_OVERRIDE:
        return RATING_OVERRIDE[sym]
    layer = LAYER.get(sym, "")
    stage = p.get("stage", "")
    if "L5" in layer:
        return "🔴"
    if "L1" in layer:
        if ("extended" in stage or p.get("ret_3m_pct", 0) > 120 or p.get("range_pos_6mo_pct", 0) >= 85):
            return "🟡"
        return "🟢"
    if "L4" in layer and sym in ("300661.SZ", "688536.SH", "688798.SH", "688052.SH", "300782.SZ", "002049.SZ", "605111.SH"):
        return "🟡"
    return "🟡"

# Manual thesis / risk / invalidation for top picks
MANUAL = {
    "688126.SH": {
        "risk": "扩产折旧压制毛利率，12寸正片客户认证进度若慢于预期，库存减值风险；当前PE因亏损无法计算，估值靠PS/政策预期支撑。",
        "thesis": "国产300mm大硅片龙头，上海+太原产能向85万片/月爬坡，目标120万片/月；晶圆厂扩产+供应链本土化双重锁定，是最上游衬底垄断型瓶颈。",
        "invalidation": "跌破6个月区间中位（约¥30）且1月动量转负；或公司公告12寸正片大客户认证显著推迟。",
        "catalyst": "大基金三期/地方国资落地、12寸硅片批量出货、中芯/华虹等晶圆厂扩产招标。"
    },
    "605358.SH": {
        "risk": "硅片价格周期触底回升但产能过剩隐忧仍存，功率半导体业务景气波动；资产负债率偏高，扩产资本开支大。",
        "thesis": "8/12寸硅片+功率器件双轮驱动，硅片业务进入一线晶圆厂供应链；相较沪硅估值更下沉，是上游材料中市值更小的替代标的。",
        "invalidation": "跌破¥50且3月动量回落至0以下；或功率器件订单连续两季度下滑。",
        "catalyst": "硅片提价、功率IDM产能利用率回升、12寸客户认证通过。"
    },
    "300655.SZ": {
        "risk": "KrF/ArF光刻胶量产进度若慢于日韩对手，高纯化学品价格战拖累毛利；锂电材料等非半导体业务稀释纯度。",
        "thesis": "国内半导体光刻胶+高纯湿电子化学品龙头，G5级双氧水/硫酸本土唯一量产，直接受益于晶圆厂耗材国产替代。",
        "invalidation": "跌破¥16且1月动量转负；或光刻胶收入占比连续两个季度下降。",
        "catalyst": "KrF光刻胶批量导入、高纯化学品订单放量、大基金三期材料子基金落地。"
    },
    "300346.SZ": {
        "risk": "ArF光刻胶仍处客户验证阶段，放量时点不确定；MO源业务增速放缓，估值（forward PE 307x）已透支乐观预期。",
        "thesis": "国内少数实现ArF光刻胶量产并导入中芯国际/长江存储的企业，同时是特种气体（磷烷/砷烷）龙头，双重卡脖子环节。",
        "invalidation": "跌破¥65且1月动量转负；或ArF光刻胶验证进度公告延后。",
        "catalyst": "ArF光刻胶通过更多客户验证、特气新产能投产。"
    },
    "688019.SH": {
        "risk": "海外Cabot/日立等降价保份额，先进制程抛光液验证周期长；当前估值（PE ~80x）已反映较高预期。",
        "thesis": "国产CMP抛光液龙头，中国大陆市占率本土第一，晶圆厂 steps 增加+耗材复购使收入可预测；是前道材料中壁垒最深的环节之一。",
        "invalidation": "跌破¥240且1月动量转负；或连续两季度毛利率下滑。",
        "catalyst": "12寸逻辑/存储客户份额提升、抛光垫等新耗材放量。"
    },
    "300706.SZ": {
        "risk": "公司规模小、产品以PVD靶材为主，溅射靶材认证壁垒高，若下游面板/光伏需求走弱将拖累收入。",
        "thesis": "国产溅射靶材小龙头，半导体靶材逐步导入，市值小、覆盖少，是上游材料中典型冷门标的。",
        "invalidation": "跌破¥55且1月动量转负；或半导体靶材收入占比未见提升。",
        "catalyst": "半导体靶材通过头部晶圆厂认证、面板/光伏订单回暖。"
    },
    "688106.SH": {
        "risk": "电子特气业务占比仍有限，工业气体价格竞争激烈；大客户集中度高，新产能爬坡若慢将压制利润。",
        "thesis": "本土综合气体供应商，电子特气（超纯氨、硅烷等）进入半导体产线，受益于晶圆厂耗材本土化与现场制气模式。",
        "invalidation": "跌破¥30且1月动量转负；或电子特气收入连续两季度负增长。",
        "catalyst": "电子特气新签长单、现场制气项目投产。"
    },
    "688521.SH": {
        "risk": "IP授权收入波动大，毛利率虽高但客户流片的不确定性大；亏损状态，估值缺乏PE锚。",
        "thesis": "国内领先的芯片IP与一站式定制平台，Chiplet/AI推理芯片IP需求上升；在A股稀缺的IP资产，具备单源卡脖子属性。",
        "invalidation": "跌破¥240且1月动量转负；或季度授权收入同比转负。",
        "catalyst": "Chiplet客户授权落地、AI芯片设计服务订单增长。"
    },
    "603005.SH": {
        "risk": "封测行业产能过剩、价格竞争激烈，先进封装收入占比仍低；市值小但流动性一般。",
        "thesis": "WLCSP/TSV先进封装小龙头，受益于AI手机/汽车传感器封装需求，是后道设备-工艺瓶颈中的冷门标的。",
        "invalidation": "跌破¥36且1月动量转负；或先进封装收入占比下滑。",
        "catalyst": "CIS/滤波器封装订单放量、先进封装产能爬坡。"
    },
    "300623.SZ": {
        "risk": "功率分立器件行业价格战，IGBT/碳化硅替代传统晶闸管；公司规模较小，研发追赶压力大。",
        "thesis": "国产晶闸管/防护器件龙头，汽车/光伏/工控BOM普适性强，估值相对可控，是功率半导体中的小而美标的。",
        "invalidation": "跌破¥32且1月动量转负；或功率器件毛利率连续两季度下滑。",
        "catalyst": "汽车电子订单增长、功率器件提价。"
    },
    "603290.SH": {
        "risk": "IGBT模块价格下行，新能源汽车需求增速放缓；海外英飞凌/安森美降价竞争。",
        "thesis": "国内IGBT模块龙头，新能源车主驱/光伏逆变器核心供应商，国产替代空间大，BOM普适性高。",
        "invalidation": "跌破¥110且1月动量转负；或新能源车用IGBT订单连续下滑。",
        "catalyst": "800V高压平台IGBT/SiC模块放量、海外客户突破。"
    },
    "688385.SH": {
        "risk": "FPGA研发周期长、生态壁垒高，高端产品仍落后赛灵思/Altera；军工需求波动影响高可靠FPGA订单。",
        "thesis": "国产FPGA/安全芯片龙头，高可靠领域市占率领先，是数字芯片中少数具备单源卡脖子属性的标的。",
        "invalidation": "跌破¥55且1月动量转负；或FPGA新品发布不及预期。",
        "catalyst": "高端FPGA量产、安全芯片订单放量。"
    }
}

BUSINESS = {
    "688126.SH": "300mm半导体硅片国产龙头",
    "605358.SH": "硅片+功率器件双主业",
    "688233.SH": "单晶硅材料/硅零部件",
    "300655.SZ": "光刻胶+高纯湿电子化学品",
    "300346.SZ": "ArF光刻胶+MO源/电子特气",
    "300666.SZ": "高纯金属溅射靶材",
    "300706.SZ": "PVD镀膜材料/溅射靶材",
    "002409.SZ": "半导体前驱体/电子特气/LDS材料",
    "300054.SZ": "CMP抛光垫+打印复印耗材",
    "688019.SH": "CMP抛光液/清洗液",
    "603688.SH": "高纯石英材料（坩埚/光纤）",
    "688268.SH": "电子特种气体",
    "603650.SH": "半导体光刻胶+酚醛树脂",
    "688106.SH": "电子特气+工业气体",
    "688519.SH": "覆铜板/IC载板基材",
    "002371.SZ": "平台型半导体设备龙头",
    "688012.SH": "等离子体刻蚀设备",
    "688072.SH": "薄膜沉积设备（PECVD/SACVD/ALD）",
    "688120.SH": "CMP设备",
    "688082.SH": "清洗/电镀/炉管设备",
    "688037.SH": "涂胶显影设备",
    "688147.SH": "ALD/光伏/半导体设备",
    "300567.SZ": "半导体检测设备",
    "688200.SH": "模拟/混合信号测试机",
    "688630.SH": "直写光刻设备",
    "688596.SH": "工艺介质供应系统+电子特气",
    "301269.SZ": "EDA工具",
    "688521.SH": "芯片IP/一站式芯片定制",
    "688206.SH": "EDA/IP与设计服务",
    "688981.SH": "晶圆代工龙头",
    "688347.SH": "特色工艺晶圆代工",
    "600460.SH": "功率IDM",
    "688396.SH": "功率半导体IDM",
    "688172.SH": "模拟IC/功率IDM",
    "603005.SH": "WLCSP先进封装",
    "002156.SZ": "封测/先进封装",
    "600584.SH": "封测龙头",
    "300661.SZ": "模拟IC",
    "688536.SH": "模拟/信号链IC",
    "688798.SH": "数模混合/音频/电源管理IC",
    "688052.SH": "模拟/隔离/接口IC",
    "300782.SZ": "射频前端芯片",
    "002049.SZ": "FPGA/安全芯片",
    "688385.SH": "FPGA/安全芯片",
    "603290.SH": "IGBT模块",
    "605111.SH": "MOSFET/功率器件",
    "300623.SZ": "晶闸管/防护器件",
    "603986.SH": "NOR Flash/MCU",
    "603501.SH": "CIS图像传感器",
    "688008.SH": "内存接口芯片",
    "688608.SH": "智能音频SoC"
}

def default_text(sym, p, v, rat):
    name = NAMES[sym]
    layer = LAYER[sym]
    business = BUSINESS[sym]
    stage = p.get("stage","")
    extended = "extended" in stage
    neutral = "neutral" in stage or "downtrend" in stage
    pe = v.get("trailing_pe") or v.get("forward_pe")
    pe_str = f"PE(TTM/forward) {pe:.1f}x" if pe else "PE缺失/亏损"
    risk = f"[{business}]面临下游景气波动、技术迭代及海外巨头降价竞争；{pe_str}，估值对周期恢复预期较敏感。"
    if extended:
        risk += f"股价处于6月区间高位（{p['range_pos_6mo_pct']}%），近3月涨幅{p['ret_3m_pct']}%已透支部分乐观预期，追高风险大。"
    elif neutral:
        risk += f"股价动能偏弱（近3月{p['ret_3m_pct']}%），若行业订单无改善可能继续跑输板块。"
    else:
        risk += f"股价已反弹但尚未严重超买（距6月高点{p['pct_off_6mo_high']}%），需警惕大盘/板块回调。"
    thesis = f"{name}主营{business}，位于{layer}，属于半导体供应链中的国产替代/瓶颈环节；"
    if "L1" in layer:
        thesis += "晶圆厂扩产+耗材本土化是确定性的资本开支方向，认证通过后订单粘性强。"
    elif "L2" in layer:
        thesis += "设备国产替代率低、海外供应受限，本土设备商订单可见度高。"
    elif "L3" in layer:
        thesis += "晶圆制造/封测是产能瓶颈本身，扩产周期长、政府与产业资本必须持续投入。"
    elif "L4" in layer:
        thesis += "模拟/功率/射频器件BOM普适，国产替代与下游新能源/汽车电子化提供长期需求。"
    else:
        thesis += "作为下游参照，验证终端需求强度，非本次主攻标的。"
    inv = f"跌破¥{p['last']*0.9:.1f}且1月动量转负；或行业订单/毛利率连续两季度低于预期。"
    cat = ""
    if "L1" in layer:
        cat = "晶圆厂扩产招标、国产材料认证通过、大基金三期投向材料/设备。"
    elif "L2" in layer:
        cat = "晶圆厂设备招标、海外设备禁令升级、国产替代订单公告。"
    elif "L3" in layer:
        cat = "晶圆厂产能利用率回升、封测景气拐点、政府产业基金落地。"
    elif "L4" in layer:
        cat = "下游新能源/汽车电子需求回暖、产品线涨价/订单公告。"
    else:
        cat = "终端新品周期、下游去库存结束。"
    return risk, thesis, inv, cat

def target_range(p):
    lo = round(p["last"]*1.05, 2)
    hi = p["high_6mo"]
    if lo >= hi:
        hi = round(p["last"]*1.12, 2)
    return f"¥{lo}–¥{hi}"

def time_frame(rating, layer):
    if rating == "🟢":
        return "3–6个月"
    if "L1" in layer or "L2" in layer:
        return "3–6个月（等回调或催化剂落地）"
    return "6–12个月"

def gates(sym, p, v, rating):
    layer = LAYER[sym]
    true_bottleneck = "PASS"
    if "L1" in layer or "L2" in layer:
        true_bottleneck = "PASS"
    elif "L3" in layer and sym not in ["600584.SH","002156.SZ","603005.SH"]:
        true_bottleneck = "HALF-PASS（制造端壁垒高但巨头集中）"
    elif "L4" in layer:
        true_bottleneck = "HALF-PASS（器件竞争较充分，靠BOM普适）"
    else:
        true_bottleneck = "FAIL（下游/参考标）"
    pre_inst = "PASS"
    if sym in ["002371.SZ","688012.SH","688981.SH","688347.SH","600584.SH","603501.SH","603986.SH","688008.SH"]:
        pre_inst = "HALF-PASS（机构覆盖度高）"
    if sym in ["688608.SH"]:
        pre_inst = "PASS"
    cheap = "HALF-PASS"
    if v.get("trailing_pe") and v["trailing_pe"] < 60:
        cheap = "PASS（估值相对可控）"
    if v.get("eps_growth") and v["eps_growth"] < -50:
        cheap = "FAIL（盈利仍在恶化）"
    if p["range_pos_6mo_pct"] >= 85 or p.get("ret_3m_pct",0) > 120:
        cheap = "FAIL（价格已大幅透支）"
    if rating == "🔴":
        cheap = "FAIL（非主攻方向/估值透支）"
    return {
        "true_bottleneck": true_bottleneck,
        "pre_institutional": pre_inst,
        "cheap_derisked": cheap
    }

with open(RAW, "r", encoding="utf-8") as f:
    raw = json.load(f)

by_ticker = {r["ticker"]: r for r in raw if "error" not in r}
errors = [r for r in raw if "error" in r]

candidates = []
for sym, p in by_ticker.items():
    name = NAMES.get(sym, sym)
    layer = LAYER.get(sym, "未知")
    v = p.pop("valuation")
    rat = rating(sym, p)
    man = MANUAL.get(sym)
    if man:
        risk, thesis, inv, cat = man["risk"], man["thesis"], man["invalidation"], man.get("catalyst","")
    else:
        risk, thesis, inv, cat = default_text(sym, p, v, rat)
    entry = p["last"]
    tr = target_range(p)
    tf = time_frame(rat, layer)
    note = f"{BUSINESS.get(sym,'')} | stage={p.get('stage','')} | 距6月高点{p.get('pct_off_6mo_high')}%"
    cand = {
        "ticker": sym,
        "name": name,
        "layer": layer,
        "archetype_hits": ARCH_BY_TICKER.get(sym, []),
        "rating": rat,
        "price": p,
        "valuation": v,
        "gates": gates(sym, p, v, rat),
        "thesis": thesis,
        "risk": risk,
        "invalidation": inv,
        "catalyst": cat,
        "target_range": tr,
        "time_frame": tf,
        "notes": note
    }
    candidates.append(cand)

player_census = [
    {"name": "沪硅产业", "ticker": "688126.SH", "exchange": "SSE STAR", "status": "covered", "note": "国产300mm大硅片龙头"},
    {"name": "立昂微", "ticker": "605358.SH", "exchange": "SSE Main", "status": "covered", "note": "硅片+功率IDM"},
    {"name": "神工股份", "ticker": "688233.SH", "exchange": "SSE STAR", "status": "covered", "note": "单晶硅材料/硅零部件"},
    {"name": "晶瑞电材", "ticker": "300655.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "光刻胶+高纯化学品"},
    {"name": "南大光电", "ticker": "300346.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "ArF光刻胶+电子特气"},
    {"name": "江丰电子", "ticker": "300666.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "高纯溅射靶材"},
    {"name": "阿石创", "ticker": "300706.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "溅射靶材/PVD材料"},
    {"name": "雅克科技", "ticker": "002409.SZ", "exchange": "SZSE Main", "status": "covered", "note": "前驱体/电子特气"},
    {"name": "鼎龙股份", "ticker": "300054.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "CMP抛光垫+打印耗材"},
    {"name": "安集科技", "ticker": "688019.SH", "exchange": "SSE STAR", "status": "covered", "note": "CMP抛光液"},
    {"name": "北方华创", "ticker": "002371.SZ", "exchange": "SZSE Main", "status": "covered", "note": "平台型设备龙头"},
    {"name": "中微公司", "ticker": "688012.SH", "exchange": "SSE STAR", "status": "covered", "note": "刻蚀设备"},
    {"name": "拓荆科技", "ticker": "688072.SH", "exchange": "SSE STAR", "status": "covered", "note": "薄膜沉积设备"},
    {"name": "华海清科", "ticker": "688120.SH", "exchange": "SSE STAR", "status": "covered", "note": "CMP设备"},
    {"name": "盛美上海", "ticker": "688082.SH", "exchange": "SSE STAR", "status": "covered", "note": "清洗/电镀/炉管设备"},
    {"name": "芯源微", "ticker": "688037.SH", "exchange": "SSE STAR", "status": "covered", "note": "涂胶显影设备"},
    {"name": "微导纳米", "ticker": "688147.SH", "exchange": "SSE STAR", "status": "covered", "note": "ALD/光伏半导体设备"},
    {"name": "精测电子", "ticker": "300567.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "半导体检测设备"},
    {"name": "华大九天", "ticker": "301269.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "EDA"},
    {"name": "芯原股份", "ticker": "688521.SH", "exchange": "SSE STAR", "status": "covered", "note": "芯片IP"},
    {"name": "概伦电子", "ticker": "688206.SH", "exchange": "SSE STAR", "status": "covered", "note": "EDA"},
    {"name": "中芯国际", "ticker": "688981.SH", "exchange": "SSE STAR", "status": "covered", "note": "晶圆代工"},
    {"name": "华虹公司", "ticker": "688347.SH", "exchange": "SSE STAR", "status": "covered", "note": "特色工艺代工"},
    {"name": "士兰微", "ticker": "600460.SH", "exchange": "SSE Main", "status": "covered", "note": "功率IDM"},
    {"name": "华润微", "ticker": "688396.SH", "exchange": "SSE STAR", "status": "covered", "note": "功率IDM"},
    {"name": "圣邦股份", "ticker": "300661.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "模拟IC"},
    {"name": "思瑞浦", "ticker": "688536.SH", "exchange": "SSE STAR", "status": "covered", "note": "模拟/信号链"},
    {"name": "艾为电子", "ticker": "688798.SH", "exchange": "SSE STAR", "status": "covered", "note": "数模混合/音频/电源"},
    {"name": "纳芯微", "ticker": "688052.SH", "exchange": "SSE STAR", "status": "covered", "note": "模拟/隔离/接口"},
    {"name": "卓胜微", "ticker": "300782.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "射频前端"},
    {"name": "紫光国微", "ticker": "002049.SZ", "exchange": "SZSE Main", "status": "covered", "note": "FPGA/安全芯片"},
    {"name": "复旦微电", "ticker": "688385.SH", "exchange": "SSE STAR", "status": "covered", "note": "FPGA/安全芯片"},
    {"name": "豪威集团(韦尔)", "ticker": "603501.SH", "exchange": "SSE Main", "status": "covered", "note": "CIS，下游参考"},
    {"name": "兆易创新", "ticker": "603986.SH", "exchange": "SSE Main", "status": "covered", "note": "NOR Flash/MCU，记忆体主题单独覆盖"},
    {"name": "澜起科技", "ticker": "688008.SH", "exchange": "SSE STAR", "status": "covered", "note": "内存接口，记忆体主题单独覆盖"},
    {"name": "恒玄科技", "ticker": "688608.SH", "exchange": "SSE STAR", "status": "covered", "note": "智能音频SoC，下游参考"},
    {"name": "石英股份", "ticker": "603688.SH", "exchange": "SSE Main", "status": "covered", "note": "高纯石英材料"},
    {"name": "华特气体", "ticker": "688268.SH", "exchange": "SSE STAR", "status": "covered", "note": "电子特气"},
    {"name": "彤程新材", "ticker": "603650.SH", "exchange": "SSE Main", "status": "covered", "note": "半导体光刻胶"},
    {"name": "金宏气体", "ticker": "688106.SH", "exchange": "SSE STAR", "status": "covered", "note": "电子特气+工业气体"},
    {"name": "华峰测控", "ticker": "688200.SH", "exchange": "SSE STAR", "status": "covered", "note": "半导体测试机"},
    {"name": "芯碁微装", "ticker": "688630.SH", "exchange": "SSE STAR", "status": "covered", "note": "直写光刻设备"},
    {"name": "晶方科技", "ticker": "603005.SH", "exchange": "SSE Main", "status": "covered", "note": "先进封装"},
    {"name": "通富微电", "ticker": "002156.SZ", "exchange": "SZSE Main", "status": "covered", "note": "封测/先进封装"},
    {"name": "南亚新材", "ticker": "688519.SH", "exchange": "SSE STAR", "status": "covered", "note": "覆铜板/IC载板基材"},
    {"name": "新洁能", "ticker": "605111.SH", "exchange": "SSE Main", "status": "covered", "note": "MOSFET/功率器件"},
    {"name": "斯达半导", "ticker": "603290.SH", "exchange": "SSE Main", "status": "covered", "note": "IGBT模块"},
    {"name": "燕东微", "ticker": "688172.SH", "exchange": "SSE STAR", "status": "covered", "note": "模拟/功率IDM"},
    {"name": "正帆科技", "ticker": "688596.SH", "exchange": "SSE STAR", "status": "covered", "note": "工艺介质系统+电子特气"},
    {"name": "捷捷微电", "ticker": "300623.SZ", "exchange": "SZSE ChiNext", "status": "covered", "note": "晶闸管/防护器件"},
    {"name": "长电科技", "ticker": "600584.SH", "exchange": "SSE Main", "status": "covered", "note": "封测龙头"},
    {"name": "Shin-Etsu", "ticker": "4063.T", "exchange": "TSE", "status": "global", "note": "全球硅片寡头"},
    {"name": "SUMCO", "ticker": "3436.T", "exchange": "TSE", "status": "global", "note": "全球硅片寡头"},
    {"name": "Siltronic", "ticker": "GlobalWafers收购", "exchange": "-", "status": "acquired", "note": "2022年被环球晶圆收购"},
    {"name": "JSR/Tokyo Ohka Kogyo", "ticker": "-", "exchange": "TSE", "status": "global", "note": "光刻胶全球龙头"},
    {"name": "Entegris", "ticker": "ENTG.US", "exchange": "NASDAQ", "status": "global", "note": "CMP/化学品/材料"},
    {"name": "Cabot Microelectronics", "ticker": "CCMP.US->ENTG", "exchange": "NASDAQ", "status": "acquired", "note": "CMP材料，被Entegris收购"},
    {"name": "Applied Materials/Lam/TEL/KLA", "ticker": "-", "exchange": "US/JP", "status": "global", "note": "前道设备全球寡头"},
    {"name": "ASML", "ticker": "ASML.US/ASML.NA", "exchange": "US/Europe", "status": "global", "note": "EUV光刻机单源"},
    {"name": "Synopsys/Cadence/Siemens EDA", "ticker": "SNPS.US/CDNS.US", "exchange": "NASDAQ", "status": "global", "note": "EDA跨主题root节点"},
    {"name": "Tower Semiconductor", "ticker": "TSEM.US", "exchange": "NASDAQ", "status": "global", "note": "特色工艺代工"},
    {"name": "昂瑞微/芯驰/兆易旗下思立微等", "ticker": "-", "exchange": "private/subsidiary", "status": "private", "note": "部分射频/模拟/汽车芯片仍处非上市或部门状态，缺乏干净纯play"}
]

supply_chain_map = {
    "cross_theme_root": ["ARM", "Synopsys (SNPS.US)", "Cadence (CDNS.US)"],
    "layers": [
        {
            "layer": "L1 上游材料",
            "focus": "硅片、特种气体/化学品、光刻胶、CMP耗材、靶材、高纯石英、IC载板基材",
            "bottleneck_archetypes": ["① 上游材料/衬底垄断", "② 单一来源卡脖子", "⑦ 冷门/前机构"],
            "tickers": [k for k,v in LAYER.items() if v=="L1 上游材料"]
        },
        {
            "layer": "L2 上游设备/EDA/IP",
            "focus": "刻蚀、沉积、CMP、清洗、检测、涂胶显影、直写光刻、测试机、EDA、IP",
            "bottleneck_archetypes": ["⑥ 测试/设备瓶颈", "② 单一来源卡脖子", "⑧ 巨头依赖护城河"],
            "tickers": [k for k,v in LAYER.items() if v=="L2 上游设备/EDA/IP"]
        },
        {
            "layer": "L3 中游制造/Foundry-IDM/OSAT",
            "focus": "晶圆代工、功率/模拟IDM、先进封装/OSAT",
            "bottleneck_archetypes": ["③ 产能售罄/已锁定", "⑧ 巨头依赖护城河", "④ 进每个设计的BOM/普适"],
            "tickers": [k for k,v in LAYER.items() if v=="L3 中游制造/Foundry-IDM"]
        },
        {
            "layer": "L4 中游器件/芯片",
            "focus": "模拟、功率、MCU、射频、FPGA、安全芯片",
            "bottleneck_archetypes": ["④ 进每个设计的BOM/普适", "⑧ 巨头依赖护城河", "② 单一来源卡脖子"],
            "tickers": [k for k,v in LAYER.items() if v=="L4 中游器件/芯片"]
        },
        {
            "layer": "L5 下游模块/参考",
            "focus": "CIS、智能音频SoC、存储接口等终端/模组，仅作参照",
            "bottleneck_archetypes": ["⑨ 宏观错杀/二阶"],
            "tickers": [k for k,v in LAYER.items() if v=="L5 下游模块/参考"]
        }
    ],
    "key_bottleneck_layers": ["L1 上游材料", "L2 上游设备/EDA/IP"]
}

output = {
    "theme_tag": TAG,
    "theme_name": THEME,
    "scope": "Broad A-share semiconductor supply chain. Focus upstream bottleneck layers: silicon wafers, specialty gases/chemicals, CMP slurries, targets, photoresist, EDA/IP, front-end equipment, advanced packaging materials/equipment, analog/power/RF discretes, MCU, foundry/IDM. Avoid duplicating pure memory/storage players.",
    "scan_date": SCAN_DATE,
    "data_source": "Tushare via scripts/price.py (default qfq); valuation() from Tushare/akshare/yfinance fallback",
    "capex_certainty": "美国对华半导体设备/材料管制持续收紧，中国政府大基金三期（3440亿元）及地方国资明确投向设备、材料、零部件等‘卡脖子’环节；国内晶圆厂（中芯、华虹、长存、长鑫等）扩产是确定的长期资本开支。钱必须花在上游材料与设备的国产替代上。",
    "supply_chain_map": supply_chain_map,
    "player_census": player_census,
    "candidates": candidates
}

if errors:
    output["data_errors"] = errors

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# CSV only 🟢/🟡
with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["theme","ticker","name","rating","entry_price","target_range","time_frame","invalidation","catalyst","notes","scan_date"])
    for c in candidates:
        if c["rating"] in ("🟢","🟡"):
            w.writerow([
                THEME, c["ticker"], c["name"], c["rating"],
                c["price"]["last"], c["target_range"], c["time_frame"],
                c["invalidation"], c["catalyst"], c["notes"], SCAN_DATE
            ])

print(f"JSON: {OUT_JSON}")
print(f"CSV: {OUT_CSV}")
print(f"candidates={len(candidates)}, errors={len(errors)}")
print("rating counts:", {r: sum(1 for c in candidates if c["rating"]==r) for r in "🟢🟡🔴"})
