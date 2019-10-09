from bs4 import BeautifulSoup


def unique(list1): 
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def get_href(url, soup):
    url_list = []
    for tag in soup.find_all("a"):
        if (tag["href"]).startswith("http"):
            url_list.append(tag["href"])
        else:
            url_list.append(url+tag["href"])
    return url_list

def get_src(url, soup):
    url_list = []
    for tag in soup.find_all(["img", "script"]):
        try:
            if (tag["src"]).startswith("http"):
                url_list.append(tag["src"])
            else:
                url_list.append(url+tag["src"])
        except KeyError:
            continue
    return url_list

def remove_other_domain(base_url, url_list):
    garbage_url_list = []
    for url in url_list:
        if not url.split("//")[1].startswith(base_url.split("//")[1].split(".")[0]):
            garbage_url_list.append(url)
    
    for url in garbage_url_list:
        url_list.remove(url)
    return [url_list, garbage_url_list]

