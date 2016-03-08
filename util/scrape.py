from bs4 import BeautifulSoup
import json
import requests
import re

class Scraper:
    """
    Scrapes foosball rules from the official foosball website
    and produces a rules.json file.
    """
    def parse_long(self):
        """Parses the long rules list"""
        self.setup_soup("http://www.foosball.com/learn/rules/ustsa/")
        return self._dfs(self.soup.ol)

    def parse_short(self):
        """Parses the short rules list"""
        self.setup_soup("http://www.foosball.com/learn/rules/onepage/")
        return self._short()

    def setup_soup(self, url):
        """initializes the soup object given a url"""
        html = requests.get(url).text
        self.soup = BeautifulSoup(html, "lxml")

    def _dfs(self, node):
        """
        perform a dfs and make a list of lists representing a tree of
        rules
        """
        if len(node.contents) <= 1:
            return node.text.replace("\n", "").replace("\r", "")
        else:
            return [self._dfs(i) for i in node.findChildren()]

    def _short(self):
        """implmentation method for short html parse"""
        table = self._get_tables()
        rule_dict = self._build_rule_dict(table)
        self._write_rules(rule_dict)

    def _get_tables(self):
        """get the table html text from the rules list"""
        tables = self.soup.findAll("td")
        table_one = re.split("[0-9]+\.", tables[0].text)
        table_two = re.split("[0-9]+\.", tables[1].text)
        table_one.extend(table_two)
        return table_one

    def _build_rule_dict(self, html):
        """build the tree of rules as a dictionary"""
        rule_dict = {}
        for i in html:
            i = self._cleanup_string(i)
            rule_name = i[0]
            rules = "".join(i[1:])
            rule_dict[rule_name] = re.split("[A-Z]\.", rules)
        return rule_dict

    def _cleanup_string(self, string):
        """cleanup gunk on strings new lines, tabs carriage returns etc"""
        string = re.sub(" +"," ", string)
        string = string.encode("ascii", "ignore")
        string = string.split("\n")
        string = [j.strip("\t\r ") for j in string]
        return string

    def _write_rules(self, rule_dict):
        """write the rules to a json file"""
        with open("rules.json", "w") as f:
            json.dump(rule_dict, f)


if __name__ == "__main__":
    scrape = Scraper().parse_short()
