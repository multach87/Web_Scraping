# test = ["Oakland Newtype Lab\u200e "]
test = ["Newtype Lab ", "Oakland Newtype Lab\u200e "]
print(test)

new = []

for i in test:
    if len(i.split('\u200e ')) == 2:
        new.append(' '.join(i.split('\u200e')[:-1]).lower())
    else:
        new.append(' '.join(i.split(' ')[:-1]).lower())

print(new)
