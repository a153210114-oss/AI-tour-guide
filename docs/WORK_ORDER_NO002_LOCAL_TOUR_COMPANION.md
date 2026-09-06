# WORK ORDER NO.002｜Local Tour Companion Prototype

## 目标

在不引入账号、支付、复杂后台或真实外部模型的前提下，跑通：

`Guide -> Tour Session -> Visitor -> Question / Rating -> Guide Review`

## 边界

- Mock narration 明确标注为 `mock-local-narration-v1`。
- 所有游客语言频道共享同一 place/topic，不做中文逐句翻译链路。
- 运行时事件和语言字段保持 provider-neutral。
- 浏览器音频输出是 Device Adapter 的本地测试层，不宣称真实硬件验收。
- 不改变 Recognition & Matching Gate 2 的未完成状态。

## 二维码策略

每位导游可以保留稳定入口，但二维码必须在进入时解析为当前 active tour session。原型二维码直接编码当前 session URL，避免不同团次的问题和评分混在一起。

建议所有游客扫码加入；是否播放个人语言讲解由游客自行决定，问导游和评分仍使用同一入口。

## 验收步骤

1. 导游打开 Live Tour，看到当前地点与动态二维码。
2. 游客手机扫码免注册加入，默认采用浏览器语言并可切换。
3. 游客播放模拟讲解；不同语言共享同一 place/topic。
4. 游客提问，导游队列在轮询周期内出现问题并可回复。
5. 游客提交评分，导游 Tour Review 显示平均分、评价数和标签。
6. 导游连接蓝牙耳机/扩音设备，播放测试音；浏览器支持时可选择具体输出。
