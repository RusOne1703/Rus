import os
import sys
import time
from playwright.sync_api import sync_playwright
from topics_config import TOPICS
from build_articles import generate_article_html

os.makedirs("pdf_articles", exist_ok=True)

def generate_all_pdfs():
    start_time = time.time()
    print("Starting batch PDF generation with Playwright...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for idx, topic in enumerate(TOPICS, 1):
            filename = f"pdf_articles/{topic['id']}.pdf"
            print(f"[{idx}/30] Generating PDF for topic '{topic['id']}'...")

            html_content = generate_article_html(topic)
            page.set_content(html_content, wait_until="load")

            page.pdf(
                path=filename,
                format="A4",
                print_background=True,
                margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
            )
            file_size_kb = os.path.getsize(filename) / 1024
            print(f"    -> Saved: {filename} ({file_size_kb:.1f} KB)")

        browser.close()

    elapsed = time.time() - start_time
    print(f"\nSuccessfully generated all 30 PDF articles in {elapsed:.2f} seconds!")

if __name__ == "__main__":
    generate_all_pdfs()
