#Scrapes foosball rules from the official foosball website
#and produces a rules.json file.

from bs4 import BeautifulSoup
import json
import requests
import re

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
        table_one = re.split("[0-9]+\.", tables[0].text)
        table_two = re.split("[0-9]+\.", tables[1].text)
        table_one.extend(table_two)

        for i in table_one:
            i = i.encode('ascii', 'ignore')
            i = i.split("\n")
            i = [j.strip("\t\r") for j in i]
            rule_name = i[0].strip(" ")
            rules = "".join(i[1:])
            tree[rule_name] = re.split("[A-Z]\.", rules)

        with open('rules.json', 'w') as f:
                json.dump(tree, f)

    def startsWithNumber(self, i):
        return i[0].isdigit()

if __name__ == "__main__":
    scrape = Scraper().parse_short()
