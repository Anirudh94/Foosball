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
        return self.__short()

    def setup_soup(self, url):
        html = requests.get(url).text
        self.soup = BeautifulSoup(html, 'lxml')

    def __dfs(self, node):
        if len(node.contents) <= 1:
            return node.text.replace("\n", "").replace("\r", "")
        else:
            return [self.__dfs(i) for i in node.findChildren()]

    def __short(self):
        table = self.__get_tables()
        rule_dict = self.__build_rule_dict(table)
        self.__write_rules(rule_dict)

    def __get_tables(self):
        tables = self.soup.findAll("td")
        table_one = re.split("[0-9]+\.", tables[0].text)
        table_two = re.split("[0-9]+\.", tables[1].text)
        table_one.extend(table_two)
        return table_one

    def __build_rule_dict(self, html):
        rule_dict = {}
        for i in html:
            i = self.__cleanup_string(i)
            rule_name = i[0]
            rules = "".join(i[1:])
            rule_dict[rule_name] = re.split("[A-Z]\.", rules)
        return rule_dict

    def __cleanup_string(self, string):
        string = re.sub(' +',' ', string)
        string = string.encode('ascii', 'ignore')
        string = string.split("\n")
        string = [j.strip("\t\r ") for j in string]
        return string

    def __write_rules(self, rule_dict):
        with open('rules.json', 'w') as f:
            json.dump(rule_dict, f)


if __name__ == "__main__":
    scrape = Scraper().parse_short()
