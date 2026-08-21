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

def count_pure_text_words(html_str):
    parser = HTMLTextExtractor()
    parser.feed(html_str)
    clean_text = parser.get_data()
    words = [w for w in clean_text.split() if len(w) > 1 or w.isalnum()]
    return len(words)

if __name__ == "__main__":
    for idx, topic in enumerate(TOPICS, 1):
        html = generate_article_html(topic)
        words = count_pure_text_words(html)
        print(f"[{idx}/30] Topic ID: '{topic['id']}' -> Pure Text Word Count: {words}")
        assert words >= 1500, f"Topic {topic['id']} pure text has less than 1500 words ({words} words)"

    print("\n✅ Verified: All 30 topics exceed 1500 pure readable words!")
