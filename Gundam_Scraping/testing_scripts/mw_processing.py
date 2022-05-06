import json
import pandas as pd

def get_main(mw_name: str):
    data_temp = data[mw_name]
    # Processing name/model - DONE
    new = pd.DataFrame([data_temp["name_en"]])
    new.columns = ["name"]
    if len(new["name"][0].split("-")) > 1 and len(new["name"][0].split(" ")) > 1:
        new["designation"] = [new["name"][0]]
        new["model_series"] = [new["name"][0].split(" ")[0].split("-")[0].lower()]
        new[str(new["model_series"][0].split(" ")[0])] = [1]
        new.columns = ["name", "designation", "model_series", \
            new["model_series"][0].split(" ")[0]]
    elif len(new["name"][0].split("-")) > 1 and len(new["name"][0].split(" ")) == 1:
        new["name"] = [new["name"][0]]
        new["model_series"] = [new["name"][0].split("-")[0].lower()]
        new[str(new["model_series"][0].split(" ")[0])] = [1]
        new.columns = ["name", "designation", "model_series", \
            new["model_series"][0].split(" ")[0]]
    else:
        new["name"] = ''.join(new["name"][0].split(" ")).lower()
        new["model_series"] = None
        new.columns = ["name", "designation", "model_series"]
    new["type"] = data_temp["type_main"]
    new[str(''.join(new["type"][0].split(" ")))] = 1
    return(new)

# vars
"""data["RX-78-2_Gundam"]["names"][0]
data["RX-78-2_Gundam"]["type"][0]"""

if __name__ == "__main__":
    jfile = open('Data/mw_data/mw_data.json')

    data = json.load(jfile)
    data_1mw = data["RX-78-2_Gundam"]
    #data_1mw = data["Super_Xamel"]
    #data_1mw = data["Pyrennes-class"]
    
    # Step 1: extact main info (full name, designation, model_series, type, and one-hots)
    """datatest = get_main("RX-78-2_Gundam")
    print(datatest)""" 

    # One-hot encoding stuff: TOBE looped
    """newnew = pd.DataFrame.from_dict(data["Profile_KnownPilots"])
    #newnew.columns = [""]
    #print(newnew)
    #print(newnew[0])
    newnew = newnew[0].str.get_dummies().add_prefix('Pilots_')
    newnew.columns = newnew.columns.str.replace(' ', '').str.replace("[", '_').str.replace(']', '')
    newnew = newnew.drop(newnew.index[1:])
    newnew[0:] = 1
    print(newnew)"""

    # store names of keys not to one-hot encode
    ohn_main = ['name', 'type', 'imgs']
    ohn_eps = ['_Television', '_OVA']
    ohn_measures = ['MassRatio', 'Height', 'Weight', \
        'Output', 'Length', 'Width', 'Range', 'Acceleration', 'Speed', 'TurningTime']
    ohn_equiparms = ["Equipment", "Armaments"]
    #print(ohn_main)
    #print(ohn_measures)
    #print(ohn_equiparms)
    [print(key) for key in list(data_1mw.keys()) \
        if any(ele in key for ele in ohn_main + ohn_eps + ohn_measures + ohn_equiparms)]
    """for key in list(data_1mw.keys()):
        if any(ele in key for ele in ohn_main + ohn_measures + ohn_equiparms):
            print(key)"""

    # for one-hot'ing shows specifically (since "first/last seen" is included \
    # but useless for our purposes)
    """shows = []
    [shows.append(i.split(":")[0]) for i in data_1mw["RealWorld_Television"]]
    print(shows)"""

    # joining
    #new = new.join(newnew)
    #print(new)
    #new[0].join(new[0]str.join('|').str.get_dummies().add_prefix('tags_'))

    # 2-level checker for equipment and armament: TOBE incorporated into counts
    """if ''.join(eq_std[0]) == eq_std[0]:
        #print('1 level!')
    else:
        #print("2 levels!")"""