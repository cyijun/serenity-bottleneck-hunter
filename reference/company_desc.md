# Company Desc — 公司业务描述库(永久可复用)

> **设计原则(2026-06-02 用户挑战驱动)**:本文件只存 **business 描述**(主营/产业链位置/技术/客户),**严禁包含 price/stage/跨主题数/市值/估值** 等动态数据 — 后者每月都变,会过期或误导。
>
> **拆分对照**:
> - 🟢 **business 描述(本文件,static)**:5 年不变的事实 — 公司是干啥的、在产业链什么位置、关键技术、主要客户
> - 🔴 **status 描述(dynamic,每份报告 LLM 现写,带日期标签)**:price/stage/跨主题数/估值/动量 — 报告生成时刻的快照,过期就过期
>
> 在 `.cnode` 里:
> - `data-desc="<business 静态>"` — 从本文件取
> - `data-status="<dynamic 动态>[YYYY-MM-DD]"` — LLM 每次报告时写,带日期
>
> HTML hover tooltip 同时显示两段:business(上,无日期)+ status(下,带日期)
>
> **维护**:每跑新主题,LLM 检查 company_desc.md,若标的没收录 → **必须先 append business 描述**(只写永久部分),再回报告写 data-status。

---

## IP / EDA / 标准

- **ARM.US** [2026-06-02] = ARM Holdings,英国芯片 IP 授权龙头。设计 CPU/GPU/NPU 架构授权给 SoC 厂(高通/苹果/NVDA Grace 都基于 ARM)。每片 ARM-based SoC 必交版税。
- **CDNS.US** [2026-06-02] = Cadence Design Systems,EDA(芯片设计软件)双寡头之一。SoC/ASIC 设计必用,与 Synopsys 双寡头垄断。
- **SNPS.US** [2026-06-02] = Synopsys,EDA 另一寡头(与 Cadence 并列)。设计自动化工具 + IP 核库,所有先进制程 SoC 设计必用。

## 半导体 / 上游材料

- **STM.US** [2026-06-02] = STMicroelectronics,欧洲半导体综合龙头(法意合资)。SiC 功率器件 + MEMS 传感器领先,汽车 + 800V 电源主供。
- **WOLF.US** [2026-06-02] = Wolfspeed,美国 SiC 衬底+器件公司。150mm → 200mm 转产中。
- **XFAB.PA** [2026-06-02] = X-FAB Silicon Foundries,欧洲半导体代工厂。美国 Commerce 点名的高产能 SiC 代工,EU + US CHIPS Act 双背书。
- **ON.US** [2026-06-02] = onsemi(安森美),美国 SiC 综合大厂。自家 fab + Treo 800V 汽车平台。
- **IFX.DE** [2026-06-02] = Infineon Technologies,德国功率半导体大厂。SiC + GaN 综合,与 NVDA 联合开发 800V 电源。
- **MPWR.US** [2026-06-02] = Monolithic Power Systems,美国高效 PMIC 电源管理芯片厂。专注高效率 buck/boost/LDO,服务数据中心 + AI PC + 机器人 + 车载电源。
- **MU.US** [2026-06-02] = Micron Technology,美国 DRAM/NAND/HBM 三大件存储厂。LPDDR5X / HBM 主要供应商之一。
- **TSM.US** [2026-06-02] = 台积电,全球最大芯片代工。InFO/SoIC/CoWoS 先进封装主导,2nm 制程领先。
- **NVDA.US** [2026-06-02] = NVIDIA,AI GPU 主流(H100/Blackwell/Rubin)。Drive Thor 自动驾驶 + NIM/Jetson 物理 AI 平台。
- **AVGO.US** [2026-06-02] = Broadcom,半导体 + 软件综合大厂。定制 ASIC(代工 Google TPU)+ 网络芯片龙头。
- **AMD.US** [2026-06-02] = Advanced Micro Devices,Ryzen CPU + Radeon GPU + MI300X AI 加速器。Ryzen AI 300 是 AI PC SoC。
- **INTC.US** [2026-06-02] = Intel,x86 CPU 巨头。Lunar Lake / Panther Lake 是 AI PC NPU SoC 主流之一。
- **QCOM.US** [2026-06-02] = Qualcomm,Snapdragon 移动 SoC 龙头。Snapdragon X Elite/Plus 是 ARM 阵营 AI PC 旗舰。

