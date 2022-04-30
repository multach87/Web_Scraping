from tkinter.messagebox import NO
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
    Scrape all the data for a given mw from the Gundam Fandom wiki.
    :param ms_name: the url-ized version of the mw name, \
        e.g., GX-9900-DV_Gundam_X_Divider
    :return: A dictionary of all the data scraped for the respective ms\
        -All attributes are pre-pended with "SectionHeader_"
        -All section names and attribute names have spaces removed
        -Measurements are separated into 2-item lists with float for the value\
            and string for the unit of measurement
        -All Armament attributes are 2-item lists:
            -List of armaments (string)
            -List of floats corresponding to each\
                armament in first string list
                e.g., [['Beam Sword', 'Breast Vulcan'], [2, 2]]\
                    indicates an mw has 2 beam swords and 2 breast vulcans
    """

    # Get the page and parse it with BeautifulSoup
    response = get(wiki_url + ms_name)
    soup_response = BeautifulSoup(response.text, 'html.parser')

    # Will store the data as a dictionary and write it as JSON later
    mw_data = {}

    # The "aside" is an HTML element containing all the important mw information
    aside = soup_response.findAll("aside")[0]

    # initialize lists of attribute keys and values
    attrs_key = []
    attrs_val = []

    # Get names and types for mw (i.e., the single-item sections)
    names = aside.find_all("h2", {"class": \
        "pi-item pi-item-spacing pi-title pi-secondary-background"})
    types = aside.find_all("td")

    # Clean and store name
    cleaned_names = [name.getText() for name in names]
    # # Add "name" to keys list
    attrs_key.append("names")
    # # Initialize value list for names
    attrs_valname = []
    # # Store english name
    attrs_valname.append(cleaned_names[0].lower())
    # # Check for japanese name and add to names value list
    if(len(cleaned_names) > 1):
        attrs_valname.append(cleaned_names[1].split(" (")[1].split(")")[0])
    # # Add list of name values to values list
    attrs_val.append(attrs_valname)
    
    # Clean and store type
    cleaned_type = [type.getText() for type in types]
    # # Add "type" to keys list
    attrs_key.append("type")
    # # Initialize value list for type
    attrs_valtype = []
    # # Store main value for type
    attrs_valtype.append((cleaned_type[0].split(" ")[-2] + \
        " " + cleaned_type[0].split(" ")[-1]).lower())
    # # Store type qualifier value
    attrs_valtype.append((' '.join(cleaned_type[0].\
        split(" ")[:-2]).split("\t\t\t\t")[1]).lower())
    # # Add list of type values to values list
    attrs_val.append(attrs_valtype)

    # Clean and store image urls, image captions
    # # Add "imgs" to keys list
    attrs_key.append("imgs")
    # # Initialize lists of captions and urls
    img_urls = []
    img_capts = []
    # # Append each link, caption to list
    for link in aside.find_all("a", {"class": \
        "image image-thumbnail"}):
        l = link.get("href")
        c = link.get("title")
        img_urls.append(l)
        img_capts.append(c)
    # # Add list of image urls and list of cpations to values list
    attrs_val.append([img_urls, img_capts])

    # Clean and store the attribute data
    # # Loop over all mw attribute sections except first \
    # # (which is covered in the "type" section)
    for sections in aside.findAll(["section", \
        {"class": "pi-item pi-group pi-border-color"}, \
        "section", {"class": \
            "pi-item pi-group pi-border-color pi-collapse pi-collapse-closed"}])[1:]:
        
        # # # Store all section headers in list
        h2 = sections.findAll("h2", {"class": \
            "pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background"})\
                [0].getText()
        
        # # # Loop over all items within each section
        for attribute in sections.find_all("div", {"class": \
            "pi-item pi-data pi-item-spacing pi-border-color"}):
            
            # # # # initialize values list for attributes with multiple values
            attrs_val2 = []

            # # # # store attribute name/key
            key = ''.join(h2.split(" ")) + "_" + \
                ''.join(attribute.find_all("h3")[0].getText().split(" "))

            # # # # for handling Overall Height in multiple measurement units
            for value in attribute.find_all("li"):
                """if value.find_all("span", {"class": "plainlinks"}):
                    attrs_val2 = [''.join(value.getText().split())]"""
                
                if value.findChildren("span", {"class": "smwtext"}):
                    attrs_val2.append(value.findChildren("span", {"class": \
                        "smwtext"})[0].getText().lower())
                else:
                    attrs_val2.append(value.getText().lower())
                    # attrs_val2 = [''.join(value.getText().split())]
            
            # # # # store attribute value
            value = attribute.find_all("div")[0]
            
            # # # # update keys and values
            attrs_key.append(key)
            attrs_val.append(attrs_val2)

    # zip together attribute keys and values into dictionary
    mw_data = dict(zip(attrs_key, attrs_val))
    
    # Clean measurements and armament numbers
    # # List of measurement words (used later)
    measures = ['Height', 'Weight', 'PowerOutput', \
        'SensorRange', 'Acceleration', 'Speed']
    # # Separate measurements from units, armament numbers from armament
    for dicts in mw_data:
        # # # Separate measurements from untis
        if any(ele in dicts for ele in measures):
            mw_data[dicts] = mw_data[dicts][0].split(" ", 1)
            mw_data[dicts][0] = float(mw_data[dicts][0])
        # # # Separate armaments from armament numbers
        if 'Armament' in dicts:
            arms = []
            nums = []
            for arm in mw_data[dicts]:
                if ' x ' in arm:
                    arms.append(arm.split(" x ", 1)[1])
                    try:
                        nums.append(int(arm.split(" x ", 1)[0]))
                    except:
                        nums.append(arm.split(" x ", 1)[0])
                else:
                    arms.append(arm)
                    nums.append(1)
            mw_data[dicts] = [arms, nums]

    return mw_data

mw_data0 = get_mw_data(mw_list[12])

# print("\n".join(mw_data0))

print(mw_data0)




"""
total_mw_data = {}
for mw in mw_list:
    print("Getting data on", mw.replace("/wiki/", "") + "...", end="")
    mw_data = get_mw_data(mw)
    print("Done")

    total_mw_data[mw] = mw_data"""




# Old/not functional stuff
# Clean and store figures
"""if ' x ' in mw_data[dicts]:
            mw_data[dicts] = mw_data[dicts].split(" x ", 1)
        else:
            mw_data[dicts] = ['1', mw_data[dicts]]"""

# print(mw_data)
"""attributes = aside.find_all("div", {"class": \
    "pi-item pi-data pi-item-spacing pi-border-color"})"""

"""figs_url = []
figs_capt = []
for link in figures.find_all("a"):
    figs_url.append(link.get("href"))
    figs_capt.append(link.get("title"))"""

"""for smwcols in soup_response.find_all(class_="smw-column"):
    for link in smwcols.find_all("a"):
        l = link.get("href")
        if l not in mw_links:
            mw_links.append(l)"""

"""mw_data["figs_url"] = figs_url
mw_data["figs_capt"] = figs_capt"""

"""
# 

    # Clean and store the attribute data
    for attribute in attributes:

        key = attribute.find_all("h3")[0].getText()
        value = attribute.find_all("div")[0]

        if key == "Birthday":
            values = [v.getText() for v in value.find_all("a", recursive=False)]
        elif key == "Initial phrase":
            values = value.find(text=True, recursive=False).strip()
        elif key == "Initial clothes":
            values = [element.strip() for element in value.getText().split(")")]
            for index in range(len(values)):
                if "(" in values[index]:
                    values[index] = values[index] + ")"
            values = [element for element in values if element]
        else:
            values = value.getText()
            if "," in values:
                values = [v.strip() for v in values.split(",")]

        mw_data[key.lower()] = values
        """