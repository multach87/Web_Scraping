from requests import get
from bs4 import BeautifulSoup
import sys

from scraping_scripts.get_mw_list import get_list
wiki_url = "https://gundam.fandom.com"

def get_data(mw_name: str):
    """
    Scrape all the data for a given mw from the Gundam Fandom wiki.
    :param mw_name: the url-ized version of the mw name, \
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
    response = get(wiki_url + mw_name)
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
        "pi-item pi-item-spacing pi-title pi-secondary-background"})[1:]
    types = aside.find_all("td")

    # Clean and store name
    cleaned_names = [name.getText() for name in names]
    # # Add "name" to keys list
    attrs_key.append("names")
    # # Initialize value list for names
    attrs_valname = []
    # # Check for MultipleNames/OneName/NoBox
    try:    
        # Store English and Japanese names if parentheses split
        if len(cleaned_names[0].split(" (")) > 1:
            attrs_valname.append(cleaned_names[0].split(" (")[0])
            attrs_valname.append(cleaned_names[0].split(" (")[1].split(")")[0])
        # Otherwise just store English
        else:
            attrs_valname.append(cleaned_names[0])
    except:
        # Store None to full MW entry if no attribute box and Exit
        return None
        sys.exit(1)
    # # Add list of names to values list
    attrs_val.append(attrs_valname)
    
    # Clean and store type
    cleaned_type = [type.getText() for type in types]
    # # Strip end spaces and tabs
    cleaned_type[0] = cleaned_type[0].strip().strip("\t")
    # # Add "type" to keys list
    attrs_key.append("type")
    # # Initialize value list for type
    attrs_valtype = []
    # # Check for type characteristics to handle: 
    # # # 1 type, ships, or all others
    if len(cleaned_type[0].split(" ")) == 1:
        attrs_valtype.append(cleaned_type[0])
    elif "ship" in cleaned_type[0]:
        attrs_valtype = [cleaned_type[0].split(" ")[-1].lower(), \
            ' '.join(cleaned_type[0].split(" ")[:-1]).lower()]
    else:
        attrs_valtype = [' '.join(cleaned_type[0].split(" ")[-2:]).lower(), \
            ' '.join(cleaned_type[0].split(" ")[:-2]).lower()]
    # # Add list of type values to values list
    attrs_val.append(attrs_valtype)

    # Clean and store image urls, image captions
    if aside.find_all("a", {"class": \
        "image image-thumbnail"}):
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
    # # Loop over all mw attribute sections except first
    # # # (which is covered in the "type" section)
    for sections in aside.findAll(["section", \
        {"class": "pi-item pi-group pi-border-color"}, \
        "section", {"class": \
            "pi-item pi-group pi-border-color pi-collapse pi-collapse-closed"}])[1:]:
        
        # Store all section headers in list
        h2 = sections.findAll("h2", {"class": \
            "pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background"})\
                [0].getText()
        
        # Loop over all items within each section
        for attribute in sections.find_all("div", {"class": \
            "pi-item pi-data pi-item-spacing pi-border-color"}):
            
            # # initialize values list for attributes with multiple values
            attrs_val2 = []

            # # store attribute name/key if contains h3's
            if(attribute.find_all("h3")):
                key = ''.join(h2.split(" ")) + "_" + \
                    ''.join(attribute.find_all("h3")[0].getText().split(" "))
            # # Otherwise it's the Mobile Weapons section for ships/carriers
            else:
                key = "MobileWeapons"

            # # handles some problem cases: multi-measures, '\u200e'
            for value in attribute.find_all("li"):
                # This span/class corresponds with features with multiple
                # # measurements (i.e., in both imperial and metric)
                if value.findChildren("span", {"class": "smwtext"}):
                    attrs_val2.append(value.findChildren("span", {"class": \
                        "smwtext"})[0].getText().lower())
                else:
                    # Handles plainlinks cases, w/ and w/o '\u200e'
                    if value.find_all("span", {"class": "plainlinks"}):
                        val2_temp = value.getText()
                        if len(val2_temp.split('\u200e ')) == 2:
                            attrs_val2.append(' '.\
                                join(val2_temp.split('\u200e')[:-1]).lower())
                        else:
                            attrs_val2.append(' '.join(value.getText().\
                                rsplit(' ', 1)[:-1]).lower())
                    # Otherwise just append the text
                    else:
                        attrs_val2.append(value.getText().lower())
            
            # # update keys and values
            attrs_key.append(key)
            attrs_val.append(attrs_val2)

    # zip together attribute keys and values into dictionary
    mw_data = dict(zip(attrs_key, attrs_val))
    
    # Clean measurements and armament numbers
    # # List of measurement words
    measures = ['RocketThrusters', 'MassRation', 'Height', 'Weight', 'Output', \
        'Length', 'Width', 'Range', 'Acceleration', 'Speed']
    # # Separate measurements from units, armament numbers from armament
    for dicts in mw_data:
        # Separate measurements from untis
        if any(ele in dicts for ele in measures):
            # # initialize numbers and units lists
            nums = []
            mes = []
            # # Separate numbers and units, handle weird "numbers"
            for eles in mw_data[dicts]:
                try:
                    nums.append(float(eles.split(" ", 1)[0]))
                    mes.append(eles.split(" ", 1)[1])
                except:
                    nums.append(eles.split(" ", 1)[0])
                    mes.append(eles.split(" ", 1)[1])
            # # Updates corresponding values in dictionary
            mw_data[dicts] = [nums, mes]
        # Separate armaments from armament numbers
        if 'Armament' in dicts:
            arms = []
            nums = []
            # # Separate equipment and numbers
            for arm in mw_data[dicts]:
                # # Handle multiples or weird "numbers" (e.g., '? x ')
                if ' x ' in arm:
                    arms.append(arm.split(" x ", 1)[1])
                    try:
                        nums.append(int(arm.split(" x ", 1)[0]))
                    except:
                        nums.append(arm.split(" x ", 1)[0])
                # # Singles (i.e. no '# x ')
                else:
                    arms.append(arm)
                    nums.append(1)
            # # Updates corresponding values in dictionary
            mw_data[dicts] = [arms, nums]

    # Save full dictionary
    return mw_data

# For testing
if __name__ == "__main__":
    #from get_mw_list import get_list
    
    # mw_data0 = get_data("/wiki/ACA-01_Gaw")
    # mw_data0 = get_data("/wiki/OZ_Shuttle")
    # mw_data0 = get_data("/wiki/ORX-009_Gundam_%EF%BC%BBSk%C3%B6ll%EF%BC%BD")
    #mw_data0 = get_data("/wiki/AMA-01X_Jamru_Fin")
    # mw_data0 = get_data("/wiki/AMS-119_Jagd_Geara_Doga")
    #mw_data0 = get_data("/wiki/Amalthea-class")
    #mw_data0 = get_data("/wiki/OZ-00MS_Tallgeese")
    #mw_data0 = get_data("/wiki/ACA-01_Gaw")
    #mw_data0 = get_data("/wiki/LMSD-76_Gray_Phantom")
    mw_data0 = get_data("/wiki/Ra_Cailum")
    print(mw_data0)