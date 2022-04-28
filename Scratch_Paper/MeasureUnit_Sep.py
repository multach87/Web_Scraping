keys = ["Developedfrom", "OverallHeight", "EmptyWeight"]
vals = ["EB-06", "13.8 meters", "25.2 metric tons"]

dict = dict(zip(keys, vals))

measures = ['Height', 'Weight', 'Power Output', 'Sensor Range', 'Acceleration', 'Speed']

for dicts in dict:
    if any(ele in dicts for ele in measures):
        print(dict[dicts].split(" ", 1))

# print(vals[2].split(" ", 1))


"""attributes = [{'Developed From': 'EB-06 Graze'}, {'Overall Height': '13.8 meters'}, {'Empty Weight': '25.2 metric tons'}]
print(attributes)

"""