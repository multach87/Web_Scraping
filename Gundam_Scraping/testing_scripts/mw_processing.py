import json
import pandas as pd
import numpy as np

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

def one_hot(key_name: str):
    data_temp = pd.DataFrame.from_dict(data_1mw[key_name])
    key_temp = key_name.split("_" , 1)[1]
    data_temp = data_temp[0].str.get_dummies().add_prefix((key_temp + "_"))
    data_temp.columns = data_temp.columns.str.replace('-', '').str.replace(' ', '').\
        str.replace('[', '_').str.replace(']', '').str.replace(':', '').\
            str.replace('\'', '').str.replace('~', '').str.replace('.', '')
    data_temp = data_temp.drop(data_temp.index[1:])
    data_temp[0:] = 1
    return(data_temp)

if __name__ == "__main__":
    jfile = open('Data/mw_data/mw_data.json')

    data = json.load(jfile)
    data_1mw = data["RX-78-2_Gundam"]
    #data_1mw = data["Super_Xamel"]
    #data_1mw = data["Pyrennes-class"]
    
    # Step 1: extact main info (full name, designation, model_series, type, and one-hots)
    data_ready = get_main("RX-78-2_Gundam")
    #print(data_ready) 

    # store names of keys not to one-hot encode
    ohn_main = ['name', 'type', 'imgs']
    ohn_eps = ['_Television', '_OVA']
    ohn_measures = ['MassRatio', 'Height', 'Weight', \
        'Output', 'Length', 'Width', 'Range', 'Acceleration', 'Speed']
    ohn_equiparms = ['Equipment', 'Armaments']
    ohn_exclude = ['TurningTime', 'RocketThrusters']
    """[print(key) for key in list(data_1mw.keys()) \
        if any(ele in key for ele in ohn_main + ohn_eps + ohn_measures + ohn_equiparms)]"""
    
    # 2-level checker for equipment and armament: TOBE incorporated into counts
    """if ''.join(eq_std[0]) == eq_std[0]:
        #print('1 level!')
    else:
        #print("2 levels!")"""
    
    # One-Hot encoding: non-name or equipment features DONE
    spec_key = []
    [spec_key.append(key) for key in list(data_1mw.keys()) \
        if any(ele in key for ele in \
            ohn_main + ohn_eps + ohn_measures + ohn_equiparms + ohn_exclude)]
    onehot_main = np.setdiff1d(list(data_1mw.keys()), spec_key)
    for key in onehot_main:
        data_ready = pd.concat([data_ready, one_hot(str(key))], axis = 1)
    """data_ready = [pd.concat([data_ready, one_hot(str(key))], axis = 1) \
        for key in onehot_main]"""
    #print(data_ready)
    #print(data_ready.columns)

    # for one-hot'ing shows/OVAs specifically (since "first/last seen" is included \
    # but useless for our purposes)
    # # LOOPED - Could refactoring onehot'ing into function later
    shows = []
    [shows.append(i.split(":")[0].replace('-', '').replace(' ', '').\
        replace('[', '_').replace(']', '').replace('\'', '').replace('~', '').replace('.', '')) \
            for i in data_1mw["RealWorld_Television"]]
    [shows.append(i.split(":")[0].replace('-', '').replace(' ', '').\
        replace('[', '_').replace(']', '').replace('\'', '').replace('~', '').replace('.', '')) \
            if "episode" in i \
                else shows.append(i.replace(':', '').replace('-', '').\
                    replace(' ', '').replace('[', '_').replace(']', '').replace('\'', '').replace('~', '').replace('.', ''))
            for i in data_1mw["RealWorld_OVA"]]
    shows = pd.DataFrame(shows, columns = ['showsOVAs'])
    shows = shows["showsOVAs"].str.get_dummies().add_prefix((shows.columns[0] + "_"))
    shows[0:] = 1
    shows = shows.drop(shows.index[1:])
    #print(data_ready)
    data_ready = pd.concat([data_ready, shows], axis = 1)
    #print(shows)
    #print(shows.columns)
    print(data_ready.columns)
    print(data_ready)

