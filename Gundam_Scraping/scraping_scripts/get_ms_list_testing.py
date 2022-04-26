# import libraries and modules
from requests import get
from bs4 import BeautifulSoup

def get_mw_list():
    """
    Gets the list of all Mobile Weapons from "smw-column"s on Gundam wiki
    :return: A list of all Mobile Weapons, [..., "/wiki/Zuck", ...]
    """
    
    # initialize url for mobile suit list, parse with BeautifulSoup
    wiki_url = "https://gundam.fandom.com/wiki/Special:BrowseData/Mobile_Weapons?limit=3243&offset=0&_cat=Mobile_Weapons"
    response = get(wiki_url)
    soup_response = BeautifulSoup(response.text, 'html.parser')

    # initialize list of links to individual ms' pages
    mw_links = []

    # search in parsed html for appropriate links
    for smwcols in soup_response.find_all(class_="smw-column"):
        for link in smwcols.find_all("a"):
            l = link.get("href")
            if l not in mw_links:
                mw_links.append(l)


"""Stuff below to verify proper operation"""
# check that numbers match up: 3240 vs 3243
# All Account For!
# # "RB-133 Ball Model 133" --> shows up twice
# # "RX-78 Gundam series" --> shows up twice
# # Weird Pale Rider image one
# print(ms_links)
# print(len(ms_links))