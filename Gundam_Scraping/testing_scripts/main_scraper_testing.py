import json
from os import mkdir

from get_ms_list_testing import get_mw_list
from get_ms_data_testing import get_mw_data

mw_list = get_mw_list()

wiki_url = "https://gundam.fandom.com"

print("Getting the list of mw's to scrape...", end="")
mw_list = get_mw_list()

# Couldn't locate the table
if len(mw_list) == 0:
    print("\nUh-oh, couldn't locate the table.\n\n" +
          "Maybe the wiki has changed, and broken this scraper.\n" +
          "In any case, please make an issue and I'll try to fix it!")
    exit(0)

print("Done")

# Create directory to store images
try:
    mkdir("Data/testing/mw_data")
    print("\nCreated directory (mw_data) for mw data")

    mkdir("Data/testing/images")
    print("Created directory (Data/images) for mw images\n")
except FileExistsError:
    print("\nDirectory already exists for mw data.\n" +
          "Delete it and try again, if you want to re-download the images.\n")

# Get the data for each mw
total_mw_data = {}
for mw in mw_list:

    # mw_local_name = mw.replace("/wiki/",  "")

    print("Getting data on", mw + "...", end="")
    mw_data = get_mw_data(mw)
    print("Done")

    total_mw_data[mw] = mw_data

print("\nSaving villager JSON data...")
with open("Data/testing/mw_data/mw_data.json", "w") as mw_data_file:
    json.dump(total_mw_data, mw_data_file, indent=4)
print("Done")