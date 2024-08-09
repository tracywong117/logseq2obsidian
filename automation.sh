#!/bin/bash

# Enter the path to your Logseq directory and Obsidian vault
LOGSEQ_SOURCE="/Users/tracywong/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents"
OBSIDIAN_DESTINATION="/Users/tracywong/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tracy's Notes"

# Do not edit below this line
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKING="$SCRIPT_DIR/graph"

rm -rf "$WORKING"
mkdir -p "$WORKING"
cp -R "$LOGSEQ_SOURCE/assets" "$WORKING"
cp -R "$LOGSEQ_SOURCE/journals" "$WORKING"
cp -R "$LOGSEQ_SOURCE/pages" "$WORKING"

python3 batch_convert.py --file_path graph --dest_path obsidian_vault

rm -rf "$OBSIDIAN_DESTINATION/assets" "$OBSIDIAN_DESTINATION/journals" "$OBSIDIAN_DESTINATION/pages"

sleep 60 # for cloud sync, otherwise the files may be duplicated; can be commented out if not using cloud

cp -R "$SCRIPT_DIR/obsidian_vault/"* "$OBSIDIAN_DESTINATION"