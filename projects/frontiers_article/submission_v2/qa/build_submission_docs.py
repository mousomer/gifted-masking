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
SUBMISSION = ROOT / "projects/frontiers_article/submission_v2"
SOURCE = ROOT / "projects/frontiers_article/ARTICLE_V2_LID_MANUSCRIPT_DRAFT.md"
SUPPLEMENT_SOURCE = ROOT / "projects/frontiers_article/ARTICLE_V2_LID_SUPPLEMENTARY_METHODS.md"
FIGURES = ROOT / "projects/frontiers_article/v2_figures/figures"
PANDOC = Path("/opt/homebrew/bin/pandoc")

ANON_MD = SUBMISSION / "manuscript/ARTICLE_V2_LID_Anonymized_Manuscript_SOURCE.md"
ANON_DOCX = SUBMISSION / "manuscript/ARTICLE_V2_LID_Anonymized_Manuscript_BLOCKED_PREVIEW.docx"
TITLE_MD = SUBMISSION / "manuscript/ARTICLE_V2_LID_Title_Page_SOURCE.md"
TITLE_DOCX = SUBMISSION / "manuscript/ARTICLE_V2_LID_Title_Page_PENDING_CONFIRMATION.docx"
SUPP_MD = SUBMISSION / "supplement/ARTICLE_V2_LID_Supplementary_Methods_SOURCE.md"
SUPP_DOCX = SUBMISSION / "supplement/ARTICLE_V2_LID_Supplementary_Methods.docx"
HIGHLIGHTS_MD = SUBMISSION / "manuscript/ARTICLE_V2_LID_Highlights.md"
HIGHLIGHTS_DOCX = SUBMISSION / "manuscript/ARTICLE_V2_LID_Highlights.docx"


FIGURE_FILES = {
    1: FIGURES / "Figure_1_underidentification_architecture.png",
    2: FIGURES / "Figure_2_history_and_action_representation.png",
    3: FIGURES / "Figure_3_persistent_state_and_disagreement.png",
    4: FIGURES / "Figure_4_discoverability_and_boundary_displacement.png",
}


def section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.index(heading) + len(heading)
    end = text.index(next_heading, start) if next_heading else len(text)
    return text[start:end].strip()


def anonymized_markdown(source: str) -> str:
    lines = source.splitlines()
    abstract_index = lines.index("## Abstract")
    lines = [lines[0], "", *lines[abstract_index:]]

    output: list[str] = []
    skip_declarations = False
    replace_data = False
    pending_figure: int | None = None

    for line in lines:
        if line == "# Funding":
            skip_declarations = True
            continue
        if skip_declarations and line == "# Data, code, and supplementary materials":
            skip_declarations = False
            replace_data = True
            output.extend(
                [
                    "# Data and Code Availability",
                    "",
                    "The public source repository and persistent E01-E05 evidence archive "
                    "are identified on the separate title page and will be restored here "
                    "after double-anonymized review. The archived outputs are "
                    "content-addressed and artifact-verified. The exact historical generator "
                    "states for E01-E03 were not recovered; those results are supported by "
                    "verified artifacts, configurations, manifests, and validation records "
                    "rather than a claim of bit-identical regeneration from current code.",
                    "",
                ]
            )
            continue
        if skip_declarations:
            continue
        if replace_data:
            if line == "# References":
                replace_data = False
                output.append(line)
            continue

        if line.startswith("**Keywords:**"):
            line = (
                "**Keywords:** giftedness; ability concealment; reinforcement learning; "
                "social feedback; individual differences"
            )

        line = line.replace("Cross et al., 1993", "T. L. Cross et al., 1993")
        line = line.replace("Cross et al., 2019", "J. R. Cross et al., 2019")
        output.append(line)

        match = re.match(r"## Figure ([1-4])\.", line)
        if match:
            pending_figure = int(match.group(1))
            continue
        if pending_figure is not None and line and not line.startswith("#"):
            figure_path = FIGURE_FILES[pending_figure]
            # Quote the Pandoc image width.  Unquoted values are rendered by
            # LibreOffice as a literal split field (``{width=...}``) around
            # the image in the generated DOCX/PDF.
            output.extend(["", f'![]({figure_path}){{width="6.5in"}}', ""])
            pending_figure = None

    return "\n".join(output).rstrip() + "\n"


def title_page_markdown(source: str) -> str:
    lines = source.splitlines()
    front = lines[:10]
    title = front[0][2:]
    authors = front[2].replace("¹", "^a^").replace("²", "^b^")
    affil_a = front[4].replace("¹", "^a^")
    affil_b = front[6].replace("²", "^b^")
    corresponding = front[8]

    funding = section(source, "# Funding", "# CRediT authorship contribution statement")
    credit = section(
        source,
        "# CRediT authorship contribution statement",
        "# Declaration of competing interests",
    )
    interests = section(
        source,
        "# Declaration of competing interests",
        "# Acknowledgements",
    )
    acknowledgements = section(
        source,
        "# Acknowledgements",
        "# Data, code, and supplementary materials",
    ).replace("Mary Jane**,**", "Mary Jane,")

    return "\n".join(
        [
            f"# {title}",
            "",
            "**Article type:** Full length article",
            "",
            authors,
            "",
            affil_a,
            "",
            affil_b,
            "",
            corresponding,
            "",
            "# Funding",
            "",
            funding,
            "",
            "# CRediT authorship contribution statement",
            "",
            credit.replace("Writing Original Draft", "Writing - original draft")
            .replace("Writing Review & Editing", "Writing - review and editing"),
            "",
            "# Declaration of competing interests",
            "",
            interests,
            "",
            "# Acknowledgements",
            "",
            acknowledgements,
            "",
        ]
    )


