# MULTILINGUAL PERSONAL AUDIO CHANNELS

Status: Governance Baseline

## 1. Principle

One Tour, Multiple Personal Audio Channels.

同一趟行程中，导游、车载扩音器和不同游客可以同时使用不同语言频道。

## 2. Example

- Guide earpiece: Mandarin
- Vehicle public audio: Mandarin or English
- Tourist A: Cantonese / yue-HK
- Tourist B: English
- Tourist C: Japanese
- Tourist D: Spanish

所有频道共享同一 Verified Fact Base 和 Narrative State，但允许针对语言、locale、客群和风格重新组织表达。

## 3. Language data model

至少区分：
- source_language
- content_language
- guide_language
- public_audio_language
- audience_language
- preferred_output_language
- fallback_language
- locale
- region

中文不能只建一个 `Chinese` 枚举。至少预留：
- zh-CN / Mandarin simplified context
- zh-TW / Taiwan Chinese context
- zh-HK / Hong Kong written Chinese context
- yue-HK / Cantonese spoken output

不要把地区、书写体系和口语输出混为同一个字段。

## 4. Visitor interaction

游客端优先使用无需安装App的二维码Web入口：
1. 加入当前Tour Session
2. 选择语言/locale
3. 选择耳机播放
4. 接收与当前主叙事同步的个人音轨
5. 可用自己的语言提问

导游端不应为每个游客手工操作语言。

## 5. Synchronization

个人语言频道必须保持同一Tour Session的叙事进度：
- current place
- active timeline
- already told nodes
- branch state
- current public topic

允许语言输出长度不同，但不得造成事实版本冲突。

## 6. Translation rule

禁止：
`Chinese script -> literal translation -> all languages`

应采用：
`Verified Facts + Narrative State + Audience/Locale + Guide Style -> target-language narration`

## 7. Audio routing

输出层至少支持：
- guide_private
- vehicle_public
- tourist_personal

未来可以扩展：
- smart_glasses_audio
- seat_audio
- tour_bus_channel

## 8. Acceptance

多语种功能不能只通过文本翻译测试验收。

真实验收至少证明：
- 同一Tour Session中两个以上语言频道并行
- 内容事实一致
- 叙事节点同步
- 普通话与粤语可分别选择
- 游客提问可以用所选语言回答
- 导游无需持续操作屏幕

## 9. Provider implementation baseline

- Live speech translation provider: OpenAI `gpt-realtime-translate`
- Browser transport: WebRTC with a server-issued short-lived client secret
- The standard API key must remain server-side and must never be sent to a browser
- Source and translated transcripts should be retained with clear timestamps when recording consent applies
- Provider readiness and guide-broadcast connectivity are separate states; the UI must not call a device microphone test a live guide broadcast
- Production listen-along requires one translation session per target language and a media relay that republishes the guide's source track to visitor channels
