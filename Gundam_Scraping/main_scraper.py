import json
from os import mkdir

from get_ms_list import get_ms_list
from get_ms_data import get_ms_data

# Get our villages

print("Getting the list of villagers to scrape...", end="")
ms_list = get_ms_list()

# Couldn't locate the table
if len(ms_list) == 0:
    print("\nUh-oh, couldn't locate the table.\n\n" +
          "Maybe the wiki has changed, and broken this scraper.\n" +
          "In any case, please make an issue and I'll try to fix it!")
    exit(0)

print("Done")

# Create directory to store images
try:
    mkdir("villager-data")
    print("\nCreated directory (villager-data) for villager data")

    mkdir("villager-data/images")
    print("Created directory (villager-data/images) for villager images\n")
except FileExistsError:
    print("\nDirectory already exists for villager data.\n" +
          "Delete it and try again, if you want to re-download the images.\n")

# Get the data for each villager
total_ms_data = {}
for villager in ms_list:

    ms_local_name = villager.replace("/wiki/",  "")

    print("Getting data on", ms_local_name + "...", end="")
    ms_data = get_ms_data(ms_local_name)
    print("Done")

    total_ms_data[ms_local_name] = ms_data

print("\nSaving villager JSON data...")
with open("villager-data/villager-data.json", "w") as ms_data_file:
    json.dump(total_ms_data, ms_data_file, indent=4)
print("Done")