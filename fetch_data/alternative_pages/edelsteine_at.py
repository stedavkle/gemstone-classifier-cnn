from tkinter.font import names
import requests
from bs4 import BeautifulSoup as bs
import shutil
import os

base = 'https://www.edelsteine.at/'
lexicon = 'https://www.edelsteine.at/en/glossaries/lexicon/'
data_path = r"C:/Users/david/Documents/projects/gemstone-classifier-cnn/data/mix/"
#%%
def get_gemstone_links():
    names_paths = {}
    for elem in table:
        names_paths[elem.find('div', {'class': 'caption'}).text] = lexicon + elem.find('a').get('href')
    return names_paths
#%%
def download_images(gem, link):
    path = data_path + gem.replace('/', '')
    path = path.replace('\"', '')
    if not os.path.exists(path):
        os.mkdir(path)
    html = requests.get(link).text
    soup = bs(html, 'html.parser')
    pictures = soup.find_all('img')
    print(gem)
    x = 0
    for picture in pictures:
        if '/z/images/' in picture.get('src'):
            img_link = base + picture.get('src')
            if not os.path.exists(path + '/' + img_link.split('/')[-1]):
                img = requests.get(img_link, stream=True)
                if img.status_code == 200:    # OK
                    #print(img_link)
                    with open(path+'/'+img_link.split('/')[-1], 'wb') as f:
                        img.raw.decode_content = True
                        shutil.copyfileobj(img.raw, f)
                        x += 1
    # print how many images were downloaded
    print("Downloaded {} images".format(x))

#%%
if __name__ == '__main__':
    html = requests.get(lexicon).text
    soup = bs(html, 'html.parser')
    table = soup.find_all('div', {'class': 'col-lg-6 col-sm-8 col-xs-12 text-center'})
    names_paths = get_gemstone_links()
    for gem, link in names_paths.items():
        download_images(gem, link)
        
# %%
