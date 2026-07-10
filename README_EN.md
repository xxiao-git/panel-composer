English | [中文](README.md)

# Panel Composer

A general-purpose tool for combining multiple panels into a single figure.

Supports mixed PDF / PNG / JPG / TIFF / BMP inputs, with three layout modes: **AI auto-layout**, **visual canvas drag-and-drop**, and **natural-language conversation**.

**No coding required** — just describe what you want in a conversation, or drag on a canvas, and the composed figure is generated.

> 💡 **Highly recommended**: Although Panel Composer is not limited to any specific scenario, it is especially well suited for **researchers assembling figures for papers** — quickly combining scattered subfigures (panels) into a Figure (e.g., Figure 1A–F), sparing you the tedious per-panel alignment in Illustrator.

### 🎯 A powerful tool for scientific figure assembly

Although Panel Composer is not limited to any specific scenario, it is **especially well suited for researchers assembling figures for papers**:

- **Batch processing**: compose Figure 1–10 in one sentence, no manual per-file work
- **Vector PDF output**: publication-grade quality, no loss when scaled up
- **Aspect-ratio protection**: panel content is never stretched or distorted, meeting journal requirements
- **Labeling system**: automatically generates A/B/C or 1/2/3 labels
- **Fast iteration**: AI auto-layout → conversational tweaks → canvas fine-tuning, done in three steps
- **Integrates with pro tools**: export PDF, then refine further in Affinity / Illustrator

### 📦 Download