## 半导体 / 上游设备

- **AEHR.US** [2026-06-02] = AEHR Test Systems,SiC 功率器件 burn-in 老化测试设备小盘。跨光子学 + 800VDC 测试。
- **0522.HK** [2026-06-02] = ASMPT,先进封装设备(TCB 热压键合)主供。CoWoS 等 2.5D/3D 封装核心装备。
- **ONTO.US** [2026-06-02] = Onto Innovation,先进封装/AI 衬底计量设备公司。封装产能扩张必用其测量设备。
- **AMAT.US** [2026-06-02] = Applied Materials,半导体设备综合大厂(沉积/刻蚀/CMP/计量)。
- **AMKR.US** [2026-06-02] = Amkor Technology,全球封装代工厂(ASE 之后第 2)。CoWoS 等先进封装的核心合作伙伴。
- **0522.HK** [2026-06-02] = ASMPT 同上。
- **TRMB.US** [2026-06-02] = Trimble Inc,高精度 GNSS + 测绘综合大厂。业务覆盖自动驾驶 + 农业 + 建筑测量。
- **HXGBY.US** [2026-06-02] = Hexagon AB ADR(瑞典),测绘 + 工业自动化综合。
- **RSW.LSE** [2026-06-02] = Renishaw,英国高精度编码器全球龙头。业务覆盖医疗 + 工业 + 航天。

## MLCC / 被动元件

- **300285.SHE** [2026-06-02] = 国瓷材料,A 股 MLCC 介质粉(钛酸钡)主要供应商。中国市场份额领先,服务三星电机等。
- **605376.SHG** [2026-06-02] = 博迁新材,纳米镍粉(MLCC 内电极材料)技术领先。
- **4078.T** [2026-06-02] = Sakai Chemical,日本钛酸钡领先供应商,水热法工艺。
- **002859.SHE** [2026-06-02] = 洁美科技,MLCC 离型膜 / 载带 国产替代领跑。
- **KN.US** [2026-06-02] = Knowles Corporation,美股特种高可靠陶瓷电容(医疗/国防/半导设备用)。MLCC 细分领域。
- **VSH.US** [2026-06-02] = Vishay Intertechnology,被动元件综合大厂(MLCC + 二极管 + 电阻)。
- **6981.T** [2026-06-02] = Murata Manufacturing,日本 MLCC 全球龙头。垂直整合自制材料 + 设备。
- **TTDKY.US** [2026-06-02] = TDK ADR,日本 TDK 公司 ADR。MLCC + HDD 磁头 + 电池 + InvenSense MEMS 综合。

## 半导体 / 中游器件

- **POWI.US** [2026-06-02] = Power Integrations,AC-DC 集成芯片中游(800V 链稳健)。
- **NVTS.US** [2026-06-02] = Navitas Semiconductor,GaN 功率半导体小盘公司。
- **VICR.US** [2026-06-02] = Vicor Corporation,DC-DC 模块产品龙头。
- **IPWR.US** [2026-06-02] = Ideal Power,B-TRAN 双向晶体管技术微盘公司。
- **MBLY.US** [2026-06-02] = Mobileye Global,Intel 拆分的 ADAS 芯片公司。EyeQ ASIC 全球辅助驾驶主流。
- **AMBA.US** [2026-06-02] = Ambarella,边缘视觉 SoC 公司。机器人 / 自动驾驶 / 安防视觉芯片。
- **NXPI.US** [2026-06-02] = NXP Semiconductors,荷兰车规 MCU 主供。汽车电子核心元件。
- **MXL.US** [2026-06-02] = MaxLinear,美国 Wi-Fi 7 + 连接芯片厂。
- **SIMO.US** [2026-06-02] = Silicon Motion,SSD 主控芯片公司。本地 AI 推理对大 SSD 需求拉动。
- **SYNA.US** [2026-06-02] = Synaptics,触控芯片 + 边缘 AI。
- **INDI.US** [2026-06-02] = Indie Semiconductor,车规模拟 + RF 芯片公司。

## 物理 AI / 机器人零部件

