import json
from sys import argv

with open(argv[1]) as fp:
    dic1 = json.load(fp)
with open(argv[2]) as fp:
    dic2 = json.load(fp)

for key in dic2:
    if dic1.get(key):
        dic1[key] += dic2[key]
    else:
        dic1[key] = dic2[key]


with open(argv[3], "w") as fp:
    json.dump(dic1, fp)

