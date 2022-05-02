import json
from os import mkdir

# from get_mw_list import get_mw_list
# from get_mw_data import get_mw_data

# Get our villages

print("Getting the list of villagers to scrape...", end="")
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
    mkdir("mw-data")
    print("\nCreated directory (mw-data) for mw data")

    mkdir("mw-data/images")
    print("Created directory (mw-data/images) for mw images\n")
except FileExistsError:
    print("\nDirectory already exists for mw data.\n" +
          "Delete it and try again, if you want to re-download the images.\n")

# Get the data for each mw
total_mw_data = {}
for mw in mw_list:

    mw_local_name = mw.replace("/wiki/",  "")

    print("Getting data on", mw_local_name + "...", end="")
    mw_data = get_mw_data(mw_local_name)
    print("Done")

    total_mw_data[mw_local_name] = mw_data

print("\nSaving villager JSON data...")
with open("villager-data/villager-data.json", "w") as mw_data_file:
    json.dump(total_mw_data, mw_data_file, indent=4)
print("Done")