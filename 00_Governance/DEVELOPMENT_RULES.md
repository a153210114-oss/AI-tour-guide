# DEVELOPMENT RULES

- 每张工单只定义一个主要目标。
- 禁止用关键词/regex硬编码冒充语义理解。
- 禁止把Mock/Stub/测试特判标记为REAL。
- 每个事实保留source、source_grade、last_verified_at。
- 每条经验保留author、scope、conditions、confidence。
- 所有真实测试保留输入、识别候选、最终匹配、讲解、输出设备、导游纠正和结果。
- 优先可逆、小步提交。