- **603297.SHG** [2026-06-02] = 绿的谐波,A 股谐波减速器主要供应商。全球第 3 梯队(Harmonic Drive、Nabtesco 之后),人形机器人关节核心。
- **603667.SHG** [2026-06-02] = 五洲新春,行星滚柱丝杠潜力公司。Tesla Optimus 线性执行器关键零件。
- **603009.SHG** [2026-06-02] = 北特科技,行星滚柱丝杠双 player 之一(与五洲新春并列)。
- **002338.SHE** [2026-06-02] = 奥普光电,A 股光电编码器纯 play。机器人关节角度精度元件。
- **603728.SHG** [2026-06-02] = 鸣志电器,空心杯电机 A 股龙头。Maxon 风格精细电机,人形机器人手指等执行器。
- **688160.SHG** [2026-06-02] = 步科股份,无框力矩电机 + 伺服。人形机器人大型关节直驱。
- **6324.T** [2026-06-02] = Harmonic Drive Systems,日本谐波减速器全球龙头。
- **6268.T** [2026-06-02] = Nabtesco,日本 RV 减速器全球龙头。
- **6954.T** [2026-06-02] = Fanuc,日本工业机器人四大家族之一。
- **6506.T** [2026-06-02] = Yaskawa Electric,日本伺服 + 工业机器人本体大厂。
- **002747.SHE** [2026-06-02] = 埃斯顿,A 股工业机器人本体龙头。
- **AVAV.US** [2026-06-02] = AeroVironment,美军主要军用无人机供应商(Switchblade 巡飞弹 + Puma 战术 + JUMP 20)。
- **KTOS.US** [2026-06-02] = Kratos Defense,XQ-58 协同战斗机 + Mako 高超音速靶机。美军 NGAD/CCA 项目承包商。
- **002415.SHE** [2026-06-02] = 海康威视,全球安防监控 / 机器视觉龙头。
- **002236.SHE** [2026-06-02] = 大华股份,全球安防第 2(海康之后)。
- **SYM.US** [2026-06-02] = Symbotic,仓储自动化公司,Walmart 长期合同。
- **AUTO.OL** [2026-06-02] = AutoStore,挪威仓储立体库自动化公司。
- **CGNX.US** [2026-06-02] = Cognex Corporation,美国机器视觉龙头(工业精密检测)。
- **6861.T** [2026-06-02] = Keyence,日本机器视觉全球第 2,以高毛利率著称。
- **ISRG.US** [2026-06-02] = Intuitive Surgical,da Vinci 手术机器人全球龙头。
- **SYK.US** [2026-06-02] = Stryker,MAKO 骨科手术机器人 + 综合医疗器械。
- **DE.US** [2026-06-02] = Deere & Company,农业机械精准化龙头。See & Spray 智能耕作。
- **AGCO.US** [2026-06-02] = AGCO Corporation,农机第 2 梯队(Fendt 品牌)。
- **CAT.US** [2026-06-02] = Caterpillar,建筑机械龙头。
- **ABBNY.US** [2026-06-02] = ABB ADR(瑞士),工业机器人 + 电气化"四大家族"之一。
- **AMZN.US** [2026-06-02] = Amazon,AWS Bedrock Agents + 自营机器人(Kiva 仓储/Astro 家用)。

## 自动驾驶 / 车载

- **HSAI.US** [2026-06-02] = Hesai Group 禾赛科技,中国 LiDAR 出货量领先(车规 + Robotaxi 双线)。
- **LAZR.US** [2026-06-02] = Luminar Technologies,美国 LiDAR 公司(Velodyne 后合并体)。
- **AEVA.US** [2026-06-02] = Aeva Inc,FMCW LiDAR 技术路线。
- **OUST.US** [2026-06-02] = Ouster,美国数字 LiDAR 厂(与 Velodyne 合并)。
- **INVZ.US** [2026-06-02] = Innoviz Technologies,以色列小盘 LiDAR。
- **603501.SHG** [2026-06-02] = 韦尔股份,A 股 CMOS 图像传感器(CIS)龙头,旗下 OmniVision 车规 CIS 全球前列。
- **AUR.US** [2026-06-02] = Aurora Innovation,美国自动驾驶卡车 L4 上市纯 play。
- **CRNC.US** [2026-06-02] = Cerence,车载语音 AI(Nuance 拆分)。
- **TSLA.US** [2026-06-02] = Tesla,FSD 自动驾驶 + Optimus 人形机器人。
- **LI.US** [2026-06-02] = 理想汽车,中国新势力 EV,L2+ 智驾。
- **XPEV.US** [2026-06-02] = 小鹏汽车,中国新势力 EV,XNGP 智驾。
- **NIO.US** [2026-06-02] = 蔚来,中国新势力 EV。
- **GM.US** [2026-06-02] = General Motors,美国传统车企(Cruise Robotaxi 子公司)。
- **F.US** [2026-06-02] = Ford Motor Company,美国传统车企。
- **688256.SHG** [2026-06-02] = 寒武纪,中国 AI 芯片公司。

