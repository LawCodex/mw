"""Malawi: download the Acts published by the Ministry of Justice
(https://www.justice.gov.mw/resources/laws-and-regulations) and by the Government of Malawi portal
(https://www.malawi.gov.mw, "Acts and Laws" and "Constitution of Malawi" pages).

Only links to statute PDFs are kept (press releases, bills, guidance papers, service charters, fee schedules
are skipped). Cache: _raw/mw/. Usage: python mw_fetch.py
"""
import html
import json
import os
import re
import sys
from urllib.parse import unquote, urljoin

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mw_text import fetch  # noqa: E402

RAW = os.environ.get("MW_RAW", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_raw", "mw"))
PAGES = ["https://www.justice.gov.mw/resources/laws-and-regulations",
         "https://www.justice.gov.mw/resources/laws-and-regulations?page=1",
         "https://www.malawi.gov.mw/index.php/resources/publications/acts",
         "https://www.malawi.gov.mw/index.php/resources/documents/constitution-of-the-republic-of-malawi"]
KEEP = re.compile(r"(?i)\b(act|code|constitution)\b")
DROP = re.compile(r"(?i)bill|memorandum|applauds|guidance|hara|merged|charter|tariff|speech")
DELAY = 3.0


def main():
    items, seen = [], set()
    for k, url in enumerate(PAGES):
        p = fetch(url, os.path.join(RAW, "html", "page%d.html" % k), delay=DELAY)
        h = open(p, encoding="utf-8", errors="replace").read()
        for u, t in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', h, re.S):
            u = html.unescape(u)
            t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()
            if not (u.lower().endswith(".pdf") or "download=" in u) or not t.lower().endswith(".pdf"):
                continue
            title = re.sub(r"(?i)\.pdf$", "", t).replace("_", " ").strip()
            if not KEEP.search(title) or DROP.search(title):
                continue
            u = urljoin(url, u)
            if u in seen:
                continue
            seen.add(u)
            items.append({"title": title, "url": u, "page": url})
    for it in items:
        name = re.sub(r"[^A-Za-z0-9]+", "_", it["title"])[:100] + ".pdf"
        f = fetch(it["url"], os.path.join(RAW, "pdf", name), delay=DELAY, check_pdf=True, timeout=300)
        it["file"] = f
        print(("ok  " if f else "FAIL"), it["title"])
    json.dump(items, open(os.path.join(RAW, "index.json"), "w"), indent=1)


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    main()
