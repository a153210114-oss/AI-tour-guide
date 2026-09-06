# WORK ORDER NO.001｜Recognition & Matching R1

## 唯一目标
跑通真实识别与匹配链路。

## 输入
camera/image + GPS + route + previous/next stop + optional voice hint

## 输出
Top 3 candidates + score breakdown + confidence + selected place

## 第一批测试点
- Torquay
- Bells Beach
- Memorial Arch
- Apollo Bay
- Gibson Steps
- Twelve Apostles
- Loch Ard Gorge
- The Grotto
- London Bridge
- Bay of Islands

## Gate
- Top1 >= 8/10
- Top3 = 10/10
- 低置信度不硬猜
- 导游纠正后当前session记住
- 识别结果能进入对应Knowledge Pack

## 禁止
- 先做漂亮UI
- 先做账号/支付
- 为测试图片/短语写特判
- 只靠视觉猜全世界
