# 贡献指南 / Contributing

欢迎投稿你的 CSS 效果！🎉

## 收录标准

- ✅ **纯 CSS 实现**：核心效果不依赖 JavaScript（个别交互类可含少量可选 JS，需注明）
- ✅ **零外部依赖**：不引第三方库、字体、图片（渐变/形状都用 CSS 画）
- ✅ **代码整洁**：属性每行一个，方便他人阅读和修改
- ✅ **效果通用**：是多数项目里用得上的常见效果，不是一次性炫技

## 提交格式

在 `effects.json` 的 `effects` 数组中添加：

```json
{
  "name": "效果名称",
  "category": "button",
  "description": "一句话说明效果",
  "html": "<button class=\"btn\">Text</button>",
  "css": ".btn {\n  ...\n}"
}
```

`category` 可选值：`button` / `loader` / `card` / `text` / `background`

提交前运行 `python build_site.py` 重新生成演示站，并在浏览器里确认效果正常，再提 PR。
