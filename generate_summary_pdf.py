from pathlib import Path
import textwrap

try:
    from reportlab.pdfgen import canvas
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
            continue
        else:
            cleaned.append(stripped)
    return cleaned


def render_pdf(markdown_path: Path, pdf_path: Path) -> None:
    text = markdown_path.read_text(encoding="utf-8")
    lines = clean_text(text)

    c = canvas.Canvas(str(pdf_path), pagesize=(612, 792))
    c.setTitle("MIT 8103 Advanced Database Systems")
    c.setAuthor("Joshua Kolo")

    y = 760
    page_width = 612
    left_margin = 54
    wrap_width = 90

    for line in lines:
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
