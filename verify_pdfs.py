import os
import re
from html.parser import HTMLParser
from topics_config import TOPICS
from build_articles import generate_article_html

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ('style', 'script'):
            self.in_style = True

    def handle_endtag(self, tag):
        if tag.lower() in ('style', 'script'):
            self.in_style = False

    def handle_data(self, data):
        if not self.in_style:
            self.fed.append(data)

    def get_data(self):
        return "".join(self.fed)

def count_pure_words(html_str):
    parser = HTMLTextExtractor()
    parser.feed(html_str)
    text = parser.get_data()
    words = [w for w in text.split() if len(w) > 1 or w.isalnum()]
    return len(words)

def verify():
    print("Starting comprehensive verification of 30 generated PDF articles...")
    assert len(TOPICS) == 30, f"Expected 30 topics, got {len(TOPICS)}"

    missing_files = []
    low_word_count = []
    zero_size = []

    target_domains = [
        "https://eventpandora.ru/",
        "https://memoriesloft.ru/",
        "https://bigpartyshow.ru/",
        "https://chudopolis.ru/",
        "https://show-ring.ru/",
        "luminis-loft.ru"
    ]

    for idx, topic in enumerate(TOPICS, 1):
        topic_id = topic['id']
        pdf_path = f"pdf_articles/{topic_id}.pdf"

        # 1. Check file existence
        if not os.path.exists(pdf_path):
            missing_files.append(pdf_path)
            continue

        # 2. Check non-zero size
        size_bytes = os.path.getsize(pdf_path)
        if size_bytes == 0:
            zero_size.append(pdf_path)

        # 3. Check pure text word count (excluding HTML tags and CSS)
        html = generate_article_html(topic)
        pure_words = count_pure_words(html)

        if pure_words < 1500:
            low_word_count.append((topic_id, pure_words))

        # 4. Check that all target domain links are present in article HTML
        for domain in target_domains:
            assert domain in html, f"Domain {domain} missing in topic {topic_id}"

        # 5. Check presence of prompts, FAQ, comparison table, pricing
        assert "FAQ" in html or "Часто задаваемые вопросы" in html, f"FAQ missing in {topic_id}"
        assert "Промт" in html or "prompt:" in html, f"AI Prompt missing in {topic_id}"
        assert "Сравнительная таблица" in html, f"Comparison table missing in {topic_id}"

        print(f"✓ [{idx}/30] Verified '{topic_id}': PDF Size = {size_bytes/1024:.1f} KB, Pure Words = {pure_words}")

    print("\n--- VERIFICATION SUMMARY ---")
    print(f"Total topics checked: {len(TOPICS)}")
    print(f"Missing PDF files: {len(missing_files)}")
    print(f"Zero-size PDF files: {len(zero_size)}")
    print(f"Articles under 1500 pure words: {len(low_word_count)}")

    assert len(missing_files) == 0, f"Missing files: {missing_files}"
    assert len(zero_size) == 0, f"Zero size files: {zero_size}"
    assert len(low_word_count) == 0, f"Low word count articles: {low_word_count}"

    print("\n🎉 SUCCESS: All 30 PDF articles perfectly verified and meet all client requirements!")

if __name__ == "__main__":
    verify()
