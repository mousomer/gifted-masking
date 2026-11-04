"""Build the human-review reading/editing copy of the Article V2 manuscript.

This is deliberately NOT the submission builder. It performs no anonymization,
strips no declarations, reduces no keywords, and adds no submission-system
placeholders. The manuscript source is used verbatim; the only transformation
is embedding the four frozen figure images beneath their existing captions.

Layout is tuned for manual annotation rather than journal typesetting.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[4]
ARTICLE = ROOT / "projects/frontiers_article"
SOURCE = ARTICLE / "ARTICLE_V2_LID_MANUSCRIPT_DRAFT.md"
FIGURES = ARTICLE / "v2_figures/figures"
REVIEW = ARTICLE / "submission_v2/review"
BUILD_MD = REVIEW / "_review_build.md"
DOCX = REVIEW / "ARTICLE_V2_LID_CURRENT_REVIEW_DRAFT.docx"
PDF = REVIEW / "ARTICLE_V2_LID_CURRENT_REVIEW_DRAFT.pdf"
PANDOC = "/opt/homebrew/bin/pandoc"

FIGURE_FILES = {
    1: FIGURES / "Figure_1_underidentification_architecture.png",
    2: FIGURES / "Figure_2_history_and_action_representation.png",
    3: FIGURES / "Figure_3_persistent_state_and_disagreement.png",
    4: FIGURES / "Figure_4_discoverability_and_boundary_displacement.png",
}

# Emitted per output format: pandoc drops the block that does not match.
PAGE_BREAK = [
    "",
    "```{=latex}",
    r"\clearpage",
    "```",
    "",
    "```{=openxml}",
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>',
    "```",
    "",
]

BODY_PT = 11.5
LINE_SPACING = 1.5


def review_markdown(source: str) -> str:
    """Manuscript verbatim, with each figure image placed under its caption."""
    output: list[str] = []
    pending: int | None = None
    for line in source.splitlines():
        match = re.match(r"## Figure ([1-4])\.", line)
        if match:
            # Start each figure caption on a fresh page so the caption and its
            # image are never split across a page break, and so there is room
            # to annotate beside the figure.
            output.extend(PAGE_BREAK)
            output.append(line)
            pending = int(match.group(1))
            continue
        output.append(line)
        if pending is not None and line and not line.startswith("#"):
            path = FIGURE_FILES[pending]
            if not path.is_file():
                raise SystemExit(f"missing figure image: {path}")
            output.extend(["", f'![]({path}){{width="6.2in"}}', ""])
            pending = None
    return "\n".join(output).rstrip() + "\n"


def set_run_font(run, name: str = "Times New Roman", size: float | None = None) -> None:
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    for tag in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rpr.rFonts.set(qn(tag), name)
    if size is not None:
        run.font.size = Pt(size)


def add_page_number(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run = paragraph.add_run()
    run._r.extend([begin, instr, separate, text, end])
    set_run_font(run, size=10)


def style_docx(path: Path) -> None:
    doc = Document(path)
    doc.core_properties.title = doc.paragraphs[0].text if doc.paragraphs else ""

    for sec in doc.sections:
        sec.start_type = WD_SECTION_START.NEW_PAGE
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
        sec.top_margin = sec.bottom_margin = Inches(1)
        sec.left_margin = Inches(1.1)
        sec.right_margin = Inches(1.1)
        sec.footer_distance = Inches(0.5)
        sec.footer.paragraphs[0].clear()
        add_page_number(sec.footer.paragraphs[0])

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    rpr = normal._element.get_or_add_rPr()
    for tag in ("w:ascii", "w:hAnsi"):
        rpr.rFonts.set(qn(tag), "Times New Roman")
    normal.font.size = Pt(BODY_PT)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = LINE_SPACING
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for name, size in (("Title", 16), ("Heading 1", 13.5), ("Heading 2", 12), ("Heading 3", 11.5)):
        style = doc.styles[name]
        style.font.name = "Times New Roman"
        srpr = style._element.get_or_add_rPr()
        for tag in ("w:ascii", "w:hAnsi"):
            srpr.rFonts.set(qn(tag), "Times New Roman")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.space_before = Pt(16)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.15

    in_refs = False
    for index, para in enumerate(doc.paragraphs):
        if index == 0:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.space_after = Pt(14)
        if para.text.strip() == "References":
            in_refs = True
        elif in_refs and para.style.name.startswith("Heading"):
            in_refs = False
        if in_refs and not para.style.name.startswith("Heading"):
            para.paragraph_format.left_indent = Inches(0.5)
            para.paragraph_format.first_line_indent = Inches(-0.5)
            para.paragraph_format.line_spacing = 1.15
            para.paragraph_format.space_after = Pt(8)
        for run in para.runs:
            if run.font.name != "Courier New":
                set_run_font(run, size=BODY_PT)

    for table in doc.tables:
        table.autofit = True
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    para.paragraph_format.line_spacing = 1.0
                    para.paragraph_format.space_after = Pt(2)
                    for run in para.runs:
                        set_run_font(run, size=10)

    doc.save(path)


def main() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    BUILD_MD.write_text(review_markdown(SOURCE.read_text(encoding="utf-8")), encoding="utf-8")

    subprocess.run([
        PANDOC, "--from=markdown+tex_math_dollars", "--to=docx", "--standalone",
        f"--resource-path={ROOT}", "--output", str(DOCX), str(BUILD_MD),
    ], check=True)
    style_docx(DOCX)

    subprocess.run([
        PANDOC, "--from=markdown+tex_math_dollars", "--to=pdf",
        "--pdf-engine=xelatex", f"--resource-path={ROOT}",
        "-V", "geometry:letterpaper,top=1in,bottom=1in,left=1.1in,right=1.1in",
        "-V", "fontsize=11pt", "-V", "mainfont=Times New Roman",
        "-V", "linestretch=1.5", "-V", "colorlinks=true", "-V", "urlcolor=black",
        "-V", "linkcolor=black",
        # Ragged-right with hyphenation suppressed: avoids the hyphenated title
        # and gives even word spacing, which reads better for hand annotation.
        "-V", r"header-includes=\AtBeginDocument{\raggedright}",
        "-V", r"header-includes=\hyphenpenalty=10000",
        "-V", r"header-includes=\exhyphenpenalty=10000",
        "--output", str(PDF), str(BUILD_MD),
    ], check=True)

    print(f"DOCX: {DOCX}")
    print(f"PDF : {PDF}")


if __name__ == "__main__":
    main()
