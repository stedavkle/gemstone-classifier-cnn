from unicodedata import name
import requests
from bs4 import BeautifulSoup as bs
import shutil
import os
all_gems = 'https://www.gemselect.com/all-gemstones.php'

#%%
html = requests.get(all_gems).text
soup = bs(html, 'html.parser')

#%%
soup.find_all('section',{'class': 'sec_pop'})
gem_table = soup.select('section[class=sec_pop] > a[class=in]')
#%%
gems_links = {}
for element in gem_table:
    print(element.find('h3').text)
    link = element.get('href')
    if link.startswith('https'):
        gems_links[element.find('h3').text] = element.get('href')
print(len(gems_links))
# %%