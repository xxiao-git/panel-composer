#!/usr/bin/env python3
"""Panel Composer — 将多个 PDF/图片 panel 组合成一张大图。

支持输入: PDF, PNG, JPG/JPEG, TIFF, BMP
支持 grid / auto / custom / mixed 四种布局，可加标签、边框、间距。
输出 PDF（矢量）或 PNG（光栅化）。

依赖: pip install reportlab PyMuPDF pypdf Pillow
"""

import math, os, sys, tempfile
from pathlib import Path
from typing import List, Union, Optional, Tuple

try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.utils import ImageReader as RLImageReader
except ImportError:
    raise ImportError("pip install reportlab")

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("pip install PyMuPDF")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise ImportError("pip install Pillow")

# 支持的图片格式
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".gif"}

def is_image(path: str) -> bool:
    """判断文件是否为支持的图片格式。"""
    return Path(path).suffix.lower() in IMAGE_EXTENSIONS

def is_pdf(path: str) -> bool:
    """判断文件是否为 PDF。"""
    return Path(path).suffix.lower() == ".pdf"

# ── 页面尺寸 ─────────────────────────────────────────────
PAGE_SIZES = {
    "a4": A4,           # (595.28, 841.89)
    "a3": (841.89, 1190.55),
    "a5": (419.53, 595.28),
    "letter": letter,   # (612, 792)
}

def resolve_page_size(name_or_tuple):
    if isinstance(name_or_tuple, (list, tuple)) and len(name_or_tuple) == 2:
        return tuple(name_or_tuple)
    key = str(name_or_tuple).lower()
    if key in PAGE_SIZES:
        return PAGE_SIZES[key]
    raise ValueError(f"Unknown page size: {name_or_tuple}")

# ── 文件类型检测 ─────────────────────────────────────────

# ── 尺寸获取 ─────────────────────────────────────────────
def get_panel_dims(path: str) -> Tuple[float, float]:
    """获取 panel 原始尺寸（pt）。
    PDF: 从 fitz 读取。
    图片: 按 72 DPI 将像素转为 pt (px / dpi * 72)。
    """
    if is_pdf(path):
        doc = fitz.open(path)
        page = doc[0]
        w, h = page.rect.width, page.rect.height
        doc.close()
        return w, h
    elif is_image(path):
        img = Image.open(path)
        pw, ph = img.size  # pixels
        # 图片可能有 DPI 信息
        dpi_info = img.info.get("dpi", (72, 72))
        dpi_x, dpi_y = dpi_info if dpi_info[0] > 0 and dpi_info[1] > 0 else (72, 72)
        # 转为 pt: pt = pixels / dpi * 72
        w_pt = pw / dpi_x * 72
        h_pt = ph / dpi_y * 72
        img.close()
        return w_pt, h_pt
    else:
        raise ValueError(f"不支持的文件格式: {path}")

# ── 渲染为 PIL Image ─────────────────────────────────────
def panel_to_pil(path: str, target_w: float, target_h: float, dpi: int = 600) -> Image.Image:
    """将 PDF/图片 渲染为 PIL Image，等比缩放到 target_w x target_h (pt)。"""
    if is_pdf(path):
        orig_w, orig_h = get_panel_dims(path)
        scale = min(target_w / orig_w, target_h / orig_h)
        zoom = scale * dpi / 72.0
        doc = fitz.open(path)
        page = doc[0]
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        doc.close()
        return img
    elif is_image(path):
        img = Image.open(path).convert("RGB")
        # 计算目标像素
        target_px_w = int(target_w * dpi / 72)
        target_px_h = int(target_h * dpi / 72)
        # 等比缩放
        img.thumbnail((target_px_w, target_px_h), Image.Resampling.LANCZOS)
        return img
    else:
        raise ValueError(f"不支持的文件格式: {path}")

# ── 标签生成 ─────────────────────────────────────────────
def make_labels(n: int, style: str) -> List[Optional[str]]:
    if style == "uppercase":
        return [chr(65 + i) for i in range(n)]
    elif style == "lowercase":
        return [chr(97 + i) for i in range(n)]
    elif style == "numeric":
        return [str(i + 1) for i in range(n)]
    return [None] * n

