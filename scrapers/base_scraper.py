import re
import pandas as pd


class BaseScraper:
    def __init__(self, source_name):
        self.source_name = source_name
        self.records = []
        self.seen_titles = set()

    def extract_year(self, text):
        match = re.search(r"(20\d{2})", str(text))
        return match.group(1) if match else "Unknown"

    def add_record(self, title, pdf_url=None, excel_url=None):
        if not title:
            return

        key = title.strip()

        existing = next(
            (r for r in self.records if r["title"] == key),
            None
        )

        if existing:
            if pdf_url:
                existing["pdf_url"] = pdf_url
            if excel_url:
                existing["excel_url"] = excel_url
            return

        self.records.append({
            "title": key,
            "pdf_url": pdf_url,
            "excel_url": excel_url,
            "source": self.source_name,
            "year": self.extract_year(title)
        })

    def save(self, path):
        df = pd.DataFrame(self.records)
        df.to_csv(path, index=False)