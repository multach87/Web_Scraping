import json
import pandas as pd

# vars
"""data["RX-78-2_Gundam"]["names"][0]
data["RX-78-2_Gundam"]["type"][0]"""

if __name__ == "__main__":
    jfile = open('Data/mw_data/mw_data.json')

    data = json.load(jfile)

    new = pd.DataFrame.from_dict(data["RX-78-2_Gundam"]["names"])
    new = new.drop(new.index[1:])
    new[1] = [1]
    new.columns = ['name', new[0][0].split(" ")[0].split("-")[0].lower()]
    #print(new)
    #print(new[0][0].split(" ")[0].split("-")[0])

    #print(new)


    """for key in data["RX-78-2_Gundam"].keys():
        print(data["RX-78-2_Gundam"][key])"""
    
    #weaps = data["RX-78-2_Gundam"]["StandardArmaments_Handheld"]
    #print(weaps)
    
    
    newnew = pd.DataFrame.from_dict(data["RX-78-2_Gundam"]["Profile_KnownPilots"])
    #newnew.columns = [""]
    #print(newnew)
    newnew = newnew[0].str.get_dummies().add_prefix('Pilots_')
    newnew.columns = newnew.columns.str.replace(' ', '')
    newnew = newnew.drop(newnew.index[1:])
    newnew[0:] = 1
    #print(newnew)
    new = new.join(newnew)
    #print(new)
    #new[0].join(new[0]str.join('|').str.get_dummies().add_prefix('tags_'))