# AI Tour Guide Copilot

全球智能导游辅助系统。

## 当前阶段
P0：项目底座 + Recognition & Matching No.001

新会话从 [`00_Governance/START_HERE.md`](00_Governance/START_HERE.md) 接棒。

## 核心链路
Device / GPS / Voice
→ Scene Context
→ Recognition & Matching
→ Knowledge
→ Narrative Timeline
→ Guide Experience Pack
→ Generation
→ Audio Output
→ Session Learning

## 产品原则
- 低屏 / 无屏优先
- 事实与经验分层
- 时间轴组织讲解
- 多语种不是逐句翻译
- 识别采用 GPS + 路线 + 视觉 + 语音 + 时序
- 真实带团验收优先于页面/API/Test PASS

## 本地 Web / PWA 原型

当前仓库包含一个可在同一 Wi-Fi 下由电脑和手机共同测试的最小原型：

- 导游端：Today / Live Tour / Visitor Channels / Review / My Packs
- 游客端：免注册扫码加入，自动匹配浏览器语言并可切换
- 共享 session：个人语言讲解、游客问题队列、导游回复、评分回传
- 音频测试：浏览器支持时选择耳机/扩音设备，否则跟随系统蓝牙路由

安装并启动：

```bash
python3 -m pip install -e .
python3 10_API/local_server.py
```

启动后打开终端显示的 Guide 地址。手机与电脑连接同一 Wi-Fi，再扫描导游端二维码加入。

> 这是本地模拟原型，不代表真实 AI、TTS、现场设备或 Gate 2 已通过。服务重启后 session 数据会清空。