## AI 算力 / AI Agent 经济

- **NBIS.US** [2026-06-02] = Nebius Group,GPU 算力出租新云公司。
- **DDOG.US** [2026-06-02] = Datadog,云监控 + APM 综合龙头,延伸到 LLM observability。
- **MDB.US** [2026-06-02] = MongoDB,Atlas Vector 是企业 RAG 主流向量数据库。NoSQL 文档数据库 + 向量搜索。
- **NET.US** [2026-06-02] = Cloudflare,CDN + 边缘计算 + AI Gateway。
- **CFLT.US** [2026-06-02] = Confluent,Kafka 流式数据平台(Apache Kafka 商业版)。
- **SNOW.US** [2026-06-02] = Snowflake,云数据仓库 + Cortex AI Agent 集成。
- **ESTC.US** [2026-06-02] = Elastic NV,Elasticsearch + vector search 搜索引擎。
- **FROG.US** [2026-06-02] = JFrog,软件供应链管理(Artifactory/Xray)。
- **FSLY.US** [2026-06-02] = Fastly,边缘 CDN(Cloudflare 竞争者)。
- **CRM.US** [2026-06-02] = Salesforce,CRM SaaS 全球龙头。Agentforce 是其企业 Agent 平台。
- **PLTR.US** [2026-06-02] = Palantir Technologies,政府 + 企业 AI 数据分析平台(Foundry + AIP)。
- **NOW.US** [2026-06-02] = ServiceNow,企业 IT 服务管理(ITSM)龙头,Now Assist 是其 Agent 产品。
- **MNDY.US** [2026-06-02] = monday.com,以色列工作管理 SaaS。AI workflow agents 新方向。
- **APPN.US** [2026-06-02] = Appian,美国低代码 BPM 平台。Process Automation + AI agents。
- **PATH.US** [2026-06-02] = UiPath,RPA(机器人流程自动化)龙头,转型 Agentic Automation。
- **HUBS.US** [2026-06-02] = HubSpot,营销/销售 SaaS 中小企业市场。
- **NICE.US** [2026-06-02] = NICE Ltd,以色列客服自动化龙头。
- **ZS.US** [2026-06-02] = Zscaler,云安全网关(SSE)龙头。
- **BILL.US** [2026-06-02] = BILL Holdings,美国 SMB 财务自动化 SaaS。
- **AI.US** [2026-06-02] = C3.ai,企业 AI 应用平台。
- **GTLB.US** [2026-06-02] = GitLab,代码托管 + DevOps 一体化(GitHub 竞争者)。
- **SOUN.US** [2026-06-02] = SoundHound AI,语音识别 + 语音 AI agents。
- **APP.US** [2026-06-02] = AppLovin,移动广告 AI 平台。
- **DBX.US** [2026-06-02] = Dropbox,云存储 + Dropbox AI 文档功能。
- **S.US** [2026-06-02] = SentinelOne,AI 驱动的端点安全。
- **MSFT.US** [2026-06-02] = Microsoft,Azure 云 + Copilot Studio + OpenAI 战略合作。
- **GOOGL.US** [2026-06-02] = Alphabet,Google + Gemini LLM + Vertex AI Agent Builder。
- **META.US** [2026-06-02] = Meta Platforms,Llama 开源 LLM 持有方 + 广告 + 元宇宙。
- **AAPL.US** [2026-06-02] = Apple,M 系列芯片 + Apple Neural Engine + 设备生态。
- **ZI.US** [2026-06-02] = ZoomInfo Technologies,B2B 销售情报数据库。

## 商业航天 / 防务

