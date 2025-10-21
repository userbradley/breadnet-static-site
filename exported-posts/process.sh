#!/bin/bash

# Loop over all markdown files in the current directory
for file in *.md; do
    # Strip the date prefix (YYYY-MM-DD-) to get the new directory name
    dirname="${file:11}"        # removes first 11 characters
    dirname="${dirname%.md}"    # remove .md extension

    # Create the directory
    mkdir -p "$dirname"

    # Copy the file into the new directory as index.md
    cp "$file" "$dirname/index.md"
done
