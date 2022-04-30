import urllib
import re

from requests import get
from bs4 import BeautifulSoup
from urllib import request

from mslist_forscrap import get_mw_list

mw_list = get_mw_list()

wiki_url = "https://gundam.fandom.com"

def get_mw_data(ms_name: str):
    """
    Scrape all the data for a given ms from the Gundam Fandom wiki.
    :param ms_name: the name of the ms, i.e. "Zucker"
    :return: A dictionary of all the data scraped for the respective ms
    """

    # Get the page and parse it with BeautifulSoup
    response = get(wiki_url + ms_name)
    soup_response = BeautifulSoup(response.text, 'html.parser')

    # Will store the data as a dictionary and write it as JSON later
    mw_data = {}

    # The "aside" is an HTML element containing all the important ms information
    aside = soup_response.findAll("aside")[0]

    # initialize attribute keys and values
    attrs_key = []
    attrs_val = []

    # Get all the data for this ms
    names = aside.find_all("h2", {"class": \
        "pi-item pi-item-spacing pi-title pi-secondary-background"})
    types = aside.find_all("td")
    measures = ['Height', 'Weight', 'Power Output', 'Sensor Range', \
        'Acceleration', 'Speed']
    

    # Clean and store name
    cleaned_names = [name.getText() for name in names]
    # print(cleaned_names)
    # mw_data["name_en"] = cleaned_names[0]
    attrs_valname = []
    attrs_key.append("names")
    attrs_valname.append(cleaned_names[0])
    if(len(cleaned_names) > 1):
        # mw_data["name_jp"] = cleaned_names[1].split(" (")[1].split(")")[0]
        # attrs_key.append("name_jp")
        attrs_valname.append(cleaned_names[1].split(" (")[1].split(")")[0])
    attrs_val.append(attrs_valname)

    # Get section heads
    h2s = aside.findAll("h2", {"class": \
        "pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background"})
    
    cleaned_h2s = [h2.getText() for h2 in h2s]

    # search in parsed html for appropriate links
    """for smwcols in soup_response.find_all(class_="smw-column"):
        for link in smwcols.find_all("a"):
            l = link.get("href")
            if l not in mw_links:
                mw_links.append(l)"""

    for sections in aside.findAll("section", {"class": \
        "pi-item pi-group pi-border-color"})[1:]:
        # attributes = 
        h2 = sections.findAll("h2", {"class": \
            "pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background"})[0].getText()
        for attribute in sections.find_all("div", {"class": \
            "pi-item pi-data pi-item-spacing pi-border-color"}):
        # # # initialize values list for attributes with multiple values
            attrs_val2 = []

            # # # store attribute name/key
            key = print(''.join(h2.split(" ")) + "_" + ''.join(attribute.find_all("h3")[0].getText().split(" ")))

            # # # for handling Overall Height in multiple measurement units
            for value in attribute.find_all("li"):
                if value.findChildren("span", {"class": "smwtext"}):
                    attrs_val2.append(value.findChildren("span", {"class": \
                        "smwtext"})[0].getText())
                else:
                    attrs_val2.append(value.getText())
            
            # # # store attribute value
            value = attribute.find_all("div")[0]
            
            # # # update keys and values
            attrs_key.append(key)
            attrs_val.append(attrs_val2)

    # # zip together attribute key and value into dictionary
    mw_data = dict(zip(attrs_key, attrs_val))
    """# # Separate measurements from units
    for dicts in mw_data:
        if any(ele in dicts for ele in measures):
            mw_data[dicts] = mw_data[dicts][0].split(" ", 1)
            mw_data[dicts][0] = float(mw_data[dicts][0])"""

    return(mw_data)

mw_data0 = get_mw_data(mw_list[12])

print(mw_data0)

# print(mw_list[1])