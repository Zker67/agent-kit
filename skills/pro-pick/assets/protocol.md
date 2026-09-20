# pro-pick 协议

一对文件：`manifest.json` 由 AI 写，`result.json` 由人给。`index.html` 由 `gallery-template.html` 生成，把 `manifest.json` 原样嵌进 `<script id="manifest" type="application/json">` 中。

## manifest.json

```json
{
  "id": "2026-01-01-short-topic",
  "topic": "一句话说明这次陈列的是什么",
  "round": 1,
  "slots": []
}
```

| 字段 | 说明 |
|---|---|
| `id` | 目录名，同一主题多轮共用，用作页面本地存储的键 |
| `topic` | 页面标题 |
| `round` | 轮次，从 1 开始；`round-N/` 目录内的 manifest 写 N |
| `slots` | 接入点数组 |

### slot

```json
{
  "id": "S01",
  "name": "首页背景音乐",
  "scene": "用户进入首页后自动循环播放，可静音",
  "constraints": "时长 60 到 120 秒，无人声，可循环",
  "candidates": [
    { "id": "S01-a", "type": "audio", "src": "media/S01-a.mp3", "label": "钢琴慢板，90 秒", "source": "项目已有 assets/audio/", "license": "project" },
    { "id": "S01-b", "type": "audio", "src": "media/S01-b.mp3", "label": "电子氛围，110 秒", "source": "生成工具产出", "license": "unknown" }
  ],
  "suggestion": "a 的结尾有 1 秒静音，循环时会有停顿"
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | slot 唯一标识，`result.json` 用它回指 |
| `name` | 是 | 接入点名字 |
| `scene` | 是 | 用在哪、用户在什么情境下看到或听到 |
| `constraints` | 否 | 硬约束：尺寸、时长、格式 |
| `candidates` | 是 | 至少 1 个；只有 1 个时人的操作是通过或打回 |
| `suggestion` | 否 | AI 建议，页面上单独标为“AI 建议”；事实字段里不放评判 |

### candidate

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 候选唯一标识，建议 `<slot-id>-<字母>` |
| `type` | 是 | `image` / `video` / `audio` / `html` / `text` |
| `src` | 视类型 | 相对路径；`text` 类型用 `content` 代替 |
| `content` | 视类型 | `text` 类型的正文 |
| `label` | 是 | 描述该候选本身，不与其他候选比较 |
| `source` | 是 | 来源：项目资产路径、生成工具、素材库名、当前实现截图 |
| `license` | 是 | 许可；不确定写 `unknown` |

| `type` | 渲染方式 |
|---|---|
| `image` | `<img>`，点击即选中，说明栏有“放大” |
| `video` | `<video controls>` |
| `audio` | `<audio controls>` |
| `html` | `<iframe>`，可新窗口打开 |
| `text` | `<pre>` 内联显示 |

候选不排序、不标推荐。

## result.json

由页面导出，人也可以手写：

```json
{
  "id": "2026-01-01-short-topic",
  "round": 1,
  "decisions": [
    { "id": "S01", "chosen": "S01-a", "more": false, "note": "" },
    { "id": "S02", "chosen": null, "more": true, "note": "都太亮，要暗一点的" },
    { "id": "S03", "chosen": null, "more": false, "note": "" }
  ]
}
```

| 字段 | 取值 |
|---|---|
| `chosen` | 候选 `id` 或 `null` |
| `more` | `true` 表示都不要、再找（单候选时即“打回”） |
| `note` | 人的批注，AI 下一轮据此补充候选或调整接入 |

`chosen` 为 `null` 且 `more` 为 `false` 表示人未处理，AI 不接入也不补候选，下一轮继续陈列。

## 轮次

- 第 1 轮在 `pick/<id>/`，之后每轮新建 `pick/<id>/round-N/`，结构相同。
- 下一轮的 manifest 只包含上一轮 `more` 或未处理的 slot，`id` 沿用，候选重新取材。
- 一轮 `result.json` 中没有 `more` 且没有未处理即结束。

## 生成 index.html

把 `gallery-template.html` 复制为 `index.html`，将其中 `<script id="manifest" type="application/json">` 标签的内容替换为 `manifest.json` 全文。若 manifest 中出现 `</script>` 字面文本，替换为 `<\/script>`。不引入外部脚本或样式，保证 `file://` 直接打开可用。
