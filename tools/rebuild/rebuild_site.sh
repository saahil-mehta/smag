#!/bin/bash
# Restore site/ HTML from the pristine mirror, then replay every edit in order.
#
# site/ is git-ignored, so it has no history of its own. It is reproducible as
# "pristine mirror + these scripts", which is what makes this recovery safe.
# Only .html files are restored; assets added since (the SMAG logo and the two
# badge images) are left in place, and swap_logo.py rewrites the shared logo.
set -euo pipefail

REPO=/Users/saahil/Documents/GitHub/smag
MIRROR="$REPO/reference-mirror/www.eclipsemagnetics.com"
SITE="$REPO/site"
SCRATCH=/private/tmp/claude-501/-Users-saahil-Documents-GitHub-smag/1a6d8a81-1486-437b-9c1f-664d93de7ded/scratchpad

cd "$REPO"

echo "=== preserving added assets ==="
mkdir -p "$SCRATCH/keep"
cp "$SITE/smag-logo.svg" "$SCRATCH/keep/" 2>/dev/null || true
cp "$SITE"/site/assets/images/badge-*.webp "$SCRATCH/keep/" 2>/dev/null || true
ls "$SCRATCH/keep/"

echo
echo "=== restoring all HTML from pristine mirror ==="
# rsync only html, delete extras so the two removed page dirs come back too
rsync -a --include='*/' --include='*.html' --exclude='*' "$MIRROR"/ "$SITE"/
echo "  html files in site/: $(find "$SITE" -name '*.html' | wc -l | tr -d ' ')"
echo "  html files in mirror: $(find "$MIRROR" -name '*.html' | wc -l | tr -d ' ')"

echo
echo "=== restoring preserved assets ==="
cp "$SCRATCH/keep/smag-logo.svg" "$SITE/" 2>/dev/null || true
cp "$SCRATCH"/keep/badge-*.webp "$SITE/site/assets/images/" 2>/dev/null || true
ls -l "$SITE"/site/assets/images/badge-*.webp

echo
echo "=== replaying edits in order ==="
for s in swap_logo.py swap_address.py swap_contact_social.py swap_lower_bar.py drop_legal_links.py; do
  echo
  echo "--- $s"
  python3 "$SCRATCH/$s"
done
