#!/usr/bin/env python3
import os
import re
import sys
import argparse
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Pattern for files we DO want (your original constraint)
TARGET_PATTERN = re.compile(r"/_media/.*\.pdf$", re.IGNORECASE)

# 🔒 Patterns for filenames we want to SKIP.
# Add or edit these as you like.
RESTRICTED_PATTERNS = [
    re.compile(r"plenum", re.IGNORECASE),
    re.compile(r"lf-plenum", re.IGNORECASE),
    re.compile(r"oving", re.IGNORECASE),
    #re.compile(r"tma4412", re.IGNORECASE),
    # re.compile(r"secret", re.IGNORECASE),  # example
]


def is_restricted(filename: str) -> bool:
    """Return True if filename matches any restricted pattern."""
    for pat in RESTRICTED_PATTERNS:
        if pat.search(filename):
            return True
    return False


def find_matching_links(page_url: str):
    """Fetch page_url and return a set of absolute URLs for matching PDF links."""
    print(f"[+] Fetching page: {page_url}")
    resp = requests.get(page_url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if TARGET_PATTERN.search(href):
            full_url = urljoin(page_url, href)
            links.add(full_url)

    print(f"[+] Found {len(links)} matching links (before restriction filter)")
    return links


def download_file(file_url: str, output_dir: str):
    """Download a single file into output_dir (unless restricted)."""
    parsed = urlparse(file_url)
    filename = os.path.basename(parsed.path) or "downloaded_file"

    # 🔒 Check restriction before downloading
    if is_restricted(filename):
        print(f"[!] Skipping restricted file: {filename}")
        return

    dest_path = os.path.join(output_dir, filename)

    # Avoid overwriting existing files
    base, ext = os.path.splitext(dest_path)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = f"{base}_{counter}{ext}"
        counter += 1

    print(f"[+] Downloading {file_url} -> {dest_path}")

    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        os.makedirs(output_dir, exist_ok=True)
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"[+] Done: {dest_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Download all PDF files with pattern '/_media/tma4412/2025h/' from a given URL."
    )
    parser.add_argument("url", help="Page URL to scan for links")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="downloads",
        help="Directory to save downloaded files (default: downloads)",
    )

    args = parser.parse_args()

    try:
        links = find_matching_links(args.url)
        if not links:
            print("[!] No matching links found.")
            sys.exit(0)

        for link in links:
            try:
                download_file(link, args.output_dir)
            except Exception as e:
                print(f"[!] Failed to download {link}: {e}")

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
