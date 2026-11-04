"""Read-only acceptance checks for the single illustrated article.

Run with the workspace venv. This never imports a simulator, runs an experiment,
fits a model, or computes a new uncertainty interval. Numeric-presence checks
complement, but do not replace, the documented scientific and visual review.
"""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

from lxml import etree
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROJECT = HERE.parent
DOCX = ROOT / "output/docx/integrated_article_20261004.docx"
PDF = ROOT / "output/pdf/integrated_article_20261004.pdf"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prior_revision() -> int:
    records = (HERE / "PRIOR_REVISION_SHA256.txt").read_text().splitlines()
    for record in records:
        expected, relative = record.split(maxsplit=1)
        require(digest(ROOT / relative) == expected, f"Earlier file changed: {relative}")
    return len(records)


def frozen_evidence() -> tuple[int, int]:
    sys.path.insert(0, str(PROJECT / "publication_v1/scripts"))
    from pubcommon import FAMILIES, verify_evidence_matrix, verify_frozen_family
    evidence = [verify_frozen_family(family) for family in FAMILIES]
    count = sum(item["protected_outputs_valid"] for item in evidence)
    total = sum(item["protected_output_count"] for item in evidence)
    require(count == total == 33, "Frozen experiment outputs differ")
    matrix = verify_evidence_matrix()
    require(matrix["referenced_files_valid"] == matrix["referenced_file_count"] == 18,
            "Frozen evidence-matrix references differ")
    return count, matrix["referenced_files_valid"]


def numeric_values(text: str) -> list[float]:
    normalized = text.replace(",", "").replace("−", "-")
    return [float(value) for value in re.findall(
        r"(?<![\w.])[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", normalized)]


def source_checks() -> dict:
    text = (HERE / "ARTICLE.md").read_text()
    coverage = (HERE / "CLAIM_COVERAGE.md").read_text()
    routes = re.findall(r"(?m)^\| (C\d\d) \| ([123]) \|", coverage)
    require(Counter(item[0] for item in routes) == Counter(f"C{i:02}" for i in range(1, 24)),
            "Coverage must route each C01–C23 once")
    require(Counter(item[1] for item in routes) == Counter({"1": 14, "2": 2, "3": 7}),
            "Contribution categories changed")
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    require(len(images) == 10 and len(set(images)) == 10, "Need ten unique inline figures")
    for index, name in enumerate(images, 1):
        require(f"figure_{index:02}_" in name, "Figures must appear in numerical order")
        require((HERE / name).is_file(), f"Missing inline image: {name}")
        require((HERE / name).with_suffix(".svg").is_file(), f"Missing vector figure: {name}")
    for index in range(1, 7):
        require(re.search(rf"(?m)^#{{1,2}} {index}\. ", text) is not None,
                f"Main chapter {index} missing")
    require("Appendix A" in text, "Internal technical appendix missing")
    require("Supplementary Methods" not in text, "Article still depends on separate supplement")
    require(not re.search(r"\b(?:TODO|TBD|FIXME)\b", text), "Unresolved source placeholder")
    require(text.count("$") % 2 == 0 and text.count("$$") % 2 == 0,
            "Unbalanced math delimiters")
    numbers = numeric_values(text)
    anchors = [40.30, .6304, .8333, 2.58, 4.66, 11.81, 25.50, 32.87,
               22.17, .029761, .032088, .038941, .025236, .38394,
               .33878, .26901, .042943, .406293, 243, 107, 357,
               99.67, 98.22, 95.42, 97.12, 89.97, 18, 21, 10,
               84.19, 87.27, 99.72, 99.64, 120, 55, .312852,
               .307836, .316918, .470588, .157736, .134076, 85.20]
    for value in anchors:
        require(any(abs(abs(found) - abs(value)) <= 0.000006 for found in numbers),
                f"Restored numeric anchor absent: {value}")
    for start in [2026081101, 2026081201, 2026081301, 2026081401, 2026081501]:
        require(str(start) in text and str(start + 4) in text, f"Seed range missing: {start}")
    captions = (HERE / "FIGURE_CAPTIONS.md").read_text()
    normalize = lambda value: " ".join(value.replace("**", "").split())
    for index in range(1, 11):
        match = re.search(rf"(?ms)^## (Figure {index}\. [^\n]+)\n+(.*?)(?=^## |\Z)", captions)
        require(match is not None, f"Package caption {index} missing")
        article_match = re.search(rf"(?m)^\*\*Figure {index}\. .+$", text)
        require(article_match is not None, f"Inline caption {index} missing")
        require(normalize(article_match.group()) == normalize(" ".join(match.groups())),
                f"Caption {index} differs between article and figure package")
    return {"claims": len(routes), "inline_figures": len(images),
            "numeric_anchors": len(anchors), "source_words": len(text.split())}


