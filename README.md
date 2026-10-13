# Malawi (MW) — legislation as Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

**Minimal corpus.** Legislation of the Republic of Malawi, in **English**, limited to what the Government of
Malawi publishes openly on its own websites: the **Constitution** and a selection of principal Acts (Penal Code,
Citizenship, Employment, Child Care, Disability, Corrupt Practices, Police, Prisons, Marriage and Family
Relations, Human Rights Commission, Liquid Fuels and Gas...). Retrieved 2026-10-13.

| Category | Files |
|---|---|
| Constitution | 1 |
| Acts / Codes | 12 |
| **Total** | **13** |

## Structure

```
constitution/constitution-of-malawi.md      Constitution of the Republic of Malawi (1995, as amended — version on the portal)
acts/cap-<chapter>-<slug>.md                 Acts that carry a Laws of Malawi chapter number (e.g. cap-7-01-penal-code.md)
acts/<year>-<slug>.md / acts/<slug>.md       other Acts
```

Front matter: `identifier` (Laws of Malawi chapter, e.g. `Cap. 7:01`, when printed in the text), `year` (year of
the Act, from the text, when found), `status: unknown`, `source` (PDF URL). Text was extracted from the PDFs with
poppler `pdftotext`; parts/chapters become headings and sections become `Section N — <title>` headings where the
structure could be recognised. Scanned PDFs without a text layer were skipped (no OCR).

## Not covered / known gaps

* This is **not** the complete statute book. There is no open official database of Malawi legislation: the
  Parliament of Malawi website (parliament.gov.mw) sits behind a Cloudflare bot challenge (not circumvented), the
  Malawi Law Commission (lawcom.gov.mw) does not publish Acts, and the Ministry of Justice publishes only ~15 Acts.
  The Malawi Legal Information Institute (MalawiLII) forbids scraping/bulk download and was not used.
* Skipped: **Gender Equality Act** and **Access to Information Act** (MoJ PDFs are scans without usable text),
  **Data Protection Act 2024** (the portal's download returned an invalid/truncated PDF).
* Subsidiary legislation, Bills, gazettes are not included.

## Sources

| Source | URL |
|---|---|
| Ministry of Justice — Laws and Regulations | https://www.justice.gov.mw/resources/laws-and-regulations |
| Government of Malawi portal — Acts and Laws; Constitution of Malawi | https://www.malawi.gov.mw/index.php/resources/publications/acts , https://www.malawi.gov.mw/index.php/resources/documents/constitution-of-the-republic-of-malawi |

Official texts of the Government of Malawi; both sites allow crawling (robots.txt `Allow: /`). Downloads were made
with an identifying User-Agent at one request every 3 s.

## Regenerate

```
pip install -r scripts/requirements.txt     # plus poppler (pdftotext, pdfinfo)
python scripts/mw_fetch.py                  # downloads into ../_raw/mw/
python scripts/mw_convert.py .
```