def highlights_markdown() -> str:
    bullets = [
        "Observed concealment does not uniquely identify its generating process.",
        "Early adverse feedback reduced later sampling, not final masking.",
        "Action and context representation changed what learners discovered.",
        "Learned masking shifted before the environmental cost crossover.",
    ]
    for bullet in bullets:
        if len(bullet) > 85:
            raise ValueError(f"Highlight exceeds 85 characters: {bullet}")
    return "# Highlights\n\n" + "\n".join(f"- {bullet}" for bullet in bullets) + "\n"


def pandoc_docx(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(PANDOC),
            "--from=markdown+tex_math_dollars",
            "--to=docx",
            "--standalone",
            f"--resource-path={ROOT}",
            "--output",
            str(output),
            str(source),
        ],
        check=True,
    )


def set_run_font(run, name: str = "Times New Roman", size: float | None = None) -> None:
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    if size is not None:
        run.font.size = Pt(size)


def add_page_number(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Page ")
    set_run_font(run, size=10)
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
    field_run = paragraph.add_run()
    field_run._r.extend([begin, instr, separate, text, end])
    set_run_font(field_run, size=10)


def style_docx(path: Path, *, anonymous: bool, title_page: bool = False) -> None:
    doc = Document(path)
    props = doc.core_properties
    if anonymous:
        props.author = ""
        props.last_modified_by = ""
        props.comments = ""
        props.subject = ""
    props.title = doc.paragraphs[0].text if doc.paragraphs else ""

    for section_obj in doc.sections:
        section_obj.start_type = WD_SECTION_START.NEW_PAGE
        section_obj.page_width = Inches(8.5)
        section_obj.page_height = Inches(11)
        section_obj.top_margin = Inches(1)
        section_obj.bottom_margin = Inches(1)
        section_obj.left_margin = Inches(1)
        section_obj.right_margin = Inches(1)
        section_obj.header_distance = Inches(0.5)
        section_obj.footer_distance = Inches(0.5)
        footer = section_obj.footer
        footer.paragraphs[0].clear()
        add_page_number(footer.paragraphs[0])

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Times New Roman")
    normal._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0 if title_page else 2.0

    for style_name, size in (("Title", 14), ("Heading 1", 12), ("Heading 2", 12), ("Heading 3", 12)):
        style = doc.styles[style_name]
        style.font.name = "Times New Roman"
        style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Times New Roman")
        style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Times New Roman")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.0

    in_references = False
    for index, paragraph in enumerate(doc.paragraphs):
        if index == 0:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.space_after = Pt(12)
        if paragraph.text.strip() in {"References", "Supplement reference"}:
            in_references = True
        elif in_references and paragraph.style.name.startswith("Heading"):
            in_references = False
        if in_references and not paragraph.style.name.startswith("Heading"):
            paragraph.paragraph_format.left_indent = Inches(0.5)
            paragraph.paragraph_format.first_line_indent = Inches(-0.5)
            paragraph.paragraph_format.line_spacing = 1.0
            paragraph.paragraph_format.space_after = Pt(6)
        for run in paragraph.runs:
            if run.font.name != "Courier New":
                set_run_font(run, size=12)

    for table in doc.tables:
        table.autofit = True
        for row_index, row in enumerate(table.rows):
            if row_index == 0:
                tr_pr = row._tr.get_or_add_trPr()
                tbl_header = OxmlElement("w:tblHeader")
                tbl_header.set(qn("w:val"), "true")
                tr_pr.append(tbl_header)
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.line_spacing = 1.0
                    paragraph.paragraph_format.space_after = Pt(2)
                    for run in paragraph.runs:
                        set_run_font(run, size=9.5)

    doc.save(path)


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    ANON_MD.write_text(anonymized_markdown(source), encoding="utf-8")
    TITLE_MD.write_text(title_page_markdown(source), encoding="utf-8")
    SUPP_MD.write_text(SUPPLEMENT_SOURCE.read_text(encoding="utf-8"), encoding="utf-8")
    HIGHLIGHTS_MD.write_text(highlights_markdown(), encoding="utf-8")

    for markdown, docx, anonymous, title_page in (
        (ANON_MD, ANON_DOCX, True, False),
        (TITLE_MD, TITLE_DOCX, False, True),
        (SUPP_MD, SUPP_DOCX, True, False),
        (HIGHLIGHTS_MD, HIGHLIGHTS_DOCX, True, False),
    ):
        pandoc_docx(markdown, docx)
        style_docx(docx, anonymous=anonymous, title_page=title_page)

    for path in (ANON_DOCX, TITLE_DOCX, SUPP_DOCX, HIGHLIGHTS_DOCX):
        print(path)


if __name__ == "__main__":
    main()