def provenance_checks() -> dict:
    figures = json.loads((HERE / "FIGURE_PROVENANCE.json").read_text())
    require(figures["mode"] == "canonical" and figures["selected_figures"] == list(range(1, 11)),
            "Figure provenance is not a complete canonical render")
    require(len(figures["outputs"]) == 20, "Expected ten PNG/SVG pairs")
    for field in ("inputs", "outputs"):
        for relative, expected in figures[field].items():
            require(digest(ROOT / relative) == expected, f"Figure {field} hash differs: {relative}")
    for field, filename in [("generator_sha256", "generate_figures.py"),
                            ("text_sha256", "figure_text.py"),
                            ("captions_sha256", "FIGURE_CAPTIONS.md")]:
        require(figures[field] == digest(HERE / filename), f"Unrendered figure source edit: {filename}")
    build = json.loads((HERE / "BUILD_METADATA.json").read_text())
    require(build["source_sha256"] == digest(HERE / "ARTICLE.md"), "DOCX/PDF article source is stale")
    require(build["builder_sha256"] == digest(HERE / "build_article.py"), "Builder changed after build")
    for record in [*build["figure_inputs"], *build["outputs"].values()]:
        require(digest(ROOT / record["path"]) == record["sha256"], f"Build hash differs: {record['path']}")
    return {"figure_inputs": len(figures["inputs"]), "figure_outputs": 20,
            "matching_article_build": True}


def archived_grid() -> dict:
    with (PROJECT / "publication_v1/data/e03_grid_map.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    counts = Counter(row["publication_category"] for row in rows)
    require(counts == Counter({"learned_suboptimal_masking": 243,
                              "learner_matches_objective": 107, "inconclusive": 7}),
            "Complete dynamic map no longer has the audited partition")
    require(len({float(row["p"]) for row in rows}) == 21, "Grid p cardinality changed")
    require(len({float(row["eta"]) for row in rows}) == 17, "Grid eta cardinality changed")
    return dict(counts)


def artifact_checks() -> dict:
    with zipfile.ZipFile(DOCX) as archive:
        xml = etree.fromstring(archive.read("word/document.xml"))
        figures = xml.findall(".//wp:inline", NS)
        maths = xml.findall(".//m:oMath", NS)
        require(len(figures) == 10, "DOCX must contain ten embedded inline figures")
        require(len(maths) >= 60, "Native editable Word equations appear missing")
        literal_overbars = xml.xpath(".//m:accPr/m:chr[@m:val='‾']", namespaces=NS)
        require(not literal_overbars, "PDF-unsafe literal overbar accent remains")
        require(len(xml.findall(".//m:bar", NS)) == 6, "Expected six native Word bars")
        title_count = len(xml.xpath(".//w:pPr/w:pStyle[@w:val='Title']", namespaces=NS))
        require(title_count == 1, "DOCX needs one native Title-style paragraph")
    with PDF.open("rb") as handle:
        pdf = PdfReader(handle)
        texts = [page.extract_text() or "" for page in pdf.pages]
        require(all(text.strip() for text in texts), "Empty PDF page")
        joined = "\n".join(texts)
        require("\ufffd" not in joined, "PDF replacement glyph detected")
        for index in range(1, 11):
            require(re.search(rf"Figure\s+{index}\.", joined), f"PDF caption {index} missing")
        require("Appendix A" in joined, "PDF appendix missing")
        require("2026081101" in joined and "2026081505" in joined, "PDF seed table missing")
        page_count = len(pdf.pages)
    return {"native_word_equations": len(maths), "embedded_figures": len(figures),
            "pdf_pages": page_count, "docx_sha256": digest(DOCX), "pdf_sha256": digest(PDF)}


def main() -> None:
    results = {"preserved_prior_revision_files": prior_revision(),
               "frozen_evidence": frozen_evidence(), "source": source_checks(),
               "provenance": provenance_checks(),
               "dynamic_grid": archived_grid(), "artifacts": artifact_checks()}
    print(json.dumps(results, indent=2))
    print("PASS: read-only integrated article checks; no experiment or estimator run")


if __name__ == "__main__":
    main()
