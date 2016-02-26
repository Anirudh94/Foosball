#Scrapes foosball rules from the official foosball website
#and produces a rules.json file.

from bs4 import BeautifulSoup
import json
import requests

class Scraper:

    def parse_long(self):
        self.setup_soup("http://www.foosball.com/learn/rules/ustsa/")
        return self.__dfs(self.soup.ol)

    def parse_short(self):
        self.setup_soup("http://www.foosball.com/learn/rules/onepage/")
        return self.short()

    def setup_soup(self, url):
        html = requests.get(url).text
        self.soup = BeautifulSoup(html, 'lxml')

    def __dfs(self, node):
        if len(node.contents) <= 1:
            return node.text.replace("\n", "").replace("\r", "")
        else:
            return [self.__dfs(i) for i in node.findChildren()]

    def short(self):
        tree = {}
        current_rule = ""
        tables = self.soup.findAll("td")
        table_list = tables[0].text.split("\n")
        table_list.extend(tables[1].text.split("\n"))

        for i in tables:
            i = i.strip()
            if self.startsWithNumber(i):
                current_rule = i
                tree[current_rule] = []
            else:
                tree[current_rule].append(i)
        print tree

    def startsWithNumber(self, i):
        return i[0].isdigit()

if __name__ == "__main__":
    scrape = Scraper().parse_short()