- **VNP.TO** [2026-06-02] = 5N Plus,西方少数能产锗 / 镓 / 铟 + AZUR 空间太阳能电池。
- **MTRN.US** [2026-06-02] = Materion Corporation,铍材料公司(空间反射镜/制导/高超音速)。
- **RKLB.US** [2026-06-02] = Rocket Lab,小型火箭发射 + 卫星总包公司。
- **RDW.US** [2026-06-02] = Redwire,空间太阳能阵(ROSA)+ 星敏感器。
- **JOBY.US** [2026-06-02] = Joby Aviation,eVTOL(电动垂直起降)飞行汽车,Toyota 投资。
- **ACHR.US** [2026-06-02] = Archer Aviation,eVTOL 飞行汽车,Stellantis 投资。
- **EHGO.US** [2026-06-02] = EHang Holdings,中国 eVTOL 公司。

## A 股半导体(韬定律)

- **688072.SHG** [2026-06-02] = 拓荆科技,混合键合 + PECVD 设备(3D NAND 堆叠核心)。
- **688120.SHG** [2026-06-02] = 华海清科,CMP(化学机械抛光)设备国产领先。
- **688012.SHG** [2026-06-02] = 中微公司,刻蚀设备国产替代主供。
- **002371.SHE** [2026-06-02] = 北方华创,半导体设备平台型公司(综合)。
- **600584.SHG** [2026-06-02] = 长电科技,先进封装代工 A 股龙头。
- **002156.SHE** [2026-06-02] = 通富微电,先进封装(给 AMD/华为代工)。

## 光子学(2026 历史种子)

- **AXTI.US** [2026-06-02] = AXT Inc,InP 衬底主要供应商(全球 40% 份额)。光通信激光器链上游。
- **SIVE.ST** [2026-06-02] = Sivers Semiconductors,瑞典 SiPh 设计 + InP 收发器小盘公司。
- **LITE.US** [2026-06-02] = Lumentum Holdings,光通信器件大厂。
- **TSEM.US** [2026-06-02] = Tower Semiconductor,SiPh / 光子学代工(IBM 收购完成后)。
- **SOI.PA** [2026-06-02] = Soitec,SOI 衬底 + CPO 衬底主要供应商(法国)。
- **IQE.LSE** [2026-06-02] = IQE plc,化合物半导体外延片(英国)。

## 中游系统 / 数据中心电源

- **VRT.US** [2026-06-02] = Vertiv Holdings,数据中心电源系统集成(液冷 + UPS + PDU)。
- **ETN.US** [2026-06-02] = Eaton Corporation,电气基础设施(数据中心配电)。
- **2382.TW** [2026-06-02] = Quanta Computer,台湾笔电 ODM 龙头。
- **2356.TW** [2026-06-02] = Inventec,台湾笔电 ODM。
- **5392.TWO** [2026-06-02] = Auras Technology,台湾散热模组 Vapor Chamber 供应商。
- **3324.TW** [2026-06-02] = 双鸿科技,台湾笔电散热龙头。
- **3483.TWO** [2026-06-02] = 力致科技,台湾散热模组公司。
- **0522.HK** [2026-06-02] = ASMPT,香港上市的封装设备公司。
- **ASEKY.US** [2026-06-02] = ASE Technology Holdings ADR(日月光),台湾封测综合大厂 ADR。
- **LPL.US** [2026-06-02] = LG Display ADR,韩国 OLED 屏幕(笔电 + 电视屏)。
- **005930.KO** [2026-06-02] = Samsung Electronics,韩国半导体 + 显示综合巨头。
- **000660.KO** [2026-06-02] = SK Hynix,韩国 LPDDR + HBM 第 2 大供应商。
- **6981.T** [2026-06-02] = Murata 同上,日本 MLCC 全球龙头。
- **CTS.US** [2026-06-02] = CTS Corporation,陶瓷元件多元(压电/传感器/MLCC)。
- **KYOCY.US** [2026-06-02] = Kyocera ADR,日本京瓷 ADR,含 Kyocera AVX MLCC 子部门。
- **MRAAY.US** [2026-06-02] = Murata ADR,日本村田制作所 ADR(MLCC #1)。

---

## 编辑日志

- **2026-06-02 创建**:初始预填 100+ 个跨 11 个主题的标的(business 描述)。
- **2026-06-02 重构(用户挑战驱动)**:**清洗所有动态信息**(price/stage/跨主题数/市值/估值)— 只保留 business static 描述。Dynamic 内容(status)交给每份报告的 LLM 在 `data-status` 属性里现写,带日期标签。
- **维护**:每跑新主题 → LLM append 新标的 business 描述到本文件 → 再到报告里写 data-status 动态。
