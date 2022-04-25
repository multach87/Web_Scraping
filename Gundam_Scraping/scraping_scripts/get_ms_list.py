from requests import get
from bs4 import BeautifulSoup


def get_ms_list():
    """
    Gets the list of all ms from a <table> on the Animal Crossing Fandom wiki
    :return: A list of all villages, ["/wiki/Admiral", ...]
    """

    # The URL of the Animal Crossing Wiki
    wiki_url = "https://gundam.fandom.com/wiki/The_Gundam_Wiki/ms_list_(New_Horizons)"

    # Get the page and parse it with BeautifulSoup
    response = get(wiki_url)
    soup_response = BeautifulSoup(response.text, 'html.parser')

    # Try to locate the specific table containing all the ms
    ms_table = []
    found = False

    # NOTES:
    # # Letter delineator: ' div class="smw-column-header" '
    # # # Item delineator: ' ::marker '
    # # # # MS Page link: ' "[/wiki/]...[" title=] '

    # Check each table
    for table in soup_response.find_all("table"):

        # The head of the "ms" table has a link to a general "ms" page
        for link in table.find_all("a"):
            if "/wiki/ms" in link.get("href"):
                ms_table = table
                found = True
                break
        if found:
            break

    # Only add each link once
    links = []
    for tr in ms_table.find_all("tr"):

        # The first column for each ms is uniquely bolded
        for bolded in tr.find_all("b"):
            for link in bolded.find_all("a"):
                l = link.get("href")
                if l not in links:
                    links.append(l)

    return links