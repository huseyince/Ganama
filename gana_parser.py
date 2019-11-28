from bs4 import BeautifulSoup
import requests as req

with open("country_list", "r") as c_list:
    country_list = [x[:-1] for x in c_list.readlines()]


def unique(list1: list) -> list:
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def get_href(url: str, soup: BeautifulSoup) -> list:
    url_list = []
    for tag in soup.find_all("a"):
        try:
            if (tag["href"]).startswith("http"):
                url_list.append(tag["href"])
            elif (tag["href"]).startswith("/"):
                url_list.append(url.split("://")[0]+"://"+url.split("://")[1].split("/")[0]+tag["href"])
            elif (tag["href"]).startswith("javascript"):
                continue
            elif (tag["href"]).startswith("$"):
                continue
            elif (tag["href"]).startswith("#"):
                continue
            elif (tag["href"]).startswith(""):
                continue
            elif (tag["href"]).startswith("mailto"):
                continue
            elif (tag["href"]).startswith("tel"):
                continue
            else:
                url_list.append(url+tag["href"])
        except KeyError:
            continue
    return url_list

def get_src(url: str, soup: BeautifulSoup) -> list:
    url_list = []
    for tag in soup.find_all(["img", "script"]):
        try:
            if (tag["src"]).startswith("http"):
                url_list.append(tag["src"])
            elif (tag["src"]).startswith("/"):
                url_list.append(url.split("://")[0]+"://"+url.split("://")[1].split("/")[0]+tag["src"])
            elif (tag["src"]).startswith("$"):
                continue
            else:
                url_list.append(url+tag["src"])
        except KeyError:
            continue
    return url_list

def remove_other_domain(base_url: str, url_list: list) -> list:
    garbage_url_list = []
    for url in url_list:
        if base_url.split("://")[1].split("/")[0].split(".")[-1] in country_list:
            if len(base_url.split("://")[1].split("/")[0].split(".")) == 2:
                domain = base_url.split("://")[1].split("/")[0].split(".")[-2]
            else:
                domain = base_url.split("://")[1].split("/")[0].split(".")[-3]
        else:
            domain = base_url.split("://")[1].split("/")[0].split(".")[-2]
        if url.split("://")[1].split("/")[0].split(".")[-1] in country_list:
            if len(url.split("://")[1].split("/")[0].split(".")) == 2:
                iter_url = url.split("://")[1].split("/")[0].split(".")[-2]
            else:
                iter_url = url.split("://")[1].split("/")[0].split(".")[-3]
        else:
            iter_url = url.split("://")[1].split("/")[0].split(".")[-2]
        if iter_url != domain:
            garbage_url_list.append(url)
    
    for url in garbage_url_list:
        url_list.remove(url)
    return [url_list, garbage_url_list]

def main(url: str) -> list:
    response = req.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    url_list = get_href(url, soup)
    url_list += get_src(url, soup)
    url_list = unique(url_list)

    clean, garbage = remove_other_domain(url, url_list)

    return [clean, garbage]