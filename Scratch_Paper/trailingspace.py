dict = {'good': "Vulture1", 'bad': "Vulture2 "}
# print(dict)

for dicts in dict:
    if ' ' in [char for char in dict[dicts]][-1]:
        dict[dicts] = ''.join([char for char in dict[dicts]][:-1])

print(dict)