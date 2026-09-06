# MASTER DEVELOPMENT PLAN V1.1

## Stage 1｜项目底座
- 仓库
- 治理文件
- 数据模型
- Runtime契约
- Device Adapter标准
- Knowledge/Narrative/Experience/Style/Learning边界
- Provider-neutral capability interfaces

Gate 1：
一张图片 + GPS + 当前路线，能够清楚说明从哪里进入、经过哪些模块、输出什么结构。

## Stage 2｜Recognition & Matching
输入：
- camera/image
- GPS
- current route
- previous/next stop
- guide voice hint

输出：
- Top 3 candidates
- score breakdown
- confidence
- selected place
- confirmation required / not required

Gate 2：
真实10个大洋路点
- Top1 >= 8/10
- Top3 = 10/10
- 低置信度不硬猜
- 导游纠正可影响当前session

## Stage 3｜Knowledge Pack
第一版 Great Ocean Road 30–50 个节点。
所有重要事实必须带来源和核验日期。

## Stage 4｜Narrative Timeline
首批：
- Australia
- Victoria / Melbourne
- Great Ocean Road

支持：
Mainline / Branch / Side Note / Return to Mainline

默认历史叙事：
最早相关时间 → 时间推进 → 原因 → 结果 → 当前所见。

## Stage 5｜Guide Experience Pack
首批：
- Great Ocean Road
- Phillip Island Penguin

经验与事实分层；经验保留作者、适用场景和验证历史。

## Stage 6｜Narration & Style
支持：
- 30s / 90s / 3min / deep
- 专业 / 故事 / 幽默 / 亲子 / 高端 / 学生 / 摄影
- Guide Style Profile

## Stage 7｜Hardware / Screenless
- phone camera
- GPS
- Bluetooth earpiece
- Bluetooth speaker / vehicle audio
- voice commands
- private/public audio routing

驾驶状态不得依赖复杂屏幕操作。

## Stage 8｜Visitor Q&A
稳定知识 / 历史主题 / 现场问题 / 实时信息 / 经验问题分流。
同一Tour Session必须记住游客已经听过的内容。

## Stage 9｜Multilingual Personal Audio
先中英真实跑通，再扩其他语言。
原则：One Fact Base, Many Languages, Many Narrations。

必须支持：
- guide_private language
- vehicle_public language
- tourist_personal language
- language + locale分离
- 普通话与粤语分别选择
- 同一Tour Session多个个人音轨同步叙事状态
- 游客以自己的语言提问和收听

详细治理见：`MULTILINGUAL_AUDIO_CHANNELS.md`。

## Stage 10｜Guide Learning Loop
至少覆盖：
- 事实准确度
- 叙事质量
- 游客问答
- 表达质量
- 经验使用
- 游客互动

带团中仅严重问题优先提示；下团后自动复盘。
AI建议必须经过导游确认/拒绝/修改，才能成为长期学习或经验候选。
下一次真实Tour必须能证明学习结果被复用。

详细治理见：`GUIDE_LEARNING_QUALITY.md`。

## Stage 11｜Guide Skill Profile
私人教练，不是公开考官。
默认形成个人成长档案，不以公开排名作为首要产品机制。

## Stage 12｜Creator Economy
角色：Contributor / Creator / Learner / Platform。
资产：Knowledge / Narrative / Experience / Route Pack。

必须包括：
- Contribution Ledger
- sales revenue share
- subscription usage share
- verified real-tour usage reward
- quality / retention reward
- correction/update reward
- scarce region/language incentive
- regional creator seed program

Creator奖励以真实使用价值为核心，不奖励垃圾上传量。
详细商业规则见：`../13_Commercial/creator_economy/README.md`。

## Stage 13｜Payment
Guide Subscription + Pack Store + Contributor Payout。
区域上线前校准支付费率、退款、税务和创作者结算。

## Stage 14｜Regional Expansion
Australia → New Zealand → Japan → other regions。
原则：Global Core + Regional Commerce + Local Content。

## Stage 15｜Agency / Enterprise
旅行社、景区、博物馆、旅游巴士、邮轮、旅游局。
企业功能必须建立在个人导游真实产品已经成立之后。

## 当前唯一工程重点
Stage 1 基线已建立，当前继续完成 Stage 2：Recognition & Matching 的真实能力Gate。

当前Gate未通过项：
- 真实Camera/Vision Provider尚未接入
- 10个地点真实现场图片尚未形成验收集
- seed coordinates尚待实地核验

在Gate 2真实通过前，不提前建设Payment、Marketplace或复杂Enterprise功能。
