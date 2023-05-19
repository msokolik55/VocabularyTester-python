from bs4 import BeautifulSoup
from requests import get
from threading import Thread
from time import sleep

BASE = "https://www.50languages.com/sk/learn"
START_PAGE = 1
END_PAGE = 42


class Language:
    def __init__(self, short, start=START_PAGE, end=END_PAGE):
        assert start <= end
        assert self.in_range(start)
        assert self.in_range(end)

        self.start = start
        self.end = end

        self.words = []

        pages = self.fill_pages(short)
        try:
            threads = [Thread(target=self.add_words, args=[page])
                       for page in pages]
            for t in threads:
                t.start()
        except Exception as e:
            print(e)
            return None

        for t in threads:
            t.join()

        self.filename = f"{short}.md"
        self.save()

    def in_range(self, n):
        return n >= START_PAGE and n <= END_PAGE

    def fill_pages(self, short):
        if not self.in_range(self.start) or not self.in_range(self.end):
            print(
                f"Given pages ids are not in range: {START_PAGE} - {END_PAGE}")
            return []

        result = [
            f"{BASE}/learn-vocab/{short}/{i}" for i in range(self.start, self.end + 1)]
        result.append(f"{BASE}/vocab/{short}")
        return result

    def get_words(self, soup, tag, attrs):
        elems = soup.find_all(tag, attrs)

        words = []
        for elem in elems:
            if elem.find("br"):
                str_elem = str(elem)
                content = str_elem.split("<br")[0].split("\n")[-1]
            else:
                content = str(elem.string)

            words.append(content.strip().lower())

        return words

    def add_words(self, page):
        content = get(page).content.decode()
        soup = BeautifulSoup(content, "html.parser")

        translations = self.get_words(
            soup, "p", {"class": "mb-lg v_style1"})
        foreigns = self.get_words(soup, "h4", {"class": "mb-sm text-blue"})

        self.words += list(zip(translations, foreigns))
        print(f"{page} processed.")

    def save(self):
        with open(self.filename, "w") as out:
            for trans, foreign in self.words:
                print(f"{trans} = {foreign}", file=out)
        print(f"Words saved into: {self.filename}")
