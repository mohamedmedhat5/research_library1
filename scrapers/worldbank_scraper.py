import requests
import pandas as pd
import re
import os


def extract_year(text):
    match = re.search(r"(20\d{2})", str(text))
    return match.group(1) if match else "Unknown"


def scrape_worldbank():
    records = []

    per_page = 200
    page = 1

    while True:
        url = (
            f"https://api.worldbank.org/v2/sources"
            f"?format=json&per_page={per_page}&page={page}"
        )

        print(f"Fetching page {page}...")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        if len(data) < 2 or not data[1]:
            break

        sources = data[1]

        for src in sources:
            title = src.get("name", "Unknown Dataset")
            dataset_id = src.get("id")
            description = src.get("description", "")

            excel_url = (
                f"https://api.worldbank.org/v2/sources/{dataset_id}/download?format=csv"
            )

            records.append({
                "title": title,
                "pdf_url": None,
                "excel_url": excel_url,
                "source": "World Bank",
                "year": extract_year(title),
                "dataset_id": dataset_id,
                "description": description
            })

        page += 1

    return records


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    data = scrape_worldbank()

    df = pd.DataFrame(data)

    df.to_csv(
        "data/worldbank_documents.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("DONE:", len(df))