from playwright.sync_api import sync_playwright
import pandas as pd
import re
import os


def extract_year(text):
    match = re.search(r"(20\d{2})", str(text))
    return match.group(1) if match else "Unknown"


def get_title(link):
    BAD_TITLES = {
        "الدورية",
        "تحميل",
        "pdf",
        "excel",
        "xlsx"
    }

    try:
        texts = link.evaluate("""
            (el) => {
                let container = el.closest('.d-flex');

                if (!container) return [];

                let parent = container.parentElement;

                if (!parent) return [];

                return parent.innerText
                    .split('\\n')
                    .map(x => x.trim())
                    .filter(x => x.length > 3);
            }
        """)

        for txt in texts:
            if (
                txt not in BAD_TITLES
                and ".pdf" not in txt.lower()
                and ".xls" not in txt.lower()
                and len(txt) > 8
            ):
                return txt

        return ""

    except:
        return ""


def collect_documents(page, records, seen_titles):
    links = page.query_selector_all("a")

    grouped = {}

    for link in links:
        try:
            href = link.get_attribute("href")

            if not href or "/documents/" not in href:
                continue

            full_url = (
                "https://www.stats.gov.sa" + href
                if href.startswith("/")
                else href
            )

            title = get_title(link)

            if not title:
                continue

            if title not in grouped:
                grouped[title] = {
                    "pdf_url": None,
                    "excel_url": None
                }

            href_lower = href.lower()

            if ".pdf" in href_lower:
                grouped[title]["pdf_url"] = full_url

            elif ".xls" in href_lower or ".xlsx" in href_lower:
                grouped[title]["excel_url"] = full_url

        except:
            continue

    added = 0

    for title, files in grouped.items():
        if title in seen_titles:
            continue

        seen_titles.add(title)
        added += 1

        records.append({
            "title": title,
            "pdf_url": files["pdf_url"],
            "excel_url": files["excel_url"],
            "source": "Saudi Statistics",
            "year": extract_year(title)
        })

    return added


def scrape_saudi():
    records = []
    seen_titles = set()

    main_url = "https://www.stats.gov.sa/statistics?index=119021&subindex=120034"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(main_url, wait_until="networkidle")
        page.wait_for_timeout(5000)

        category_ids = page.evaluate("""
            () => Array.from(
                document.querySelectorAll("a[data-category-id]")
            ).map(el => el.getAttribute("data-category-id"))
        """)

        category_ids = list(set(category_ids))

        print(f"Found {len(category_ids)} categories")

        for i, cat_id in enumerate(category_ids, start=1):
            url = f"https://www.stats.gov.sa/ar/statistics-tabs?tab=436312&category={cat_id}"

            try:
                print(f"[{i}/{len(category_ids)}]")

                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(2500)

                added = collect_documents(page, records, seen_titles)

                print(f"Added: {added} | Total: {len(records)}")

            except Exception as e:
                print("Failed:", e)

        browser.close()

    return records


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    data = scrape_saudi()

    pd.DataFrame(data).to_csv(
        "data/saudi_documents.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("DONE:", len(data))