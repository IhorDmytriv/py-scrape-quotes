from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def parse_one_quote(quote: Tag) -> Quote:
    text = quote.select_one("span.text").text
    author = quote.select_one("small.author").text

    tags_container = quote.select_one("div.tags")
    tags = [
        tag.text
        for tag in tags_container.find_all("a", class_="tag")
    ]

    return Quote(text=text, author=author, tags=tags)


def get_quotes() -> list[Quote]:
    content = requests.get(BASE_URL).content
    soup = BeautifulSoup(content, "html.parser")
    quotes = soup.select("div.quote")
    return [parse_one_quote(quote) for quote in quotes]


def main(output_csv_path: str) -> None:
    print(get_quotes())


if __name__ == "__main__":
    main("quotes.csv")
