import requests
from bs4 import BeautifulSoup as bs
import shutil
import os

base = 'https://www.gemstone7.com/'
all_gems = 'https://www.gemstone7.com/all-gemstone.html'

#%%
def get_gemstone_links(table):
    names_paths = {}
    for image in table:
        img_link = image.get('src')
        if img_link.startswith('image/gemstone'):
            names_paths[image.get('alt')] = base + img_link[:-5] + img_link[-4:]
    return names_paths
#%%
def download_images(gem, link):
    path = 'data/' + gem
    print(gem)
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path + '/' + link.split('/')[-1]):
        img = requests.get(link, stream=True)
        if img.status_code == 200:    # OK
            with open(path+'/'+link.split('/')[-1], 'wb') as f:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw, f)
        print('1')
#%%
if __name__ == '__main__':
    html = requests.get(all_gems).text
    soup = bs(html, 'html.parser')
    images_table = soup.find_all('img')
    names_paths = get_gemstone_links(images_table)
    
    for gem, link in names_paths.items():
        download_images(gem, link)

# %%
