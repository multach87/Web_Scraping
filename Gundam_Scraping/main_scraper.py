import json
from os import mkdir
import traceback
import timeit

from scraping_scripts.get_mw_list import get_list
from scraping_scripts.get_mw_data import get_data

if __name__ == "__main__":

    # start timer
    start = timeit.default_timer()

    # get list of mw's
    print("Getting the list of mw's to scrape...", end="")
    mw_list = get_list()

    # Couldn't locate the table
    if len(mw_list) == 0:
        print("\nUh-oh, couldn't locate the table.\n\n" +
            "Maybe the wiki has changed, and broken this scraper.\n" +
            "In any case, please make an issue and I'll try to fix it!")
        exit(0)

    print("Done")

    # Create directories for data storage
    try:
        mkdir("Data/mw_data")
        print("\nCreated directory (mw_data) for mw data")

        mkdir("Data/images")
        print("Created directory (Data/images) for mw images\n")
    except FileExistsError:
        print("\nDirectory already exists for mw data.\n" +
            "Delete it and try again, if you want to re-download the images.\n")

    # Get the data for each mw
    total_mw_data = {}
    total_mw_errors = {}
    for mw in mw_list:

        print("Getting data on", mw + "...", end="")
        try:
            mw_data = get_data(mw)
            total_mw_data[mw] = mw_data
        except:
            mw_data = [traceback.format_exc()]
            total_mw_errors[mw] = mw_data
        print("Done")

    print("\nSaving mw JSON data...")
    with open("Data/mw_data/mw_data.json", "w") as mw_data_file:
        json.dump(total_mw_data, mw_data_file, indent=4)
    with open("Data/mw_data/mw_errors.json", "w") as total_mw_errors_file:
        json.dump(total_mw_errors, total_mw_errors_file, indent=4)
    print("Done")

    stop = timeit.default_timer()
    print ('Time: ', stop - start)