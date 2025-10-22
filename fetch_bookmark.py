#!/usr/bin/env python3
import requests, json, sys, os, re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def sanitize_name(url):
    """Generate a simple, safe name from URL for shortcode usage"""
    u = urlparse(url)
    name = u.netloc + u.path
    name = name.strip("/").replace("/", "_")
    # remove unsafe chars
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    return name.lower() or "bookmark"

def get_meta(soup, property_names):
    for name in property_names:
        tag = soup.find("meta", property=name) or soup.find("meta", attrs={"name": name})
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""

def get_favicon(soup, url):
    """Try to find favicon from HTML; fallback to /favicon.ico"""
    icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
    if icon_link and icon_link.get("href"):
        href = icon_link["href"].strip()
        if not href.startswith("http"):
            parsed = urlparse(url)
            href = f"{parsed.scheme}://{parsed.netloc}{href if href.startswith('/') else '/' + href}"
        return href
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/favicon.ico"

def fetch_bookmark(url):
    r = requests.get(url, headers={"User-Agent": "HugoBookmark/1.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    # JSON-LD fallback
    jsonld = soup.find("script", type="application/ld+json")
    jd = {}
    if jsonld:
        try:
            jd = json.loads(jsonld.string)
        except:
            jd = {}

    title = get_meta(soup, ["og:title"]) or jd.get("headline") or jd.get("name") or (soup.title.string.strip() if soup.title else "")
    description = get_meta(soup, ["og:description", "description"]) or jd.get("description", "")
    image = get_meta(soup, ["og:image"]) or (jd.get("image") if isinstance(jd.get("image"), str) else jd.get("image", {}).get("url", ""))
    site_name = get_meta(soup, ["og:site_name"]) or urlparse(url).netloc
    publisher = get_meta(soup, ["author"]) or (jd.get("author", {}).get("name") if isinstance(jd.get("author"), dict) else "")
    favicon = get_favicon(soup, url)

    return {
        "url": url,
        "title": title,
        "description": description,
        "image": image,
        "site": site_name,
        "publisher": publisher,
        "favicon": favicon
    }

def save_bookmark(data, name):
    os.makedirs("data/bookmarks", exist_ok=True)
    path = os.path.join("data/bookmarks", f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {data['url']} → data/bookmarks/{name}.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_bookmarks.py <url1> <url2> ...")
        sys.exit(1)

    for url in sys.argv[1:]:
        try:
            data = fetch_bookmark(url)
            name = sanitize_name(url)
            save_bookmark(data, name)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
