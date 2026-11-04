#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)
archive_dir="$repo_root/projects/frontiers_article/submission_v2/archive"
package_root="$archive_dir/evidence_package"
archive_file="$archive_dir/ability_concealment_e01_e05_evidence.zip"
candidate="$repo_root/projects/frontiers_article/ARTICLE_V2_LID_STAGE11_5_REPAIRED_CANDIDATE_PACKAGE.md"

if [ -e "$package_root" ] || [ -e "$archive_file" ]; then
    echo "Refusing to overwrite an existing evidence package or archive." >&2
    exit 1
fi

mkdir -p "$package_root"

link_path() {
    relative=$1
    source="$repo_root/$relative"
    target="$package_root/$relative"
    if [ ! -f "$source" ]; then
        echo "Missing required archive input: $relative" >&2
        exit 1
    fi
    mkdir -p "$(dirname -- "$target")"
    ln "$source" "$target"
}

ln "$archive_dir/README.md" "$package_root/README.md"
ln "$archive_dir/REPRODUCIBILITY.md" "$package_root/REPRODUCIBILITY.md"
ln "$archive_dir/SOFTWARE_REVISION.md" "$package_root/SOFTWARE_REVISION.md"

awk -F'`' '
    /^## 4\./ { capture=1; next }
    /^## 5\./ { capture=0 }
    capture && /^\| `/ { print $2 }
' "$candidate" | while IFS= read -r relative; do
    link_path "$relative"
done

for relative in \
    configs/frontiers_article/e01_hot_stove_standard.json \
    configs/frontiers_article/e02_binary_graded_standard.json \
    configs/frontiers_article/e03_m2_regime_standard.json \
    configs/frontiers_article/e04_m3_search_architectures_standard.json \
    configs/frontiers_article/e05_m3_bflpe_crossover_standard.json \
    projects/frontiers_article/ARTICLE_V1_EVIDENCE_MATRIX.csv \
    projects/frontiers_article/ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md \
    projects/frontiers_article/ARTICLE_V1_E01_E02_INTERPRETATION.md \
    projects/frontiers_article/ARTICLE_V1_E03_INTERPRETATION.md \
    projects/frontiers_article/ARTICLE_V1_E04_INTERPRETATION.md \
    projects/frontiers_article/ARTICLE_V1_E05_INTERPRETATION.md \
    projects/frontiers_article/ARTICLE_V1_ANALYTIC_RESULTS.md \
    projects/frontiers_article/ARTICLE_V1_INFERENTIAL_AUDIT.md \
    projects/frontiers_article/ARTICLE_V1_MODEL_ANALYSIS_CONSISTENCY_AUDIT.md \
    projects/frontiers_article/ARTICLE_V1_GENERATOR_SOURCE_PROVENANCE_INDEX.csv \
    projects/frontiers_article/ARTICLE_V1_GENERATOR_SOURCE_PROVENANCE_AUDIT.md \
    projects/frontiers_article/ARTICLE_V2_LID_SUPPLEMENTARY_METHODS.md \
    projects/frontiers_article/v2_figures/FIGURE_CAPTIONS.md \
    projects/frontiers_article/v2_figures/FIGURE_PROVENANCE.md \
    projects/frontiers_article/v2_figures/FIGURE_TEXT_CONSISTENCY_MATRIX.md \
    projects/frontiers_article/v2_figures/generate_v2_figures.py \
    projects/frontiers_article/publication_v1/data/PROVENANCE.json \
    projects/frontiers_article/publication_v1/data/e01_intervention_effects.csv \
    projects/frontiers_article/publication_v1/data/e01_lambda_response.csv \
    projects/frontiers_article/publication_v1/data/e01_primary_effects.csv \
    projects/frontiers_article/publication_v1/data/e02_arm_expected_rewards.csv \
    projects/frontiers_article/publication_v1/data/e02_primary_effects.csv \
    projects/frontiers_article/publication_v1/data/e03_grid_map.csv \
    projects/frontiers_article/publication_v1/data/e03_grid_summary.csv \
    projects/frontiers_article/publication_v1/data/e03_objective_thresholds.csv \
    projects/frontiers_article/publication_v1/data/e04_headline_effects.csv \
    projects/frontiers_article/publication_v1/data/e04_k_response.csv \
    projects/frontiers_article/publication_v1/data/e05_crossings.csv \
    projects/frontiers_article/publication_v1/data/e05_displacement.csv \
    projects/frontiers_article/publication_v1/data/e05_response_vs_bf.csv
do
    link_path "$relative"
done

find "$repo_root/projects/frontiers_article/provenance/frozen_generator_sources/E04" -type f -print |
while IFS= read -r source; do
    relative=${source#"$repo_root/"}
    link_path "$relative"
done

find "$repo_root/projects/frontiers_article/provenance/frozen_generator_sources/E05" -type f -print |
while IFS= read -r source; do
    relative=${source#"$repo_root/"}
    link_path "$relative"
done

(
    cd "$package_root"
    find . -type f ! -name MANIFEST.sha256 -print0 |
        sort -z |
        xargs -0 shasum -a 256 > MANIFEST.sha256
)

(
    cd "$archive_dir"
    zip -X -9 -r "$(basename -- "$archive_file")" "$(basename -- "$package_root")"
)

shasum -a 256 "$archive_file"
