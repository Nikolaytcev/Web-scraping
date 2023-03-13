import requests

from fake_headers import Headers

from bs4 import BeautifulSoup

from pprint import pprint

import re

import json


def get_headers():
    return Headers(browser="hrome", os="win").generate()


def get_links(data_list):
    return map(lambda x: x["href"], data_list)


def get_one_link_info(link):
    print(link)
    data = {}
    info = requests.get(link, headers=get_headers()).text
    bs = BeautifulSoup(info, features="lxml")
    description = bs.find(class_="vacancy-description").text
    if "Django" in description and "Flask" in description:
        data["link"] = link
        data["company"] = bs.find(class_="vacancy-company-name").text
        data["salary"] = (
            bs.find(class_="vacancy-title")
            .find(class_="bloko-header-section-2 bloko-header-section-2_lite")
            .text
        )
        city = re.findall(
            r"(Москва)|(Санкт-Петербург)",
            bs.find(class_="vacancy-company-redesigned").text,
        )
        data["city"] = [i for i in city[0] if i][0]
    return data


def get_true_info(links):
    all_data = list(filter(lambda x: x, map(lambda x: get_one_link_info(x), links)))
    pprint(all_data)
    with open("data_info.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)


def main():
    titles = []
    HOST = f"https://spb.hh.ru/search/vacancy?area=1&area=2&ored_clusters=true&text=Python&search_period=1&page=0"
    info = requests.get(HOST, headers=get_headers()).text
    titles_list = BeautifulSoup(info, features="lxml").find_all(
        class_="serp-item__title"
    )
    titles += titles_list
    i = 1
    while titles_list:
        HOST = f"{HOST[:-1]}{str(i)}"
        info = requests.get(HOST, headers=get_headers(), timeout=2).text
        titles_list = BeautifulSoup(info, features="lxml").find_all(
            class_="serp-item__title"
        )
        titles += titles_list
        print(f"page #{i}")
        i += 1
    links = get_links(titles)
    get_true_info(links)


if __name__ == "__main__":
    main()
