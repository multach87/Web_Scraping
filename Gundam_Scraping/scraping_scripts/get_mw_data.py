from pickle import FALSE
from requests import get
from bs4 import BeautifulSoup
import sys

try:
    from scraping_scripts.get_mw_list import get_list
except:
    from get_mw_list import get_list
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
    names = aside.findAll("h2", {"class": \
        "pi-item pi-item-spacing pi-title pi-secondary-background"})[1:]
    types = aside.findAll("td")

    # Clean and store name
    cleaned_names = [name.getText() for name in names]
    # # Add "name" to keys list
    attrs_key.append("name_en")
    attrs_key.append("name_jp")
    # # Initialize value list for names
    #attrs_valname = []
    # # Check for MultipleNames/OneName/NoBox
    try:    
        # Store English and Japanese names if parentheses split
        if len(cleaned_names[0].split(" (")) > 1:
            attrs_val.append(cleaned_names[0].split(" (")[0].strip("\uff3d"))
            attrs_val.append(cleaned_names[0].split(" (")[1].split(")")[0].strip("\uff3d"))
        # Otherwise just store English
        else:
            attrs_val.append(cleaned_names[0].strip("\uff3d"))
            attrs_val.append(None)
    except:
        # Store None to full MW entry if no attribute box and Exit
        return None
        sys.exit(1)
    # # Add list of names to values list
    #attrs_val.append(attrs_valname)
    
    # Clean and store type
    cleaned_type = [type.getText() for type in types]
    # # Strip end spaces and tabs
    cleaned_type[0] = cleaned_type[0].strip().strip("\t")
    # # Add "type" to keys list
    attrs_key.append("type_main")
    attrs_key.append("type_details")
    # # Initialize value list for type
    #attrs_valtype = []
    # # Check for type characteristics to handle: 
    # # # 1 type, ships, or all others
    if len(cleaned_type[0].split(" ")) == 1:
        attrs_val.append(cleaned_type[0])
    elif "ship" in cleaned_type[0]:
        attrs_val.append(cleaned_type[0].split(" ")[-1].lower())
        attrs_val.append(' '.join(cleaned_type[0].split(" ")[:-1]).lower())
    else:
        attrs_val.append(' '.join(cleaned_type[0].split(" ")[-2:]).lower())
        attrs_val.append(' '.join(cleaned_type[0].split(" ")[:-2]).lower())
    # # Add list of type values to values list
    #attrs_val.append(attrs_val)

    # Clean and store image urls, image captions
    if aside.findAll("a", {"class": \
        "image image-thumbnail"}):
        # # Add "imgs" to keys list
        attrs_key.append("imgs")
        # # Initialize lists of captions and urls
        img_urls = []
        img_capts = []
        # # Append each link, caption to list
        [img_urls.append(link.get("href")) for link in aside.findAll("a", {"class": \
            "image image-thumbnail"})]
        [img_capts.append(link.get("title")) for link in aside.findAll("a", {"class": \
            "image image-thumbnail"})]
        # # Add list of image urls and list of cpations to values list
        attrs_val.append([img_urls, img_capts])

    for sect in aside.findAll("section")[1:]:
        h2_temp = sect.find("h2", \
            {"class": "pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background"})\
                .getText()
        [attrs_key.append(''.join((h2_temp + "_" + h3_temp.getText()).split(" "))) \
            for h3_temp in sect.findAll("h3")]

    for div in aside.findAll("div", {"class": "pi-data-value pi-font"}):
        lis = []
        [lis.append(li.getText().lower()) for li in div.findAll("li")]
        attrs_val.append(lis)

    mw_data = dict(zip(attrs_key, attrs_val))

    measures = ['MassRatio', 'Height', 'Weight', 'Output', \
        'Length', 'Width', 'Range', 'Acceleration', 'Speed', 'TurningTime']

    for key in list(mw_data.keys())[4:]:
        #if any(ele in key for ele in measures):
        mw_data[key] = [i.split(' <br />', 1)[0] \
            if ' <br />' in i \
                else i \
                    for i in mw_data[key]]
        mw_data[key] = [i.split(u'\xa0', 1)[0].rstrip(",1234567890.") \
            if u'\xa0' in i \
                else i \
                    for i in mw_data[key]]
        mw_data[key] = [i.split(' \u00d7 ', 1) \
            if ' \u00d7 ' in i \
                else i \
                    for i in mw_data[key]]
        mw_data[key] = [i.split(' x ', 1) \
            if ' x ' in i \
                else i \
                    for i in mw_data[key]]
        mw_data[key] = [i.split('\u200e ', 1)[0] \
            if '\u200e ' in i \
                else i \
                    for i in mw_data[key]]
        if any(ele in key for ele in measures):
            mw_data[key] = [i.split(' ', 1) for i in mw_data[key]]
        """if 'StandardArmaments' in key:
            mw_data[key]"""

    ### TESTING STARTS HERE

    """for key in list(mw_data.keys())[4:]:
        if any(ele in key for ele in measures):
            mw_data[]"""

    """# Clean and store the attribute data
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
        for attribute in sections.findAll("div", {"class": \
            "pi-item pi-data pi-item-spacing pi-border-color"}):
            
            # # initialize values list for attributes with multiple values
            attrs_val2 = []

            # # store attribute name/key if contains h3's
            if(attribute.findAll("h3")):
                attrs_key.append((''.join(h2.split(" ")) + "_" + \
                    ''.join(attribute.findAll("h3")[0].getText().split(" "))))
            # # Otherwise it's the Mobile Weapons section for ships/carriers
            else:
                attrs_key.append("MobileWeapons")
            #print(attrs_key)

            # # handles some problem cases: multi-measures, '\u200e'
            for value in attribute.findAll("li"):
                # This span/class corresponds with features with multiple
                # # measurements (i.e., in both imperial and metric)
                if value.findChildren("span", {"class": "smwtext"}):
                    attrs_val2.append(value.findChildren("span", {"class": \
                        "smwtext"})[0].getText().lower())
                else:
                    # Handles plainlinks cases, w/ and w/o '\u200e'
                    if value.findAll("span", {"class": "plainlinks"}):
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
                #print(attrs_val2)

                
            
            # # update keys and values
            #attrs_key.append(key)
            attrs_val.append(attrs_val2)


    # zip together attribute keys and values into dictionary
    mw_data = dict(zip(attrs_key, attrs_val))"""
    #mw_data = dict(zip(attrs_key, (x for x in attrs_val)))
    #mw_data = [attrs_key, attrs_val]
    #mw_data = dict(zip(mw_data["attrs_key"], mw_data["attrs_val"]))
    
    """# Clean measurements and armament numbers
    # # List of measurement words
    measures = ['RocketThrusters', 'MassRation', 'Height', 'Weight', 'Output', \
        'Length', 'Width', 'Range', 'Acceleration', 'Speed', 'TurningTime']
    # # Separate measurements from units, armament numbers from armament
    for dicts in mw_data:
        #print(dicts)
        #attrs_keynew = []
        #attrs_valnew = []
        #dict_equip = {}
        # Separate measurements from untis
        if any(ele in dicts for ele in measures):
            #keytop = dicts
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
                #print(keytop)
                #print(mes)
                #newkey = [keytop, mes[0]]
                #attrs_keynew.append('_'.join(newkey))
                #attrs_valnew.append(nums)
                #print(newkey)
                #print(nums)
                #attrs_key.append('_'.join(newkey))
                #attrs_val.append(nums)
                #print(attrs_key)
            # # Updates corresponding values in dictionary
            mw_data[dicts] = [nums, mes]
            #dict_equip.update(dict(zip(attrs_keynew, attrs_valnew)))
            #print(dict_equip)
            #mw_data.update(dict_equip)
            #print(dict_equip)
            #print(mw_data[dicts])
        # Separate armaments from armament numbers
        if 'Armament' in dicts:
            arms = []
            nums = []
            # # Separate equipment and numbers
            for arm in mw_data[dicts]:
                # # Handle multiples or weird "numbers" (e.g., '? x ')
                if ' \u00d7 ' in arm:
                    arm = ' x '.join(arm.split(" \u00d7 "))

                if ' x ' in arm:
                    if (len(arm.split(" x ", 1)[1].split(" (")) > 1) and \
                        (" x " in arm.split(" x ", 1)[1].split(" (")[1]):
                        arms.append(arm.split(" x ", 1)[1].split(" (")[1].\
                            strip(")").split(" x ", 1)[1])
                        arms.append(arm.split(" x ", 1)[1].split(" (", 1)[0])
                        try:
                            nums.append(int(arm.split(" x ", 1)[1].split(" (")[1].\
                                strip(")").split(" x ", 1)[0]))
                        except:
                            nums.append(arm.split(" x ", 1)[1].split(" (")[1].\
                                strip(")").split(" x ", 1)[0])
                    else:
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
            mw_data[dicts] = [arms, nums]"""
    #print(dict_equip)
    #mw_data.update(dict_equip)

    # Save full dictionary
    return mw_data
    #print(attrs_key)

