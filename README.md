# breadNET but now it's static

```shell
hugo server -DF --noHTTPCache  --disableFastRender --logLevel debug --renderToMemory
```

## Migrate from Ghost blogs

<https://github.com/hswolff/ghost-to-md>

```shell
for file in *.md; do
    awk '
    BEGIN { in_front_matter=0 }
    /^---/ {
        if (in_front_matter==0) { in_front_matter=1; print; next }
        else { in_front_matter=0; print; next }
    }
    in_front_matter && /^tags:/ { next }   # skip tags line
    { print }
    ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done

```

```shell
for file in *.md; do
    awk '
    BEGIN { in_front_matter=0 }
    /^---/ {
        if (in_front_matter==0) { in_front_matter=1; print; next }
        else { in_front_matter=0; print; next }
    }
    in_front_matter {
        if (/^tags:/) next                 # remove tags line
        sub(/^excerpt:/, "summary:")       # change excerpt to summary
    }
    { print }
    ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done
```

```shell
for file in *.md; do
    awk '
    BEGIN { in_front_matter=0 }
    /^---/ {
        if (in_front_matter==0) { in_front_matter=1; print; next }
        else { in_front_matter=0; print; next }
    }
    in_front_matter {
        if (/^tags:/) next                 # remove tags line
        sub(/^excerpt:/, "summary:")       # change excerpt to summary
        sub(/^date_published:/, "date:")
    }
    { print }
    ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done
```

Create a file called `process.sh`

```shell
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
```

```shell
chmod +x process.sh
./process.sh
```
