# breadNET but now it's static

```shell
hugo server -DF --noHTTPCache  --disableFastRender --logLevel debug
```


## Migrate from Ghost blogs

https://github.com/hswolff/ghost-to-md

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
