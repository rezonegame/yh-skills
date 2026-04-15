# 结构化输出扩展指南 (JSON/XML Formatting)

当用户不仅需要可阅读的 Markdown，还需要将大批量的文本加工为 **完全脱水的结构化数据模型**（以便存入 RAG 向量数据库或知识图谱）时，必须在此基础上追加 JSON/XML 输出。

## 适用场景
- 批量处理说明书、产品页面、学术文摘。
- 用户明确要求提供适合机器解析的格式。

## JSON/XML 约束 (Machine Only Rules)
1. **纯净性**：绝对禁止在数据字段中包含思考过程。
2. **扁平化结构**：优先使用一维对象数组而非过度嵌套的深层结构。
3. **标签语义化**：字段的 Key 或标签必须是清晰易懂的英文。

## Markdown 附带输出格式示例

---

### JSON 格式输出示范 (可选)

```json
{
  "entity_name": "实体名称",
  "category": "分类",
  "core_definition": "一句话核心定义摘要",
  "facts": {
    "feature_1": "事实数据 1",
    "feature_2": "事实数据 2",
    "missing_data": ["[需补充真实数据：销售额]"]
  },
  "intent_faq": [
    {
      "question": "用户会问什么问题？",
      "mechanism": "核心机制结论",
      "support": "事实支撑"
    }
  ],
  "e_e_a_t": {
    "related_terms": ["术语1", "术语2"],
    "suggested_citations": ["建议引用的补充报告"]
  }
}
```

### XML 格式输出示范 (可选)

```xml
<geo_document>
  <entity>
    <name>实体名称</name>
    <category>分类</category>
    <definition>一句话核心定义摘要</definition>
  </entity>
  <facts>
    <fact dimension="维度1">事实数据 1</fact>
    <fact dimension="维度2">事实数据 2</fact>
    <fact dimension="缺失关键"><![CDATA[[需补充真实数据：销售额]]]></fact>
  </facts>
  <intent_faq>
    <faq>
      <question>用户会问什么问题？</question>
      <mechanism>核心机制结论</mechanism>
      <support>事实支撑</support>
    </faq>
  </intent_faq>
  <e_e_a_t>
    <term>术语1</term>
    <term>术语2</term>
    <suggested_citation>建议引用的补充报告</suggested_citation>
  </e_e_a_t>
</geo_document>
```

## 字段命名与版本约定

1. **命名规范**：所有 JSON 字段统一使用 `snake_case`（小写下划线），XML 标签同理。禁止 camelCase 混用。
2. **Schema 版本**：在 JSON 根对象中始终包含 `"schema_version": "1.0"` 字段，便于下游程序识别格式变更。XML 中通过根元素属性声明：`<geo_document version="1.0">`。
3. **日期格式**：所有日期字段统一使用 ISO 8601 格式（`YYYY-MM-DD`），禁止使用模糊表述如"去年"或"近期"。
