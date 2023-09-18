#link: "https://clist.by:443/api/v3/statistics/?username=Apiros3&api_key={APIKEY}&coder_id=25319&order_by=-date"

from urllib.request import urlopen
import json
import requests
from bs4 import BeautifulSoup as bs
import datetime

print("retrieve_rating.py starting...")

#!!!!! LOCAL ONLY !!!!!
url = "https://clist.by:443/api/v3/statistics/?username=Apiros3&api_key=9ff90d500d596b7a40a62c515ec8e6dcacaf04c3&coder_id=25319&order_by=-date"

response = urlopen(url)
data_json = json.loads(response.read())

f = open('rating_list.txt', 'w')

atcur = -1
cfcur = -1

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
    if (ev[0] == "AtCoder" and atcur == -1):
        atcur = data["new_rating"]
    if (ev[0] == "Codeforces" and cfcur == -1):
        cfcur = data["new_rating"]
    f.writelines(f'{ev[0]}\n')
    f.writelines(' '.join(ev) + '\n')
    #codeforces contests without a # implies div1&2
    f.writelines(f'{data["new_rating"]} {data["rating_change"]} {data["date"]}\n')
    #info to have: date, place, rating change, new rating, contest site (AtCoder/Codeforces)

f.close()

url = "https://onlinemathcontest.com/users/apiros3"
res = requests.get(url)
lis = bs(res.content, features="html.parser").find_all('p', {'id' : 'rating'})
omccur = lis[0].text.split()[-1]

f = open('current_rating.txt', 'w')
f.writelines(f'{atcur}\n{cfcur}\n{omccur}')
f.close()

f = open('display_rating.js', 'w')
today = datetime.datetime.now()
f.writelines(
f"""
function update_rating_once() {{ 
    document.getElementById("rating_atcoder").innerHTML = {atcur}
    document.getElementById("rating_codeforces").innerHTML = {cfcur}
    document.getElementById("rating_omc").innerHTML = {omccur}
    
    document.getElementById("rating_last_update").innerHTML = "{today.isoformat(timespec='seconds')}"
}} 
"""
)

#use the given data above to also find, current rating for both AtCoder and Codeforces (simply the first instance)
print("done!!")





