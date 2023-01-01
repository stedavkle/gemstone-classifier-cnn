#%%
from dataclasses import replace
from tkinter.font import names
import requests
from bs4 import BeautifulSoup as bs
import shutil
import os
base = 'https://www.gemdat.org/'
index = 'https://www.gemdat.org/gemindex.php'
gallery_link = 'https://www.gemdat.org/gallery.php'
data_path = r"C:/Users/david/Documents/projects/gemstone-classifier-cnn/data/mix/"

#%%
def get_gemstone_names(table):
    for elem in table:
        names_paths = {}
        for link in elem.find_all('a'):
            if(link.text!=''):                 
                names_paths[link.text.replace("'", '').replace('"', '')] = link.get('href').split('-')[1].split('.')[0]
    return names_paths
#%%
def download_images(gem, id):
    path = data_path + gem
    print(path)
    if not os.path.exists(path):
        os.mkdir(path)
    img_link = gallery_link + '?min=' + id
    # get all divs with class 'gallery'
    html = requests.get(img_link).text
    soup = bs(html, 'html.parser')
    gallery = soup.find('div', {'class': 'gallerytable'})
    x = 0
    if gallery is not None:
        divs = gallery.find_all('div')
        for div in divs:
            links = div.find_all('a')
            for link in links:
                img_p_link = base + link.get('href')
                if 'photo-' in img_p_link:
                    r = requests.get(img_p_link).text
                    soup = bs(r, 'html.parser')
                    img_link = base + soup.find('div', {'id': 'picshowimgwrap'}).find('img').get('src') 
                    #print(img_link)
                    if not os.path.exists(path + '/' + img_link.split('/')[-1]):     
                        img_html = requests.get(img_link, stream=True)
                        if img_html.status_code == 200:    # OK
                            with open(path+'/'+img_link.split('/')[-1], 'wb') as f:
                                img_html.raw.decode_content = True
                                shutil.copyfileobj(img_html.raw, f)
                                x += 1
    # print how many images were downloaded
    print("Downloaded {} images".format(x))
#%%
if __name__ == '__main__':
    html = requests.get(index).text
    soup = bs(html, 'html.parser')
    table = soup.find_all('table')
    gem_dict = get_gemstone_names(table)
    for gem, id in gem_dict.items():
        download_images(gem, id)
        
# %%
