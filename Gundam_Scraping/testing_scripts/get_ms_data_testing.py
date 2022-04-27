import urllib
import re

from requests import get
from bs4 import BeautifulSoup
from urllib import request

from get_ms_list_testing import get_mw_list

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

    # Get all the data for this ms
    names = aside.find_all("h2", {"class": "pi-item pi-item-spacing pi-title pi-secondary-background"})
    # figure = aside.find_all("figure", {"class": "pi-item pi-image"})[0]
    types = aside.find_all("td")
    # attributes = aside.find_all("div", {"class": "pi-item pi-data pi-item-spacing pi-border-color"})

    # Clean and store name
    cleaned_names = [name.getText() for name in names]
    mw_data["name_en"] = cleaned_names[0]
    if(len(cleaned_names) > 1):
        mw_data["name_jp"] = cleaned_names[1].split(" (")[1].split(")")[0]
    
    # Clean and store type
    cleaned_type = [type.getText() for type in types]
    mw_data["type_main"] = cleaned_type[0].split(" ")[-2] + " " + cleaned_type[0].split(" ")[-1]
    mw_data["type_extra"] = ' '.join(cleaned_type[0].split(" ")[:-2]).split("\t\t\t\t")[1]
    # mw_data["name_en"] = cleaned_names[0]
    # if(len(cleaned_names) > 1):
    #    mw_data["name_jp"] = cleaned_names[1].split(" (")[1].split(")")[0]

    # mw_data["names"] = names
    # mw_data["type"] = cleaned_type

    return mw_data

mw_data0 = get_mw_data(mw_list[12])

print(mw_data0)

"""
total_mw_data = {}
for mw in mw_list:
    print("Getting data on", mw.replace("/wiki/", "") + "...", end="")
    mw_data = get_mw_data(mw)
    print("Done")

    total_mw_data[mw] = mw_data"""


