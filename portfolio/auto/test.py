import requests
from bs4 import BeautifulSoup as bs

url = "https://onlinemathcontest.com/users/apiros3"
res = requests.get(url)
lis = bs(res.content, features="html.parser").find_all('p', {'id' : 'rating'})
ret = lis[0].text.split()
print(ret[-1])