# For testing
if __name__ == "__main__":
    #from get_mw_list import get_list
    
    #mw_data0 = get_data("/wiki/ACA-01_Gaw")
    #mw_data0 = get_data("/wiki/OZ_Shuttle")
    mw_data0 = get_data("/wiki/ORX-009_Gundam_%EF%BC%BBSk%C3%B6ll%EF%BC%BD")
    #mw_data0 = get_data("/wiki/AMA-01X_Jamru_Fin")
    #mw_data0 = get_data("/wiki/AMS-119_Jagd_Geara_Doga")
    #mw_data0 = get_data("/wiki/Amalthea-class")
    #mw_data0 = get_data("/wiki/OZ-00MS_Tallgeese")
    #mw_data0 = get_data("/wiki/ACA-01_Gaw")
    #mw_data0 = get_data("/wiki/LMSD-76_Gray_Phantom")
    #mw_data0 = get_data("/wiki/Ra_Cailum")
    #mw_data0 = get_data("/wiki/RX-78-2_Gundam")
    #mw_data0 = get_data("/wiki/A/FMSZ-007II_Zeta")
    print(mw_data0)


# 
    """print(nums)
                    print(mes)
                    for i in range(len(nums)):
                        newkey = [keytop, mes[i]]
                        attrs_key.append('_'.join(newkey))
                        attrs_val.append(nums[i])"""
"""print(attrs_keynew)
                print(attrs_valnew)"""