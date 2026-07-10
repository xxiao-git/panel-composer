---
name: panel-composer
version: 0.5.0
description: 将多个 panel（PDF/PNG/JPG/TIFF/BMP）组合成一张大图，支持三种布局工作流
description_zh: 将多个 panel（PDF/PNG/JPG/TIFF/BMP）组合成一张大图，支持自动/画布/对话三种布局工作流
tags: [figure, panel, composite, layout, bioinformatics, image, pdf, workflow]
author: WorkBuddy
created: 2026-07-08
updated: 2026-07-10
---

# Panel Composer

通用 panel 组图工具。输入多个文件（PDF 或图片，每个是一个 panel），按指定布局拼成一张大图。

## When to Use

- 用户有多个独立文件（PDF/PNG/JPG/TIFF/BMP，每个是一个 panel/子图），需要组合成一张大图
- 支持 PDF 和图片混合输入，自动等比缩放
- 需要按网格布局（2x2, 3x3 等）或自定义位置排列 panel
- 需要给 panel 添加标签（A, B, C, D... 或 1, 2, 3, 4...）
- 输出格式：PDF 或 PNG
- 适用于投稿、报告、海报等场景

## Triggers

关键词：组合 PDF、拼接 panel、组图、拼图、composite figure、panel assembly、网格布局、figure assembly、图片拼接、合并图片、PDF 拼图

## Dependencies

```bash
pip install reportlab PyMuPDF Pillow
```

---

## 三条工作流

Panel Composer 提供三种布局方式，适配不同场景：

### 工作流 1：AI 自动布局（默认）

**场景**：快速出图，不需要精细控制

**用法**：
```python
compose_figure(
    panels=["a.pdf", "b.png", "c.jpg"],
    layout="auto",  # 自动计算行列
    output="figure.pdf",
    labels=True,
)
```

AI 会按 panel 数量自动选择接近正方形的网格（如 4 个 → 2x2，6 个 → 2x3 或 3x2）。

---

### 工作流 2：HTML 画布布局（可视化拖拽）

**场景**：需要精确控制每个 panel 的位置和大小

**流程**：
1. 在浏览器打开 `scripts/layout-canvas.html`
2. 拖拽画矩形定义每个 panel 的位置
3. 导出 JSON（复制到对话或保存文件）
4. 用 `json_layout` 参数读取 JSON 出图

**示例**：
```python
compose_figure(
    panels=["a.pdf", "b.png", "c.jpg"],  # 按画布上画的顺序对应
    json_layout="layout.json",  # 画布导出的 JSON
    output="figure.pdf",
)
```

**放心拖拽**：无论你在画布上拖出什么比例和尺寸的框，panel 内容始终保持原始宽高比，不会被拉伸或压缩变形。如果框的比例与原图不一致，原图会在框内等比缩放并居中，多余空间留白。所以你只需要关注位置和大小，不用担心比例问题。

**JSON 格式**：
```json
{
  "page_size": "a4",
  "margin": 36,
  "panels": [
    {"label": "A", "x": 50, "y": 400, "width": 200, "height": 150},
    {"label": "B", "x": 270, "y": 400, "width": 200, "height": 150},
    {"label": "C", "x": 50, "y": 200, "width": 420, "height": 150}
  ]
}
```

---

### 工作流 3：对话式布局（自然语言描述）

**场景**：不想用画布，直接用文字描述布局

**示例**：
- "上面两个 A B 并排，下面 C 占满整行"
- "左边 A 占一半高度，右边 B C D 竖着排"
- "A 大一点放左上，B C D 小一点在右下一列"

AI 会解析描述，转换为 `custom` 布局的 dict 列表，直接调用 `compose_figure`。

---

## 核心参数

### 基本参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `panels` | list | 必填 | 文件路径列表（PDF/PNG/JPG/TIFF/BMP，可混合），或 dict 列表（custom 布局时） |
| `output` | str | 必填 | 输出文件路径（.pdf 或 .png） |
| `dpi` | int | 300 | PNG 输出分辨率 |

### 布局控制

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `layout` | str | `"auto"` | 布局方式：`grid` / `auto` / `custom` / `mixed` |
| `rows` | int | None | 网格行数（layout=grid 时必填） |
| `cols` | int | None | 网格列数（layout=grid 时必填） |
| `json_layout` | str\|dict | None | JSON 布局文件路径或 dict（优先级最高，忽略其他布局参数） |
| `page_size` | str\|tuple | `"a4"` | 页面尺寸：`"a4"` / `"letter"` / `"a3"` / `(width, height)` |
| `margin` | int | 36 | 页面外边距 pt（默认 0.5 inch） |
| `spacing` | int | 12 | panel 间距 pt |

### 标签样式

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `labels` | bool | False | 是否添加 panel 标签 |
| `label_style` | str | `"uppercase"` | 标签样式：`uppercase` (A,B,C) / `numeric` (1,2,3) / `lowercase` (a,b,c) |
| `label_font_size` | int | 14 | 标签字体大小 pt |
| `label_offset` | tuple | `(-18, -18)` | 标签相对 panel 左上角的偏移 (x, y) |