- **Latest (v0.6.0)**: [panel-composer-v0.6.0.zip](panel-composer-v0.6.0.zip)
- Or visit the [Releases page](https://github.com/xxiao-git/panel-composer/releases) for older versions

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Three Layout Modes](#three-layout-modes)
- [FAQ](#faq)
- [Advanced Usage](#advanced-usage)
- [API Reference](#api-reference)

---

## Installation

### Install via AI assistant (recommended)

If you use [WorkBuddy](https://www.codebuddy.cn/workbuddy), you can simply ask the AI to install it for you in a conversation:

**Install from GitHub:**

Just say in the conversation:

> "Install the panel-composer skill from GitHub, repo: https://github.com/xxiao-git/panel-composer"

Or:

> "Install skill https://github.com/xxiao-git/panel-composer"

The AI will clone the repo from GitHub and install it into your local skills directory.

**Install from a local zip package:**

If you have a packaged zip file, you can say in the conversation:

> "Install this skill package for me", then send the zip file to the AI

The AI will unzip and install it automatically.

**Once installed, you can use it directly in a conversation:**

> "Use panel-composer to combine these 4 PDFs into a 2x2 figure"

### Manual installation

If you don't use an AI assistant, you can also install manually:

1. Clone or download this repo
2. Copy the `panel-composer` folder into the WorkBuddy skills directory:
   - Windows: `C:\Users\<username>\.workbuddy\skills\panel-composer\`
   - macOS/Linux: `~/.workbuddy/skills/panel-composer/`
3. Install Python dependencies (one time only):

```bash
pip install reportlab PyMuPDF Pillow
```

### Requirements

- Python 3.7+
- Windows / macOS / Linux
- Dependencies: `reportlab`, `PyMuPDF`, `Pillow`

---

## Quick Start

After installation, just say in a conversation:

> "Combine a.pdf, b.pdf, c.pdf, d.pdf into a 2x2 figure, with labels"

The AI will automatically invoke the panel-composer skill, generate a 2x2 grid composition, and add A, B, C, D labels.

### Full workflow demo

The following walkthrough shows the complete flow from "a pile of scattered panels" to "one composed figure".

**Step 1: Your files**

Suppose you have a `FigureProduction` folder, with subfolders for each Figure, and each subfolder contains individual panels:

<img src="docs/01-figure-folders-overview.png" width="340" alt="Overview of Figure 1-5 folders">

**Step 2: Batch compose in one sentence**

No need to open folders one by one — just tell the AI which ones to combine:

> "Combine all images from Figure1 to Figure5 in FigureProduction"

The AI processes them all at once and generates five composed figures, Figure1–Figure5. This is the power of **batch processing** — you don't open each folder manually or combine one by one; one sentence does it all.

**Step 3: Understand the panel naming rule (using Figure 4 as an example)**

Panels in each Figure folder are named with letters (A, B, C, D...), and these letters become the labels on the composed figure:

<img src="docs/02-figure4-panels.png" width="410" alt="The 6 PDF panels in Figure 4 (4A to 4F)">

> **Note**: This step is only to help you understand how panels are named. In practice you don't need to open folders manually — the AI recognizes them automatically.

**You can even skip manual numbering**

If your panel filenames are like `result1.png`, `heatmap.pdf` — without A/B/C/D — that's perfectly fine. You don't need to open the images and number them by hand. Just let the AI decide the narrative order from the image content and rename automatically:

> "Based on the content of these images, order them by narrative logic and label them A, B, C, D automatically"

The AI reads what each image shows, decides which should come first and which later, and applies the labels automatically. You only say one sentence — numbering and ordering are both handled by the AI.

**Step 4: Auto-layout result**

Taking Figure 4 as an example, the 6 panels are auto-arranged into a 2x3 grid with A–F labels:

<img src="docs/04-output-result.png" width="486" alt="Auto-layout result">

**Step 5: Conversational tweaks (optional)**

If the default layout isn't to your liking, adjust it in natural language:

> "Adjust Figure4: first row AB, second row CD, third row EF"

The AI rearranges it into a 3x2 layout:

<img src="docs/05-dialogue-adjust-layout.png" width="340" alt="Result after conversational adjustment">

That's all. The whole workflow only requires you to talk — no coding, no manual file operations.

---

## Three Layout Modes

Panel Composer offers three layout modes for different scenarios. AI auto-layout is the default; switch when not satisfied.

### Method 1: AI auto-layout (default)

**When to use**: quick output, no need for precise position control.

**How**: just talk

> "Combine these 6 panels into one figure"

> "Auto-arrange a.pdf b.pdf c.pdf d.pdf"

The AI automatically picks the grid closest to a square based on panel count (e.g., 4 → 2x2, 6 → 2x3) and outputs the composition.

---

### Method 2: HTML canvas layout (visual drag-and-drop)

**When to use**: you need precise control over each panel's position and size, but don't want to use pro software or write code.

**Walkthrough**:

1. Say "adjust using the html method" in the conversation, and the AI opens the canvas:

<img src="docs/06-html-canvas-instruction.png" width="480" alt="Conversation triggers the canvas">

2. Canvas interface: page size / label style / operation mode on the left, grid canvas on the right.

<img src="docs/07-html-canvas-interface.png" width="480" alt="Canvas interface">

3. Switch to "draw mode" (shortcut `D`), drag to draw rectangles on the canvas; each rectangle is auto-labeled A, B, C...

<img src="docs/08-html-canvas-dragged.png" width="490" alt="Layout after dragging">

4. After drawing, click "Copy JSON", send the JSON to the AI, and the AI generates the composition per your layout immediately:

<img src="docs/09-html-canvas-output.png" width="460" alt="Canvas layout output">

**Drag with confidence**: no matter what aspect ratio you draw, panel content always keeps its original aspect ratio and is never stretched. If the box ratio differs from the original, the image scales proportionally and centers within the box, leaving whitespace. You only care about position and rough size.

**Shortcuts**:
- `D` — switch to draw mode
- `S` — switch to select mode
- `Delete` — delete the selected panel

---

### Method 3: Conversational layout (natural-language description)

**When to use**: you're not happy with auto-layout but don't want to use the canvas. Just describe the layout you want in words.

**Examples**:

> "Top two A B side by side, bottom C spans the full row"

> "Left A takes half the height, right B C D stacked vertically"

> "A larger in top-left, B C D smaller in a column at bottom-right"

> "First row 3, second row 2 centered"

The AI understands your description, automatically computes each panel's position and size, and generates the composition.

---

## FAQ

### Q: Will panels be stretched or distorted?

**No**. In every layout mode, panel content always keeps its original aspect ratio, scaled proportionally and centered. If the target area ratio differs from the original, whitespace is added around it automatically.

### Q: What input formats are supported?

PDF, PNG, JPG, TIFF, BMP — can be mixed. For example, passing PDF and PNG together is handled automatically.

### Q: What is the output format?

PDF by default (vector, good for submission). You can also request PNG (rasterized, adjustable DPI):

> "Output PNG format, 600 DPI"

### Q: Can labels be customized?

Yes. Default is A, B, C, D..., but can be changed to 1, 2, 3, 4... or a, b, c, d...:

> "Change labels to numbers"

> "Use lowercase letters for labels"

You can also adjust label position and size:

> "Put labels at bottom-right"

> "Make labels a bit larger"

### Q: What is the JSON on the canvas?

JSON is the layout config exported by the canvas, containing each panel's position and size. You can save it and load it directly next time, without redrawing.

### Q: Can the page size be changed?

Yes. Default A4, but can be changed to Letter or A3:

> "Change page to Letter size"

### Q: Is the output vector or raster? Can I control it?

By default all PDF panels **stay vector** (lossless when scaled up, good for further editing in Affinity / Illustrator).

If a subfigure has especially many elements (e.g., a heatmap, scatter plot), you can rasterize it individually:

> "Rasterize the heatmap"

> "Panel C has too many elements, rasterize it"

> "Rasterize the 1st and 3rd panels"

You can also rasterize everything:

> "Rasterize all"

### Q: Can I add borders?

The current version does not support borders, but you can add them later in pro software (e.g., Affinity Designer, Adobe Illustrator).

---

## Advanced Usage

### Save and reuse layouts

If you often use a fixed layout (like 2x2, 1+3), ask the AI to save a layout template:

> "Save this layout as a template for future use"

Next time just say:

> "Compose using the 2x2 template"

### Working with other tools

Panel Composer solves the repetitive labor of "quickly combining multiple panels into one figure" — much faster than opening, aligning, and exporting them one by one in pro software.

But if your scenario needs finer, more personalized typesetting (e.g., complex annotation systems, branded design, special visual effects, print-grade color management), we recommend:

1. **Use Panel Composer for a quick first draft** — fix panel positions, sizes, labels
2. **Export as PDF** — preserve vector quality
3. **Refine in pro software**:
   - **Affinity Designer / Adobe Illustrator** — vector editing, fine annotations, brand colors
   - **Adobe Photoshop** — raster processing, color correction, special effects
   - **Inkscape** (free) — open-source vector editing

This way you skip the most time-consuming "alignment and positioning" step and focus your energy on the details that truly need manual adjustment.

---

## API Reference

> The following is for developers who need to call the Python API directly. Ordinary users can ignore it.

### Basic call

```python
from compose import compose_figure

compose_figure(
    panels=["a.pdf", "b.png", "c.jpg"],
    output="figure.pdf",
    labels=True,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `panels` | list | **required** | list of file paths (PDF/PNG/JPG/TIFF/BMP, mixable) |
| `output` | str | **required** | output file path (`.pdf` or `.png`) |
| `layout` | str | `"auto"` | `grid` / `auto` / `custom` / `mixed` |
| `rows` / `cols` | int | None | grid rows/cols (required when `layout="grid"`) |
| `json_layout` | str/dict | None | JSON layout file or dict (highest priority) |
| `page_size` | str/tuple | `"a4"` | `"a4"` / `"letter"` / `"a3"` / `"a5"` / `(w, h)` |
| `margin` | int | 36 | outer margin (pt) |
| `spacing` | int | 12 | panel gap (pt) |
| `labels` | bool | False | whether to add labels |
| `label_style` | str | `"uppercase"` | `uppercase` (A,B,C) / `numeric` (1,2,3) / `lowercase` (a,b,c) |
| `label_font_size` | int | 14 | label font size (pt) |
| `label_offset` | tuple | `(-18, -18)` | label offset `(x, y)` (pt) |
| `dpi` | int | 300 | PNG resolution |
| `background_color` | str | `"white"` | background color (applies to PNG output) |
| `rasterize` | bool/list | `False` | `False`=all vector; `True`=all raster (600 DPI); `[0,2]`=rasterize specified indices |

### JSON layout format

```json
{
  "page_size": "a4",
  "margin": 36,
  "panels": [
    {"label": "A", "x": 50, "y": 400, "width": 200, "height": 150},
    {"label": "B", "x": 270, "y": 400, "width": 200, "height": 150}
  ]
}
```

- `x`, `y`: bottom-left coordinates (PDF coordinate system, origin at page bottom-left)
- `width`, `height`: panel size (pt, 1 pt = 1/72 inch)

### CLI

```bash
python scripts/compose.py output.pdf panel1.pdf panel2.png panel3.jpg
python scripts/compose.py output.pdf --grid 2 3 panel1.pdf panel2.png ...
```

---

## License

MIT License

---

## Feedback & Support

Questions or suggestions? Feel free to open an Issue or PR.
