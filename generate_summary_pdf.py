from pathlib import Path
import re
import textwrap

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "reportlab is required. Install it with: pip install reportlab"
    ) from exc

ROOT = Path(__file__).resolve().parent
MD_PATH = ROOT / "Kolo_Joshua_301905772_FinalSummary.md"
PDF_PATH = ROOT / "Kolo_Joshua_301905772_FinalSummary.pdf"


def clean_text(raw: str) -> list[str]:
    cleaned: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            cleaned.append(stripped[2:])
        elif stripped.startswith("## "):
            cleaned.append(stripped[3:])
        elif stripped.startswith("- "):
            cleaned.append("- " + stripped[2:])
        elif stripped.startswith("!["):
            cleaned.append(stripped)
        else:
            cleaned.append(stripped)
    return cleaned


def draw_markdown_image(c, markdown_path: Path, line: str, y: float) -> float:
    match = re.search(r"!\[[^\]]*\]\(([^)]+)\)", line)
    if not match:
        return y

    image_rel = match.group(1).strip()
    image_path = (markdown_path.parent / image_rel).resolve()
    if not image_path.exists():
        return y

    if y < 160:
        c.showPage()
        y = 760

    img = ImageReader(str(image_path))
    width, height = img.getSize()
    max_width = 440
    scale = min(1.0, max_width / width)
    draw_width = width * scale
    draw_height = height * scale
    x = (612 - draw_width) / 2
    c.drawImage(img, x, y - draw_height, width=draw_width, height=draw_height, preserveAspectRatio=True)
    return y - draw_height - 20


def render_pdf(markdown_path: Path, pdf_path: Path) -> None:
    text = markdown_path.read_text(encoding="utf-8")
    lines = clean_text(text)

    c = canvas.Canvas(str(pdf_path), pagesize=(612, 792))
    c.setTitle("MIT 8103 Advanced Database Systems")
    c.setAuthor("Joshua Kolo")

    y = 760
    left_margin = 54
    wrap_width = 90

    for line in lines:
        if re.search(r"!\[[^\]]*\]\(([^)]+)\)", line):
            y = draw_markdown_image(c, markdown_path, line, y)
            continue

        if y < 60:
            c.showPage()
            y = 760

        if line.startswith("- "):
            text_lines = textwrap.wrap(line, width=wrap_width, subsequent_indent="  ")
        else:
            text_lines = textwrap.wrap(line, width=wrap_width)

        for chunk in text_lines:
            if y < 60:
                c.showPage()
                y = 760
            c.drawString(left_margin, y, chunk)
            y -= 18

        y -= 6

    c.save()


if __name__ == "__main__":
    render_pdf(MD_PATH, PDF_PATH)
    print(f"Created {PDF_PATH}")