# ── 布局计算 ─────────────────────────────────────────────
def calc_grid_positions(n, rows, cols, page_w, page_h, margin, spacing):
    avail_w = page_w - 2 * margin
    avail_h = page_h - 2 * margin
    cell_w = (avail_w - (cols - 1) * spacing) / cols
    cell_h = (avail_h - (rows - 1) * spacing) / rows
    positions = []
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= n:
                break
            x = margin + c * (cell_w + spacing)
            y = page_h - margin - (r + 1) * cell_h - r * spacing  # PDF 坐标：左下为原点
            positions.append((x, y, cell_w, cell_h))
            idx += 1
    return positions

# ── 核心函数 ─────────────────────────────────────────────
def compose_figure(
    panels,
    layout="auto",
    rows=None,
    cols=None,
    output="figure_combined.pdf",
    dpi=300,
    labels=False,
    label_style="uppercase",
    label_font_size=14,
    label_offset=(-18, -18),
    margin=36,
    spacing=12,
    page_size="a4",
    background_color="white",
    grid_panels=None,
    custom_panels=None,
    json_layout=None,
):
    """
    将多个 PDF/图片 panel 组合成一张大图。

    Parameters
    ----------
    panels : list
        文件路径列表 (str)，支持 PDF/PNG/JPG/TIFF/BMP，可混合。
        自定义布局时为 dict 列表:
        {"file": str, "x": float, "y": float, "width": float, "height": float}
    layout : str
        "grid" | "auto" | "custom" | "mixed"
    rows, cols : int
        网格行列数（layout=grid 时必填）
    output : str
        输出路径（.pdf 或 .png）
    dpi : int
        PNG 输出分辨率（默认 300）
    labels : bool
        是否添加标签
    label_style : str
        "uppercase" | "lowercase" | "numeric"
    label_font_size : int
        标签字号 (pt)
    label_offset : tuple
        标签相对 panel 左上角的偏移 (x, y) pt
    margin : int
        页面外边距 (pt)，默认 36 = 0.5 inch
    spacing : int
        panel 间距 (pt)
    page_size : str | tuple
        "a4" | "letter" | (w, h)
    background_color : str
        PNG 背景色
    json_layout : str | dict | None
        JSON 布局文件路径 (str) 或 dict。格式:
        {"page_size": "a4", "margin": 36,
         "panels": [{"label": "A", "x": 50, "y": 400, "width": 200, "height": 150}, ...]}
        传入后 panels 列表按顺序对应 JSON 中的 panel 定义。
        layout / rows / cols 等参数会被忽略。
    """
    output_path = Path(output)
    is_png = output_path.suffix.lower() == ".png"

    # ── JSON 布局模式（优先级最高）──
    if json_layout is not None:
        import json
        if isinstance(json_layout, str):
            with open(json_layout, 'r', encoding='utf-8') as f:
                jdata = json.load(f)
        else:
            jdata = json_layout

        page_size = jdata.get("page_size", page_size)
        margin = jdata.get("margin", margin)
        jpanels = jdata.get("panels", [])
        n = len(jpanels)

        page_w, page_h = resolve_page_size(page_size)
        entries = []
        for i, jp in enumerate(jpanels):
            if i >= len(panels):
                break
            entries.append((
                jp["x"], jp["y"], jp["width"], jp["height"],
                jp.get("label"), panels[i]
            ))
    else:
        page_w, page_h = resolve_page_size(page_size)
        n = len(panels)

        # 生成标签
        if labels:
            label_list = make_labels(n, label_style)
        else:
            label_list = [None] * n

        # 计算每个 panel 的位置: (x, y, w, h)
        entries = []  # (x, y, w, h, label, file_path)

        if layout in ("grid", "auto"):
            if layout == "auto":
                cols = math.ceil(math.sqrt(n))
                rows = math.ceil(n / cols)
            if not rows or not cols:
                raise ValueError("grid/auto 布局需要 rows 和 cols")
            positions = calc_grid_positions(n, rows, cols, page_w, page_h, margin, spacing)
            for i, (x, y, w, h) in enumerate(positions):
                entries.append((x, y, w, h, label_list[i], panels[i]))

        elif layout == "custom":
            if not isinstance(panels[0], dict):
                raise ValueError("custom 布局需要 panels 为 dict 列表")
            for i, p in enumerate(panels):
                entries.append((p["x"], p["y"], p["width"], p["height"], label_list[i], p["file"]))

        elif layout == "mixed":
            # 先排 grid 部分
            gp = grid_panels if grid_panels else n - (len(custom_panels) or 0)
            gr = rows or math.ceil(math.sqrt(gp))
            gc = cols or math.ceil(gp / gr)
            positions = calc_grid_positions(gp, gr, gc, page_w, page_h, margin, spacing)
            for i, (x, y, w, h) in enumerate(positions):
                entries.append((x, y, w, h, label_list[i], panels[i]))
            # 再排 custom 部分
            if custom_panels:
                for cp in custom_panels:
                    idx = cp["index"]
                    entries.append((cp["x"], cp["y"], cp["width"], cp["height"],
                                    label_list[idx], panels[idx]))
        else:
            raise ValueError(f"未知布局: {layout}")

    # ── 输出 PDF ──
    if not is_png:
        c = rl_canvas.Canvas(str(output_path), pagesize=(page_w, page_h))
        for x, y, w, h, label, file_path in entries:
            orig_w, orig_h = get_panel_dims(file_path)
            scale = min(w / orig_w, h / orig_h)
            rw, rh = orig_w * scale, orig_h * scale
            ox = x + (w - rw) / 2
            oy = y + (h - rh) / 2

            # 渲染为 PIL Image 再写入 PDF
            img = panel_to_pil(file_path, rw, rh, dpi=600)
            tmp_fd, tmp_path = tempfile.mkstemp(suffix=".png")
            os.close(tmp_fd)
            img.save(tmp_path, dpi=(600, 600))
            c.drawImage(tmp_path, ox, oy, width=rw, height=rh)
            os.unlink(tmp_path)

            if label:
                c.setFont("Helvetica-Bold", label_font_size)
                c.setFillColor("black")
                c.drawString(x + label_offset[0], y + h - label_offset[1], label)
        c.save()

    # ── 输出 PNG ──
    else:
        scale = dpi / 72.0
        img_w, img_h = int(page_w * scale), int(page_h * scale)
        composite = Image.new("RGB", (img_w, img_h), background_color)

        for x, y, w, h, label, file_path in entries:
            orig_w, orig_h = get_panel_dims(file_path)
            scale_fit = min(w / orig_w, h / orig_h)
            rw, rh = orig_w * scale_fit, orig_h * scale_fit
            ox = (w - rw) / 2
            oy = (h - rh) / 2

            img = panel_to_pil(file_path, rw, rh, dpi=dpi)
            # PDF 坐标左下原点 → 图像坐标左上原点
            px = int((x + ox) * scale)
            py = int((page_h - y - oy - rh) * scale)
            composite.paste(img, (px, py))

            if label:
                draw = ImageDraw.Draw(composite)
                try:
                    font = ImageFont.truetype("arial.ttf", int(label_font_size * scale))
                except Exception:
                    font = ImageFont.load_default()
                lx = int((x + label_offset[0]) * scale)
                ly = int((page_h - y - h + label_offset[1]) * scale)
                draw.text((lx, ly), label, fill="black", font=font)

        composite.save(str(output_path), dpi=(dpi, dpi))

    print(f"✓ 组图完成: {output_path.resolve()}")
    return str(output_path.resolve())


# ── CLI ──────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法:")
        print("  python compose.py <output> <panel1> [panel2 ...]")
        print("  python compose.py <output> --grid 2 2 <panel1> ...")
        print("  支持输入: PDF, PNG, JPG, TIFF, BMP（可混合）")
        sys.exit(1)

    output = sys.argv[1]
    rest = sys.argv[2:]

    if rest[0] == "--grid":
        r, c_ = int(rest[1]), int(rest[2])
        panels = rest[3:]
        compose_figure(panels, layout="grid", rows=r, cols=c_, output=output, labels=True)
    else:
        compose_figure(rest, layout="auto", output=output, labels=True)
