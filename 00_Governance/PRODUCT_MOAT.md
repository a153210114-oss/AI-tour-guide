# PRODUCT MOAT｜以人的体验为中心的产品护城河

Status: ACTIVE
Authority: Strategic product moat baseline

## 1. Core Positioning

AI Tour Guide Copilot 不以“景点内容”“AI导览功能”或“某个模型能力”为产品中心。

产品中心是：

> 人的完整旅游体验。

系统连接：

`Guide <-> AI System <-> Visitors`

真正要持续优化的是：
- 导游是否更轻松、更专业、更有成长
- 游客是否听得懂、记得住、愿意问、体验更好
- 同一团不同游客是否能获得适合自己的语言、深度和表达
- 整个团是否形成连续、有记忆、有反馈的真实体验

因此，模型、视觉识别、TTS、多语种、搜索都属于可替换能力，不是最终护城河。

---

## 2. Moat No.001｜Live Tour State

一次真人带团必须被视为一个持续运行的 Live Tour Session，而不是一连串孤立问答。

系统持续维护：
- guide
- route
- current location
- current visual scene
- group composition
- active languages
- what has already been told
- current narrative timeline
- branches already entered
- visitor questions
- visitor interest signals
- guide corrections
- active experience packs
- next best narration/action

核心价值：

> AI知道“这个团一路发生了什么”。

因此游客说“刚才那个英国人后来怎么样了？”时，系统应能理解其所指，而不是重新从零开始。

Live Tour State 是现场连续体验的基础，也是第一层数据护城河。

---

## 3. Moat No.002｜Experience Graph

Knowledge Pack 解决“什么是真的”。
Experience Graph 解决“什么情况下，怎样做，人的体验会更好”。

Experience Graph 不只是内容，而是结构化、条件化、可执行的专业经验。

例如一条企鹅岛经验，不应只是文章，而应能够表达：
- 什么客群
- 什么时间
- 什么天气
- 什么位置
- 之前已经讲过什么
- 现在应该提醒什么
- 哪些内容应该延后
- 哪种观察/摄影建议更合适

经验节点应至少包含：
- author/source
- applicable route/place
- audience
- conditions
- recommended action
- evidence / observed outcome
- confidence
- usage count
- correction rate
- visitor feedback

原则：

> Experience Pack 不是静态文件，而是 AI Runtime 可调用的专业决策层。

---

## 4. Moat No.003｜Guide Learning Loop

产品不仅帮助导游完成今天这一团，还必须让导游下一团做得更好。

带团中：
- 仅严重事实/安全错误即时私下提醒
- 不用AI频繁打断导游

下团后：
- Fact Accuracy
- Narrative Quality
- Visitor Answer Quality
- Delivery Quality
- Guide Experience Use
- Visitor Engagement

系统输出：
- 错在哪里
- 为什么
- 正确知识/时间轴是什么
- 哪些内容游客最感兴趣
- 哪些表达过长/重复/断裂
- 哪些现场做法值得保留
- 哪些做法适合升级为个人 Experience Pack 候选

学习链：

`Tour -> Record -> Review -> Correct -> Learn -> Candidate Experience -> Guide Confirm -> Reuse`

原则：

> AI负责发现和建议，真人导游保留专业最终判断。

这使系统成为私人教练，而不是监考系统。

---

## 5. Moat No.004｜One Live Tour, Many Personal Experiences

多语种本身不是护城河。

护城河是：

> 同一个真人导游、同一个真实行程、同一个 Live Tour State，下的多路个性化体验。

例如：
- 导游耳机：普通话私人提示
- 车载主音轨：普通话
- 香港游客手机：粤语
- 英语游客手机：英语
- 日本游客手机：日语

不同游客可拥有：
- language
- narration depth
- preferred style
- personal Q&A
- accessibility needs

但所有人仍然属于同一个 Live Tour Session，继承同一团已经发生的上下文。

原则：

> One live guide, one tour, many personalized channels.

---

## 6. Moat No.005｜Creator Experience Network

Creator Economy 的价值不在“让人上传内容”，而在建立经过真实带团验证的专业经验网络。

贡献可包括：
- Experience Pack
- Narrative Branch
- route practice
- factual correction
- language correction
- viewing / photography advice
- local operational update

平台奖励重点不是上传数量，而是 Verified Utility：
- real-tour usage
- repeat use
- learner retention
- low correction rate
- guide ratings
- visitor feedback
- regional scarcity
- language scarcity
- successful reuse

长期形成：

`优秀导游贡献 -> 其他导游学习 -> 真实带团验证 -> 新反馈 -> 经验优化 -> 更多使用 -> 创作者收益`

专业经验因此成为可持续增值的数字资产。

---

## 7. Moat Flywheel

五层护城河必须互相增强：

`Live Tour State`
-> 产生真实现场数据
-> `Experience Graph`
-> 指导更好的现场行为
-> `Guide Learning Loop`
-> 形成更成熟的导游与经验
-> `Personalized Group Experience`
-> 提升不同游客体验与反馈
-> `Creator Experience Network`
-> 引入更多高质量经验
-> 回到更强的 Live Tour State 与 Runtime

这不是单一功能护城河，而是数据、经验、反馈和网络共同形成的复合护城河。

---

## 8. What Is NOT the Moat

以下能力很重要，但不得被误认为长期护城河：
- 单一大模型
- 单一Vision Provider
- TTS
- GPS触发
- 拍照识别
- 普通AI问答
- 多语种翻译
- 固定录音/讲解词
- 单独的二维码游客页

这些能力都可能被快速复制或商品化。

真正难复制的是：

> 实时团状态 + 结构化专业经验 + 导游成长数据 + 游客反馈 + 真实使用验证 + 创作者经验网络。

---

## 9. Product Decision Rule

以后任何产品功能、数据表、算法、模型接入或商业设计，都必须回答：

> 它是否让“人的完整体验”更好？

具体至少对应以下一项：
- 导游更懂该怎么带
- 游客更容易理解和记住
- 不同游客得到更适合自己的体验
- 系统更理解本团实时状态
- 导游下一团明显更好
- 优秀经验更容易被验证、复用和奖励

如果一个功能只增加技术复杂度，却不能强化以上任一项，应默认延后。

---

## 10. Strategic Statement

> AI Tour Guide 不以“讲解景点”为终点，而是建立一套持续优化“人如何被带好、被讲好、被服务好”的实时体验系统。

Long-term moat:

> Human Experience Intelligence Network for Live Tourism.
