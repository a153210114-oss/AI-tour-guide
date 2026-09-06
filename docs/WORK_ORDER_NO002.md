# WORK ORDER NO.002｜Live Guide Translation Channel R1

Status: ACTIVE PRIORITY TEST

## 目标

先只跑通真人导游实时讲解通路：

`导游耳麦 -> 导游手机 -> 实时语音输入 -> STT -> 多语种翻译/重述 -> TTS/音频流 -> 游客手机 -> 游客耳机`

这是当前优先测试闭环。Recognition & Matching No.001 保留，不删除，但本轮不扩展其 scope。

## A. 导游端改动

### A1. 导游端国际化
- 首次进入读取 `navigator.languages` / `navigator.language`
- 中文设备默认中文 UI
- 英文设备默认英文 UI
- 保留手动语言切换
- 选择写入 localStorage；以后优先使用上次选择

必须分离以下字段，禁止绑死：
- guide_ui_language
- guide_prompt_language
- guide_spoken_language
- public_audio_language
- visitor_output_language

### A2. 真人讲解输入设备
导游端新增“讲解输入设备”选项：
1. 蓝牙耳麦 / 领夹麦（本轮默认测试）
2. 手机麦克风
3. 车载 / 无线麦系统（占位，不冒充已连接）
4. 智能眼镜麦克风（未来占位）

本轮必须真实测试：
- 蓝牙耳麦 / 领夹麦 -> 导游手机

导游运行态至少显示：
- 麦克风连接状态
- 当前输入源
- 主讲语言
- 实时翻译开/关
- 当前游客语言频道
- 一个大按钮：`暂停实时讲解`

驾驶状态禁止复杂菜单操作。

## B. 游客端改动

游客端由三个入口改为四个：

1. `系统讲解`
   - AI 根据当前 Live Tour State / Knowledge / Narrative 生成个人语言补充讲解

2. `听导游`
   - 真人导游实时语音频道
   - 导游讲话实时 STT -> 翻译/重述 -> 游客语言音频
   - 游客只需自己的手机 + 自己的耳机

3. `问导游`
   - 普通知识问题可由系统回答
   - 需要真人决定的问题进入导游问题队列

4. `评价导游`
   - 评分/反馈进入 Tour Review / Guide Learning Loop

游客首次扫码：
- 默认读取浏览器/手机语言
- 不强制先选语言
- 顶部保留一键切换
- 语言选择持久化

## C. 第一轮语言范围

导游主讲：普通话

游客频道先真实验证：
- 普通话（原声/直接频道，可不经翻译）
- 粤语
- English

不要先扩十几种语言。

## D. 实时链路技术要求

### D1. 音频必须流式
禁止“整段录完再翻译”。

目标链：
`streaming audio -> VAD/segmentation -> streaming STT -> semantic chunk -> translation -> TTS/audio stream`

### D2. Provider-neutral
接口至少抽象：
- AudioInputProvider
- STTProvider
- TranslationProvider
- TTSProvider
- VisitorAudioChannelProvider

本轮允许选择一个真实 Provider 跑通，但不得把核心业务写死在单一模型厂商。

### D3. 隐私/公开讲解开关
系统必须支持导游一键：
- 开始公开讲解
- 暂停公开讲解

暂停时不得继续把导游与工作人员/私人对话转发给游客。

## E. 第一轮验收

使用真实设备，不接受 mock-only：

1. 导游手机成功使用蓝牙耳麦/领夹麦作为实际输入源
2. 系统能持续收到真人导游实时普通话
3. 普通话 STT 稳定产生分段文本
4. English 频道实时生成并在游客手机播放
5. 粤语频道实时生成并在游客手机播放
6. 普通话游客可以收听原声/直接频道
7. 游客手机只连接自己的耳机即可收听
8. 导游端可看到至少 3 个语言频道状态
9. `暂停实时讲解` 后，游客端停止接收新的导游语音
10. 中英文手机首次打开导游端，UI 默认语言正确；手动切换后刷新保持
11. 游客端四入口均存在且语义清晰
12. 不允许把预录音频或固定文本播放冒充“真人实时讲解”

## F. 必须记录的三项指标

每次实测至少记录：
- end_to_end_latency_ms
- stt_accuracy / obvious transcript errors
- translation_semantic_fidelity

同时记录：
- input device
- guide spoken language
- visitor output language
- network condition
- provider/model

## G. 本轮不做

- 支付
- Creator Marketplace
- 复杂账号系统
- AR
- 视觉识别扩展
- 全球多语言全覆盖
- 导游评分算法优化
- 复杂后台

## H. 完成回执

完成后必须提交：
- 变更文件
- commit SHA
- 实际 Provider / 模型
- 实际输入设备
- 实际游客手机测试证据
- 普通话/粤语/English 三频道结果
- 端到端延迟
- 已知问题
- 哪些仍是 mock / placeholder

唯一完成标准：

> 导游戴着耳麦正常讲话，至少一台游客手机能通过自己的耳机实时听到另一种语言，且明确不是预录音频或手动触发固定文本。
