"""Malawi: convert downloaded statute PDFs to Markdown (pdftotext; scanned PDFs without a text layer are
skipped — no OCR). Usage: python mw_convert.py <repo_dir>"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mw_text import pdf_text, clean_pages, structure, write_md, slug, text_quality  # noqa: E402

RAW = os.environ.get("MW_RAW", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_raw", "mw"))
TODAY = datetime.date.today().isoformat()


def meta_from_text(title, text):
    cap = re.search(r"CHAPTER\s+(\d+:\d+)", text[:3000])
    year = re.search(r"\b(?:Act|Acts)\s+(?:No\.\s*)?\d+\s+of\s+((?:18|19|20)\d\d)", text[:5000])
    if not year:
        year = re.search(r"\b((?:18|19|20)\d\d)\b", title)
    return (cap.group(1) if cap else ""), (year.group(1) if year else "")


def main(repo):
    items = json.load(open(os.path.join(RAW, "index.json")))
    n = 0
    for it in items:
        if not it.get("file"):
            continue
        pages, ocr = pdf_text(it["file"])
        full = "\n".join(pages)
        if len(full.strip()) < 500 or text_quality(full) < 0.75:
            print("SKIP (no usable text layer)", it["title"], round(text_quality(full), 2))
            it["skipped"] = True
            continue
        title = re.sub(r"\s+", " ", it["title"]).strip()
        cap, year = meta_from_text(title, full)
        if re.search(r"\[Ch\d+s\d+", full):
            # Laws of Malawi electronic edition: "[Ch0701s1]1." anchors precede each section, title on next line
            pages = [re.sub(r"\s*\[Ch\d+s(\d+[A-Z]*)\]\s*\d*[A-Z]*\.?\s*\n\s*([^\n]{2,200})\n",
                            lambda m: "\n\nSection %s — %s\n" % (m.group(1), m.group(2).strip()), p) for p in pages]
        body = structure(clean_pages(pages), "en")
        typ = "constitution" if "constitution" in title.lower() else ("code" if "code" in title.lower() else "act")
        if typ == "constitution":
            path = os.path.join(repo, "constitution", "constitution-of-malawi.md")
            title = "Constitution of the Republic of Malawi"
        else:
            name = ("cap-" + cap.replace(":", "-") + "-" if cap else (year + "-" if year else "")) + slug(title)
            path = os.path.join(repo, "acts", name + ".md")
        meta = {"title": title, "identifier": ("Cap. " + cap) if cap else "", "type": typ, "jurisdiction": "mw",
                "language": "en", "year": year, "status": "unknown", "source": it["url"], "retrieved": TODAY}
        write_md(path, meta, title, body)
        n += 1
    json.dump(items, open(os.path.join(RAW, "index.json"), "w"), indent=1)
    print("written", n)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