### 其他

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `background_color` | str | `"white"` | 背景色（PNG 输出时生效） |
| `rasterize` | bool\|list | False | PDF 矢量化控制：`False`（默认，全部矢量）/ `True`（全部位图）/ `[0, 2]`（指定索引的 panel 转位图） |

**关于 `rasterize` 参数**：
- 默认所有 PDF panel 保持矢量（推荐，可无损放大编辑）
- 如果某个子图元素特别多（热图、散点图），可指定该 panel 转位图以减小文件大小
- 示例：`rasterize=[2]` 表示将第 3 个 panel（索引从 0 开始）转为位图
- 用户说"把热图转成位图"或"C 子图元素太多，转位图"时，识别对应 panel 索引并传参

---

## Layout Modes

### `grid`
固定行列网格。需提供 `rows` 和 `cols`。

```python
compose_figure(
    panels=["a.pdf", "b.pdf", "c.pdf", "d.pdf"],
    layout="grid", rows=2, cols=2,
    output="figure.pdf", labels=True,
)
```

### `auto`
自动计算最佳行列数（接近正方形）。panel 数 = rows × cols（空位留白）。

```python
compose_figure(
    panels=["a.pdf", "b.pdf", "c.pdf"],
    layout="auto",  # 3 个 → 2x2 网格，右下角留空
    output="figure.pdf", labels=True,
)
```

### `custom`
每个 panel 单独指定位置和大小。`panels` 参数需为 dict 列表。

```python
compose_figure(
    panels=[
        {"file": "a.pdf", "x": 50, "y": 400, "width": 200, "height": 150},
        {"file": "b.pdf", "x": 270, "y": 400, "width": 200, "height": 150},
    ],
    layout="custom",
    output="figure.pdf", labels=True,
)
```

### `mixed`
部分 panel 按网格排，部分按自定义位置排。通过 `grid_panels` / `custom_panels` 控制。

```python
compose_figure(
    panels=["a.pdf", "b.pdf", "c.pdf", "d.pdf", "big.pdf"],
    layout="mixed",
    grid_panels=4,  # 前 4 个按网格
    grid_rows=2, grid_cols=2,
    custom_panels=[
        {"index": 4, "x": 50, "y": 50, "width": 500, "height": 200},  # 第 5 个自定义
    ],
    output="figure.pdf", labels=True,
)
```

---

## Supported Input Formats

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | .pdf | 取首页，矢量渲染 |
| PNG | .png | 读取像素，保留 DPI 元信息 |
| JPEG | .jpg / .jpeg | 同上 |
| TIFF | .tiff / .tif | 同上 |
| BMP | .bmp | 同上 |
| GIF | .gif | 同上 |

所有格式可混合使用，图片会自动等比缩放并居中。

---

## CLI

```bash
# 自动布局
python scripts/compose.py output.pdf panel1.pdf panel2.png panel3.jpg

# 指定网格
python scripts/compose.py output.pdf --grid 2 3 panel1.pdf panel2.png ...
```

---

## Notes

- PDF 渲染通过 PyMuPDF (fitz)，图片通过 Pillow
- 图片尺寸按 DPI 元信息转换为 pt，无 DPI 信息时默认 72 DPI
- 标签默认放在 panel 左上角外侧，可通过 `label_offset` 调整
- 页面尺寸默认 A4，投稿时可能需要 Letter 或自定义尺寸
- 自定义布局时坐标原点在页面左下角（PDF 标准坐标系）
- panel 原始尺寸与目标不一致时自动等比缩放并居中
- `json_layout` 参数优先级最高，传入后会忽略 `layout` / `rows` / `cols` 等参数

---

## 与其他工具配合

Panel Composer 解决的是"快速把多个 panel 拼成一张图"的重复劳动——比你在专业软件里一个个打开、对齐、导出要快得多。

但如果你的场景需要更精细的个性化排版（比如复杂的标注系统、品牌化设计、特殊视觉效果、印刷级色彩管理等），建议：

1. **用 Panel Composer 快速出初版** — 确定 panel 位置、大小、标签
2. **导出为 PDF 或 PNG** — 保留矢量或高分辨率
3. **在专业软件中继续打磨**：
   - **Affinity Designer / Adobe Illustrator** — 矢量编辑、精细标注、品牌配色
   - **Adobe Photoshop** — 位图处理、色彩校正、特殊效果
   - **Inkscape**（免费）— 开源矢量编辑

这样你省掉了最耗时的"对齐和定位"环节，把精力集中在真正需要手工调整的细节上。

---

## Troubleshooting

**Q: Panel 被拉伸变形？**  
A: 不会。本工具始终保留 panel 原始宽高比，无论画布拖拽或 custom 布局指定的尺寸如何，内容都等比缩放居中。如果指定区域比例与原图不一致，周围会自动留白。

**Q: 标签被裁切**  
A: 增大 `margin` 或调整 `label_offset`。

**Q: PNG 输出模糊**  
A: 提高 `dpi` 参数（默认 300，投稿建议 300-600）。

**Q: 图片尺寸异常**  
A: 部分图片无 DPI 元信息，默认按 72 DPI 换算。可用 `custom` 布局手动指定尺寸。
