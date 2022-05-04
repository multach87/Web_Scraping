test = ["2 \u00d7 Beam Saber (2 \u00d7 Beam Javelin)", "2 \u00d7 Beam Saber (Beam Javelin)", "1-2 \u00d7 BLASH", "2 \u00d7 60mm vulcan gun"]

print(" x " in ' x '.join(test[1].split(" \u00d7 ")).split(" (")[1].strip(")"))

#print(' x '.join(test[0].split(" \u00d7 ")[1:]))

for i in range(len(test)):
    if len(' x '.join(test[i].split(" \u00d7 ")).split(" (")) > 1:
        test.append(' x '.join(test[i].split(" \u00d7 ")).split(" (")[1].strip(")"))
    test[i] = ' x '.join(test[i].split(" \u00d7 ")).split(" (")[0]
    

print(test)


"""for i in test:
    print(i.split(" \u00d7 "))
    print(len(i.split(" \u00d7 ")))"""