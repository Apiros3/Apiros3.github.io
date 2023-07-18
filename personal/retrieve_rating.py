#link: "https://clist.by:443/api/v3/statistics/?username=Apiros3&api_key={APIKEY}&coder_id=25319&order_by=-date"

from urllib.request import urlopen
import json

#!!!!! LOCAL ONLY !!!!!
url = "https://clist.by:443/api/v3/statistics/?username=Apiros3&api_key=9ff90d500d596b7a40a62c515ec8e6dcacaf04c3&coder_id=25319&order_by=-date"

response = urlopen(url)
data_json = json.loads(response.read())

for data in data_json["objects"]:
    if (data["new_rating"] == None):
        continue
    ev = data["event"].replace("（", " ").replace("）", " ").replace("(", " ").replace(")", " ").split(" ")
    ev = list(filter(None, ev)) #remove any unnecessary spacing in between words
    for i in range(len(ev)):
        if (ev[i] == "AtCoder"):
            ev = ev[i:i+4]
            break 
        if (ev[i] == "Codeforces"):
            ev = ev[i:i+3]
            break 
    print(ev[0])
    print(' '.join(ev))
    #codeforces contests without a # implies div1&2
    print(f'{data["new_rating"]} {data["rating_change"]} {data["date"]}')
    #info to have: date, place, rating change, new rating, contest site (AtCoder/Codeforces)


#use the given data above to also find, current rating for both AtCoder and Codeforces (simply the first instance)


f = open('out.txt', 'w')


f.writelines(str(data_json))

