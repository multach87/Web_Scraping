# import libraries and modules
from requests import get
from bs4 import BeautifulSoup

def get_list():
    """
    Gets the list of all Mobile Weapons from "smw-column"s on Gundam wiki
    :return: A list of all Mobile Weapons, [..., "/wiki/Zuck", ...]
    """
    
    # initialize url for mobile suit list, parse with BeautifulSoup
    wiki_url = "https://gundam.fandom.com/wiki/Special:BrowseData/Mobile_Weapons?limit=3243&offset=0&_cat=Mobile_Weapons"
    #wiki_url = "https://gundam.fandom.com/wiki/Special:BrowseData/Mobile_Weapons?limit=100&offset=0&_cat=Mobile_Weapons"
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
    
    # store the links
    return mw_links


if __name__ == "__main__":
    mw_list = get_list()
    print(len(mw_list))