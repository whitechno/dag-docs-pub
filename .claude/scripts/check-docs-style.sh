#!/usr/bin/env bash
# Mechanical docs-style checks for docs/**/*.md.
#
# Covers the machine-checkable subset of .claude/rules/docs-style.md:
#   1. ASCII only, outside fenced code blocks. Permitted exceptions: the
#      center dot (U+00B7) and the multiplication sign (U+00D7).
#   2. Line width <= 80 characters, except fenced code blocks and table
#      rows. URLs do not count toward the limit.
#
# Only fenced code blocks (``` or ~~~) are exempt, tracked by marker type
# and length per CommonMark. Indented code blocks are NOT exempt; the docs
# convention is to always use fences.
#
# Judgment rules (American spelling, "we" voice, moderate formatting) are
# NOT checked here; they are reviewed by the model against the rule file.
# When a new mechanically checkable rule is added to docs-style.md, add
# the corresponding check to this script.
#
# Usage: check-docs-style.sh [file ...]
# Explicit file arguments resolve against the caller's directory first,
# then the repo root. With no arguments, checks docs/**/*.md files changed
# vs HEAD (deleted files are skipped), plus untracked ones. Exits 0 if
# clean, 1 if violations were found.

set -uo pipefail
top="$(git rev-parse --show-toplevel)"

status=0
files=()
if [ "$#" -gt 0 ]; then
  for a in "$@"; do
    if [ -f "$a" ]; then
      files+=("$a")
    elif [ -f "$top/$a" ]; then
      files+=("$top/$a")
    else
      echo "$a: file not found"
      status=1
    fi
  done
else
  cd "$top"
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    files+=("$f")
  done < <(
    {
      git diff --name-only --diff-filter=d HEAD -- 'docs/*.md' 'docs/**/*.md'
      git ls-files --others --exclude-standard -- 'docs/*.md' 'docs/**/*.md'
    } | sort -u
  )
fi

if [ "${#files[@]}" -eq 0 ]; then
  if [ "$status" -ne 0 ]; then
    echo "docs-style: violations found."
    exit 1
  fi
  echo "docs-style: no changed docs/**/*.md files to check."
  exit 0
fi

for f in "${files[@]}"; do
  perl -CSD -ne '
    BEGIN { $fence = "" }
    chomp;
    if ($fence eq "" && /^\s*(`{3,}|~{3,})/) { $fence = $1; next }
    if ($fence ne "" && /^\s*([`~]{3,})\s*$/
        && substr($1, 0, 1) eq substr($fence, 0, 1)
        && length($1) >= length($fence)) { $fence = ""; next }
    next if $fence ne "";
    my $line = $_;
    (my $stripped = $line) =~ s/[\x{00B7}\x{00D7}]//g;
    while ($stripped =~ /([^\x00-\x7F])/g) {
      my $ch = $1;
      my $name = $ch eq "\x{2014}" ? " (em-dash)" : "";
      printf "%s:%d: non-ASCII character U+%04X%s: %s\n",
        $ARGV, $., ord($ch), $name, $line;
      $::bad = 1;
    }
    (my $no_url = $line) =~ s{https?://\S+}{}g;
    if (length($no_url) > 80 && $line !~ /^\s*\|/) {
      my $note = $no_url ne $line ? ", excluding URLs" : "";
      printf "%s:%d: line exceeds 80 characters (%d%s)\n",
        $ARGV, $., length($no_url), $note;
      $::bad = 1;
    }
    END { exit($::bad ? 1 : 0) }
  ' "$f" || status=1
done

if [ "$status" -eq 0 ]; then
  echo "docs-style: mechanical checks passed (${#files[@]} file(s))."
else
  echo "docs-style: violations found."
fi
exit "$status"
