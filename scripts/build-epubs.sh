#!/usr/bin/env bash

set -euo pipefail

readonly output_dir="books/epub"
readonly author="gellsmore-svg"
readonly rights="Copyright (c) 2026 gellsmore-svg. Licensed under the MIT License."

command -v pandoc >/dev/null || {
  printf '%s\n' 'pandoc is required to build the EPUB editions.' >&2
  exit 1
}

command -v epubcheck >/dev/null || {
  printf '%s\n' 'epubcheck is required to validate the EPUB editions.' >&2
  exit 1
}

mkdir -p "$output_dir"

build_book() {
  local source="$1"
  local output="$2"
  local title="$3"
  local identifier="$4"
  local toc_depth="$5"
  local remove_manual_contents="$6"
  local -a metadata=(
    --metadata "title=$title"
    --metadata "author=$author"
    --metadata 'lang=en-GB'
    --metadata "rights=$rights"
    --metadata "identifier=$identifier"
  )

  if [[ "$remove_manual_contents" == 'true' ]]; then
    metadata+=(--metadata 'epub-remove-manual-contents=true')
  fi

  pandoc "$source" \
    --to=epub2 \
    --toc \
    --toc-depth="$toc_depth" \
    --split-level=1 \
    --epub-title-page=false \
    --lua-filter scripts/epub-cleanup.lua \
    "${metadata[@]}" \
    --output "$output"

  epubcheck "$output"
}

build_second_edition() {
  local output="$output_dir/coherent-biblical-ontology-second-edition.epub"

  python3 books/v2/tools/assemble_manuscript.py --check || {
    printf '%s\n' 'The second-edition manuscript is out of date: run python3 books/v2/tools/assemble_manuscript.py' >&2
    exit 1
  }

  pandoc books/coherent-biblical-ontology-second-edition.md books/v2/epub-back-cover.md \
    --to=epub2 \
    --toc \
    --toc-depth=1 \
    --split-level=1 \
    --resource-path=books \
    --epub-cover-image=books/v2/covers/front-cover.png \
    --css=books/v2/epub.css \
    --lua-filter scripts/epub-v2.lua \
    --metadata 'title=Coherent Biblical Ontology' \
    --metadata 'subtitle=Second Edition' \
    --metadata "author=$author" \
    --metadata 'lang=en-GB' \
    --metadata "rights=$rights" \
    --metadata 'identifier=https://github.com/gellsmore-svg/Relational-Substrate#coherent-biblical-ontology-second-edition' \
    --metadata 'date=2026-10' \
    --metadata 'description=A Scripture-first account of a relational creation: physical order, life, persons, corruption and restoration.' \
    --output "$output"

  epubcheck "$output"
}

if [[ "${1:-all}" == 'v2' ]]; then
  build_second_edition
  exit 0
fi

build_book \
  books/relational-substrate.md \
  "$output_dir/relational-substrate.epub" \
  'The Relational Substrate: A Hierarchical Ontology of Runtime Physical Reality' \
  'https://github.com/gellsmore-svg/Relational-Substrate#the-relational-substrate' \
  2 \
  true

build_book \
  books/coherent-biblical-ontology-bachelors.md \
  "$output_dir/coherent-biblical-ontology.epub" \
  'Coherent Biblical Ontology' \
  'https://github.com/gellsmore-svg/Relational-Substrate#coherent-biblical-ontology' \
  1 \
  false

build_second_edition
