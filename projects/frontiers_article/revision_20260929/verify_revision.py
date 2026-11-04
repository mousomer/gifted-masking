"""Read-only editorial checks; never import a model or invoke an experiment.

Run with /Users/omer/workspace/venvs/venv314/bin/python from any directory.
Numerical figure selection is additionally checked by generate_figures.py.
This script reports evidence identity and structural checks, not a substitute
for the documented scientific and visual review.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys


REVISION = Path(__file__).resolve().parent
ARTICLE = REVISION.parent
ROOT = REVISION.parents[2]
sys.path.insert(0, str(ARTICLE / "publication_v1" / "scripts"))
from pubcommon import FAMILIES, verify_evidence_matrix, verify_frozen_family  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def words(text: str) -> int:
    return len(text.split())


def section(text: str, number: str) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(number)}\s+[^\n]+\n(.*?)(?=^##? |\Z)", text
    )
    require(match is not None, f"Missing main section {number}")
    return match.group(1)


def has_number(text: str, value: float, tolerance: float) -> bool:
    normalized = text.replace(",", "").replace("−", "-")
    numbers = re.findall(r"(?<![\w.])[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", normalized)
    return any(math.isclose(float(number), value, abs_tol=tolerance, rel_tol=0)
               for number in numbers)


def main() -> None:
    baseline = {
        "ARTICLE_V2_LID_MANUSCRIPT_DRAFT.md": "7742f7542541d61ee74fb22183b400e796f8a8d2c770dae1d9883a0d079df1f9",
        "ARTICLE_V2_LID_SUPPLEMENTARY_METHODS.md": "341a91b2ff5386c54a86d761de25e60e1f02da280802e8d8865f8f12daea6a26",
    }
    for name, expected in baseline.items():
        actual = hashlib.sha256((ARTICLE / name).read_bytes()).hexdigest()
        require(actual == expected, f"As-found historical source changed: {name}")
    print("PASS: 2/2 as-found historical sources preserved")

    evidence = [verify_frozen_family(family) for family in FAMILIES]
    total = sum(record["protected_output_count"] for record in evidence)
    valid = sum(record["protected_outputs_valid"] for record in evidence)
    require(total == valid == 33, "Expected 33 protected outputs")
    print(f"PASS: {valid}/{total} protected experiment outputs")
    matrix = verify_evidence_matrix()
    require(matrix["referenced_files_valid"] == matrix["referenced_file_count"] == 18,
            "Expected 18 evidence-matrix references")
    print("PASS: 18/18 evidence-matrix references")

    manuscript = (REVISION / "MANUSCRIPT.md").read_text()
    supplement = (REVISION / "SUPPLEMENTARY_METHODS.md").read_text()
    claim_map = (REVISION / "CLAIM_MAP.md").read_text()
    title = "How Learning and Social Opportunity Shape Ability Concealment: A Computational Study"
    require(manuscript.startswith("# " + title), "Unexpected manuscript title")
    require(title in supplement, "Supplement title differs")
    abstract = manuscript.split("## Abstract\n", 1)[1].split("**Keywords:", 1)[0].strip()
    abstract_words = words(abstract)
    require(abstract_words <= 150, f"Abstract too long: {abstract_words}")
    keywords = manuscript.split("**Keywords:", 1)[1].split("\n", 1)[0].strip("* ")
    require(1 <= len(keywords.split(";")) <= 5, "Keyword count outside 1–5")
    print(f"PASS: matching titles; Abstract {abstract_words} whitespace words; keywords {len(keywords.split(';'))}")

    for chapter in range(1, 7):
        require(re.search(rf"(?m)^# {chapter}\. ", manuscript) is not None,
                f"Missing main chapter {chapter}")
    for prefix, count in [("1", 6), ("2", 7), ("3", 6), ("4", 7)]:
        for index in range(1, count + 1):
            section(manuscript, f"{prefix}.{index}")
    for chapter in range(1, 11):
        require(re.search(rf"(?m)^## S{chapter}\. ", supplement) is not None,
                f"Missing supplement chapter S{chapter}")
    for heading in ["Educational Relevance", "Funding", "CRediT", "Declaration of competing", "Acknowledgements", "References"]:
        require(heading in manuscript, f"Missing manuscript back matter: {heading}")
    print("PASS: six main chapters, 26 main subsections, S1–S10, and back matter")

    rows = re.findall(r"(?m)^\| (C\d\d) \| ([123]) \|", claim_map)
    require(Counter(identifier for identifier, _ in rows) == Counter(f"C{i:02}" for i in range(1, 24)),
            "Claim map must contain each C01–C23 exactly once")
    require(Counter(category for _, category in rows) == Counter({"1": 14, "2": 2, "3": 7}),
            "Contribution categories differ from reviewed 14/2/7 assignment")
    print("PASS: 23/23 claim routes; category counts 14/2/7")

    # Spot checks are tied to the appropriate Results subsection, not a number
    # appearing elsewhere. Both exact and editorially rounded values are valid.
    anchors = {
        "3.1": [(58.89, .01), (99.19, .01), (40.30, .01), (.6304, .0001), (.8333, .0001)],
        "3.2": [(25.50, .01), (32.87, .01), (.029761, .000001)],
        "3.3": [(.384, .001), (.339, .001), (.269, .001), (243, 0), (357, 0), (5000, 0)],
        "3.4": [(84.19, .01), (87.27, .01), (99.72, .01), (99.64, .01), (99.36, .01), (95.80, .01)],
        "3.5": [(.312852, .0000001), (.470588, .0000001), (.134076, .0000001), (58.82, .01), (78.95, .01)],
    }
    for number, values in anchors.items():
        body = section(manuscript, number)
        for value, tolerance in values:
            require(has_number(body, value, tolerance), f"Check restored value {value} in section {number}")
    print(f"PASS: {sum(map(len, anchors.values()))} section-specific restored numerical anchors")

    body, references = manuscript.split("# References\n", 1)
    reference_entries = [entry for entry in references.strip().split("\n\n") if entry.strip()]
    require(len(reference_entries) == 14, "Review changed reference inventory")
    citations = {
        "Chaudoir": r"Chaudoir & Fisher, 2010", "Cicchetti": r"Cicchetti & Rogosch, 1996",
        "Coleman": r"Coleman & Cross, 1988", "Cross2019": r"Cross et al\., 2019",
        "Cross1993": r"Cross et al\., 1993", "Denrell2005": r"Denrell, 2005",
        "DenrellMarch": r"Denrell & March, 2001", "Klimecka": r"Klimecká, 2023",
        "Lavrijsen": r"Lavrijsen & Verschueren, 2023", "LeMens": r"Le Mens & Denrell, 2011",
        "March": r"March, 1996", "Swiatek": r"Swiatek, 1995",
        "Tourreix": r"Tourreix et al\., 2023", "Zeidner": r"Zeidner (?:and|&) Schleyer(?:, | \()1999",
    }
    for name, pattern in citations.items():
        require(re.search(pattern, body) is not None, f"Unused/missing expected citation: {name}")
    dois = re.findall(r"https://doi\.org/\S+", references)
    require(len(dois) == len(set(dois)) == 14, "Reference DOI inventory differs")
    print("PASS: 14 retained/added references have body citations and distinct DOI links")

    # Exact algebra under the documented reference payoff/variance conditions.
    b, a, c, r = 1.0, .6, .25, 2.0
    close = lambda x, y: math.isclose(x, y, abs_tol=1e-12, rel_tol=0)
    require(close(1 - (a + c) / (b + r), 43 / 60), "M0 objective boundary")
    threshold = lambda weight: (b - c + weight * (r - a)) / (b + a + weight * (r - a))
    require(close(threshold(.5), 1.45 / 2.3), "Subjective low threshold")
    require(close(threshold(2.5), 5 / 6), "Subjective high threshold")
    require(close(threshold(1), 43 / 60), "Lambda=1 exact baseline")
    variance = lambda disclosure: (b + r) ** 2 * .25 * disclosure * (1 - .25 * disclosure)
    require(close(variance(.5), .984375), "Partial-disclosure variance")
    require(close(variance(1), 1.6875), "Full-disclosure variance")
    require(close(.75 + .5 * (3 * .75 - 2.15), .8), "Partial-disclosure expected reward")
    require(close(.4 / .85, 8 / 17), "Global comparison-cost boundary")
    require(close(.4 - .85 * .325, .12375), "Remaining advantage at .325")
    print("PASS: nine exact reference-algebra checks")

    for text, name in [(manuscript, "main"), (supplement, "supplement")]:
        require("\ufffd" not in text, f"Replacement character in {name}")
        require(not re.search(r"\b(?:TODO|TBD|PLACEHOLDER)\b", text), f"Unfinished placeholder in {name}")
        require(text.count("$$") % 2 == 0, f"Unbalanced displayed-math delimiters in {name}")
    for index in range(1, 7):
        require(f"Figure {index}" in manuscript, f"Missing Figure {index} callout")
    pngs = sorted((REVISION / "figures").glob("Figure_*.png"))
    pdfs = sorted((ROOT / "output" / "pdf" / "revision_20260929").glob("Figure_*.pdf"))
    require(len(pngs) == len(pdfs) == 6, f"Expected six PNG/PDF figures; found {len(pngs)}/{len(pdfs)}")
    print("PASS: math delimiters, no placeholders, six figure callouts, six PNG/PDF pairs")
    provenance = json.loads((REVISION / "FIGURE_PROVENANCE.json").read_text())
    require(len(provenance["outputs"]) == 12, "Figure manifest must bind 12 outputs")
    for name, digest in {**provenance["inputs"], **provenance["outputs"]}.items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                f"Figure-provenance hash mismatch: {name}")
    require(hashlib.sha256((REVISION / "generate_figures.py").read_bytes()).hexdigest()
            == provenance["generator_sha256"], "Figure generator changed after last render")
    text_source = REVISION / "figure_text.py"
    require(provenance.get("text_source") == str(text_source.relative_to(ROOT)),
            "Figure provenance must name the active text catalog")
    require(hashlib.sha256(text_source.read_bytes()).hexdigest()
            == provenance.get("text_sha256"), "Figure text catalog changed after last render")
    require(provenance.get("selected_figures") == list(range(1, 7)),
            "Canonical provenance must contain all six figures")
    require(provenance.get("mode") == "canonical",
            "Preview provenance cannot certify the canonical figure package")
    print(f"PASS: {len(provenance['inputs'])} figure inputs, 12 figure outputs, generator and text-catalog hashes")
    source_captions = (REVISION / "FIGURE_CAPTIONS.md").read_text().split("## Figure 1.", 1)[1].strip()
    main_captions = manuscript.split("## Figure 1.", 1)[1].split("# Funding", 1)[0].strip()
    require(" ".join(source_captions.split()) == " ".join(main_captions.split()),
            "Main-text captions differ from the figure package")
    print("PASS: all six manuscript captions match the figure package")
    main_body = manuscript.split("# Figure captions", 1)[0]
    print(f"INFO: main source before captions: {words(main_body)} whitespace words (includes front matter and equations)")
    print("PASS: read-only revision checks; no simulation or estimator was run")


if __name__ == "__main__":
    main()
