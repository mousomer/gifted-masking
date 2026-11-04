"""Build the single illustrated article without touching historical packages.

Markdown is the prose authority; Pandoc provides native editable Word equations.
python-docx applies presentation only. The skill renderer exports that exact DOCX
through bundled LibreOffice, then renders every PDF page for human inspection.

Run from any directory with the workspace virtual environment::

    /Users/omer/workspace/venvs/venv314/bin/python -B build_article.py

No simulations, estimates, scientific source edits, or dependency installs occur.
The metadata checks structure and provenance, not scientific or visual acceptance.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from zipfile import ZipFile

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from lxml import etree
from PIL import Image
from pypdf import PdfReader


ARTICLE_DIR = Path(__file__).resolve().parent
ROOT = ARTICLE_DIR.parents[2]
SOURCE = ARTICLE_DIR / "ARTICLE.md"
STEM = "integrated_article_20261004"
DOCX = ROOT / "output/docx" / f"{STEM}.docx"
PDF = ROOT / "output/pdf" / f"{STEM}.pdf"
METADATA = ARTICLE_DIR / "BUILD_METADATA.json"
PYTHON = Path("/Users/omer/workspace/venvs/venv314/bin/python")
PANDOC = Path("/opt/homebrew/bin/pandoc")
DEPENDENCIES = Path("/Users/omer/.cache/codex-runtimes/codex-primary-runtime/dependencies")
BUNDLED_BIN = DEPENDENCIES / "bin/override"
BUNDLED_SOFFICE = (
    DEPENDENCIES
    / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/MacOS/soffice"
)
RENDERER = Path(
    "/Users/omer/.codex/plugins/cache/openai-primary-runtime/documents/"
    "26.905.11957/skills/documents/render_docx.py"
)
BODY_PT = 11.0
FIGURE_WIDTH_IN = 6.2
FIGURE_MAX_HEIGHT_IN = 5.9
EXPECTED_STEMS = (
    "figure_01_overview", "figure_02_state_kernel", "figure_03_architectures",
    "figure_04_weighting_history_information", "figure_05_graded_engagement_intensity",
    "figure_06_dynamic_thresholds_persistence", "figure_07_dynamic_grid",
    "figure_08_sensitivity_matrix", "figure_09_context_encounter_sustained_use",
    "figure_10_learned_boundary_actual_masking",
)
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
CAPTION_RE = re.compile(r"^Figure\s+(\d+)\.")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(command, cwd=ROOT, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {command}\n{result.stdout}")
    return result.stdout


def inspect_source() -> tuple[str, list[Path]]:
    """Fail before building if figures or self-contained article structure drift."""
    source = SOURCE.read_text(encoding="utf-8")
    images = [ARTICLE_DIR / value.strip().strip("<>") for value in IMAGE_RE.findall(source)]
    if [path.stem for path in images] != list(EXPECTED_STEMS):
        raise ValueError("The article must contain the ten named figures once, in order")
    for path in images:
        if not path.is_file() or not path.resolve().is_relative_to(ARTICLE_DIR):
            raise ValueError(f"Missing or out-of-edition figure: {path}")
    captions = [int(value) for value in re.findall(r"^\*\*Figure (\d+)\.", source, re.M)]
    if captions != list(range(1, 11)):
        raise ValueError(f"Expected one explicit caption per figure; found {captions}")
    if re.search(r"(?:see|refer to|in the)\s+(?:the\s+)?Supplementary Methods", source, re.I):
        raise ValueError("Integrated article still depends on separate Supplementary Methods")
    if not re.search(r"^#{1,3}\s+.*Appendix", source, re.M | re.I):
        raise ValueError("Expected the technical appendix inside the article")
    if any(token in source for token in ("TODO", "TBD", ":codex-file-citation", "[INSERT")):
        raise ValueError("Unresolved placeholder or tool citation in article")
    return source, images


def set_font(target, size: float, *, bold: bool | None = None) -> None:
    target.font.name = "Times New Roman"
    target.font.size = Pt(size)
    target.font.color.rgb = RGBColor(0, 0, 0)
    if bold is not None:
        target.font.bold = bold
    rpr = target._element.get_or_add_rPr()
    fonts = rpr.rFonts
    for tag in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        fonts.set(qn(tag), "Times New Roman")
    for attr in list(fonts.attrib):
        if attr.endswith("Theme"):
            del fonts.attrib[attr]


def remove_borders(target) -> None:
    for element in list(target._element.iter(qn("w:pBdr"))):
        element.getparent().remove(element)


def page_number(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    run_element = OxmlElement("w:r")
    text = OxmlElement("w:t")
    text.text = "1"
    run_element.append(text)
    field.append(run_element)
    paragraph._p.append(field)
    paragraph.style = "Footer"


def normalize_overbar_accents(doc) -> int:
    """Represent literal overbar accents as native top bars, preserving math.

    Pandoc maps LaTeX ``\\bar`` to an OMML accent with spacing overline U+203E.
    Bundled LibreOffice renders that accent as an acute-looking mark. Its native
    ``m:bar`` top structure (also used for ``\\overline``) renders correctly and
    remains fully editable Word math. No base expression or other accent changes.
    """
    count = 0
    for accent in list(doc._element.xpath(".//m:acc")):
        props = accent.find(qn("m:accPr"))
        char = None if props is None else props.find(qn("m:chr"))
        if char is None or char.get(qn("m:val")) != "\u203e":
            continue
        expression = accent.find(qn("m:e"))
        if expression is None:
            raise ValueError("Overbar accent lacks its base expression")
        bar = OxmlElement("m:bar")
        bar_props = OxmlElement("m:barPr")
        position = OxmlElement("m:pos")
        position.set(qn("m:val"), "top")
        bar_props.append(position)
        control = props.find(qn("m:ctrlPr"))
        if control is not None:
            bar_props.append(deepcopy(control))
        bar.append(bar_props)
        bar.append(expression)
        accent.getparent().replace(accent, bar)
        count += 1
    return count


def style_tables(doc) -> None:
    for table in doc.tables:
        table.autofit = False
        widths = {2: [2.9, 3.3], 3: [1.4, 2.5, 2.3],
                  5: [1.78, .73, .65, 1.18, 1.86]}.get(
                      len(table.columns), [6.2 / len(table.columns)] * len(table.columns))
        for column, width in zip(table.columns, widths):
            column.width = Inches(width)
        props = table._tbl.tblPr
        borders = props.find(qn("w:tblBorders"))
        if borders is None:
            borders = OxmlElement("w:tblBorders")
            props.append(borders)
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            border = OxmlElement(f"w:{edge}")
            for key, value in (("val", "single"), ("sz", "4"), ("color", "D9D9D9")):
                border.set(qn(f"w:{key}"), value)
            borders.append(border)
        for row_index, row in enumerate(table.rows):
            row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
            if row_index == 0:
                header = OxmlElement("w:tblHeader")
                row._tr.get_or_add_trPr().append(header)
            for cell_index, (cell, width) in enumerate(zip(row.cells, widths)):
                cell.width = Inches(width)
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                cell_props = cell._tc.get_or_add_tcPr()
                margin = OxmlElement("w:tcMar")
                for edge in ("top", "left", "bottom", "right"):
                    value = OxmlElement(f"w:{edge}")
                    value.set(qn("w:w"), "90")
                    value.set(qn("w:type"), "dxa")
                    margin.append(value)
                cell_props.append(margin)
                if row_index == 0:
                    shade = OxmlElement("w:shd")
                    shade.set(qn("w:fill"), "EAEAEA")
                    cell_props.append(shade)
                for paragraph in cell.paragraphs:
                    paragraph.alignment = (WD_ALIGN_PARAGRAPH.CENTER
                                           if len(table.columns) == 5 and cell_index in (1, 2, 3)
                                           else WD_ALIGN_PARAGRAPH.LEFT)
                    paragraph.paragraph_format.space_before = Pt(2)
                    paragraph.paragraph_format.space_after = Pt(2)
                    paragraph.paragraph_format.line_spacing = 1.05
                    for run_element in paragraph.runs:
                        set_font(run_element, 10.0, bold=True if row_index == 0 else None)


def style_docx(path: Path, image_paths: list[Path]) -> dict:
    """Change presentation without replacing text or native math XML."""
    doc = Document(path)
    for name in ("Title", "Heading 1", "Heading 2", "Heading 3", "Caption", "Footer"):
        if name not in doc.styles:
            doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    doc.core_properties.title = doc.paragraphs[0].text
    doc.core_properties.subject = "Integrated scientific article on ability concealment and learning"
    # Preserve names supplied in the article itself; do not infer authorship.
    doc.core_properties.last_modified_by = ""
    for section in doc.sections:
        section.page_width, section.page_height = Inches(8.5), Inches(11)
        section.top_margin = section.bottom_margin = Inches(0.85)
        section.left_margin = section.right_margin = Inches(1.15)
        section.footer_distance = Inches(0.4)
        footer = section.footer.paragraphs[0]
        footer.clear()
        page_number(footer)
    normal = doc.styles["Normal"]
    set_font(normal, BODY_PT)
    normal.paragraph_format.line_spacing = 1.12
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.widow_control = True
    for name, size in (("Title", 17), ("Heading 1", 13), ("Heading 2", 11.5), ("Heading 3", 11)):
        style = doc.styles[name]
        set_font(style, size, bold=True)
        style.paragraph_format.space_before = Pt(13)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.05
        style.paragraph_format.keep_with_next = True
        remove_borders(style)
    for name in ("Body Text", "First Paragraph", "Compact"):
        if name in doc.styles:
            set_font(doc.styles[name], BODY_PT)
            doc.styles[name].paragraph_format.line_spacing = 1.12
            doc.styles[name].paragraph_format.space_after = Pt(6)
    set_font(doc.styles["Caption"], 10.0)
    set_font(doc.styles["Footer"], 9.0)

    caption_numbers: list[int] = []
    image_number = 0
    reference_mode = False
    for index, paragraph in enumerate(doc.paragraphs):
        paragraph.paragraph_format.widow_control = True
        if paragraph._p.xpath(".//m:oMathPara"):
            paragraph.paragraph_format.keep_together = True
            if index:
                doc.paragraphs[index - 1].paragraph_format.keep_with_next = True
        if index == 0:
            paragraph.style = "Title"
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph.paragraph_format.space_after = Pt(12)
            remove_borders(paragraph)
        is_heading = paragraph.style.name.startswith("Heading") or paragraph.style.name == "Title"
        if paragraph.text.strip() == "References":
            reference_mode = True
        elif is_heading:
            reference_mode = False
        if reference_mode and not is_heading:
            paragraph.paragraph_format.left_indent = Inches(0.22)
            paragraph.paragraph_format.first_line_indent = Inches(-0.22)
            paragraph.paragraph_format.space_after = Pt(6)
        for run_element in paragraph.runs:
            # Style selection owns heading size; body direct fonts inherit size.
            size = paragraph.style.font.size.pt if is_heading else BODY_PT
            set_font(run_element, size)
        if paragraph._p.xpath(".//w:drawing"):
            image_number += 1
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.keep_with_next = True
            paragraph.paragraph_format.keep_together = True
            paragraph.paragraph_format.space_before = Pt(8)
            paragraph.paragraph_format.space_after = Pt(5)
            paragraph.paragraph_format.line_spacing = 1.0
            following = next((p for p in doc.paragraphs[index + 1:] if p.text.strip()), None)
            if following is None or not CAPTION_RE.match(following.text):
                raise ValueError(f"Figure {image_number} is not followed by its explicit caption")
        caption_match = CAPTION_RE.match(paragraph.text)
        if caption_match:
            caption_numbers.append(int(caption_match.group(1)))
            paragraph.style = "Caption"
            # Long scientific captions may flow onto the following page. The
            # image's keep-next joins its first lines to the visual; making a
            # 200-300 word caption indivisible creates half-empty text pages.
            paragraph.paragraph_format.keep_together = len(paragraph.text.split()) <= 160
            paragraph.paragraph_format.keep_with_next = False
            paragraph.paragraph_format.line_spacing = 1.05
            paragraph.paragraph_format.space_after = Pt(9)
            for run_element in paragraph.runs:
                set_font(run_element, 10.0)
        if re.match(r"^Table\s+\d+\.", paragraph.text):
            paragraph.paragraph_format.keep_with_next = True
            paragraph.paragraph_format.space_before = Pt(6)
            paragraph.paragraph_format.space_after = Pt(5)

    sizes = []
    for shape, source in zip(doc.inline_shapes, image_paths, strict=True):
        with Image.open(source) as picture:
            pixels_wide, pixels_high = picture.size
        width = min(FIGURE_WIDTH_IN, FIGURE_MAX_HEIGHT_IN * pixels_wide / pixels_high)
        height = width * pixels_high / pixels_wide
        shape.width, shape.height = Inches(width), Inches(height)
        sizes.append({"figure": source.stem, "width_inches": width, "height_inches": height})
    style_tables(doc)
    normalized_accents = normalize_overbar_accents(doc)
    doc.save(path)
    return {"caption_numbers": caption_numbers, "figure_sizes": sizes,
            "normalized_overbar_accents": normalized_accents}


def inspect_docx(path: Path) -> dict:
    with ZipFile(path) as archive:
        tree = etree.fromstring(archive.read("word/document.xml"))
        relationships = etree.fromstring(archive.read("word/_rels/document.xml.rels"))
        external = [node.get("Target") for node in relationships if node.get("TargetMode") == "External"]
    equations = len(tree.findall(".//m:oMath", NS))
    display_equations = len(tree.findall(".//m:oMathPara", NS))
    native_bars = len(tree.findall(".//m:bar", NS))
    remaining_overbar_accents = len(tree.xpath('.//m:accPr/m:chr[@m:val="\u203e"]', namespaces=NS))
    images = len(tree.findall(".//w:drawing", NS))
    body = Document(path)
    captions = [int(match.group(1)) for para in body.paragraphs
                if (match := CAPTION_RE.match(para.text))]
    if images != 10 or captions != list(range(1, 11)):
        raise ValueError(f"DOCX image/caption mismatch: {images}, {captions}")
    if equations < 20 or display_equations < 5:
        raise ValueError("Native Word equations missing or unexpectedly sparse")
    if remaining_overbar_accents:
        raise ValueError("Literal overbar accents still require native-bar normalization")
    if body.paragraphs[0].style.name != "Title":
        raise ValueError("Document title does not use native Title style")
    raw_tex = [para.text for para in body.paragraphs if re.search(r"\$[^$]+\$|\\(?:frac|lambda|gamma)\b", para.text)]
    if raw_tex:
        raise ValueError(f"Unconverted math in DOCX: {raw_tex[:2]}")
    return {"images": images, "captions": captions, "native_equations": equations,
            "display_equations": display_equations, "native_top_bars": native_bars,
            "remaining_literal_overbar_accents": remaining_overbar_accents,
            "external_hyperlinks": external,
            "title_style": body.paragraphs[0].style.name, "raw_latex_paragraphs": 0}


def build(*, render: bool = True) -> dict:
    if Path(sys.executable) != PYTHON:
        raise RuntimeError(f"Use the required workspace interpreter: {PYTHON}")
    source, images = inspect_source()
    for tool in (PANDOC, RENDERER, BUNDLED_SOFFICE, BUNDLED_BIN / "soffice"):
        if not tool.is_file():
            raise FileNotFoundError(f"Required existing tool is missing: {tool}")
    started = datetime.now(timezone.utc)
    DOCX.parent.mkdir(parents=True, exist_ok=True)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    command = [str(PANDOC), "--from=markdown+tex_math_dollars-implicit_figures",
               "--to=docx", "--standalone", f"--resource-path={ARTICLE_DIR}",
               "--output", str(DOCX), str(SOURCE)]
    pandoc_output = run(command)
    presentation = style_docx(DOCX, images)
    checks = inspect_docx(DOCX)
    info = {
        "schema_version": 1, "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": sha256(SOURCE), "builder_sha256": sha256(Path(__file__)),
        "started_utc": started.isoformat(),
        "scientific_effect": "Presentation only; no simulation or estimation run",
        "source_word_count": len(source.split()),
        "figure_inputs": [{"path": str(p.relative_to(ROOT)), "sha256": sha256(p)} for p in images],
        "tools": {"python": sys.executable, "pandoc": run([str(PANDOC), "--version"]).splitlines()[0],
                  "bundled_soffice": str(BUNDLED_SOFFICE), "renderer": str(RENDERER),
                  "python_packages": {name: importlib.metadata.version(name)
                                      for name in ("python-docx", "Pillow", "pypdf", "lxml", "pdf2image")}},
        "pandoc_command": command, "pandoc_output": pandoc_output,
        "presentation": presentation, "docx_checks": checks,
        "outputs": {"docx": {"path": str(DOCX.relative_to(ROOT)), "sha256": sha256(DOCX)}},
        "human_visual_acceptance": "Pending inspection of every final rendered page",
    }
    if render:
        render_dir = ROOT / "output/qa" / STEM / started.strftime("render_%Y%m%dT%H%M%S%fZ")
        env = dict(os.environ)
        env["PATH"] = str(BUNDLED_BIN) + os.pathsep + env.get("PATH", "")
        # Renderer receives the wrapper's absolute location through PATH. That
        # wrapper resolves only the bundled binary and never desktop LibreOffice.
        if Path(shutil.which("soffice", path=env["PATH"]) or "") != BUNDLED_BIN / "soffice":
            raise RuntimeError("Renderer would not resolve bundled LibreOffice")
        render_command = [str(PYTHON), "-B", str(RENDERER), str(DOCX), "--output_dir",
                          str(render_dir), "--emit_pdf", "--dpi", "150", "--verbose"]
        render_log = run(render_command, env=env)
        rendered_pdf = render_dir / f"{STEM}.pdf"
        if not rendered_pdf.is_file():
            raise FileNotFoundError("DOCX renderer produced no matching PDF")
        shutil.copyfile(rendered_pdf, PDF)
        reader = PdfReader(PDF)
        texts = [page.extract_text() or "" for page in reader.pages]
        page_images = [render_dir / f"page-{number}.png" for number in range(1, len(reader.pages) + 1)]
        if not all(path.is_file() for path in page_images):
            raise ValueError("One or more PDF pages are missing their inspection PNG")
        pdf_captions = Counter(int(number) for number in
                               re.findall(r"^Figure\s+(\d+)\.", "\n".join(texts), re.M))
        if pdf_captions != Counter(range(1, 11)):
            raise ValueError(f"Missing or duplicate PDF captions: {pdf_captions}")
        if any(len(text.strip()) < 40 for text in texts):
            raise ValueError("Unexpected blank or nearly blank PDF page")
        info["outputs"]["pdf"] = {"path": str(PDF.relative_to(ROOT)), "sha256": sha256(PDF)}
        info["render"] = {"command": render_command, "log": render_log,
                          "directory": str(render_dir), "pages": len(reader.pages),
                          "page_images": [str(path) for path in page_images],
                          "caption_counts": dict(sorted(pdf_captions.items())),
                          "pdf_encrypted": reader.is_encrypted}
    info["finished_utc"] = datetime.now(timezone.utc).isoformat()
    METADATA.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    return info


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-render", action="store_true", help="Build DOCX only; not final acceptance")
    args = parser.parse_args()
    result = build(render=not args.no_render)
    print(f"DOCX: {DOCX}")
    print(f"Native equations: {result['docx_checks']['native_equations']}; embedded figures: 10")
    if "render" in result:
        print(f"PDF: {PDF}; pages: {result['render']['pages']}")
        print(f"Page PNGs: {result['render']['directory']}")
    print(f"Build metadata: {METADATA}")


if __name__ == "__main__":
    main()
