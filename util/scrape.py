#Scrapes foosball rules from the official foosball website
#and produces a rules.json file.

from bs4 import BeautifulSoup
import json
import requests

class Scraper:

    def __init__(self, destintation_file):
        self.destintation_file = destintation_file
        html = requests.get("http://www.foosball.com/learn/rules/ustsa/").text
        self.soup = BeautifulSoup(html, 'lxml')

    def parse(self):
        return self.__dfs(self.soup.ol)

    def __dfs(self, node):
        if len(node.contents) <= 1:
            return node.text.replace("\n", "").replace("\r", "")
        else:
            return [self.__dfs(i) for i in node.findChildren()]

if __name__ == "__main__":
    scrape = Scraper("test").parse()
    print scrape
